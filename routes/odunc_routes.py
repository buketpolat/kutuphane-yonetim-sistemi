from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from extensions import db
from models import Odunc, Kitap, Ceza

odunc_bp = Blueprint("odunc_bp", __name__)

# -------------------------------------------------
# USER → KENDİ ÖDÜNÇLERİ (KİTAP ADIYLA)
# GET /api/user/oduncler
# -------------------------------------------------
@odunc_bp.route("/api/user/oduncler", methods=["GET"])
@jwt_required()
def get_user_oduncler():
    kullanici_id = int(get_jwt_identity())

    oduncler = Odunc.query.filter_by(kullanici_id=kullanici_id).all()

    data = []
    for o in oduncler:
        kitap = Kitap.query.get(o.kitap_id)

        data.append({
            "id": o.id,
            "kitap_adi": kitap.ad if kitap else "Bilinmeyen Kitap",
            "baslangic_tarih": o.baslangic_tarih.strftime("%Y-%m-%d"),
            "iade_tarih": o.iade_tarih.strftime("%Y-%m-%d"),
            "teslim_edildi": o.teslim_edildi
        })

    return jsonify(data), 200



# -------------------------------------------------
# HTML SAYFALAR
# -------------------------------------------------

@odunc_bp.route("/oduncler-sayfa", methods=["GET"])
def oduncler_sayfa():
    return render_template("oduncler.html")


@odunc_bp.route("/user/oduncler", methods=["GET"])
def user_oduncler_sayfa():
    return render_template("user_oduncler.html")


# -------------------------------------------------
# ADMIN / GENEL API
# -------------------------------------------------

@odunc_bp.route("/api/oduncler", methods=["GET"])
def get_oduncler():
    oduncler = Odunc.query.all()
    return jsonify([
        {
            "id": o.id,
            "kullanici_id": o.kullanici_id,
            "kitap_id": o.kitap_id,
            "baslangic_tarih": o.baslangic_tarih.strftime("%Y-%m-%d"),
            "iade_tarih": o.iade_tarih.strftime("%Y-%m-%d"),
            "teslim_edildi": o.teslim_edildi
        }
        for o in oduncler
    ]), 200


# -------------------------------------------------
# ÖDÜNÇ AL
# -------------------------------------------------
@odunc_bp.route("/api/oduncler", methods=["POST"])
@jwt_required()
def add_odunc():
    kullanici_id = int(get_jwt_identity())
    data = request.get_json()
    kitap_id = data.get("kitap_id")

    kitap = Kitap.query.get_or_404(kitap_id)

    if kitap.stok <= 0:
        return jsonify({"hata": "Bu kitap stokta yok!"}), 400

    yeni_odunc = Odunc(
        kullanici_id=kullanici_id,
        kitap_id=kitap_id,
        baslangic_tarih=datetime.now(),
        iade_tarih=datetime.now() + timedelta(days=7),
        teslim_edildi=False
    )

    kitap.stok -= 1
    db.session.add(yeni_odunc)
    db.session.commit()

    return jsonify({"mesaj": "Kitap ödünç alındı"}), 201


# -------------------------------------------------
# İADE + CEZA
# -------------------------------------------------
@odunc_bp.route("/api/oduncler/<int:id>/iade", methods=["PUT"])
@jwt_required()
def iade_et(id):
    odunc = Odunc.query.get_or_404(id)

    if odunc.teslim_edildi:
        return jsonify({"hata": "Zaten iade edilmiş"}), 400

    odunc.teslim_edildi = True
    kitap = Kitap.query.get(odunc.kitap_id)
    kitap.stok += 1

    bugun = datetime.now().date()

    if odunc.iade_tarih.date() < bugun:
        gecikme = (bugun - odunc.iade_tarih.date()).days
        ceza = Ceza(
            miktar=gecikme * 5,
            tarih=bugun,
            aciklama=f"{gecikme} gün gecikme",
            odunc_id=odunc.id
        )
        db.session.add(ceza)

    db.session.commit()
    return jsonify({"mesaj": "Kitap iade edildi"}), 200
