from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    anuncios = db.relationship("Anuncio", back_populates="usuario")

    def set_password(self, plano):
        self.password_hash = generate_password_hash(plano)

    def check_password(self, plano):
        return check_password_hash(self.password_hash, plano)

    def __repr__(self):
        return f"<Usuario {self.username}>"


class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))

    anuncios = db.relationship("Anuncio", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria {self.nombre}>"


class Anuncio(db.Model):
    __tablename__ = "anuncios"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="anuncios")
    usuario = db.relationship("Usuario", back_populates="anuncios")

    def __repr__(self):
        return f"<Anuncio {self.titulo}>"


def sembrar_datos():
    """Crea un usuario administrador y categorias iniciales si la BD esta vacia."""
    if Usuario.query.count() == 0:
        admin = Usuario(nombre="Administrador", username="admin", email="admin@upea.bo")
        admin.set_password("admin123")
        db.session.add(admin)
    if Categoria.query.count() == 0:
        db.session.add_all([
            Categoria(nombre="Avisos academicos", descripcion="Comunicados de la carrera"),
            Categoria(nombre="Eventos", descripcion="Actividades y talleres"),
            Categoria(nombre="Venta y compra", descripcion="Productos y servicios"),
        ])
    db.session.commit()