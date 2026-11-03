from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Categoria
from app.auth.utils import login_required

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias", template_folder="templates")


@categorias_bp.route("/")
@login_required
def lista():
    categorias = Categoria.query.order_by(Categoria.id).all()
    return render_template("categorias/lista.html", categorias=categorias)


@categorias_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        categoria = Categoria(
            nombre=request.form["nombre"].strip(),
            descripcion=request.form["descripcion"].strip(),
        )
        db.session.add(categoria)
        try:
            db.session.commit()
            flash("Categoria registrada correctamente.", "success")
            return redirect(url_for("categorias.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe una categoria con ese nombre.", "danger")
    return render_template("categorias/formulario.html", categoria=None)


@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    categoria = db.get_or_404(Categoria, id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"].strip()
        categoria.descripcion = request.form["descripcion"].strip()
        try:
            db.session.commit()
            flash("Categoria actualizada correctamente.", "success")
            return redirect(url_for("categorias.lista"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe una categoria con ese nombre.", "danger")
    return render_template("categorias/formulario.html", categoria=categoria)


@categorias_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    categoria = db.get_or_404(Categoria, id)
    if categoria.anuncios:
        flash("No se puede eliminar: la categoria tiene anuncios asociados.", "danger")
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria eliminada.", "success")
    return redirect(url_for("categorias.lista"))