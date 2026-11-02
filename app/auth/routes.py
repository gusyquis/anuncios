from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@auth_bp.app_context_processor
def inyectar_usuario():
    return {"usuario_actual": session.get("username")}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.check_password(password):
            session["usuario_id"] = usuario.id
            session["username"] = usuario.username
            flash(f"Bienvenido, {usuario.nombre}.", "success")
            return redirect(url_for("main.index"))

        flash("Usuario o contrasena incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))