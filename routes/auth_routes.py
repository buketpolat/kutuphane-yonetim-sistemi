from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import check_password_hash
from models import Kullanici

auth_bp = Blueprint("auth_bp", __name__)

# -------------------------------------------------
# LOGIN (Admin / Kullanıcı)
# POST /api/login
# -------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"hata": "JSON verisi gönderilmedi"}), 400

    email = data.get("email")
    sifre = data.get("sifre")

    if not email or not sifre:
        return jsonify({"hata": "E-posta ve şifre girilmelidir"}), 400

    kullanici = Kullanici.query.filter_by(email=email).first()

    if not kullanici or not check_password_hash(kullanici.sifre, sifre):
        return jsonify({"hata": "Geçersiz e-posta veya şifre"}), 401

    access_token = create_access_token(
        identity=str(kullanici.id),
        additional_claims={"rol": kullanici.rol}
    )

    return jsonify({
        "mesaj": "Giriş başarılı!",
        "kullanici_id": kullanici.id,
        "rol": kullanici.rol,
        "token": access_token
    }), 200


# -------------------------------------------------
# SADECE ADMIN ERİŞEBİLİR (TEST AMAÇLI)
# GET /api/admin-panel
# -------------------------------------------------
@auth_bp.route("/admin-panel", methods=["GET"])
@jwt_required()
def admin_panel():
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get("rol") != "admin":
        return jsonify({
            "hata": "Bu alana yalnızca admin kullanıcılar erişebilir!"
        }), 403

    return jsonify({
        "mesaj": "Hoş geldin admin!",
        "kullanici_id": current_user_id
    }), 200
