from flask import Flask, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from extensions import db

# -------------------------------------------------
# Flask Uygulaması
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# PostgreSQL
# -------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:buket1234@localhost/akilli_kutuphane"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -------------------------------------------------
# JWT
# -------------------------------------------------
app.config["JWT_SECRET_KEY"] = "super-gizli-anahtar"

# -------------------------------------------------
# Extensions Init
# -------------------------------------------------
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# -------------------------------------------------
# Modeller
# -------------------------------------------------
from models import Kullanici, Kitap, Yazar, Kategori, Odunc, Ceza

# -------------------------------------------------
# Blueprint'ler
# -------------------------------------------------
from routes.auth_routes import auth_bp
from routes.kitap_routes import kitap_bp
from routes.kullanici_routes import kullanici_bp
from routes.odunc_routes import odunc_bp
from routes.ceza_routes import ceza_bp

# -------------------------------------------------
# Blueprint Kayıtları
# -------------------------------------------------

#AUTH → SADECE API
app.register_blueprint(auth_bp, url_prefix="/api")

#HTML + API
app.register_blueprint(kitap_bp)
app.register_blueprint(kullanici_bp)
app.register_blueprint(odunc_bp)
app.register_blueprint(ceza_bp)

# -------------------------------------------------
# ANA SAYFALAR
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/admin/kitap-ekle")
def admin_kitap_ekle():
    return render_template("admin_kitap_ekle.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user")
def user_page():
    return render_template("user.html")

@app.route("/user/oduncler")
def user_oduncler_page():
    return render_template("user_oduncler.html")

@app.route("/user/kitaplar")
def user_kitaplar():
    return render_template("user_kitaplar.html")



# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
