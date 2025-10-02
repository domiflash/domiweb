from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app, session, flash
from utils.auth_helpers import login_required, role_required
from utils.validation_decorators import validate_form, require_fields
from utils.input_validator import input_validator

restaurante_bp = Blueprint("restaurante", __name__)

# ----------------------------
# PRODUCTOS
# ----------------------------
@restaurante_bp.route("/productos", methods=["GET"])
@login_required
@role_required("restaurante")
def listar_productos():
    cursor = current_app.db.cursor()
    usuario_id = session.get("usuario_id")  # Usar el id del usuario desde la sesión

    if not usuario_id:
        return jsonify({"msg": "No se pudo identificar al usuario logueado."}), 403

    cursor.execute(
        """
        SELECT p.idpro, p.nompro, p.despro, p.prepro, p.stopro, c.tipcat
        FROM productos p
        JOIN categorias c ON p.idcat = c.idcat
        JOIN restaurantes r ON p.idres = r.idres
        WHERE r.idusu = %s
        """,
        (usuario_id,)
    )
    productos = cursor.fetchall()
    cursor.execute("SELECT idcat, tipcat FROM categorias")
    categorias = cursor.fetchall()
    return render_template("restaurante/productos.html", productos=productos, categorias=categorias)

@restaurante_bp.route("/productos", methods=["POST"])
@login_required
@role_required("restaurante")
@validate_form({
    'nompro': 'name',
    'despro': 'description',
    'prepro': 'price',
    'stopro': 'quantity',
    'idcat': 'numeric'
})
def crear_producto():
    # Los datos ya están validados por el decorador
    nompro = request.validated_data["nompro"]
    despro = request.validated_data.get("despro", "")
    prepro = request.validated_data["prepro"]
    stopro = request.validated_data["stopro"]
    idcat = request.validated_data["idcat"]

    # Obtener el idres del restaurante logueado
    usuario_id = session.get("usuario_id")
    cursor = current_app.db.cursor()
    cursor.execute("SELECT idres FROM restaurantes WHERE idusu = %s", (usuario_id,))
    restaurante = cursor.fetchone()

    if not restaurante:
        flash("No se encontró un restaurante asociado al usuario logueado.", "danger")
        return redirect(url_for("restaurante.listar_productos"))

    idres = restaurante["idres"]  # Obtener el idres del resultado de la consulta

    # Insertar el producto con el idres correcto
    cursor.execute(
        "INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES (%s, %s, %s, %s, %s, %s)",
        (idres, idcat, nompro, despro, prepro, stopro)
    )
    current_app.db.commit()
    flash("Producto creado exitosamente.", "success")
    return redirect(url_for("restaurante.listar_productos"))

@restaurante_bp.route("/productos/<int:idpro>/editar", methods=["GET", "POST"])
@login_required
@role_required("restaurante")
def editar_producto(idpro):
    cursor = current_app.db.cursor()

    if request.method == "POST":
        nompro = request.form["nompro"]
        despro = request.form.get("despro")
        prepro = request.form["prepro"]
        stopro = request.form["stopro"]
        idcat = request.form["idcat"]

        cursor.execute(
            "UPDATE productos SET nompro = %s, despro = %s, prepro = %s, stopro = %s, idcat = %s WHERE idpro = %s",
            (nompro, despro, prepro, stopro, idcat, idpro)
        )
        current_app.db.commit()
        return redirect(url_for("restaurante.listar_productos"))

    cursor.execute("SELECT * FROM productos WHERE idpro = %s", (idpro,))
    producto = cursor.fetchone()
    cursor.execute("SELECT idcat, nomcat FROM categorias")
    categorias = cursor.fetchall()
    return render_template("restaurante/editar_producto.html", producto=producto, categorias=categorias)

@restaurante_bp.route("/productos/<int:idpro>/eliminar", methods=["POST"])
@login_required
@role_required("restaurante")
def eliminar_producto(idpro):
    cursor = current_app.db.cursor()
    cursor.execute("DELETE FROM productos WHERE idpro = %s", (idpro,))
    current_app.db.commit()
    return redirect(url_for("restaurante.listar_productos"))

# ----------------------------
# PEDIDOS
# ----------------------------
@restaurante_bp.route("/pedidos", methods=["GET"])
@login_required
@role_required("restaurante")
def listar_pedidos():
    """Lista todos los pedidos del restaurante actual"""
    usuario_id = session.get("usuario_id")  # Usar el id del usuario desde la sesión

    if not usuario_id:
        return jsonify({"msg": "No se pudo identificar al usuario logueado."}), 403

    cursor = current_app.db.cursor()
    cursor.execute(
        """
        SELECT p.idped, u.nomusu AS cliente, 
               p.estped, p.fecha_creacion, p.fecha_actualizacion,
               COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) AS total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        JOIN restaurantes r ON p.idres = r.idres
        WHERE r.idusu = %s
        GROUP BY p.idped, u.nomusu, p.estped, p.fecha_creacion, p.fecha_actualizacion
        ORDER BY p.fecha_creacion DESC
        """,
        (usuario_id,)
    )
    pedidos = cursor.fetchall()
    return render_template("restaurante/pedidos.html", pedidos=pedidos)

@restaurante_bp.route("/pedidos/<int:idped>", methods=["GET"])
@login_required
@role_required("restaurante")
def detalle_pedido(idped):
    """Detalle de un pedido con productos"""
    cursor = current_app.db.cursor()

    # Info general del pedido
    cursor.execute("""
        SELECT p.idped, u.nomusu AS cliente, 
               p.estped, p.fecha_creacion, p.fecha_actualizacion,
               COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) AS total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idped = %s
        GROUP BY p.idped, u.nomusu, p.estped, p.fecha_creacion, p.fecha_actualizacion
    """, (idped,))
    pedido = cursor.fetchone()

    if not pedido:
        flash("Pedido no encontrado", "error")
        return redirect(url_for("restaurante.listar_pedidos"))

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
@role_required("restaurante")
def cambiar_estado_pedido(idped):
    """Actualizar estado de un pedido"""
    nuevo_estado = request.form["estado"]

    cursor = current_app.db.cursor()
    cursor.execute("CALL cambiar_estado_pedido(%s, %s)", (idped, nuevo_estado))
    current_app.db.commit()

    return redirect(url_for("restaurante.detalle_pedido", idped=idped))

# ----------------------------
# PERFIL
# ----------------------------
@restaurante_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@role_required("restaurante")
def perfil():
    """Permite al restaurante modificar su información."""
    cursor = current_app.db.cursor()
    usuario_id = session.get("usuario_id")  # Usar el id del usuario desde la sesión

    if not usuario_id:
        return jsonify({"msg": "No se pudo identificar al usuario logueado."}), 403

    if request.method == "POST":
        nomres = request.form["nomres"]
        desres = request.form.get("desres")
        dirres = request.form["dirres"]
        telres = request.form["telres"]

        cursor.execute(
            """
            UPDATE restaurantes
            SET nomres = %s, desres = %s, dirres = %s, telres = %s
            WHERE idusu = %s
            """,
            (nomres, desres, dirres, telres, usuario_id)
        )
        current_app.db.commit()
        flash("Perfil actualizado exitosamente.", "success")
        return redirect(url_for("restaurante.perfil"))

    cursor.execute("SELECT nomres, desres, dirres, telres FROM restaurantes WHERE idusu = %s", (usuario_id,))
    restaurante = cursor.fetchone()
    return render_template("restaurante/perfil.html", restaurante=restaurante)
