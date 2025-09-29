from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from utils.auth_helpers import login_required, role_required
from utils.delivery_calculator import DeliveryCalculator
from datetime import datetime

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/test")
@login_required
def test():
    return "Ruta de cliente funcionando 🚀"

# # Panel de Menús
# @cliente_bp.route("/menu", methods=["GET"])
# @login_required
# @role_required("cliente")
# def menu():
#     cursor = current_app.db.cursor()
#     cursor.execute("SELECT idpro, nompro, despro, prepro FROM productos")
#     productos = cursor.fetchall()
#     return render_template("cliente/menu.html", productos=productos)
@cliente_bp.route("/menu", methods=["GET"])
@login_required
@role_required("cliente")
def menu():
    cursor = current_app.db.cursor()
    
    # Obtener restaurantes y sus productos
    cursor.execute("""
        SELECT r.idres, r.nomres, p.idpro, p.nompro, p.despro, p.prepro
        FROM restaurantes r
        LEFT JOIN productos p ON r.idres = p.idres
        WHERE r.estres = 'activo'
        ORDER BY r.nomres, p.nompro
    """)
    data = cursor.fetchall()
    
    # Agrupar productos por restaurante
    restaurantes = {}
    for row in data:
        idres = row['idres']
        if idres not in restaurantes:
            restaurantes[idres] = {
                'nombre': row['nomres'],
                'productos': []
            }
        if row['idpro']:  # Si el restaurante tiene productos
            restaurantes[idres]['productos'].append({
                'idpro': row['idpro'],
                'nompro': row['nompro'],
                'despro': row['despro'],
                'prepro': row['prepro']
            })
    
    # Pasar la variable `restaurantes` a la plantilla
    return render_template("cliente/menu.html", restaurantes=restaurantes)

# Carrito de Compras
@cliente_bp.route("/carrito", methods=["GET"])
@login_required
@role_required("cliente")
def mostrar_carrito():
    """Muestra los productos en el carrito del cliente."""
    user_id = session.get("usuario_id")
    cursor = current_app.db.cursor()
    cursor.execute("""
        SELECT c.idpro, p.nompro, p.prepro, c.canprocar
        FROM carritos c
        JOIN productos p ON c.idpro = p.idpro
        WHERE c.idusu = %s
    """, (user_id,))
    carrito = cursor.fetchall()
    return render_template("cliente/carrito.html", carrito=carrito)

@cliente_bp.route("/carrito/agregar", methods=["POST"])
@login_required
@role_required("cliente")
def agregar_al_carrito():
    """Agrega un producto al carrito."""
    user_id = session.get("usuario_id")
    producto_id = request.form.get("producto_id")
    cantidad = int(request.form.get("cantidad", 1))

    cursor = current_app.db.cursor()
    # Verificar el stock disponible
    cursor.execute("SELECT stopro FROM productos WHERE idpro = %s", (producto_id,))
    producto = cursor.fetchone()

    if not producto or cantidad > producto['stopro']:
        flash("La cantidad solicitada excede el stock disponible.", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))

    # Verificar si el producto ya está en el carrito
    cursor.execute("""
        SELECT canprocar FROM carritos WHERE idusu = %s AND idpro = %s
    """, (user_id, producto_id))
    resultado = cursor.fetchone()

    if resultado:
        # Actualizar la cantidad si ya existe
        nueva_cantidad = resultado['canprocar'] + cantidad
        if nueva_cantidad > producto['stopro']:
            flash("La cantidad total excede el stock disponible.", "danger")
            return redirect(url_for("cliente.mostrar_carrito"))
        cursor.execute("""
            UPDATE carritos SET canprocar = %s WHERE idusu = %s AND idpro = %s
        """, (nueva_cantidad, user_id, producto_id))
    else:
        # Insertar un nuevo producto en el carrito
        cursor.execute("""
            INSERT INTO carritos (idusu, idpro, canprocar)
            VALUES (%s, %s, %s)
        """, (user_id, producto_id, cantidad))

    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/actualizar", methods=["POST"])
