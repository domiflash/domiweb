from flask import Blueprint
from utils.auth_helpers import login_required

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/test")
@login_required
def test():
    return "Ruta de cliente funcionando 🚀"
