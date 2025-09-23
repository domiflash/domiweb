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
def mostrar_carrito():
    """Muestra los productos en el carrito del cliente."""
    user_id = session.get("user_id")
    cursor = current_app.db.cursor()
    cursor.execute("""
        SELECT c.idproducto, p.nompro, p.prepro, c.cantidad
        FROM carritos c
        JOIN productos p ON c.idproducto = p.idpro
        WHERE c.idusuario = %s
    """, (user_id,))
    carrito = cursor.fetchall()
    return render_template("cliente/carrito.html", carrito=carrito)

@cliente_bp.route("/carrito/agregar", methods=["POST"])
@login_required
@role_required("cliente")
def agregar_al_carrito():
    """Agrega un producto al carrito."""
    user_id = session.get("user_id")
    producto_id = request.form.get("producto_id")
    cantidad = int(request.form.get("cantidad", 1))

    cursor = current_app.db.cursor()
    # Verificar si el producto ya está en el carrito
    cursor.execute("""
        SELECT cantidad FROM carritos WHERE idusuario = %s AND idproducto = %s
    """, (user_id, producto_id))
    resultado = cursor.fetchone()

    if resultado:
        # Actualizar la cantidad si ya existe
        nueva_cantidad = resultado[0] + cantidad
        cursor.execute("""
            UPDATE carritos SET cantidad = %s WHERE idusuario = %s AND idproducto = %s
        """, (nueva_cantidad, user_id, producto_id))
    else:
        # Insertar un nuevo producto en el carrito
        cursor.execute("""
            INSERT INTO carritos (idusuario, idproducto, cantidad)
            VALUES (%s, %s, %s)
        """, (user_id, producto_id, cantidad))

    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/actualizar", methods=["POST"])
@login_required
@role_required("cliente")
def actualizar_carrito():
    """Actualiza la cantidad de un producto en el carrito."""
    user_id = session.get("user_id")
    producto_id = request.form.get("producto_id")
    nueva_cantidad = int(request.form.get("cantidad"))

    if nueva_cantidad <= 0:
        # Si la cantidad es 0 o menor, eliminar el producto
        return eliminar_del_carrito(producto_id)

    cursor = current_app.db.cursor()
    cursor.execute("""
        UPDATE carritos SET cantidad = %s WHERE idusuario = %s AND idproducto = %s
    """, (nueva_cantidad, user_id, producto_id))
    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/eliminar", methods=["POST"])
@login_required
@role_required("cliente")
def eliminar_del_carrito():
    """Elimina un producto del carrito."""
    user_id = session.get("user_id")
    producto_id = request.form.get("producto_id")

    cursor = current_app.db.cursor()
    cursor.execute("""
        DELETE FROM carritos WHERE idusuario = %s AND idproducto = %s
    """, (user_id, producto_id))
    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/vaciar", methods=["POST"])
@login_required
@role_required("cliente")
def vaciar_carrito():
    """Vacía el carrito del cliente."""
    user_id = session.get("user_id")

    cursor = current_app.db.cursor()
    cursor.execute("""
        DELETE FROM carritos WHERE idusuario = %s
    """, (user_id,))
    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))

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
