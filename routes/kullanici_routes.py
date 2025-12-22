from flask import Blueprint, jsonify, request, render_template
from extensions import db
from models import Kullanici

kullanici_bp = Blueprint("kullanici_bp", __name__)

# -------------------------------------------------
# HTML SAYFA
# -------------------------------------------------
@kullanici_bp.route("/kullanicilar", methods=["GET"])
def kullanicilar_sayfa():
    return render_template("kullanicilar.html")


# -------------------------------------------------
# API
# -------------------------------------------------

# Tüm kullanıcıları listele
@kullanici_bp.route("/api/kullanicilar", methods=["GET"])
def get_kullanicilar():
    kullanicilar = Kullanici.query.all()
    return jsonify([
        {
            "id": k.id,
            "ad": k.ad,
            "email": k.email,
            "rol": k.rol
        } for k in kullanicilar
    ]), 200


# Yeni kullanıcı ekle
@kullanici_bp.route("/api/kullanicilar", methods=["POST"])
def add_kullanici():
    data = request.get_json()

    yeni = Kullanici(
        ad=data.get("ad"),
        email=data.get("email"),
        sifre=data.get("sifre"),
        rol=data.get("rol", "ogrenci")
    )

    db.session.add(yeni)
    db.session.commit()

    return jsonify({
        "mesaj": "Yeni kullanıcı eklendi",
        "id": yeni.id
    }), 201


# Kullanıcı güncelle
@kullanici_bp.route("/api/kullanicilar/<int:id>", methods=["PUT"])
def update_kullanici(id):
    kullanici = Kullanici.query.get_or_404(id)
    data = request.get_json()

    kullanici.ad = data.get("ad", kullanici.ad)
    kullanici.email = data.get("email", kullanici.email)
    kullanici.sifre = data.get("sifre", kullanici.sifre)
    kullanici.rol = data.get("rol", kullanici.rol)

    db.session.commit()

    return jsonify({
        "mesaj": "Kullanıcı bilgileri güncellendi"
    }), 200


# Kullanıcı sil
@kullanici_bp.route("/api/kullanicilar/<int:id>", methods=["DELETE"])
def delete_kullanici(id):
    kullanici = Kullanici.query.get_or_404(id)
    db.session.delete(kullanici)
    db.session.commit()

    return jsonify({
        "mesaj": "Kullanıcı silindi"
    }), 200
