-- Script simplificado para phpMyAdmin - Recuperación de contraseña
-- Ejecutar comando por comando en phpMyAdmin

-- 1. Crear tabla tokens_recuperacion
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

-- 2. Crear índices
CREATE INDEX IF NOT EXISTS idx_token_email ON tokens_recuperacion(email, usado);
CREATE INDEX IF NOT EXISTS idx_token_expiracion ON tokens_recuperacion(token, fecha_expiracion, usado);