from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Ceza, Odunc

ceza_bp = Blueprint("ceza_bp", __name__)

# -------------------------------------------------
# HTML SAYFALAR
# -------------------------------------------------

# ADMIN → TÜM CEZALAR
@ceza_bp.route("/cezalar-sayfa", methods=["GET"])
def cezalar_sayfa():
    return render_template("cezalar.html")


# USER → CEZALARIM
@ceza_bp.route("/user/cezalar", methods=["GET"])
def user_cezalar_sayfa():
    return render_template("user_cezalar.html")


# -------------------------------------------------
# API (ADMIN)
# -------------------------------------------------

# Tüm cezaları listele (ADMIN)
@ceza_bp.route("/api/cezalar", methods=["GET"])
def get_cezalar():
    cezalar = Ceza.query.all()
    return jsonify([
        {
            "id": c.id,
            "odunc_id": c.odunc_id,
            "miktar": c.miktar,
            "tarih": c.tarih.strftime("%Y-%m-%d") if c.tarih else None,
            "aciklama": c.aciklama
        } for c in cezalar
    ]), 200


# Belirli bir ceza kaydını getir
@ceza_bp.route("/api/cezalar/<int:id>", methods=["GET"])
def get_ceza(id):
    ceza = Ceza.query.get_or_404(id)
    return jsonify({
        "id": ceza.id,
        "odunc_id": ceza.odunc_id,
        "miktar": ceza.miktar,
        "tarih": ceza.tarih.strftime("%Y-%m-%d") if ceza.tarih else None,
        "aciklama": ceza.aciklama
    }), 200


# Ceza sil
@ceza_bp.route("/api/cezalar/<int:id>", methods=["DELETE"])
def delete_ceza(id):
    ceza = Ceza.query.get_or_404(id)
    db.session.delete(ceza)
    db.session.commit()
    return jsonify({"mesaj": "Ceza kaydı silindi"}), 200


# Ceza güncelle
@ceza_bp.route("/api/cezalar/<int:id>", methods=["PUT"])
def update_ceza(id):
    ceza = Ceza.query.get_or_404(id)
    data = request.get_json()
    ceza.aciklama = data.get("aciklama", ceza.aciklama)
    db.session.commit()
    return jsonify({"mesaj": "Ceza açıklaması güncellendi"}), 200


# -------------------------------------------------
# API (USER)
# -------------------------------------------------

# USER → KENDİ CEZALARIM
@ceza_bp.route("/api/user/cezalar", methods=["GET"])
@jwt_required()
def get_user_cezalar():
    kullanici_id = int(get_jwt_identity())

    cezalar = (
        db.session.query(Ceza)
        .join(Odunc, Ceza.odunc_id == Odunc.id)
        .filter(Odunc.kullanici_id == kullanici_id)
        .all()
    )

    return jsonify([
        {
            "id": c.id,
            "odunc_id": c.odunc_id,
            "miktar": c.miktar,
            "tarih": c.tarih.strftime("%Y-%m-%d") if c.tarih else None,
            "aciklama": c.aciklama
        } for c in cezalar
    ]), 200
