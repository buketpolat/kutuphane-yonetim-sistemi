from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Kitap, Kullanici, Yazar, Kategori

kitap_bp = Blueprint("kitap_bp", __name__)

# -------------------------------------------------
# HTML SAYFA
# -------------------------------------------------
@kitap_bp.route("/kitaplar", methods=["GET"])
def kitaplar_sayfa():
    return render_template("kitaplar.html")

# -------------------------------------------------
# API
# -------------------------------------------------

# Tüm kitapları listele
@kitap_bp.route("/api/kitaplar", methods=["GET"])
def get_kitaplar():
    kitaplar = Kitap.query.all()
    return jsonify([
        {
            "id": k.id,
            "ad": k.ad,
            "yazar_id": k.yazar_id,
            "kategori_id": k.kategori_id,
            "stok": k.stok
        } for k in kitaplar
    ]), 200


# Yeni kitap ekle (ADMIN)
@kitap_bp.route("/api/kitaplar", methods=["POST"])
@jwt_required()
def add_kitap():
    kullanici = Kullanici.query.get(int(get_jwt_identity()))

    if not kullanici or kullanici.rol != "admin":
        return jsonify({"hata": "Sadece admin kitap ekleyebilir"}), 403

    data = request.get_json()

    # FK KONTROLLERİ
    if not Yazar.query.get(data.get("yazar_id")):
        return jsonify({"hata": "Geçersiz yazar ID"}), 400

    if not Kategori.query.get(data.get("kategori_id")):
        return jsonify({"hata": "Geçersiz kategori ID"}), 400

    yeni_kitap = Kitap(
        ad=data["ad"],
        yazar_id=data["yazar_id"],
        kategori_id=data["kategori_id"],
        stok=data.get("stok", 0)
    )

    db.session.add(yeni_kitap)
    db.session.commit()

    return jsonify({"mesaj": "Kitap başarıyla eklendi"}), 201


# Kitap güncelle (ADMIN)
@kitap_bp.route("/api/kitaplar/<int:id>", methods=["PUT"])
@jwt_required()
def update_kitap(id):
    kullanici = Kullanici.query.get(int(get_jwt_identity()))

    if not kullanici or kullanici.rol != "admin":
        return jsonify({"hata": "Yetkisiz işlem"}), 403

    kitap = Kitap.query.get_or_404(id)
    data = request.get_json()

    if "yazar_id" in data and not Yazar.query.get(data["yazar_id"]):
        return jsonify({"hata": "Geçersiz yazar ID"}), 400

    if "kategori_id" in data and not Kategori.query.get(data["kategori_id"]):
        return jsonify({"hata": "Geçersiz kategori ID"}), 400

    kitap.ad = data.get("ad", kitap.ad)
    kitap.yazar_id = data.get("yazar_id", kitap.yazar_id)
    kitap.kategori_id = data.get("kategori_id", kitap.kategori_id)
    kitap.stok = data.get("stok", kitap.stok)

    db.session.commit()

    return jsonify({"mesaj": "Kitap güncellendi"}), 200


# Kitap sil (ADMIN)
@kitap_bp.route("/api/kitaplar/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_kitap(id):
    kullanici = Kullanici.query.get(int(get_jwt_identity()))

    if not kullanici or kullanici.rol != "admin":
        return jsonify({"hata": "Yetkisiz işlem"}), 403

    kitap = Kitap.query.get_or_404(id)
    db.session.delete(kitap)
    db.session.commit()

    return jsonify({"mesaj": "Kitap silindi"}), 200