@login_required
@role_required("cliente")
def actualizar_carrito():
    """Actualiza la cantidad de un producto en el carrito."""
    user_id = session.get("usuario_id")
    producto_id = request.form.get("producto_id")
    nueva_cantidad = int(request.form.get("cantidad"))

    cursor = current_app.db.cursor()
    # Verificar el stock disponible
    cursor.execute("SELECT stopro FROM productos WHERE idpro = %s", (producto_id,))
    producto = cursor.fetchone()

    if not producto or nueva_cantidad > producto['stopro']:
        flash("La cantidad solicitada excede el stock disponible.", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))

    if nueva_cantidad <= 0:
        # Si la cantidad es 0 o menor, eliminar el producto
        return eliminar_del_carrito()

    cursor.execute("""
        UPDATE carritos SET canprocar = %s WHERE idusu = %s AND idpro = %s
    """, (nueva_cantidad, user_id, producto_id))
    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/eliminar", methods=["POST"])
@login_required
@role_required("cliente")
def eliminar_del_carrito():
    """Elimina un producto del carrito."""
    user_id = session.get("usuario_id")
    producto_id = request.form.get("producto_id")

    cursor = current_app.db.cursor()
    cursor.execute("""
        DELETE FROM carritos WHERE idusu = %s AND idpro = %s
    """, (user_id, producto_id))
    current_app.db.commit()
    return redirect(url_for("cliente.mostrar_carrito"))


