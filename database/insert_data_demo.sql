-- ============================================
-- Script de Datos Demo para DomiFlash
-- ============================================
-- Propósito: Poblar la base de datos con datos de ejemplo para presentación y pruebas
-- Ejecutar después de crear el esquema con dbflash_postgresql.sql
-- ============================================

-- IMPORTANTE: Este script asume que ya existe:
-- - 1 usuario administrador (admin@domiflash)
-- Para crear más usuarios, necesitas generar los hashes de contraseña con scrypt en Python

-- ============================================
-- 1. USUARIOS DE EJEMPLO
-- ============================================

-- Restaurantes
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu) VALUES
('Pizzería Bella Napoli', 'napoli@domiflash.com', 'scrypt:32768:8:1$salt123$hash123', 'Cra 45 #123-45, Centro', '3001234567', 'restaurante', 'activo'),
('Hamburguesas El Rancho', 'rancho@domiflash.com', 'scrypt:32768:8:1$salt456$hash456', 'Av. Libertador #67-89, Norte', '3009876543', 'restaurante', 'activo'),
('Comida Asiática Dragon Wok', 'dragon@domiflash.com', 'scrypt:32768:8:1$salt789$hash789', 'Calle 72 #34-12, Chapinero', '3105556677', 'restaurante', 'activo');

-- Repartidores
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu) VALUES
('Carlos Rodríguez', 'carlos.repartidor@domiflash.com', 'scrypt:32768:8:1$saltabc$hashabc', 'Cra 10 #20-30', '3112223344', 'repartidor', 'activo'),
('María González', 'maria.repartidor@domiflash.com', 'scrypt:32768:8:1$saltdef$hashdef', 'Calle 50 #15-25', '3123334455', 'repartidor', 'activo');

-- Clientes
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, telusu, rolusu, estusu) VALUES
('Juan Pérez', 'juan.perez@gmail.com', 'scrypt:32768:8:1$saltghi$hashghi', 'Cra 7 #45-67, Apto 301', '3134445566', 'cliente', 'activo'),
('Ana Martínez', 'ana.martinez@gmail.com', 'scrypt:32768:8:1$saltjkl$hashjkl', 'Calle 100 #20-40, Casa 5', '3145556677', 'cliente', 'activo'),
('Pedro López', 'pedro.lopez@hotmail.com', 'scrypt:32768:8:1$saltmno$hashmno', 'Cra 15 #80-90, Edificio Central', '3156667788', 'cliente', 'activo'),
('Laura Gómez', 'laura.gomez@yahoo.com', 'scrypt:32768:8:1$saltpqr$hashpqr', 'Av. 68 #123-45, Apto 502', '3167778899', 'cliente', 'activo'),
('Diego Silva', 'diego.silva@outlook.com', 'scrypt:32768:8:1$saltstu$hashstu', 'Calle 26 #50-60', '3178889900', 'cliente', 'activo');

-- Obtener IDs para referencias (ajustar según tu BD)
-- SELECT idusu, nomusu, rolusu FROM usuarios WHERE rolusu IN ('restaurante', 'repartidor', 'cliente') ORDER BY rolusu, idusu;

-- ============================================
-- 2. PRODUCTOS - Pizzería Bella Napoli
-- ============================================
-- Asumiendo que Pizzería Bella Napoli tiene idusu = 2

INSERT INTO productos (idrest, nompro, despro, prepro, catpro, estpro, rutimg) VALUES
-- Pizzas
(2, 'Pizza Margarita', 'Clásica pizza con tomate, mozzarella fresca y albahaca', 28000, 'Pizzas', 'disponible', '/static/img/pizza-margarita.jpg'),
(2, 'Pizza Pepperoni', 'Pizza con abundante pepperoni y queso mozzarella', 32000, 'Pizzas', 'disponible', '/static/img/pizza-pepperoni.jpg'),
(2, 'Pizza Hawaiana', 'Pizza con jamón, piña y queso', 30000, 'Pizzas', 'disponible', '/static/img/pizza-hawaiana.jpg'),
(2, 'Pizza Cuatro Quesos', 'Deliciosa mezcla de mozzarella, parmesano, gorgonzola y provolone', 35000, 'Pizzas', 'disponible', '/static/img/pizza-4quesos.jpg'),
(2, 'Pizza Vegetariana', 'Pizza con pimientos, champiñones, cebolla, tomate y aceitunas', 31000, 'Pizzas', 'disponible', '/static/img/pizza-veggie.jpg'),
-- Bebidas
(2, 'Coca Cola 1.5L', 'Gaseosa Coca Cola familiar', 6000, 'Bebidas', 'disponible', '/static/img/coca-cola.jpg'),
(2, 'Jugo Natural Naranja', 'Jugo 100% natural de naranja recién exprimido', 8000, 'Bebidas', 'disponible', '/static/img/jugo-naranja.jpg'),
-- Entradas
(2, 'Pan de Ajo', 'Pan crujiente con mantequilla de ajo y perejil', 8000, 'Entradas', 'disponible', '/static/img/pan-ajo.jpg'),
(2, 'Alitas BBQ (8 unidades)', 'Alitas de pollo con salsa barbecue', 18000, 'Entradas', 'disponible', '/static/img/alitas-bbq.jpg');

