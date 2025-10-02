-- Script SQL para implementar límite de intentos de login
-- Agregar campos a la tabla usuarios para tracking de intentos

USE domiweb;

-- Agregar columnas para control de intentos de login
ALTER TABLE usuarios 
ADD COLUMN intentos_fallidos INT DEFAULT 0,
ADD COLUMN bloqueado_hasta DATETIME NULL,
ADD COLUMN ultimo_intento DATETIME NULL;

-- Crear tabla para log de intentos de acceso (auditoría)
CREATE TABLE IF NOT EXISTS log_intentos_acceso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    exito BOOLEAN DEFAULT FALSE,
    fecha_intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    motivo_fallo VARCHAR(100)
);

-- Crear índices para optimizar consultas
CREATE INDEX idx_usuarios_email_intentos ON usuarios(corusu, intentos_fallidos);
CREATE INDEX idx_log_email_fecha ON log_intentos_acceso(email, fecha_intento);

-- Procedimiento para resetear intentos fallidos
DELIMITER //
CREATE PROCEDURE reset_intentos_fallidos(IN p_email VARCHAR(100))
BEGIN
    UPDATE usuarios 
    SET intentos_fallidos = 0, 
        bloqueado_hasta = NULL,
        ultimo_intento = NULL
    WHERE corusu = p_email;
END //
DELIMITER ;

-- Procedimiento para incrementar intentos fallidos
DELIMITER //
CREATE PROCEDURE incrementar_intentos_fallidos(
    IN p_email VARCHAR(100),
    IN p_ip VARCHAR(45),
    IN p_user_agent TEXT
)
BEGIN
    DECLARE intentos_actuales INT DEFAULT 0;
    DECLARE max_intentos INT DEFAULT 5;
    DECLARE tiempo_bloqueo INT DEFAULT 15; -- minutos
    
    -- Obtener intentos actuales
    SELECT intentos_fallidos INTO intentos_actuales 
    FROM usuarios WHERE corusu = p_email;
    
    -- Incrementar intentos
    SET intentos_actuales = intentos_actuales + 1;
    
    -- Actualizar usuario
    IF intentos_actuales >= max_intentos THEN
        -- Bloquear cuenta por tiempo determinado
        UPDATE usuarios 
        SET intentos_fallidos = intentos_actuales,
            bloqueado_hasta = DATE_ADD(NOW(), INTERVAL tiempo_bloqueo MINUTE),
            ultimo_intento = NOW()
        WHERE corusu = p_email;
    ELSE
        -- Solo incrementar intentos
        UPDATE usuarios 
        SET intentos_fallidos = intentos_actuales,
            ultimo_intento = NOW()
        WHERE corusu = p_email;
    END IF;
    
    -- Log del intento fallido
    INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
    VALUES (p_email, p_ip, FALSE, p_user_agent, 
            IF(intentos_actuales >= max_intentos, 'CUENTA_BLOQUEADA', 'CREDENCIALES_INCORRECTAS'));
            
END //
DELIMITER ;

-- Procedimiento para verificar si cuenta está bloqueada
DELIMITER //
CREATE PROCEDURE verificar_bloqueo_cuenta(
    IN p_email VARCHAR(100),
    OUT p_bloqueada BOOLEAN,
    OUT p_intentos INT,
    OUT p_tiempo_restante INT
)
BEGIN
    DECLARE bloqueo_hasta DATETIME;
    
    SELECT intentos_fallidos, bloqueado_hasta 
    INTO p_intentos, bloqueo_hasta
    FROM usuarios WHERE corusu = p_email;
    
    -- Verificar si está bloqueada
    IF bloqueo_hasta IS NOT NULL AND bloqueo_hasta > NOW() THEN
        SET p_bloqueada = TRUE;
        SET p_tiempo_restante = TIMESTAMPDIFF(MINUTE, NOW(), bloqueo_hasta);
    ELSE
        SET p_bloqueada = FALSE;
        SET p_tiempo_restante = 0;
        
        -- Si el bloqueo ya expiró, resetear
        IF bloqueo_hasta IS NOT NULL AND bloqueo_hasta <= NOW() THEN
            UPDATE usuarios 
            SET intentos_fallidos = 0, bloqueado_hasta = NULL, ultimo_intento = NULL
            WHERE corusu = p_email;
        END IF;
    END IF;
END //
DELIMITER ;

-- Procedimiento para login exitoso
DELIMITER //
CREATE PROCEDURE login_exitoso(
    IN p_email VARCHAR(100),
    IN p_ip VARCHAR(45),
    IN p_user_agent TEXT
)
BEGIN
    -- Resetear intentos fallidos
    CALL reset_intentos_fallidos(p_email);
    
    -- Log del intento exitoso
    INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
    VALUES (p_email, p_ip, TRUE, p_user_agent, 'LOGIN_EXITOSO');
END //
DELIMITER ;