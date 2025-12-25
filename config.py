class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:kendi_sifren@localhost:5432/akilli_kutuphane"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"