-- ============================================
-- 3. PRODUCTOS - Hamburguesas El Rancho
-- ============================================
-- Asumiendo que Hamburguesas El Rancho tiene idusu = 3

INSERT INTO productos (idrest, nompro, despro, prepro, catpro, estpro, rutimg) VALUES
-- Hamburguesas
(3, 'Hamburguesa Clásica', 'Carne de res 200g, lechuga, tomate, cebolla, pepinillos', 22000, 'Hamburguesas', 'disponible', '/static/img/burger-classic.jpg'),
(3, 'Hamburguesa BBQ Bacon', 'Carne 200g, tocineta, queso cheddar, salsa BBQ, aros de cebolla', 28000, 'Hamburguesas', 'disponible', '/static/img/burger-bbq.jpg'),
(3, 'Hamburguesa Doble Queso', 'Doble carne 400g, doble queso americano, salsa especial', 32000, 'Hamburguesas', 'disponible', '/static/img/burger-doble.jpg'),
(3, 'Hamburguesa de Pollo', 'Pechuga de pollo apanada, lechuga, tomate, mayonesa', 20000, 'Hamburguesas', 'disponible', '/static/img/burger-pollo.jpg'),
-- Acompañamientos
(3, 'Papas Fritas Grandes', 'Papas criollas fritas con sal', 8000, 'Acompañamientos', 'disponible', '/static/img/papas-fritas.jpg'),
(3, 'Aros de Cebolla', 'Aros de cebolla apanados y fritos', 9000, 'Acompañamientos', 'disponible', '/static/img/aros-cebolla.jpg'),
-- Bebidas
(3, 'Limonada Natural', 'Limonada hecha en casa', 7000, 'Bebidas', 'disponible', '/static/img/limonada.jpg'),
(3, 'Malteada de Vainilla', 'Malteada cremosa de vainilla', 10000, 'Bebidas', 'disponible', '/static/img/malteada-vainilla.jpg');

-- ============================================
-- 4. PRODUCTOS - Comida Asiática Dragon Wok
-- ============================================
-- Asumiendo que Dragon Wok tiene idusu = 4

INSERT INTO productos (idrest, nompro, despro, prepro, catpro, estpro, rutimg) VALUES
-- Platos principales
(4, 'Arroz Chino con Pollo', 'Arroz salteado con vegetales, pollo y salsa de soya', 24000, 'Platos Principales', 'disponible', '/static/img/arroz-pollo.jpg'),
(4, 'Wok de Carne con Verduras', 'Carne de res salteada con brócoli, zanahoria y pimentón', 26000, 'Platos Principales', 'disponible', '/static/img/wok-carne.jpg'),
(4, 'Chow Mein de Camarones', 'Fideos salteados con camarones y vegetales', 30000, 'Platos Principales', 'disponible', '/static/img/chow-mein.jpg'),
(4, 'Pollo Agridulce', 'Trozos de pollo en salsa agridulce con piña', 25000, 'Platos Principales', 'disponible', '/static/img/pollo-agridulce.jpg'),
-- Entradas
(4, 'Rollitos Primavera (4 unidades)', 'Rollitos crujientes rellenos de vegetales', 12000, 'Entradas', 'disponible', '/static/img/rollitos.jpg'),
(4, 'Sopa Wonton', 'Sopa tradicional con wontons de cerdo', 15000, 'Entradas', 'disponible', '/static/img/sopa-wonton.jpg'),
-- Bebidas
(4, 'Té Verde Helado', 'Té verde natural servido frío', 6000, 'Bebidas', 'disponible', '/static/img/te-verde.jpg');

