-- Paso 5: Procedimientos adicionales
-- Ejecutar este comando completo en phpMyAdmin

-- Procedimiento para limpiar tokens expirados
DROP PROCEDURE IF EXISTS limpiar_tokens_expirados;

DELIMITER $$

CREATE PROCEDURE limpiar_tokens_expirados()
BEGIN
    DELETE FROM tokens_recuperacion 
    WHERE fecha_expiracion < NOW() OR usado = TRUE;
END$$

DELIMITER ;

-- Procedimiento para estadísticas de recuperación
DROP PROCEDURE IF EXISTS estadisticas_recuperacion;

DELIMITER $$

CREATE PROCEDURE estadisticas_recuperacion(
    IN p_dias INT
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
END$$

DELIMITER ;