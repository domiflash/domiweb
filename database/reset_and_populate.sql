-- =====================================================
-- 🍕 DomiFlash - Script de Reset y Población de Datos
-- Elimina datos actuales e inserta datos de prueba
-- =====================================================

-- =====================================================
-- PASO 1: LIMPIAR DATOS EXISTENTES
-- =====================================================
-- Importante: Se eliminan en orden inverso por las llaves foráneas

DELETE FROM log_intentos_acceso;
DELETE FROM tokens_recuperacion;
DELETE FROM pagos;
DELETE FROM detalle_pedidos;
DELETE FROM pedidos;
DELETE FROM carritos;
DELETE FROM productos;
DELETE FROM repartidores;
DELETE FROM restaurantes;
DELETE FROM categorias;
DELETE FROM usuarios;

-- Reiniciar secuencias
ALTER SEQUENCE usuarios_idusu_seq RESTART WITH 1;
ALTER SEQUENCE categorias_idcat_seq RESTART WITH 1;
ALTER SEQUENCE restaurantes_idres_seq RESTART WITH 1;
ALTER SEQUENCE productos_idpro_seq RESTART WITH 1;
ALTER SEQUENCE repartidores_idrep_seq RESTART WITH 1;
ALTER SEQUENCE carritos_idcar_seq RESTART WITH 1;
ALTER SEQUENCE pedidos_idped_seq RESTART WITH 1;
ALTER SEQUENCE detalle_pedidos_iddet_seq RESTART WITH 1;
ALTER SEQUENCE pagos_idpag_seq RESTART WITH 1;

-- =====================================================
-- PASO 2: INSERTAR CATEGORÍAS
-- =====================================================
INSERT INTO categorias (tipcat) VALUES
('Comida Rápida'),
('Pizza'),
('Hamburguesas'),
('Comida China'),
('Comida Mexicana'),
('Postres'),
('Bebidas'),
('Ensaladas'),
('Pasta'),
('Mariscos');

-- =====================================================
-- PASO 3: INSERTAR USUARIOS
-- =====================================================
-- Contraseña para todos: 1234 (hash werkzeug)
-- Hash generado con: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('1234'))"

-- 1 ADMINISTRADOR
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu, lat_usuario, lng_usuario) VALUES
('Administrador DomiFlash', 'admin@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle Admin 123, Neiva', 'administrador', 'activo', 2.9273, -75.2819);

-- 10 CLIENTES
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu, lat_usuario, lng_usuario) VALUES
('Juan Pérez', 'cliente@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 5 #15-20, Neiva', 'cliente', 'activo', 2.9284, -75.2853),
('María González', 'maria.gonzalez@gmail.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 7 #8-45, Neiva', 'cliente', 'activo', 2.9295, -75.2870),
('Carlos Rodríguez', 'carlos.rodriguez@hotmail.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Avenida Circunvalar #20-30, Neiva', 'cliente', 'activo', 2.9310, -75.2890),
('Ana Martínez', 'ana.martinez@outlook.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 9 #12-15, Neiva', 'cliente', 'activo', 2.9250, -75.2810),
('Luis Hernández', 'luis.hernandez@yahoo.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 10 #5-30, Neiva', 'cliente', 'activo', 2.9320, -75.2900),
('Laura Torres', 'laura.torres@gmail.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 7 #18-40, Neiva', 'cliente', 'activo', 2.9265, -75.2830),
('Diego Ramírez', 'diego.ramirez@hotmail.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 15 #20-25, Neiva', 'cliente', 'activo', 2.9280, -75.2845),
('Sofía López', 'sofia.lopez@outlook.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Avenida La Toma #30-15, Neiva', 'cliente', 'activo', 2.9305, -75.2880),
('Andrés Gómez', 'andres.gomez@gmail.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 3 #8-12, Neiva', 'cliente', 'activo', 2.9240, -75.2800),
('Valentina Castro', 'valentina.castro@yahoo.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 22 #14-18, Neiva', 'cliente', 'activo', 2.9330, -75.2910);