-- ============================================
-- 5. PEDIDOS DE EJEMPLO
-- ============================================
-- Nota: Ajustar los IDs según los generados en tu BD

-- Pedido 1: Completado - Cliente Juan Pérez (idusu=6) - Pizzería Napoli (idrest=2) - Repartidor Carlos (idrepa=4)
INSERT INTO pedidos (idcli, idrest, idrepa, fecped, estped, totped, dirped, metpag, tardom, obsped) VALUES
(6, 2, 5, CURRENT_TIMESTAMP - INTERVAL '2 days', 'entregado', 64000, 'Cra 7 #45-67, Apto 301', 'efectivo', 8000, 'Tocar timbre 301');

-- Detalle del pedido 1
INSERT INTO detalle_pedidos (idped, idpro, canpro, prepro) VALUES
(1, 1, 1, 28000),  -- Pizza Margarita
(1, 2, 1, 32000),  -- Pizza Pepperoni
(1, 6, 1, 6000);   -- Coca Cola 1.5L

-- Pedido 2: En preparación - Cliente Ana Martínez (idusu=7) - El Rancho (idrest=3)
INSERT INTO pedidos (idcli, idrest, fecped, estped, totped, dirped, metpag, tardom, obsped) VALUES
(7, 3, CURRENT_TIMESTAMP - INTERVAL '30 minutes', 'en preparacion', 60000, 'Calle 100 #20-40, Casa 5', 'tarjeta', 10000, 'Sin cebolla en las hamburguesas');

-- Detalle del pedido 2
INSERT INTO detalle_pedidos (idped, idpro, canpro, prepro) VALUES
(2, 10, 2, 28000),  -- 2x Hamburguesa BBQ Bacon
(2, 14, 1, 8000),   -- Papas Fritas
(2, 17, 2, 10000);  -- 2x Malteada

-- Pedido 3: En camino - Cliente Pedro López (idusu=8) - Dragon Wok (idrest=4) - Repartidor María (idrepa=5)
INSERT INTO pedidos (idcli, idrest, idrepa, fecped, estped, totped, dirped, metpag, tardom, obsped) VALUES
(8, 4, 6, CURRENT_TIMESTAMP - INTERVAL '45 minutes', 'en camino', 69000, 'Cra 15 #80-90, Edificio Central', 'efectivo', 12000, 'Llamar al llegar');

-- Detalle del pedido 3
INSERT INTO detalle_pedidos (idped, idpro, canpro, prepro) VALUES
(3, 19, 1, 26000),  -- Wok de Carne
(3, 21, 1, 25000),  -- Pollo Agridulce
(3, 22, 2, 12000),  -- 2x Rollitos Primavera
(3, 24, 1, 6000);   -- Té Verde

-- Pedido 4: Pendiente - Cliente Laura Gómez (idusu=9) - Pizzería Napoli (idrest=2)
INSERT INTO pedidos (idcli, idrest, fecped, estped, totped, dirped, metpag, tardom, obsped) VALUES
(9, 2, CURRENT_TIMESTAMP - INTERVAL '10 minutes', 'pendiente', 83000, 'Av. 68 #123-45, Apto 502', 'tarjeta', 10000, 'Pizza sin albahaca');

-- Detalle del pedido 4
INSERT INTO detalle_pedidos (idped, idpro, canpro, prepro) VALUES
(4, 4, 1, 35000),  -- Pizza 4 Quesos
(4, 5, 1, 31000),  -- Pizza Vegetariana
(4, 8, 2, 8000),   -- 2x Pan de Ajo
(4, 7, 1, 8000);   -- Jugo Naranja

-- Pedido 5: Entregado (pedido antiguo) - Cliente Diego Silva (idusu=10) - El Rancho (idrest=3) - Repartidor Carlos (idrepa=4)
INSERT INTO pedidos (idcli, idrest, idrepa, fecped, estped, totped, dirped, metpag, tardom, obsped) VALUES
(10, 3, 5, CURRENT_TIMESTAMP - INTERVAL '5 days', 'entregado', 50000, 'Calle 26 #50-60', 'efectivo', 8000, '');

