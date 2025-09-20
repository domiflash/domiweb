from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from utils.auth_helpers import login_required

restaurante_bp = Blueprint("restaurante", __name__)

# ----------------------------
# PRODUCTOS
# ----------------------------
@restaurante_bp.route("/productos", methods=["GET"])
@login_required
def listar_productos():
    cursor = current_app.db.cursor()
    cursor.execute("SELECT idpro, nompro, despro, prepro, stopro FROM productos")
    productos = cursor.fetchall()
    return render_template("restaurante/productos.html", productos=productos)

@restaurante_bp.route("/productos", methods=["POST"])
@login_required
def crear_producto():
    nompro = request.form["nompro"]
    despro = request.form.get("despro")
    prepro = request.form["prepro"]
    stopro = request.form["stopro"]
    idres = 1  # ⚠️ Temporal: debería salir del restaurante logueado
    idcat = 1  # ⚠️ Temporal: categoría por defecto

    cursor = current_app.db.cursor()
    cursor.execute(
        "INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES (%s, %s, %s, %s, %s, %s)",
        (idres, idcat, nompro, despro, prepro, stopro)
    )
    current_app.db.commit()
    return redirect(url_for("restaurante.listar_productos"))

# ----------------------------
# PEDIDOS
# ----------------------------
@restaurante_bp.route("/pedidos", methods=["GET"])
@login_required
def listar_pedidos():
    """Lista todos los pedidos del restaurante actual"""
    idres = 1  # ⚠️ Temporal: debería obtenerse del restaurante logueado
    cursor = current_app.db.cursor()
    cursor.execute("""
        SELECT p.idped, u.nomusu AS cliente, u.dirusu AS direccion, 
               p.estped, p.fecha_creacion, p.fecha_actualizacion,
               SUM(dp.cantidad * dp.precio_unitario) AS total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idres = %s
        GROUP BY p.idped, u.nomusu, u.dirusu, p.estped, p.fecha_creacion, p.fecha_actualizacion
        ORDER BY p.fecha_creacion DESC
    """, (idres,))
    pedidos = cursor.fetchall()
    return render_template("restaurante/pedidos.html", pedidos=pedidos)

@restaurante_bp.route("/pedidos/<int:idped>", methods=["GET"])
@login_required
def detalle_pedido(idped):
    """Detalle de un pedido con productos"""
    cursor = current_app.db.cursor()

    # Info general del pedido
    cursor.execute("""
        SELECT p.idped, u.nomusu AS cliente, u.dirusu AS direccion, 
               p.estped, p.fecha_creacion, p.fecha_actualizacion,
               SUM(dp.cantidad * dp.precio_unitario) AS total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idped = %s
        GROUP BY p.idped, u.nomusu, u.dirusu, p.estped, p.fecha_creacion, p.fecha_actualizacion
    """, (idped,))
    pedido = cursor.fetchone()

    if not pedido:
        return jsonify({"msg": "Pedido no encontrado"}), 404

    # Productos del pedido
    cursor.execute("""
        SELECT pr.nompro AS nombre, dp.cantidad, dp.precio_unitario
        FROM detalle_pedidos dp
        JOIN productos pr ON dp.idpro = pr.idpro
        WHERE dp.idped = %s
    """, (idped,))
    productos = cursor.fetchall()

    return render_template("restaurante/detalle_pedido.html", pedido=pedido, productos=productos)

@restaurante_bp.route("/pedidos/<int:idped>/estado", methods=["POST"])
@login_required
def cambiar_estado_pedido(idped):
    """Actualizar estado de un pedido"""
    nuevo_estado = request.form["estado"]

    cursor = current_app.db.cursor()
    cursor.execute("CALL cambiar_estado_pedido(%s, %s)", (idped, nuevo_estado))
    current_app.db.commit()

    return redirect(url_for("restaurante.detalle_pedido", idped=idped))
