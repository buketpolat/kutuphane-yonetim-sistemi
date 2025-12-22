# Akıllı Kütüphane Yönetim Sistemi

Bu proje, **Flask (Python)** kullanılarak geliştirilmiş, **JWT tabanlı kimlik doğrulama** içeren, **Admin ve User (Kullanıcı)** rolleri bulunan, **tam kapsamlı bir Kütüphane Yönetim Sistemi**dir.

Proje; kitap yönetimi, kullanıcı yönetimi, ödünç alma–iade işlemleri ve gecikmeye bağlı ceza hesaplamalarını kapsar.  
Backend (API) ve Frontend (HTML/CSS/JS) katmanları birlikte tasarlanmıştır.

---

## Projenin Amacı

- Kütüphane süreçlerini dijital ortamda yönetmek
- Rol bazlı (Admin / Kullanıcı) yetkilendirme sağlamak
- Kitap ödünç alma ve iade işlemlerini kontrol altına almak
- Gecikmeli iadelerde otomatik ceza üretmek
- RESTful API mantığını uygulamak
- Gerçek hayata yakın bir web projesi geliştirmek

---

## Kullanılan Teknolojiler

| Katman | Teknoloji |
|------|-----------|
| Backend | Python, Flask |
| Veritabanı | PostgreSQL |
| ORM | SQLAlchemy |
| Migration | Flask-Migrate |
| Kimlik Doğrulama | Flask-JWT-Extended |
| Frontend | HTML, CSS, JavaScript |
| API Test | Postman |
| Versiyon Kontrol | Git & GitHub |

---

## Proje Klasör Yapısı

```
AkilliKutuphane/
│
├── app.py                 # Ana Flask uygulaması
├── main.py                # Alternatif giriş noktası
├── config.py              # Konfigürasyon ayarları
├── extensions.py          # db, jwt gibi extension'lar
│
├── models.py              # Veritabanı modelleri
│
├── routes/                # Blueprint yapısı
│   ├── auth_routes.py     # Login / JWT
│   ├── kitap_routes.py   # Kitap işlemleri
│   ├── kullanici_routes.py
│   ├── odunc_routes.py   # Ödünç & iade
│   └── ceza_routes.py    # Ceza işlemleri
│
├── templates/             # HTML sayfaları
│   ├── admin.html
│   ├── admin_dashboard.html
│   ├── user.html
│   ├── user_kitaplar.html
│   ├── user_oduncler.html
│   ├── user_cezalar.html
│   └── ...
│
├── migrations/            # Veritabanı migration dosyaları
│
├── venv/                  # Sanal ortam (GitHub'a dahil edilmez)
└── README.md
```
---
## Projeyi Çalıştırma
```
# Sanal ortam
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows

# Bağımlılıklar
pip install -r requirements.txt

# Migration
flask db upgrade

# Uygulama
python app.py
```
---
## Geliştirici
Nehir Buket Polat
Software Engineering Student
GitHub: https://github.com/buketpolat


