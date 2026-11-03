from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Anuncio, Categoria, Usuario
from app.auth.utils import login_required

anuncios_bp = Blueprint("anuncios", __name__, url_prefix="/anuncios", template_folder="templates")


@anuncios_bp.route("/")
@login_required
def lista():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template("anuncios/lista.html", anuncios=anuncios)


@anuncios_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        anuncio = Anuncio(
            titulo=request.form["titulo"].strip(),
            descripcion=request.form["descripcion"].strip(),
            categoria_id=int(request.form["categoria_id"]),
            usuario_id=int(request.form["usuario_id"]),
        )
        db.session.add(anuncio)
        db.session.commit()
        flash("Anuncio registrado correctamente.", "success")
        return redirect(url_for("anuncios.lista"))
    return render_template(
        "anuncios/formulario.html",
        anuncio=None,
        categorias=Categoria.query.order_by(Categoria.nombre).all(),
        usuarios=Usuario.query.order_by(Usuario.nombre).all(),
    )


@anuncios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    anuncio = db.get_or_404(Anuncio, id)
    if request.method == "POST":
        anuncio.titulo = request.form["titulo"].strip()
        anuncio.descripcion = request.form["descripcion"].strip()
        anuncio.categoria_id = int(request.form["categoria_id"])
        anuncio.usuario_id = int(request.form["usuario_id"])
        db.session.commit()
        flash("Anuncio actualizado correctamente.", "success")
        return redirect(url_for("anuncios.lista"))
    return render_template(
        "anuncios/formulario.html",
        anuncio=anuncio,
        categorias=Categoria.query.order_by(Categoria.nombre).all(),
        usuarios=Usuario.query.order_by(Usuario.nombre).all(),
    )


@anuncios_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    anuncio = db.get_or_404(Anuncio, id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anuncio eliminado.", "success")
    return redirect(url_for("anuncios.lista"))