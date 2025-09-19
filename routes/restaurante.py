from flask import Blueprint
from utils.auth_helpers import login_required

restaurante_bp = Blueprint("restaurante", __name__)

@restaurante_bp.route("/test")
@login_required
def test():
    return "Ruta de restaurante funcionando 🚀"
