from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from utils.auth_helpers import login_required, role_required

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/test")
@login_required
def test():
    return "Ruta de cliente funcionando 🚀"

# Panel de Menús
@cliente_bp.route("/menu", methods=["GET"])
@login_required
@role_required("cliente")
def menu():
    cursor = current_app.db.cursor()
    cursor.execute("SELECT idpro, nompro, despro, prepro FROM productos")
    productos = cursor.fetchall()
    return render_template("cliente/menu.html", productos=productos)

# Carrito de Compras
@cliente_bp.route("/carrito", methods=["GET"])
@login_required
@role_required("cliente")
def carrito():
    carrito = session.get("carrito", [])
    return render_template("cliente/carrito.html", carrito=carrito)

@cliente_bp.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
@login_required
@role_required("cliente")
def agregar_al_carrito(producto_id):
    cursor = current_app.db.cursor()
    cursor.execute("SELECT idpro, nompro, prepro FROM productos WHERE idpro = %s", (producto_id,))
    producto = cursor.fetchone()

    if producto:
        carrito = session.get("carrito", [])
        carrito.append(producto)
        session["carrito"] = carrito
        flash("Producto agregado al carrito", "success")
    else:
        flash("Producto no encontrado", "danger")

    return redirect(url_for("cliente.menu"))

@cliente_bp.route("/carrito/eliminar/<int:producto_id>", methods=["POST"])
@login_required
@role_required("cliente")
def eliminar_del_carrito(producto_id):
    carrito = session.get("carrito", [])
    carrito = [p for p in carrito if p["idpro"] != producto_id]
    session["carrito"] = carrito
    flash("Producto eliminado del carrito", "info")
    return redirect(url_for("cliente.carrito"))

# Perfil del Cliente
@cliente_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@role_required("cliente")
def perfil():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        direccion = request.form["direccion"]

        cursor = current_app.db.cursor()
        cursor.execute(
            "UPDATE usuarios SET nomusu=%s, corusu=%s, dirusu=%s WHERE idusu=%s",
            (nombre, email, direccion, session["usuario_id"]),
        )
        current_app.db.commit()
        flash("Perfil actualizado correctamente", "success")

    cursor = current_app.db.cursor()
    cursor.execute("SELECT nomusu, corusu, dirusu FROM usuarios WHERE idusu=%s", (session["usuario_id"],))
    usuario = cursor.fetchone()
    return render_template("cliente/perfil.html", usuario=usuario)
