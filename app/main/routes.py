from flask import Blueprint, render_template, request
from app.models import Anuncio, Categoria

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)
    consulta = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc())
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template(
        "main/index.html",
        anuncios=consulta.all(),
        categorias=categorias,
        categoria_id=categoria_id,
    )