-- Detalle del pedido 5
INSERT INTO detalle_pedidos (idped, idpro, canpro, prepro) VALUES
(5, 11, 1, 22000),  -- Hamburguesa Clásica
(5, 13, 1, 20000),  -- Hamburguesa de Pollo
(5, 14, 2, 8000);   -- 2x Papas Fritas

-- ============================================
-- 6. CARRITOS ACTIVOS (Ejemplos)
-- ============================================

-- Carrito de Ana Martínez - Pizzería Napoli
INSERT INTO carritos (idcli, idpro, canpro, fecagr) VALUES
(7, 2, 2, CURRENT_TIMESTAMP),  -- 2 Pizzas Pepperoni
(7, 6, 1, CURRENT_TIMESTAMP);  -- 1 Coca Cola

-- Carrito de Diego Silva - Dragon Wok
INSERT INTO carritos (idcli, idpro, canpro, fecagr) VALUES
(10, 18, 1, CURRENT_TIMESTAMP),  -- Arroz Chino con Pollo
(10, 22, 1, CURRENT_TIMESTAMP),  -- Rollitos Primavera
(10, 24, 2, CURRENT_TIMESTAMP);  -- 2 Té Verde

-- ============================================
-- 7. PAGOS (Para pedidos completados)
-- ============================================

-- Pago del pedido 1
INSERT INTO pagos (idped, monpag, metpag, estpag, fecpag) VALUES
(1, 64000, 'efectivo', 'completado', CURRENT_TIMESTAMP - INTERVAL '2 days');

-- Pago del pedido 5
INSERT INTO pagos (idped, monpag, metpag, estpag, fecpag) VALUES
(5, 50000, 'efectivo', 'completado', CURRENT_TIMESTAMP - INTERVAL '5 days');

-- ============================================
-- 8. VERIFICACIÓN DE DATOS INSERTADOS
-- ============================================

-- Ver resumen de usuarios por rol
SELECT rolusu, COUNT(*) as cantidad FROM usuarios GROUP BY rolusu ORDER BY rolusu;

-- Ver restaurantes con sus productos
SELECT u.nomusu as restaurante, COUNT(p.idpro) as total_productos
FROM usuarios u
LEFT JOIN productos p ON u.idusu = p.idrest
WHERE u.rolusu = 'restaurante'
GROUP BY u.idusu, u.nomusu;

-- Ver pedidos por estado
SELECT estped, COUNT(*) as cantidad, SUM(totped) as total_ventas
FROM pedidos
GROUP BY estped
ORDER BY estped;

-- Ver productos más pedidos
SELECT p.nompro, COUNT(dp.idpro) as veces_pedido, SUM(dp.canpro) as cantidad_total
FROM productos p
JOIN detalle_pedidos dp ON p.idpro = dp.idpro
GROUP BY p.idpro, p.nompro
ORDER BY veces_pedido DESC
LIMIT 10;

-- ============================================
-- FIN DEL SCRIPT
-- ============================================

/*
NOTAS IMPORTANTES:

1. **Hashes de Contraseña:**
   Los hashes en este script son EJEMPLOS. Para crear usuarios reales que puedan loguearse,
   debes generar hashes scrypt válidos desde Python:
   
   ```python
   from werkzeug.security import generate_password_hash
   hash = generate_password_hash('tu_password')
   print(hash)
   ```

2. **IDs de Usuarios:**
   Los IDs asumidos (2, 3, 4 para restaurantes, etc.) pueden variar según tu BD.
   Verifica con: SELECT idusu, nomusu, rolusu FROM usuarios ORDER BY idusu;
   
   Ajusta los INSERTs de productos y pedidos con los IDs correctos.

3. **Rutas de Imágenes:**
   Las rutas '/static/img/...' son ejemplos. Necesitarás:
   - Tener las imágenes en esa carpeta
   - O usar URLs de placeholders como: 'https://via.placeholder.com/300x200'
   - O actualizar a NULL si no usas imágenes

4. **Ejecutar en Orden:**
   1. Primero dbflash_postgresql.sql (crear esquema)
   2. Crear usuario admin manualmente
   3. Luego este script de datos demo

5. **Para Producción:**
   Este script es para DEMOSTRACIÓN. En producción:
   - Genera hashes válidos para todos los usuarios
   - Usa datos reales de tu negocio
   - Ajusta precios y productos según tu oferta
*/
