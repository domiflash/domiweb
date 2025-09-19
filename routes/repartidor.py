from flask import Blueprint

repartidor_bp = Blueprint("repartidor", __name__)

@repartidor_bp.route("/test")
def test():
    return "Ruta de repartidor funcionando 🚀"