@cliente_bp.route("/carrito/vaciar", methods=["POST"])
@login_required
@role_required("cliente")
def vaciar_carrito():
    """Vacía el carrito del cliente."""
    user_id = session.get("usuario_id")

    cursor = current_app.db.cursor()
    cursor.execute("""
        DELETE FROM carritos WHERE idusu = %s
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

# Sistema de Checkout
@cliente_bp.route("/checkout", methods=["GET", "POST"])
@login_required
@role_required("cliente")
def checkout():
    """Proceso de checkout para finalizar pedido."""
    user_id = session.get("usuario_id")
    cursor = current_app.db.cursor()
    
    if request.method == "POST":
        # Obtener datos del formulario
        restaurante_id = request.form.get("restaurante_id")
        metodo_pago = request.form.get("metodo_pago")
        
        if not restaurante_id:
            flash("Debe seleccionar un restaurante", "danger")
            return redirect(url_for("cliente.checkout"))
        
        try:
            # Usar el procedimiento almacenado para confirmar pedido
            cursor.callproc("confirmar_pedido", (user_id, restaurante_id))
            result = cursor.fetchone()
            
            if result:
                pedido_id = result['id_pedido_creado']
                
                # Calcular total del pedido
                cursor.execute("""
                    SELECT SUM(cantidad * precio_unitario) as total
                    FROM detalle_pedidos WHERE idped = %s
                """, (pedido_id,))
                total_result = cursor.fetchone()
                total = total_result['total'] if total_result else 0
                
                # Registrar pago
                cursor.callproc("registrar_pago", (pedido_id, metodo_pago, total))
                current_app.db.commit()
                
                # 🕐 Calcular tiempo estimado de entrega
                try:
                    tiempo_info = DeliveryCalculator.calcular_tiempo_para_pedido(pedido_id)
                    
                    if tiempo_info:
                        tiempo_formateado = DeliveryCalculator.formatear_tiempo_estimado(tiempo_info['tiempo_estimado'])
                        flash(f"¡Pedido realizado con éxito! Total: ${total:.2f} - Llegará en {tiempo_formateado}", "success")
                        
                        # Guardar info de tiempo en sesión para mostrar en página de éxito
                        session['ultimo_pedido'] = {
                            'id': pedido_id,
                            'total': float(total),
                            'tiempo_estimado': tiempo_info['tiempo_estimado'],
                            'hora_estimada': tiempo_info['hora_estimada'].strftime('%H:%M'),
                            'distancia': tiempo_info['distancia_km'],
                            'restaurante': tiempo_info['restaurante'],
                            'metodo_pago': metodo_pago
                        }
                    else:
                        flash(f"¡Pedido realizado con éxito! Total: ${total:.2f}", "success")
                except Exception as e:
                    print(f"Error calculando tiempo: {e}")
                    flash(f"¡Pedido realizado con éxito! Total: ${total:.2f}", "success")
                
                # Redirigir a página de pago exitoso
                return redirect(url_for("cliente.pago_exitoso", pedido_id=pedido_id, metodo=metodo_pago, total=total))
                
        except Exception as e:
            flash(f"Error al procesar pedido: {str(e)}", "danger")
            return redirect(url_for("cliente.checkout"))
    
    # GET: Mostrar formulario de checkout
    # Obtener productos del carrito
    cursor.execute("""
        SELECT c.idpro, p.nompro, p.prepro, c.canprocar, 
               (p.prepro * c.canprocar) as subtotal, r.idres, r.nomres
        FROM carritos c
        JOIN productos p ON c.idpro = p.idpro
        JOIN restaurantes r ON p.idres = r.idres
        WHERE c.idusu = %s
    """, (user_id,))
    carrito_items = cursor.fetchall()
    
    if not carrito_items:
        flash("Tu carrito está vacío", "warning")
        return redirect(url_for("cliente.menu"))
    
    # Agrupar por restaurante
    restaurantes = {}
    total_general = 0
    for item in carrito_items:
        if item['idres'] not in restaurantes:
            restaurantes[item['idres']] = {
                'nombre': item['nomres'],
                'productos': [],
                'total': 0
            }
        restaurantes[item['idres']]['productos'].append(item)
        restaurantes[item['idres']]['total'] += item['subtotal']
        total_general += item['subtotal']

    return render_template("cliente/checkout.html", restaurantes=restaurantes, total_general=total_general)

@cliente_bp.route("/mis-pedidos")
@login_required
@role_required("cliente")
def mis_pedidos():
    """Muestra el historial de pedidos del cliente con tiempo estimado."""
    user_id = session.get("usuario_id")
    cursor = current_app.db.cursor()
    
    cursor.execute("""
        SELECT p.idped, r.nomres, p.estped, p.fecha_creacion,
               p.tiempo_estimado_minutos, p.hora_estimada_entrega,
               COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) as total,
               pg.metodo, pg.estado as estado_pago
        FROM pedidos p
        JOIN restaurantes r ON p.idres = r.idres
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        LEFT JOIN pagos pg ON p.idped = pg.idped
        WHERE p.idusu = %s
        GROUP BY p.idped, r.nomres, p.estped, p.fecha_creacion, 
                 p.tiempo_estimado_minutos, p.hora_estimada_entrega, pg.metodo, pg.estado
        ORDER BY p.fecha_creacion DESC
    """, (user_id,))
    
    pedidos_raw = cursor.fetchall()
    
    # Enriquecer datos de pedidos con información de entrega
    pedidos = []
    for pedido in pedidos_raw:
        pedido_dict = dict(pedido)
        
        # Calcular estado de entrega si hay tiempo estimado
        if pedido['tiempo_estimado_minutos']:
            estado_entrega = DeliveryCalculator.obtener_estado_entrega_con_tiempo(pedido['idped'])
            if estado_entrega:
                pedido_dict.update(estado_entrega)
        
        pedidos.append(pedido_dict)
    
    return render_template("cliente/mis_pedidos.html", pedidos=pedidos)

@cliente_bp.route("/pago-exitoso")
@login_required
@role_required("cliente")
def pago_exitoso():
    """Página de confirmación de pago exitoso."""
    pedido_id = request.args.get("pedido_id")
    metodo_pago = request.args.get("metodo", "efectivo")
    monto = request.args.get("total", "0")
    
    return render_template("cliente/pago_exitoso.html", 
                         pedido_id=pedido_id, 
                         metodo_pago=metodo_pago, 
                         monto=monto)

@cliente_bp.route("/actualizar-pago/<int:pedido_id>", methods=["POST"])
@login_required
@role_required("cliente")
def actualizar_pago_simulado(pedido_id):
    """Simula la actualización del estado del pago."""
    try:
        cursor = current_app.db.cursor()
        
        # Obtener el ID del pago asociado al pedido
        cursor.execute("SELECT idpag FROM pagos WHERE idped = %s", (pedido_id,))
        pago = cursor.fetchone()
        
        if pago:
            cursor.callproc("actualizar_estado_pago", (pago['idpag'], "pagado"))
            current_app.db.commit()
        
        return {"status": "success"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
