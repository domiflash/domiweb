from flask import Blueprint

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/test")
def test():
    return "Ruta de cliente funcionando 🚀"
