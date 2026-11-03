from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Usuario
from app.auth.utils import login_required

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios", template_folder="templates")


@usuarios_bp.route("/")
@login_required
def lista():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    return render_template("usuarios/lista.html", usuarios=usuarios)


@usuarios_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        usuario = Usuario(
            nombre=request.form["nombre"].strip(),
            username=request.form["username"].strip(),
            email=request.form["email"].strip(),
        )
        usuario.set_password(request.form["password"])
        db.session.add(usuario)
        try:
            db.session.commit()
            flash("Usuario registrado correctamente.", "success")
            return redirect(url_for("usuarios.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("El usuario o el email ya existen.", "danger")
    return render_template("usuarios/formulario.html", usuario=None)


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)
    if request.method == "POST":
        usuario.nombre = request.form["nombre"].strip()
        usuario.username = request.form["username"].strip()
        usuario.email = request.form["email"].strip()
        if request.form["password"]:
            usuario.set_password(request.form["password"])
        try:
            db.session.commit()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("El usuario o el email ya existen.", "danger")
    return render_template("usuarios/formulario.html", usuario=usuario)


@usuarios_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    usuario = db.get_or_404(Usuario, id)
    if usuario.id == session.get("usuario_id"):
        flash("No puede eliminar su propio usuario.", "danger")
    elif usuario.anuncios:
        flash("No se puede eliminar: el usuario tiene anuncios asociados.", "danger")
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado.", "success")
    return redirect(url_for("usuarios.lista"))