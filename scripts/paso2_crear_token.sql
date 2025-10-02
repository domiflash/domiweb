-- Paso 2: Procedimiento crear_token_recuperacion
-- Ejecutar este comando completo en phpMyAdmin

DROP PROCEDURE IF EXISTS crear_token_recuperacion;

DELIMITER $$

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
END$$

DELIMITER ;