-- 10 RESTAURANTES (usuarios)
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu, lat_usuario, lng_usuario) VALUES
('Restaurante El Sabor', 'restaurante@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 5 #10-20, Neiva', 'restaurante', 'activo', 2.9273, -75.2819),
('Pizza Express', 'pizza.express@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 8 #12-30, Neiva', 'restaurante', 'activo', 2.9285, -75.2835),
('Burger King Premium', 'burger.premium@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Avenida Pastrana #15-40, Neiva', 'restaurante', 'activo', 2.9300, -75.2860),
('China Wok', 'china.wok@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 7 #20-15, Neiva', 'restaurante', 'activo', 2.9260, -75.2825),
('Taco Loco', 'taco.loco@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 11 #8-25, Neiva', 'restaurante', 'activo', 2.9290, -75.2850),
('Postres del Valle', 'postres.valle@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 9 #16-30, Neiva', 'restaurante', 'activo', 2.9270, -75.2840),
('Café & Bebidas', 'cafe.bebidas@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 13 #10-18, Neiva', 'restaurante', 'activo', 2.9310, -75.2875),
('Green Salads', 'green.salads@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Avenida Circunvalar #22-10, Neiva', 'restaurante', 'activo', 2.9320, -75.2890),
('Pasta Italiana', 'pasta.italiana@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Carrera 4 #14-22, Neiva', 'restaurante', 'activo', 2.9255, -75.2815),
('Mar y Tierra', 'mar.tierra@restaurant.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Calle 19 #18-35, Neiva', 'restaurante', 'activo', 2.9330, -75.2905);

-- 10 REPARTIDORES (usuarios)
INSERT INTO usuarios (nomusu, corusu, conusu, dirusu, rolusu, estusu, lat_usuario, lng_usuario) VALUES
('Pedro Repartidor', 'repartidor@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Sur, Neiva', 'repartidor', 'activo', 2.9273, -75.2819),
('Miguel Delivery', 'miguel.delivery@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Centro, Neiva', 'repartidor', 'activo', 2.9280, -75.2830),
('Roberto Express', 'roberto.express@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Norte, Neiva', 'repartidor', 'activo', 2.9295, -75.2855),
('Fernando Veloz', 'fernando.veloz@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Este, Neiva', 'repartidor', 'activo', 2.9260, -75.2810),
('Javier Rápido', 'javier.rapido@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Oeste, Neiva', 'repartidor', 'activo', 2.9315, -75.2885),
('Sergio Flash', 'sergio.flash@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio La Gaitana, Neiva', 'repartidor', 'activo', 2.9270, -75.2825),
('Ricardo Turbo', 'ricardo.turbo@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Cándido, Neiva', 'repartidor', 'activo', 2.9305, -75.2870),
('Alberto Speed', 'alberto.speed@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Altico, Neiva', 'repartidor', 'activo', 2.9250, -75.2805),
('Gustavo Moto', 'gustavo.moto@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Granjas, Neiva', 'repartidor', 'activo', 2.9325, -75.2895),
('Héctor Jet', 'hector.jet@domiflash.com', 'scrypt:32768:8:1$yAcFkjMMoyMvrxOK$1df069696e06f31747996159c31d85507246c637e2debfb292a3f7782cdd4286227c514e1b323d17fe164eaa47bad33599377b36f294b4c7591c34962ff4df29', 'Barrio Limonar, Neiva', 'repartidor', 'activo', 2.9245, -75.2800);

-- =====================================================
-- PASO 4: INSERTAR RESTAURANTES
-- =====================================================
INSERT INTO restaurantes (idusu, nomres, desres, dirres, telres, estres, lat_restaurante, lng_restaurante) VALUES
(12, 'Restaurante El Sabor', 'Comida típica colombiana y platos a la carta', 'Carrera 5 #10-20, Neiva', '3001234567', 'activo', 2.9273, -75.2819),
(13, 'Pizza Express', 'Las mejores pizzas artesanales de Neiva', 'Calle 8 #12-30, Neiva', '3009876543', 'activo', 2.9285, -75.2835),
(14, 'Burger King Premium', 'Hamburguesas gourmet y comida rápida', 'Avenida Pastrana #15-40, Neiva', '3112345678', 'activo', 2.9300, -75.2860),
(15, 'China Wok', 'Auténtica comida china y sushi', 'Carrera 7 #20-15, Neiva', '3201234567', 'activo', 2.9260, -75.2825),
(16, 'Taco Loco', 'Tacos, burritos y comida mexicana', 'Calle 11 #8-25, Neiva', '3159876543', 'activo', 2.9290, -75.2850),
(17, 'Postres del Valle', 'Postres artesanales y tortas personalizadas', 'Carrera 9 #16-30, Neiva', '3002345678', 'activo', 2.9270, -75.2840),
(18, 'Café & Bebidas', 'Café premium, jugos naturales y smoothies', 'Calle 13 #10-18, Neiva', '3119876543', 'activo', 2.9310, -75.2875),
(19, 'Green Salads', 'Ensaladas frescas y comida saludable', 'Avenida Circunvalar #22-10, Neiva', '3203456789', 'activo', 2.9320, -75.2890),
(20, 'Pasta Italiana', 'Pastas artesanales y comida italiana', 'Carrera 4 #14-22, Neiva', '3154567890', 'activo', 2.9255, -75.2815),
(21, 'Mar y Tierra', 'Mariscos frescos y carnes a la parrilla', 'Calle 19 #18-35, Neiva', '3006789012', 'activo', 2.9330, -75.2905);

