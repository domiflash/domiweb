-- Script SQL para implementar sistema de recuperación de contraseña
-- Crear tabla para tokens de recuperación y procedimientos almacenados

USE dbflash;

-- Crear tabla para tokens de recuperación de contraseña
CREATE TABLE IF NOT EXISTS tokens_recuperacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion DATETIME NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    ip_solicitud VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (email) REFERENCES usuarios(corusu) ON DELETE CASCADE
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_token_email ON tokens_recuperacion(email, usado);
CREATE INDEX IF NOT EXISTS idx_token_expiracion ON tokens_recuperacion(token, fecha_expiracion, usado);

-- Procedimiento para crear token de recuperación
DROP PROCEDURE IF EXISTS crear_token_recuperacion;
DELIMITER //
CREATE PROCEDURE crear_token_recuperacion(
    IN p_email VARCHAR(100),
    IN p_token VARCHAR(255),
    IN p_ip VARCHAR(45),
    IN p_user_agent TEXT,
    OUT p_token_creado BOOLEAN
)
BEGIN
    DECLARE usuario_existe INT DEFAULT 0;
    DECLARE tokens_activos INT DEFAULT 0;
    
    -- Verificar si el usuario existe
    SELECT COUNT(*) INTO usuario_existe 
    FROM usuarios WHERE corusu = p_email AND estusu = 'activo';
    
    IF usuario_existe > 0 THEN
        -- Verificar tokens activos (máximo 3 por usuario)
        SELECT COUNT(*) INTO tokens_activos 
        FROM tokens_recuperacion 
        WHERE email = p_email AND usado = FALSE AND fecha_expiracion > NOW();
        
        IF tokens_activos < 3 THEN
            -- Crear nuevo token (válido por 1 hora)
            INSERT INTO tokens_recuperacion (email, token, fecha_expiracion, ip_solicitud, user_agent)
            VALUES (p_email, p_token, DATE_ADD(NOW(), INTERVAL 1 HOUR), p_ip, p_user_agent);
            
            SET p_token_creado = TRUE;
        ELSE
            SET p_token_creado = FALSE;
        END IF;
    ELSE
        SET p_token_creado = FALSE;
    END IF;
END //
DELIMITER ;

-- Procedimiento para validar token de recuperación
DROP PROCEDURE IF EXISTS validar_token_recuperacion;
DELIMITER //
CREATE PROCEDURE validar_token_recuperacion(
    IN p_token VARCHAR(255),
    OUT p_valido BOOLEAN,
    OUT p_email VARCHAR(100),
    OUT p_tiempo_restante INT
)
BEGIN
    DECLARE token_expiracion DATETIME;
    
    -- Buscar token válido
    SELECT email, fecha_expiracion 
    INTO p_email, token_expiracion
    FROM tokens_recuperacion 
    WHERE token = p_token AND usado = FALSE AND fecha_expiracion > NOW()
    LIMIT 1;
    
    IF p_email IS NOT NULL THEN
        SET p_valido = TRUE;
        SET p_tiempo_restante = TIMESTAMPDIFF(MINUTE, NOW(), token_expiracion);
    ELSE
        SET p_valido = FALSE;
        SET p_email = NULL;
        SET p_tiempo_restante = 0;
    END IF;
END //
DELIMITER ;

-- Procedimiento para usar token y cambiar contraseña
DROP PROCEDURE IF EXISTS cambiar_password_con_token;
DELIMITER //
CREATE PROCEDURE cambiar_password_con_token(
    IN p_token VARCHAR(255),
    IN p_nueva_password VARCHAR(255),
    IN p_ip VARCHAR(45),
    OUT p_cambiado BOOLEAN
)
BEGIN
    DECLARE v_email VARCHAR(100);
    DECLARE token_valido BOOLEAN DEFAULT FALSE;
    DECLARE tiempo_restante INT;
    
    -- Validar token
    CALL validar_token_recuperacion(p_token, token_valido, v_email, tiempo_restante);
    
    IF token_valido = TRUE THEN
        -- Cambiar contraseña
        UPDATE usuarios 
        SET conusu = p_nueva_password
        WHERE corusu = v_email;
        
        -- Marcar token como usado
        UPDATE tokens_recuperacion 
        SET usado = TRUE 
        WHERE token = p_token;
        
        -- Resetear intentos fallidos por seguridad
        CALL reset_intentos_fallidos(v_email);
        
        -- Log del cambio exitoso
        INSERT INTO log_intentos_acceso (email, ip_address, exito, user_agent, motivo_fallo)
        VALUES (v_email, p_ip, TRUE, 'PASSWORD_RECOVERY', 'PASSWORD_CAMBIADO_EXITOSAMENTE');
        
        SET p_cambiado = TRUE;
    ELSE
        SET p_cambiado = FALSE;
    END IF;
END //
DELIMITER ;

-- Procedimiento para limpiar tokens expirados
DROP PROCEDURE IF EXISTS limpiar_tokens_expirados;
DELIMITER //
CREATE PROCEDURE limpiar_tokens_expirados()
BEGIN
    DELETE FROM tokens_recuperacion 
    WHERE fecha_expiracion < NOW() OR usado = TRUE;
END //
DELIMITER ;

-- Procedimiento para obtener estadísticas de recuperación
DROP PROCEDURE IF EXISTS estadisticas_recuperacion;
DELIMITER //
CREATE PROCEDURE estadisticas_recuperacion(
    IN p_dias INT DEFAULT 7
)
BEGIN
    SELECT 
        DATE(fecha_creacion) as fecha,
        COUNT(*) as tokens_creados,
        SUM(CASE WHEN usado = TRUE THEN 1 ELSE 0 END) as tokens_usados,
        COUNT(DISTINCT email) as usuarios_unicos
    FROM tokens_recuperacion 
    WHERE fecha_creacion >= DATE_SUB(NOW(), INTERVAL p_dias DAY)
    GROUP BY DATE(fecha_creacion)
    ORDER BY fecha DESC;
END //
DELIMITER ;