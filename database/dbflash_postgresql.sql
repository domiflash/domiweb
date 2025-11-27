-- =====================================================
-- 🍕 DomiFlash - Base de Datos PostgreSQL
-- Migrado desde MySQL/MariaDB
-- Fecha: 2025-11-26
-- =====================================================

-- Eliminar tipos ENUM si existen (para recrear limpio)
DROP TYPE IF EXISTS rol_usuario CASCADE;

DROP TYPE IF EXISTS estado_usuario CASCADE;

DROP TYPE IF EXISTS estado_pedido CASCADE;

DROP TYPE IF EXISTS metodo_pago CASCADE;

DROP TYPE IF EXISTS estado_pago CASCADE;

DROP TYPE IF EXISTS estado_repartidor CASCADE;

DROP TYPE IF EXISTS estado_restaurante CASCADE;

-- =====================================================
-- TIPOS ENUM (PostgreSQL requiere crear tipos primero)
-- =====================================================

CREATE TYPE rol_usuario AS ENUM ('cliente', 'restaurante', 'repartidor', 'administrador');

CREATE TYPE estado_usuario AS ENUM ('activo', 'inactivo');

CREATE TYPE estado_pedido AS ENUM ('pendiente', 'aceptado', 'preparando', 'en_camino', 'entregado', 'cancelado');

CREATE TYPE metodo_pago AS ENUM ('efectivo', 'tarjeta', 'nequi', 'daviplata', 'otro');

CREATE TYPE estado_pago AS ENUM ('pendiente', 'pagado');

CREATE TYPE estado_repartidor AS ENUM ('activo', 'inactivo');

CREATE TYPE estado_restaurante AS ENUM ('activo', 'inactivo');

-- =====================================================
-- TABLAS
-- =====================================================

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    idusu SERIAL PRIMARY KEY,
    nomusu VARCHAR(100) NOT NULL,
    corusu VARCHAR(100) NOT NULL UNIQUE,
    conusu VARCHAR(255) NOT NULL,
    dirusu VARCHAR(200) DEFAULT NULL,
    rolusu rol_usuario NOT NULL,
    estusu estado_usuario DEFAULT 'activo',
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lat_usuario DECIMAL(10, 8) DEFAULT NULL,
    lng_usuario DECIMAL(11, 8) DEFAULT NULL,
    intentos_fallidos INT DEFAULT 0,
    bloqueado_hasta TIMESTAMP DEFAULT NULL,
    ultimo_intento TIMESTAMP DEFAULT NULL
);

CREATE INDEX idx_usuarios_email_intentos ON usuarios (corusu, intentos_fallidos);

-- Tabla: categorias
CREATE TABLE IF NOT EXISTS categorias (
    idcat SERIAL PRIMARY KEY,
    tipcat VARCHAR(100) NOT NULL
);

-- Tabla: restaurantes
CREATE TABLE IF NOT EXISTS restaurantes (
    idres SERIAL PRIMARY KEY,
    idusu INT NOT NULL REFERENCES usuarios (idusu),
    nomres VARCHAR(100) NOT NULL,
    desres VARCHAR(300) DEFAULT NULL,
    dirres VARCHAR(200) DEFAULT NULL,
    telres VARCHAR(50) DEFAULT NULL,
    imgres VARCHAR(200) DEFAULT NULL,
    estres estado_restaurante DEFAULT 'activo',
    lat_restaurante DECIMAL(10, 8) DEFAULT -4.29810000,
    lng_restaurante DECIMAL(11, 8) DEFAULT -74.78460000
);

-- Tabla: productos
CREATE TABLE IF NOT EXISTS productos (
    idpro SERIAL PRIMARY KEY,
    idres INT NOT NULL REFERENCES restaurantes (idres),
    idcat INT NOT NULL REFERENCES categorias (idcat),
    nompro VARCHAR(100) NOT NULL,
    despro VARCHAR(255) DEFAULT NULL,
    prepro DECIMAL(10, 2) NOT NULL,
    imgpro VARCHAR(200) DEFAULT NULL,
    stopro INT NOT NULL
);

-- Tabla: repartidores
CREATE TABLE IF NOT EXISTS repartidores (
    idrep SERIAL PRIMARY KEY,
    idusu INT NOT NULL REFERENCES usuarios (idusu),
    nomrep VARCHAR(100) DEFAULT NULL,
    vehrep VARCHAR(100) DEFAULT NULL,
    estrep estado_repartidor DEFAULT 'activo'
);

