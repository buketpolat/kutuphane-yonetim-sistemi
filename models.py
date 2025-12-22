from datetime import datetime
from extensions import db

# ----------------------------
# Kullanıcı Tablosu
# ----------------------------
class Kullanici(db.Model):
    __tablename__ = "kullanici"

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), default="ogrenci")  # ogrenci / personel / admin

    oduncler = db.relationship("Odunc", back_populates="kullanici")


# ----------------------------
# Yazar Tablosu
# ----------------------------
class Yazar(db.Model):
    __tablename__ = "yazar"

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)

    kitaplar = db.relationship("Kitap", back_populates="yazar")


# ----------------------------
# Kategori Tablosu
# ----------------------------
class Kategori(db.Model):
    __tablename__ = "kategori"

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)

    kitaplar = db.relationship("Kitap", back_populates="kategori")


# ----------------------------
# Kitap Tablosu
# ----------------------------
class Kitap(db.Model):
    __tablename__ = "kitap"

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(200), nullable=False)
    stok = db.Column(db.Integer, default=1)

    yazar_id = db.Column(db.Integer, db.ForeignKey("yazar.id"))
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))

    yazar = db.relationship("Yazar", back_populates="kitaplar")
    kategori = db.relationship("Kategori", back_populates="kitaplar")
    oduncler = db.relationship("Odunc", back_populates="kitap")


# ----------------------------
# Ödünç Tablosu
# ----------------------------
class Odunc(db.Model):
    __tablename__ = "odunc"

    id = db.Column(db.Integer, primary_key=True)
    baslangic_tarih = db.Column(db.DateTime, default=datetime.utcnow)
    iade_tarih = db.Column(db.DateTime, nullable=False)
    teslim_edildi = db.Column(db.Boolean, default=False)

    kitap_id = db.Column(db.Integer, db.ForeignKey("kitap.id"))
    kullanici_id = db.Column(db.Integer, db.ForeignKey("kullanici.id"))

    kitap = db.relationship("Kitap", back_populates="oduncler")
    kullanici = db.relationship("Kullanici", back_populates="oduncler")
    ceza = db.relationship("Ceza", back_populates="odunc", uselist=False)


# ----------------------------
# Ceza Tablosu
# ----------------------------
class Ceza(db.Model):
    __tablename__ = "ceza"

    id = db.Column(db.Integer, primary_key=True)
    miktar = db.Column(db.Float, default=0.0)
    tarih = db.Column(db.Date, default=datetime.utcnow)
    aciklama = db.Column(db.String(200), nullable=True)

    odunc_id = db.Column(db.Integer, db.ForeignKey("odunc.id"))
    odunc = db.relationship("Odunc", back_populates="ceza")
