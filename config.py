import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_gmq_anuncios")
    # Base de datos relacional: bd_anuncios (SQLite por defecto)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "bd_anuncios.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False