-- Tabla: carritos
CREATE TABLE IF NOT EXISTS carritos (
    idcar SERIAL PRIMARY KEY,
    idusu INT NOT NULL REFERENCES usuarios (idusu),
    idpro INT NOT NULL REFERENCES productos (idpro),
    canprocar INT NOT NULL
);

-- Tabla: pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    idped SERIAL PRIMARY KEY,
    idusu INT NOT NULL REFERENCES usuarios (idusu),
    idres INT NOT NULL REFERENCES restaurantes (idres),
    idrep INT DEFAULT NULL REFERENCES repartidores (idrep),
    estped estado_pedido DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tiempo_estimado_minutos INT DEFAULT 30,
    hora_estimada_entrega TIMESTAMP DEFAULT NULL
);

-- Tabla: detalle_pedidos
CREATE TABLE IF NOT EXISTS detalle_pedidos (
    iddet SERIAL PRIMARY KEY,
    idped INT NOT NULL REFERENCES pedidos (idped),
    idpro INT NOT NULL REFERENCES productos (idpro),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL
);

-- Tabla: pagos
CREATE TABLE IF NOT EXISTS pagos (
    idpag SERIAL PRIMARY KEY,
    idped INT NOT NULL REFERENCES pedidos (idped),
    metodo metodo_pago NOT NULL,
    estado estado_pago DEFAULT 'pendiente',
    monto DECIMAL(10, 2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: tokens_recuperacion
CREATE TABLE IF NOT EXISTS tokens_recuperacion (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL REFERENCES usuarios (corusu) ON DELETE CASCADE,
    token VARCHAR(255) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    ip_solicitud VARCHAR(45) DEFAULT NULL,
    user_agent TEXT DEFAULT NULL
);

CREATE INDEX idx_token_email ON tokens_recuperacion (email, usado);

CREATE INDEX idx_token_expiracion ON tokens_recuperacion (
    token,
    fecha_expiracion,
    usado
);

-- Tabla: log_intentos_acceso
CREATE TABLE IF NOT EXISTS log_intentos_acceso (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    exito BOOLEAN DEFAULT FALSE,
    fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT DEFAULT NULL,
    motivo_fallo VARCHAR(100) DEFAULT NULL
);

CREATE INDEX idx_log_email_fecha ON log_intentos_acceso (email, fecha_intento);

-- =====================================================
-- FUNCIONES Y PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento: registrar_usuario
CREATE OR REPLACE PROCEDURE registrar_usuario(
    p_nomusu VARCHAR(100),
    p_corusu VARCHAR(100),
    p_conusu VARCHAR(255),
    p_dirusu VARCHAR(200),
    p_rolusu rol_usuario
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu)
    VALUES (p_nomusu, p_corusu, p_conusu, p_dirusu, p_rolusu);
END;
$$;

-- Procedimiento: actualizar_usuario
CREATE OR REPLACE PROCEDURE actualizar_usuario(
    p_idusu INT,
    p_nomusu VARCHAR(100),
    p_corusu VARCHAR(100),
    p_conusu VARCHAR(255),
    p_dirusu VARCHAR(200),
    p_rolusu rol_usuario,
    p_estusu estado_usuario
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE usuarios
    SET nomusu = p_nomusu,
        corusu = p_corusu,
        conusu = p_conusu,
        dirusu = p_dirusu,
        rolusu = p_rolusu,
        estusu = p_estusu
    WHERE idusu = p_idusu;
END;
$$;

-- Procedimiento: desactivar_usuario
CREATE OR REPLACE PROCEDURE desactivar_usuario(p_idusu INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE usuarios SET estusu = 'inactivo' WHERE idusu = p_idusu;
END;
$$;

-- Procedimiento: registrar_producto
CREATE OR REPLACE PROCEDURE registrar_producto(
    p_idres INT,
    p_idcat INT,
    p_nompro VARCHAR(100),
    p_despro VARCHAR(255),
    p_prepro DECIMAL(10,2),
    p_imgpro VARCHAR(200),
    p_stopro INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO productos (idres, idcat, nompro, despro, prepro, imgpro, stopro)
    VALUES (p_idres, p_idcat, p_nompro, p_despro, p_prepro, p_imgpro, p_stopro);
END;
$$;

-- Procedimiento: actualizar_producto
CREATE OR REPLACE PROCEDURE actualizar_producto(
    p_idpro INT,
    p_nompro VARCHAR(100),
    p_despro VARCHAR(255),
    p_prepro DECIMAL(10,2),
    p_imgpro VARCHAR(200),
    p_stopro INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET nompro = p_nompro,
        despro = p_despro,
        prepro = p_prepro,
        imgpro = p_imgpro,
        stopro = p_stopro
    WHERE idpro = p_idpro;
END;
$$;

-- Procedimiento: eliminar_producto
CREATE OR REPLACE PROCEDURE eliminar_producto(p_idpro INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos WHERE idpro = p_idpro;
END;
$$;

-- Procedimiento: agregar_al_carrito
CREATE OR REPLACE PROCEDURE agregar_al_carrito(
    p_idusu INT,
    p_idpro INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    existe INT;
BEGIN
    SELECT COUNT(*) INTO existe
    FROM carritos
    WHERE idusu = p_idusu AND idpro = p_idpro;

    IF existe > 0 THEN
        UPDATE carritos
        SET canprocar = canprocar + p_cantidad
        WHERE idusu = p_idusu AND idpro = p_idpro;
    ELSE
        INSERT INTO carritos (idusu, idpro, canprocar)
        VALUES (p_idusu, p_idpro, p_cantidad);
    END IF;
END;
$$;

-- Procedimiento: actualizar_carrito
CREATE OR REPLACE PROCEDURE actualizar_carrito(p_idcar INT, p_cantidad INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE carritos SET canprocar = p_cantidad WHERE idcar = p_idcar;
END;
$$;

-- Procedimiento: eliminar_del_carrito
CREATE OR REPLACE PROCEDURE eliminar_del_carrito(p_idcar INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM carritos WHERE idcar = p_idcar;
END;
$$;

-- Procedimiento: vaciar_carrito
CREATE OR REPLACE PROCEDURE vaciar_carrito(p_idusu INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM carritos WHERE idusu = p_idusu;
END;
$$;

-- Procedimiento: crear_pedido
CREATE OR REPLACE PROCEDURE crear_pedido(p_idusu INT, p_idres INT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO pedidos (idusu, idres, estped)
    VALUES (p_idusu, p_idres, 'pendiente');
END;
$$;

-- Función: confirmar_pedido (retorna el ID del pedido creado)
CREATE OR REPLACE FUNCTION confirmar_pedido(p_idusu INT, p_idres INT)
RETURNS TABLE(id_pedido_creado INT)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido INT;
BEGIN
    -- Crear el pedido vacío
    INSERT INTO pedidos (idusu, idres, estped)
    VALUES (p_idusu, p_idres, 'pendiente')
    RETURNING idped INTO nuevo_pedido;

    -- Pasar los productos del carrito al detalle del pedido
    INSERT INTO detalle_pedidos (idped, idpro, cantidad, precio_unitario)
    SELECT nuevo_pedido, c.idpro, c.canprocar, p.prepro
    FROM carritos c
    INNER JOIN productos p ON c.idpro = p.idpro
    WHERE c.idusu = p_idusu;

    -- Vaciar el carrito (el trigger ya no lo hace automáticamente)
    DELETE FROM carritos WHERE idusu = p_idusu;

    -- Devolver el id del pedido recién creado
    RETURN QUERY SELECT nuevo_pedido;
END;
$$;

-- Procedimiento: cambiar_estado_pedido
CREATE OR REPLACE PROCEDURE cambiar_estado_pedido(p_idped INT, p_estado estado_pedido)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE pedidos SET estped = p_estado, fecha_actualizacion = CURRENT_TIMESTAMP WHERE idped = p_idped;
END;
$$;

-- Procedimiento: asignar_repartidor
CREATE OR REPLACE PROCEDURE asignar_repartidor(p_idped INT, p_idrep INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE pedidos
    SET idrep = p_idrep, estped = 'aceptado', fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE idped = p_idped;
END;
$$;

-- Procedimiento: registrar_pago
CREATE OR REPLACE PROCEDURE registrar_pago(
    p_idped INT,
    p_metodo metodo_pago,
    p_monto DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO pagos (idped, metodo, estado, monto)
    VALUES (p_idped, p_metodo, 'pendiente', p_monto);
END;
$$;

-- Procedimiento: actualizar_estado_pago
CREATE OR REPLACE PROCEDURE actualizar_estado_pago(p_idpag INT, p_estado estado_pago)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE pagos SET estado = p_estado WHERE idpag = p_idpag;
END;
$$;

-- Procedimiento: reset_intentos_fallidos
CREATE OR REPLACE PROCEDURE reset_intentos_fallidos(p_email VARCHAR(100))
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE usuarios 
    SET intentos_fallidos = 0, 
        bloqueado_hasta = NULL,
        ultimo_intento = NULL
    WHERE corusu = p_email;
END;
$$;

-- Procedimiento: incrementar_intentos_fallidos
CREATE OR REPLACE PROCEDURE incrementar_intentos_fallidos(
    p_email VARCHAR(100),
    p_ip VARCHAR(45),
    p_user_agent TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    intentos_actuales INT DEFAULT 0;
    max_intentos INT DEFAULT 5;
    tiempo_bloqueo INT DEFAULT 15;
BEGIN
    SELECT intentos_fallidos INTO intentos_actuales 
    FROM usuarios WHERE corusu = p_email;
    
    intentos_actuales := COALESCE(intentos_actuales, 0) + 1;
    
    IF intentos_actuales >= max_intentos THEN
        UPDATE usuarios 
        SET intentos_fallidos = intentos_actuales,
            bloqueado_hasta = CURRENT_TIMESTAMP + (tiempo_bloqueo || ' minutes')::INTERVAL,
            ultimo_intento = CURRENT_TIMESTAMP
        WHERE corusu = p_email;
    ELSE
        UPDATE usuarios 
        SET intentos_fallidos = intentos_actuales,
            ultimo_intento = CURRENT_TIMESTAMP
        WHERE corusu = p_email;
    END IF;
    
    INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
    VALUES (p_email, p_ip, FALSE, p_user_agent, 
            CASE WHEN intentos_actuales >= max_intentos THEN 'CUENTA_BLOQUEADA' ELSE 'CREDENCIALES_INCORRECTAS' END);
END;
$$;

-- Procedimiento: login_exitoso
CREATE OR REPLACE PROCEDURE login_exitoso(
    p_email VARCHAR(100),
    p_ip VARCHAR(45),
    p_user_agent TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL reset_intentos_fallidos(p_email);
    
    INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
    VALUES (p_email, p_ip, TRUE, p_user_agent, 'LOGIN_EXITOSO');
END;
$$;

-- Función: verificar_bloqueo_cuenta (retorna estado de bloqueo)
CREATE OR REPLACE FUNCTION verificar_bloqueo_cuenta(p_email VARCHAR(100))
RETURNS TABLE(bloqueada BOOLEAN, intentos INT, tiempo_restante INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_intentos INT;
    v_bloqueo_hasta TIMESTAMP;
BEGIN
    SELECT intentos_fallidos, bloqueado_hasta 
    INTO v_intentos, v_bloqueo_hasta
    FROM usuarios WHERE corusu = p_email;
    
    IF v_bloqueo_hasta IS NOT NULL AND v_bloqueo_hasta > CURRENT_TIMESTAMP THEN
        RETURN QUERY SELECT 
            TRUE, 
            COALESCE(v_intentos, 0), 
            EXTRACT(EPOCH FROM (v_bloqueo_hasta - CURRENT_TIMESTAMP))::INT / 60;
    ELSE
        IF v_bloqueo_hasta IS NOT NULL AND v_bloqueo_hasta <= CURRENT_TIMESTAMP THEN
            UPDATE usuarios 
            SET intentos_fallidos = 0, bloqueado_hasta = NULL, ultimo_intento = NULL
            WHERE corusu = p_email;
        END IF;
        
        RETURN QUERY SELECT FALSE, COALESCE(v_intentos, 0), 0;
    END IF;
END;
$$;

-- Procedimiento: crear_token_recuperacion
CREATE OR REPLACE PROCEDURE crear_token_recuperacion(
    p_email VARCHAR(100),
    p_token VARCHAR(255),
    p_ip VARCHAR(45),
    p_user_agent TEXT,
    INOUT p_token_creado BOOLEAN DEFAULT FALSE
)
LANGUAGE plpgsql
AS $$
DECLARE
    usuario_existe INT DEFAULT 0;
    tokens_activos INT DEFAULT 0;
BEGIN
    SELECT COUNT(*) INTO usuario_existe 
    FROM usuarios WHERE corusu = p_email AND estusu = 'activo';
    
    IF usuario_existe > 0 THEN
        SELECT COUNT(*) INTO tokens_activos 
        FROM tokens_recuperacion 
        WHERE email = p_email AND usado = FALSE AND fecha_expiracion > CURRENT_TIMESTAMP;
        
        IF tokens_activos < 3 THEN
            INSERT INTO tokens_recuperacion (email, token, fecha_expiracion, ip_solicitud, user_agent)
            VALUES (p_email, p_token, CURRENT_TIMESTAMP + INTERVAL '1 hour', p_ip, p_user_agent);
            
            p_token_creado := TRUE;
        END IF;
    END IF;
END;
$$;

-- Función: validar_token_recuperacion
CREATE OR REPLACE FUNCTION validar_token_recuperacion(p_token VARCHAR(255))
RETURNS TABLE(valido BOOLEAN, email VARCHAR(100), tiempo_restante INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_email VARCHAR(100);
    v_expiracion TIMESTAMP;
BEGIN
    SELECT t.email, t.fecha_expiracion 
    INTO v_email, v_expiracion
    FROM tokens_recuperacion t
    WHERE t.token = p_token AND t.usado = FALSE AND t.fecha_expiracion > CURRENT_TIMESTAMP
    LIMIT 1;
    
    IF v_email IS NOT NULL THEN
        RETURN QUERY SELECT 
            TRUE, 
            v_email, 
            EXTRACT(EPOCH FROM (v_expiracion - CURRENT_TIMESTAMP))::INT / 60;
    ELSE
        RETURN QUERY SELECT FALSE, NULL::VARCHAR(100), 0;
    END IF;
END;
$$;

-- Procedimiento: cambiar_password_con_token
CREATE OR REPLACE PROCEDURE cambiar_password_con_token(
    p_token VARCHAR(255),
    p_nueva_password VARCHAR(255),
    p_ip VARCHAR(45),
    INOUT p_cambiado BOOLEAN DEFAULT FALSE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_email VARCHAR(100);
    v_valido BOOLEAN;
    v_tiempo INT;
BEGIN
    SELECT valido, email INTO v_valido, v_email
    FROM validar_token_recuperacion(p_token);
    
    IF v_valido = TRUE THEN
        UPDATE usuarios SET conusu = p_nueva_password WHERE corusu = v_email;
        UPDATE tokens_recuperacion SET usado = TRUE WHERE token = p_token;
        CALL reset_intentos_fallidos(v_email);
        
        INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
        VALUES (v_email, p_ip, TRUE, 'PASSWORD_RECOVERY', 'PASSWORD_CAMBIADO_EXITOSAMENTE');
        
        p_cambiado := TRUE;
    END IF;
END;
$$;

-- Procedimiento: limpiar_tokens_expirados
CREATE OR REPLACE PROCEDURE limpiar_tokens_expirados()
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM tokens_recuperacion 
    WHERE fecha_expiracion < CURRENT_TIMESTAMP OR usado = TRUE;
END;
$$;

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger: Descontar stock al insertar detalle de pedido
CREATE OR REPLACE FUNCTION fn_descontar_stock()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE productos
    SET stopro = stopro - NEW.cantidad
    WHERE idpro = NEW.idpro;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_descontar_stock
AFTER INSERT ON detalle_pedidos
FOR EACH ROW EXECUTE FUNCTION fn_descontar_stock();

-- Trigger: Actualizar fecha de pedido
CREATE OR REPLACE FUNCTION fn_actualizar_fecha_pedido()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_fecha_pedido
BEFORE UPDATE ON pedidos
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_fecha_pedido();

-- Trigger: Crear restaurante cuando usuario cambia a rol restaurante
CREATE OR REPLACE FUNCTION fn_after_role_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rolusu = 'restaurante' AND OLD.rolusu != 'restaurante' THEN
        INSERT INTO restaurantes (idusu, nomres, desres, dirres, telres, estres)
        VALUES (NEW.idusu, NEW.nomusu, 'Mi restaurante', NEW.dirusu, '0000000000', 'activo');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_after_role_update
AFTER UPDATE ON usuarios
FOR EACH ROW EXECUTE FUNCTION fn_after_role_update();

-- =====================================================
-- VISTAS
-- =====================================================

-- Vista: Historial completo de pedidos
CREATE OR REPLACE VIEW vista_historial AS
SELECT
    p.idped,
    u.nomusu AS cliente,
    r.nomres AS restaurante,
    rep.nomrep AS repartidor,
    p.estped AS estado_pedido,
    SUM(
        d.cantidad * d.precio_unitario
    ) AS total_pedido,
    pg.metodo AS metodo_pago,
    pg.estado AS estado_pago,
    p.fecha_creacion,
    p.fecha_actualizacion
FROM
    pedidos p
    JOIN usuarios u ON p.idusu = u.idusu
    JOIN restaurantes r ON p.idres = r.idres
    LEFT JOIN repartidores rep ON p.idrep = rep.idrep
    JOIN detalle_pedidos d ON p.idped = d.idped
    LEFT JOIN pagos pg ON p.idped = pg.idped
GROUP BY
    p.idped,
    u.nomusu,
    r.nomres,
    rep.nomrep,
    p.estped,
    pg.metodo,
    pg.estado,
    p.fecha_creacion,
    p.fecha_actualizacion;

-- Vista: Menú de restaurantes
CREATE OR REPLACE VIEW vista_menu_restaurante AS
SELECT
    r.nomres AS restaurante,
    c.tipcat AS categoria,
    p.nompro AS producto,
    p.despro AS descripcion,
    p.prepro AS precio,
    p.stopro AS stock,
    p.imgpro AS imagen
FROM
    productos p
    JOIN restaurantes r ON p.idres = r.idres
    JOIN categorias c ON p.idcat = c.idcat
WHERE
    r.estres = 'activo';

-- Vista: Pagos
CREATE OR REPLACE VIEW vista_pagos AS
SELECT
    p.idped,
    u.nomusu AS cliente,
    r.nomres AS restaurante,
    pg.metodo,
    pg.estado,
    pg.monto,
    pg.fecha
FROM
    pagos pg
    JOIN pedidos p ON pg.idped = p.idped
    JOIN usuarios u ON p.idusu = u.idusu
    JOIN restaurantes r ON p.idres = r.idres;

-- Vista: Pedidos por cliente
CREATE OR REPLACE VIEW vista_pedidos_cliente AS
SELECT
    u.nomusu AS cliente,
    r.nomres AS restaurante,
    p.idped,
    p.estped AS estado,
    SUM(
        d.cantidad * d.precio_unitario
    ) AS total,
    p.fecha_creacion,
    p.fecha_actualizacion
FROM
    pedidos p
    JOIN usuarios u ON p.idusu = u.idusu
    JOIN restaurantes r ON p.idres = r.idres
    JOIN detalle_pedidos d ON p.idped = d.idped
GROUP BY
    p.idped,
    u.nomusu,
    r.nomres,
    p.estped,
    p.fecha_creacion,
    p.fecha_actualizacion;

-- Vista: Pedidos por repartidor
CREATE OR REPLACE VIEW vista_pedidos_repartidor AS
SELECT
    rep.nomrep AS repartidor,
    cli.nomusu AS cliente,
    res.nomres AS restaurante,
    p.idped,
    p.estped AS estado,
    p.fecha_creacion,
    p.fecha_actualizacion
FROM
    pedidos p
    JOIN repartidores rep ON p.idrep = rep.idrep
    JOIN usuarios cli ON p.idusu = cli.idusu
    JOIN restaurantes res ON p.idres = res.idres;

-- =====================================================
-- DATOS INICIALES (Categorías)
-- =====================================================

INSERT INTO
    categorias (tipcat)
VALUES ('Comida Rápida'),
    ('Bebidas'),
    ('Postres'),
    ('Entradas'),
    ('Platos Fuertes'),
    ('Comida Saludable'),
    ('Comida Internacional'),
    ('Promociones'),
    ('Comida Tipica') ON CONFLICT DO NOTHING;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================