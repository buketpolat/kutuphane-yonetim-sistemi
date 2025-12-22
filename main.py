from flask import Flask, render_template
from routes.kitap_routes import kitap_bp
from routes.kullanici_routes import kullanici_bp
from routes.odunc_routes import odunc_bp
from routes.ceza_routes import ceza_bp

app = Flask(__name__)
app.register_blueprint(kitap_bp)
app.register_blueprint(kullanici_bp)
app.register_blueprint(odunc_bp)
app.register_blueprint(ceza_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/kitaplar")
def kitaplar():
    return render_template("kitaplar.html")

@app.route("/kullanicilar")
def kullanicilar():
    return render_template("kullanicilar.html")

@app.route("/oduncler")
def oduncler():
    return render_template("oduncler.html")

@app.route("/cezalar")
def cezalar():
    return render_template("cezalar.html")

if __name__ == "__main__":
    app.run(debug=True)
