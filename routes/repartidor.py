from flask import Blueprint
from utils.auth_helpers import login_required

repartidor_bp = Blueprint("repartidor", __name__)

@repartidor_bp.route("/test")
@login_required
def test():
    return "Ruta de repartidor funcionando 🚀"
