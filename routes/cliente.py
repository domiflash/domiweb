from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from utils.auth_helpers import login_required, role_required
from utils.delivery_calculator import DeliveryCalculator
from utils.validation_decorators import validate_form, require_fields
from utils.input_validator import input_validator
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
#     db = current_app.get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT idpro, nompro, despro, prepro FROM productos")
#     productos = cursor.fetchall()
#     return render_template("cliente/menu.html", productos=productos)
@cliente_bp.route("/menu", methods=["GET"])
@login_required
@role_required("cliente")
def menu():
    db = current_app.get_db()

    cursor = db.cursor()
    
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
    db = current_app.get_db()

    cursor = db.cursor()
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
    
    try:
        cantidad = int(request.form.get("cantidad", 1))
    except (ValueError, TypeError):
        flash("Cantidad inválida.", "danger")
        return redirect(url_for("cliente.menu"))

    db = current_app.get_db()
    cursor = db.cursor()
    
    try:
        # Verificar el stock disponible
        cursor.execute("SELECT stopro FROM productos WHERE idpro = %s", (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            flash("Producto no encontrado.", "danger")
            return redirect(url_for("cliente.menu"))
            
        if cantidad > producto['stopro']:
            flash("La cantidad solicitada excede el stock disponible.", "danger")
            return redirect(url_for("cliente.menu"))

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

        # ✅ Con autocommit=True, no necesita db.commit()
        flash("Producto agregado al carrito exitosamente.", "success")
        return redirect(url_for("cliente.mostrar_carrito"))
        
    except Exception as e:
        print(f"❌ Error agregando al carrito: {e}")
        flash(f"Error al agregar producto al carrito: {str(e)}", "danger")
        return redirect(url_for("cliente.menu"))
    finally:
        cursor.close()


@cliente_bp.route("/carrito/actualizar", methods=["POST"])
@login_required
@role_required("cliente")
def actualizar_carrito():
    """Actualiza la cantidad de un producto en el carrito."""
    user_id = session.get("usuario_id")
    producto_id = request.form.get("producto_id")
    
    try:
        nueva_cantidad = int(request.form.get("cantidad"))
    except (ValueError, TypeError):
        flash("Cantidad inválida.", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))

    db = current_app.get_db()
    cursor = db.cursor()
    
    try:
        # Si la cantidad es 0 o menor, eliminar el producto
        if nueva_cantidad <= 0:
            cursor.execute("""
                DELETE FROM carritos WHERE idusu = %s AND idpro = %s
            """, (user_id, producto_id))
            flash("Producto eliminado del carrito.", "info")
            return redirect(url_for("cliente.mostrar_carrito"))
        
        # Verificar el stock disponible
        cursor.execute("SELECT stopro FROM productos WHERE idpro = %s", (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            flash("Producto no encontrado.", "danger")
            return redirect(url_for("cliente.mostrar_carrito"))
            
        if nueva_cantidad > producto['stopro']:
            flash("La cantidad solicitada excede el stock disponible.", "danger")
            return redirect(url_for("cliente.mostrar_carrito"))

        cursor.execute("""
            UPDATE carritos SET canprocar = %s WHERE idusu = %s AND idpro = %s
        """, (nueva_cantidad, user_id, producto_id))
        
        # ✅ Con autocommit=True, no necesita db.commit()
        flash("Carrito actualizado exitosamente.", "success")
        return redirect(url_for("cliente.mostrar_carrito"))
        
    except Exception as e:
        print(f"❌ Error actualizando carrito: {e}")
        flash(f"Error al actualizar carrito: {str(e)}", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))
    finally:
        cursor.close()


@cliente_bp.route("/carrito/eliminar", methods=["POST"])
@login_required
@role_required("cliente")
def eliminar_del_carrito():
    """Elimina un producto del carrito."""
    user_id = session.get("usuario_id")
    producto_id = request.form.get("producto_id")

    db = current_app.get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM carritos WHERE idusu = %s AND idpro = %s
        """, (user_id, producto_id))
        
        # ✅ Con autocommit=True, no necesita db.commit()
        flash("Producto eliminado del carrito.", "info")
        return redirect(url_for("cliente.mostrar_carrito"))
        
    except Exception as e:
        print(f"❌ Error eliminando del carrito: {e}")
        flash(f"Error al eliminar producto: {str(e)}", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))
    finally:
        cursor.close()


@cliente_bp.route("/carrito/vaciar", methods=["POST"])
@login_required
@role_required("cliente")
def vaciar_carrito():
    """Vacía el carrito del cliente."""
    user_id = session.get("usuario_id")

    db = current_app.get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM carritos WHERE idusu = %s
        """, (user_id,))
        
        # ✅ Con autocommit=True, no necesita db.commit()
        flash("Carrito vaciado exitosamente.", "info")
        return redirect(url_for("cliente.mostrar_carrito"))
        
    except Exception as e:
        print(f"❌ Error vaciando carrito: {e}")
        flash(f"Error al vaciar carrito: {str(e)}", "danger")
        return redirect(url_for("cliente.mostrar_carrito"))
    finally:
        cursor.close()

# Perfil del Cliente
@cliente_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@role_required("cliente")
def perfil():
    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]

        db = current_app.get_db()


        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET nomusu=%s, dirusu=%s WHERE idusu=%s",
            (nombre, direccion, session["usuario_id"]),
        )
        db.commit()
        flash("Perfil actualizado correctamente", "success")

    db = current_app.get_db()


    cursor = db.cursor()
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
    db = current_app.get_db()

    cursor = db.cursor()
    
    if request.method == "POST":
        # Obtener datos del formulario
        restaurante_id = request.form.get("restaurante_id")
        metodo_pago = request.form.get("metodo_pago")
        
        if not restaurante_id:
            flash("Debe seleccionar un restaurante", "danger")
            return redirect(url_for("cliente.checkout"))
        
        # 🔥 VALIDAR QUE HAY PRODUCTOS EN EL CARRITO ANTES DE PROCEDER
        cursor.execute("""
            SELECT COUNT(*) as count_items
            FROM carritos c
            WHERE c.idusu = %s
        """, (user_id,))
        carrito_check = cursor.fetchone()
        
        if not carrito_check or carrito_check['count_items'] == 0:
            flash("Tu carrito está vacío. Agrega productos antes de continuar.", "warning")
            return redirect(url_for("cliente.menu"))
        
        try:
            # 🔥 CALCULAR TOTAL ANTES DE CREAR EL PEDIDO
            # (porque el carrito se vacía automáticamente al crear el pedido)
            cursor.execute("""
                SELECT COALESCE(SUM(c.canprocar * p.prepro), 0) as total,
                       COUNT(*) as num_items
                FROM carritos c
                JOIN productos p ON c.idpro = p.idpro
                WHERE c.idusu = %s
            """, (user_id,))
            total_result = cursor.fetchone()
            total = float(total_result['total']) if total_result and total_result['total'] is not None else 0.0
            num_items = total_result['num_items'] if total_result else 0
            
            print(f"🔍 DEBUG - Usuario: {user_id}, Items en carrito: {num_items}, Total calculado: {total}")
            
            # Validar que el total no sea 0 (debería haber productos)
            if total <= 0 or num_items == 0:
                flash(f"Error: No se pueden procesar pedidos sin productos o con monto 0. Items: {num_items}, Total: {total}", "danger")
                return redirect(url_for("cliente.checkout"))
            
            # Usar la función confirmar_pedido (PostgreSQL retorna tabla)
            cursor.execute("SELECT * FROM confirmar_pedido(%s, %s)", (user_id, restaurante_id))
            result = cursor.fetchone()
            
            if result:
                pedido_id = result['id_pedido_creado']
                
                # Registrar pago con CALL
                cursor.execute("CALL registrar_pago(%s, %s, %s)", (pedido_id, metodo_pago, total))
                
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
                return redirect(url_for("cliente.pago_exitoso", pedido_id=pedido_id, metodo=metodo_pago, total=f"{total:.2f}"))
                
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
    db = current_app.get_db()

    cursor = db.cursor()
    
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
    monto_str = request.args.get("total", "0.00")
    
    # Convertir monto a float de forma segura
    try:
        monto = float(monto_str)
    except (ValueError, TypeError):
        monto = 0.00
    
    return render_template("cliente/pago_exitoso.html", 
                         pedido_id=pedido_id, 
                         metodo_pago=metodo_pago, 
                         monto=f"{monto:.2f}")

@cliente_bp.route("/actualizar-pago/<int:pedido_id>", methods=["POST"])
@login_required
@role_required("cliente")
def actualizar_pago_simulado(pedido_id):
    """Simula la actualización del estado del pago."""
    try:
        db = current_app.get_db()

        cursor = db.cursor()
        
        # Obtener el ID del pago asociado al pedido
        cursor.execute("SELECT idpag FROM pagos WHERE idped = %s", (pedido_id,))
        pago = cursor.fetchone()
        
        if pago:
            cursor.execute("CALL actualizar_estado_pago(%s, %s)", (pago['idpag'], "pagado"))
        
        cursor.close()
        return {"status": "success"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
