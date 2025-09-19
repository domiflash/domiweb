from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/test")
def test():
    return "Ruta de Administrador funcionando 🚀"
