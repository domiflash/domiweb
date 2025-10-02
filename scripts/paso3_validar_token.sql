-- Paso 3: Procedimiento validar_token_recuperacion
-- Ejecutar este comando completo en phpMyAdmin

DROP PROCEDURE IF EXISTS validar_token_recuperacion;

DELIMITER $$

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
END$$

DELIMITER ;