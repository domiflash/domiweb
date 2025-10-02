-- Paso 4: Procedimiento cambiar_password_con_token
-- Ejecutar este comando completo en phpMyAdmin

DROP PROCEDURE IF EXISTS cambiar_password_con_token;

DELIMITER $$

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
END$$

DELIMITER ;