-- =====================================================
-- PASO 5: INSERTAR REPARTIDORES
-- =====================================================
INSERT INTO repartidores (idusu, nomrep, vehrep, estrep) VALUES
(22, 'Pedro Repartidor', 'Moto Yamaha XTZ 125', 'activo'),
(23, 'Miguel Delivery', 'Moto Honda CB 150', 'activo'),
(24, 'Roberto Express', 'Moto Suzuki GN 125', 'activo'),
(25, 'Fernando Veloz', 'Moto Bajaj Pulsar 180', 'activo'),
(26, 'Javier Rápido', 'Moto TVS Apache 160', 'activo'),
(27, 'Sergio Flash', 'Moto Honda CBR 250', 'activo'),
(28, 'Ricardo Turbo', 'Moto Yamaha FZ 150', 'activo'),
(29, 'Alberto Speed', 'Moto Suzuki Gixxer 155', 'activo'),
(30, 'Gustavo Moto', 'Moto Kawasaki Ninja 300', 'activo'),
(31, 'Héctor Jet', 'Moto Hero Glamour 125', 'activo');

-- =====================================================
-- PASO 6: INSERTAR PRODUCTOS POR RESTAURANTE
-- =====================================================

-- Restaurante El Sabor (Comida Rápida)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(1, 1, 'Bandeja Paisa', 'Tradicional bandeja paisa completa', 18000.00, 15),
(1, 1, 'Sancocho de Gallina', 'Sancocho tradicional huilense', 15000.00, 10),
(1, 1, 'Ajiaco Santafereño', 'Sopa tradicional con pollo', 14000.00, 12),
(1, 8, 'Ensalada Mixta', 'Ensalada fresca con aderezo', 8000.00, 20),
(1, 7, 'Jugo Natural', 'Jugos de frutas naturales', 4000.00, 30);

-- Pizza Express (Pizza)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(2, 2, 'Pizza Margarita', 'Tomate, mozzarella y albahaca', 25000.00, 20),
(2, 2, 'Pizza Pepperoni', 'Pepperoni y queso mozzarella', 28000.00, 18),
(2, 2, 'Pizza Hawaiana', 'Jamón, piña y queso', 27000.00, 15),
(2, 2, 'Pizza Cuatro Quesos', 'Mozzarella, parmesano, gorgonzola y provolone', 30000.00, 12),
(2, 7, 'Gaseosa 1.5L', 'Gaseosa sabores variados', 5000.00, 25);

-- Burger King Premium (Hamburguesas)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(3, 3, 'Hamburguesa Clásica', 'Carne, queso, lechuga y tomate', 15000.00, 25),
(3, 3, 'Hamburguesa Doble', 'Doble carne y queso', 22000.00, 20),
(3, 3, 'Hamburguesa BBQ', 'Carne, queso, tocino y salsa BBQ', 20000.00, 18),
(3, 1, 'Papas Fritas Grandes', 'Porción grande de papas crujientes', 8000.00, 30),
(3, 7, 'Malteada', 'Malteada de chocolate, vainilla o fresa', 7000.00, 22);

-- China Wok (Comida China)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(4, 4, 'Arroz Chino Especial', 'Arroz frito con pollo, cerdo y camarones', 18000.00, 20),
(4, 4, 'Chop Suey de Pollo', 'Verduras salteadas con pollo', 16000.00, 15),
(4, 4, 'Wantan Frito', 'Wantanes crujientes rellenos', 12000.00, 18),
(4, 4, 'Arroz con Pollo', 'Arroz con trozos de pollo', 15000.00, 22),
(4, 7, 'Té Verde', 'Té verde tradicional chino', 3000.00, 25);

