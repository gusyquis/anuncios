from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registro de los blueprints (modulos)
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.usuarios.routes import usuarios_bp
    from app.categorias.routes import categorias_bp
    from app.anuncios.routes import anuncios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(anuncios_bp)

    # Crear tablas y datos iniciales
    with app.app_context():
        from app import models
        db.create_all()
        models.sembrar_datos()

    return app