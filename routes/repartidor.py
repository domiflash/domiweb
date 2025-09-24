from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from utils.auth_helpers import login_required, role_required

repartidor_bp = Blueprint("repartidor", __name__)

@repartidor_bp.route("/test")
@login_required
def test():
    return "Ruta de repartidor funcionando 🚀"

@repartidor_bp.route("/pedidos")
@login_required
@role_required("repartidor")
def listar_pedidos():
    """Lista pedidos disponibles para asignar o ya asignados al repartidor."""
    usuario_id = session.get("usuario_id")
    cursor = current_app.db.cursor()
    
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
        current_app.db.commit()
        
        cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
        repartidor = cursor.fetchone()
    
    idrep = repartidor['idrep']
    
    # Pedidos asignados al repartidor
    cursor.execute("""
        SELECT p.idped, u.nomusu as cliente, u.dirusu, r.nomres, 
               p.estped, p.fecha_creacion,
               SUM(dp.cantidad * dp.precio_unitario) as total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN restaurantes r ON p.idres = r.idres
        JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.idrep = %s
        GROUP BY p.idped, u.nomusu, u.dirusu, r.nomres, p.estped, p.fecha_creacion
        ORDER BY p.fecha_creacion DESC
    """, (idrep,))
    pedidos_asignados = cursor.fetchall()
    
    # Pedidos disponibles para asignar (estado aceptado, sin repartidor)
    cursor.execute("""
        SELECT p.idped, u.nomusu as cliente, u.dirusu, r.nomres, 
               p.estped, p.fecha_creacion,
               SUM(dp.cantidad * dp.precio_unitario) as total
        FROM pedidos p
        JOIN usuarios u ON p.idusu = u.idusu
        JOIN restaurantes r ON p.idres = r.idres
        JOIN detalle_pedidos dp ON p.idped = dp.idped
        WHERE p.estped IN ('aceptado', 'preparando') AND p.idrep IS NULL
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
    cursor = current_app.db.cursor()
    
    # Obtener ID del repartidor
    cursor.execute("SELECT idrep FROM repartidores WHERE idusu = %s", (usuario_id,))
    repartidor = cursor.fetchone()
    
    if repartidor:
        try:
            cursor.callproc("asignar_repartidor", (pedido_id, repartidor['idrep']))
            current_app.db.commit()
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
        cursor = current_app.db.cursor()
        cursor.callproc("cambiar_estado_pedido", (pedido_id, nuevo_estado))
        current_app.db.commit()
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
    cursor = current_app.db.cursor()
    
    if request.method == "POST":
        nomrep = request.form["nomrep"]
        vehrep = request.form["vehrep"]
        
        cursor.execute("""
            UPDATE repartidores SET nomrep = %s, vehrep = %s WHERE idusu = %s
        """, (nomrep, vehrep, usuario_id))
        current_app.db.commit()
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
        current_app.db.commit()
        
        cursor.execute("SELECT nomrep, vehrep, estrep FROM repartidores WHERE idusu = %s", (usuario_id,))
        repartidor = cursor.fetchone()
    
    return render_template("repartidor/perfil.html", repartidor=repartidor)
