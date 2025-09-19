from flask import Blueprint

restaurante_bp = Blueprint("restaurante", __name__)

@restaurante_bp.route("/test")
def test():
    return "Ruta de restaurante funcionando 🚀"
