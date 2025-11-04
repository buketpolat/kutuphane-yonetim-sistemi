from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask uygulamasını oluştur
app = Flask(__name__)

# config.py dosyasındaki ayarları yükle
app.config.from_object("config.Config")

# Veritabanı bağlantısını başlat
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelleri içe aktar (models.py içindeki tablolar)
from models import *

# Ana sayfa (test için)
@app.route("/")
def home():
    return render_template("index.html")

# Uygulamayı çalıştır
if __name__ == "__main__":
    app.run(debug=True)