-- Taco Loco (Comida Mexicana)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(5, 5, 'Tacos al Pastor x3', 'Tres tacos con carne al pastor', 12000.00, 20),
(5, 5, 'Burrito de Carne', 'Burrito grande con carne y frijoles', 15000.00, 18),
(5, 5, 'Quesadilla', 'Tortilla con queso y carne', 13000.00, 16),
(5, 5, 'Nachos con Queso', 'Nachos con queso fundido', 10000.00, 22),
(5, 7, 'Limonada', 'Limonada natural', 4000.00, 25);

-- Postres del Valle (Postres)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(6, 6, 'Torta de Chocolate', 'Porción de torta de chocolate', 8000.00, 15),
(6, 6, 'Cheesecake', 'Porción de cheesecake de frutos rojos', 10000.00, 12),
(6, 6, 'Tiramisú', 'Postre italiano tradicional', 11000.00, 10),
(6, 6, 'Brownie con Helado', 'Brownie caliente con helado', 9000.00, 18),
(6, 7, 'Café Espresso', 'Café espresso doble', 5000.00, 25);

-- Café & Bebidas (Bebidas)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(7, 7, 'Cappuccino', 'Café cappuccino cremoso', 6000.00, 30),
(7, 7, 'Smoothie de Frutas', 'Smoothie de frutas tropicales', 8000.00, 20),
(7, 7, 'Jugo Verde', 'Jugo detox verde', 9000.00, 15),
(7, 7, 'Té Chai Latte', 'Té chai con leche', 7000.00, 18),
(7, 6, 'Muffin', 'Muffin de arándanos o chocolate', 5000.00, 22);

-- Green Salads (Ensaladas)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(8, 8, 'Ensalada César', 'Lechuga, pollo, crutones y aderezo césar', 14000.00, 18),
(8, 8, 'Ensalada Griega', 'Tomate, pepino, aceitunas y queso feta', 13000.00, 16),
(8, 8, 'Ensalada de Quinoa', 'Quinoa con vegetales frescos', 15000.00, 14),
(8, 8, 'Bowl de Salmón', 'Salmón con vegetales y aguacate', 22000.00, 10),
(8, 7, 'Agua Saborizada', 'Agua con frutas naturales', 4000.00, 25);

-- Pasta Italiana (Pasta)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(9, 9, 'Spaghetti Carbonara', 'Pasta con salsa carbonara', 16000.00, 18),
(9, 9, 'Lasagna Bolognesa', 'Lasagna con carne y queso', 18000.00, 15),
(9, 9, 'Ravioli de Ricotta', 'Ravioles rellenos de ricotta', 17000.00, 12),
(9, 9, 'Fettuccine Alfredo', 'Pasta con salsa blanca cremosa', 15000.00, 20),
(9, 7, 'Vino Tinto Copa', 'Copa de vino tinto', 8000.00, 15);

-- Mar y Tierra (Mariscos)
INSERT INTO productos (idres, idcat, nompro, despro, prepro, stopro) VALUES
(10, 10, 'Ceviche de Camarón', 'Ceviche fresco de camarón', 20000.00, 12),
(10, 10, 'Mojarra Frita', 'Mojarra frita completa', 25000.00, 10),
(10, 10, 'Arroz con Camarones', 'Arroz marinero con camarones', 22000.00, 15),
(10, 10, 'Filete de Pescado', 'Filete a la plancha', 24000.00, 14),
(10, 7, 'Cerveza Artesanal', 'Cerveza artesanal 330ml', 7000.00, 20);

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================

-- Verificar datos insertados
SELECT 
    (SELECT COUNT(*) FROM usuarios WHERE rolusu = 'administrador') as administradores,
    (SELECT COUNT(*) FROM usuarios WHERE rolusu = 'cliente') as clientes,
    (SELECT COUNT(*) FROM usuarios WHERE rolusu = 'restaurante') as restaurantes_usuarios,
    (SELECT COUNT(*) FROM usuarios WHERE rolusu = 'repartidor') as repartidores_usuarios,
    (SELECT COUNT(*) FROM restaurantes) as restaurantes,
    (SELECT COUNT(*) FROM repartidores) as repartidores,
    (SELECT COUNT(*) FROM productos) as productos,
    (SELECT COUNT(*) FROM categorias) as categorias;