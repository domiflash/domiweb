-- ============================================
-- Script para crear usuario de prueba en Render
-- ============================================

-- Verificar que la tabla usuarios existe:
SELECT COUNT(*) FROM usuarios;

-- Insertar usuario administrador de prueba
-- Email: admin@test.com
-- Password: 123456
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu) 
VALUES (
    'Administrador',
    'admin@test.com',
    'scrypt:32768:8:1$1QNl0rUpiSaLbu7U$8886b635214d6a53ae093f9d07e4872727f2766b503c4ee1c782bfdb98ff3694bfe9edd792b13adfee2b3c0fe32bca09f2a729c04b4d35389d13b7458cd7c65f',
    'Calle Principal 123',
    '3001234567',
    'administrador',
    'activo'
);

-- Verificar que se creó:
SELECT idusu, nomusu, corusu, rolusu FROM usuarios WHERE corusu = 'admin@test.com';

-- ============================================
-- Usuario cliente de prueba
-- Email: cliente@test.com
-- Password: 123456
-- ============================================
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu) 
VALUES (
    'Cliente Prueba',
    'cliente@test.com',
    'scrypt:32768:8:1$1QNl0rUpiSaLbu7U$8886b635214d6a53ae093f9d07e4872727f2766b503c4ee1c782bfdb98ff3694bfe9edd792b13adfee2b3c0fe32bca09f2a729c04b4d35389d13b7458cd7c65f',
    'Calle 45 #67-89',
    '3009876543',
    'cliente',
    'activo'
);

-- Ver todos los usuarios:
SELECT idusu, nomusu, corusu, rolusu, estusu FROM usuarios;
