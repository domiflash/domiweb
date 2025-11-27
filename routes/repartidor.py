from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from utils.auth_helpers import login_required, role_required

repartidor_bp = Blueprint("repartidor", __name__)

@repartidor_bp.route("/test")
@login_required
def test():
    return "Ruta de repartidor funcionando 🚀"

@repartidor_bp.route("/dashboard")
@login_required
@role_required("repartidor")
def dashboard():
    """Dashboard con estadísticas del repartidor."""
    usuario_id = session.get("usuario_id")
    db = current_app.get_db()

    cursor = db.cursor()
    
    # Obtener ID del repartidor
    cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
    repartidor = cursor.fetchone()
    
    if not repartidor:
        return redirect(url_for("repartidor.perfil"))
    
    idrep = repartidor['idrep']
    
    # Estadísticas del repartidor
    stats = {}
    
    # Total de pedidos entregados
    cursor.execute("""
        SELECT COUNT(*) as total_entregados
        FROM pedidos WHERE idrep = %s AND estped = 'entregado'
    """, (idrep,))
    stats['entregados'] = cursor.fetchone()['total_entregados']
    
    # Pedidos en proceso
    cursor.execute("""
        SELECT COUNT(*) as en_proceso
        FROM pedidos WHERE idrep = %s AND estped IN ('aceptado', 'preparando', 'en_camino')
    """, (idrep,))
    stats['en_proceso'] = cursor.fetchone()['en_proceso']
    
    # Total ganado (simulado - 10% del total de pedidos)
    cursor.execute("""
        SELECT COALESCE(SUM(dp.cantidad * dp.precio_unitario * 0.1), 0) as total_ganado
        FROM pedidos p
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idrep = %s AND p.estped = 'entregado'
    """, (idrep,))
    result = cursor.fetchone()
    stats['ganado'] = result['total_ganado'] if result['total_ganado'] else 0
    
    # Pedidos de hoy
    cursor.execute("""
        SELECT COUNT(*) as hoy
        FROM pedidos WHERE idrep = %s AND DATE(fecha_creacion) = CURDATE()
    """, (idrep,))
    stats['hoy'] = cursor.fetchone()['hoy']
    
    return render_template("repartidor/dashboard.html", stats=stats)

@repartidor_bp.route("/pedidos")
@login_required
@role_required("repartidor")
def listar_pedidos():
    """Lista pedidos disponibles para asignar o ya asignados al repartidor."""
    usuario_id = session.get("usuario_id")
    db = current_app.get_db()

    cursor = db.cursor()
    
    # Verificar si el usuario tiene registro de repartidor
    cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
    repartidor = cursor.fetchone()
    
    if not repartidor:
        # Crear registro de repartidor automáticamente
        cursor.execute("SELECT nomusu FROM usuarios WHERE idusu = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.execute("""
            INSERT INTO repartidores (idusu, nomrep, vehrep, estrep) 
            VALUES (%s, %s, 'Vehículo por definir', 'activo')
        """, (usuario_id, usuario['nomusu']))
        db.commit()
        
        cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
        repartidor = cursor.fetchone()
    
    idrep = repartidor['idrep']
    
    # Pedidos asignados al repartidor
    cursor.execute("""
        SELECT p.idped, u.nomusu as cliente, u.dirusu, r.nomres, 
               p.estped, p.fecha_creacion,
               COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) as total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN restaurantes r ON p.idres = r.idres
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idrep = %s
        GROUP BY p.idped, u.nomusu, u.dirusu, r.nomres, p.estped, p.fecha_creacion
        ORDER BY p.fecha_creacion DESC
    """, (idrep,))
    pedidos_asignados = cursor.fetchall()
    
    # Pedidos disponibles para asignar (estado pendiente, aceptado o preparando, sin repartidor)
    cursor.execute("""
        SELECT p.idped, u.nomusu as cliente, u.dirusu, r.nomres, 
               p.estped, p.fecha_creacion,
               COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) as total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN restaurantes r ON p.idres = r.idres
        LEFT JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.estped IN ('pendiente', 'aceptado', 'preparando') AND p.idrep IS NULL
        GROUP BY p.idped, u.nomusu, u.dirusu, r.nomres, p.estped, p.fecha_creacion
        ORDER BY p.fecha_creacion ASC
    """)
    pedidos_disponibles = cursor.fetchall()
    
    return render_template("repartidor/pedidos.html", 
                         pedidos_asignados=pedidos_asignados,
                         pedidos_disponibles=pedidos_disponibles)

@repartidor_bp.route("/tomar-pedido/<int:pedido_id>", methods=["POST"])
@login_required
@role_required("repartidor")
def tomar_pedido(pedido_id):
    """Asigna un pedido al repartidor actual."""
    usuario_id = session.get("usuario_id")
    db = current_app.get_db()

    cursor = db.cursor()
    
    # Obtener ID del repartidor
    cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
    repartidor = cursor.fetchone()
    
    if repartidor:
        try:
            cursor.execute("CALL asignar_repartidor(%s, %s)", (pedido_id, repartidor['idrep']))
            flash(f"Pedido #{pedido_id} asignado exitosamente", "success")
        except Exception as e:
            flash(f"Error al asignar pedido: {str(e)}", "danger")
    
    return redirect(url_for("repartidor.listar_pedidos"))

@repartidor_bp.route("/actualizar-estado/<int:pedido_id>", methods=["POST"])
@login_required
@role_required("repartidor")
def actualizar_estado(pedido_id):
    """Actualiza el estado de un pedido asignado al repartidor."""
    nuevo_estado = request.form.get("estado")
    
    try:
        db = current_app.get_db()

        cursor = db.cursor()
        cursor.execute("CALL cambiar_estado_pedido(%s, %s)", (pedido_id, nuevo_estado))
        cursor.close()
        flash(f"Estado del pedido #{pedido_id} actualizado a {nuevo_estado}", "success")
    except Exception as e:
        flash(f"Error al actualizar estado: {str(e)}", "danger")
    
    return redirect(url_for("repartidor.listar_pedidos"))

@repartidor_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@role_required("repartidor")
def perfil():
    """Gestión del perfil del repartidor."""
    usuario_id = session.get("usuario_id")
    db = current_app.get_db()

    cursor = db.cursor()
    
    if request.method == "POST":
        nomrep = request.form["nomrep"]
        vehrep = request.form["vehrep"]
        
        cursor.execute("""
            UPDATE repartidores SET nomrep = %s, vehrep = %s WHERE idusu = %s
        """, (nomrep, vehrep, usuario_id))
        db.commit()
        flash("Perfil actualizado correctamente", "success")
    
    cursor.execute("SELECT nomrep, vehrep, estrep FROM repartidores WHERE idusu = %s", (usuario_id,))
    repartidor = cursor.fetchone()
    
    if not repartidor:
        # Crear registro si no existe
        cursor.execute("SELECT nomusu FROM usuarios WHERE idusu = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.execute("""
            INSERT INTO repartidores (idusu, nomrep, vehrep, estrep) 
            VALUES (%s, %s, 'Por definir', 'activo')
        """, (usuario_id, usuario['nomusu']))
        db.commit()
        
        cursor.execute("SELECT nomrep, vehrep, estrep FROM repartidores WHERE idusu = %s", (usuario_id,))
        repartidor = cursor.fetchone()
    
    return render_template("repartidor/perfil.html", repartidor=repartidor)
