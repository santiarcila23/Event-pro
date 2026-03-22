-- init.sql — EventPro
-- Se ejecuta automáticamente al iniciar el contenedor MySQL

CREATE DATABASE IF NOT EXISTS eventpro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE eventpro;

-- ── TABLAS ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS Recintos (
    codigo_recinto   VARCHAR(10)  PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    tipo             VARCHAR(30),
    ubicacion        VARCHAR(100),
    capacidad_teatro INT,
    tarifa           VARCHAR(50),
    disponibilidad   VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Clientes (
    codigo_cliente   VARCHAR(10)  PRIMARY KEY,
    tipo_cliente     VARCHAR(20),
    razon_social     VARCHAR(100) NOT NULL,
    documento_fiscal VARCHAR(20),
    telefono         VARCHAR(20),
    correo           VARCHAR(80),
    contacto         VARCHAR(80),
    clasificacion    VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Eventos (
    num_evento     VARCHAR(15)  PRIMARY KEY,
    titulo         VARCHAR(100) NOT NULL,
    tipo_evento    VARCHAR(30),
    cliente        VARCHAR(100),
    fecha_inicio   VARCHAR(20),
    fecha_fin      VARCHAR(20),
    num_asistentes INT,
    estado         VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Personal (
    codigo_empleado VARCHAR(10)  PRIMARY KEY,
    nombres         VARCHAR(60)  NOT NULL,
    apellidos       VARCHAR(60)  NOT NULL,
    especialidad    VARCHAR(40),
    tarifa          VARCHAR(50),
    evento_asignado VARCHAR(100),
    horario         VARCHAR(40),
    disponibilidad  VARCHAR(30)
);

-- ── DATOS DE EJEMPLO ────────────────────────────────────────────
INSERT IGNORE INTO Recintos VALUES
('RC-001','Salón Imperial',      'Salón',             'Ala Norte, Piso 1',500,'$350.000/hora','Disponible'),
('RC-002','Auditorio Magna',     'Auditorio',         'Edificio Central', 800,'$600.000/hora','Reservado'),
('RC-003','Sala Ejecutiva A',    'Sala de reuniones', 'Torre B, Piso 3',   50,'$120.000/hora','Disponible'),
('RC-004','Salón Jardín',        'Salón',             'Área Exterior',    300,'$280.000/hora','Disponible'),
('RC-005','Sala Conferencias VIP','Sala de reuniones','Torre A, Piso 5',   30,'$150.000/hora','En mantenimiento');

INSERT IGNORE INTO Clientes VALUES
('CL-001','Corporativo','Tech Summit S.A.',       '900.123.456-1','+57 300 111 2233','info@techsummit.com',  'Carlos Ruiz',    'Cliente VIP'),
('CL-002','Agencia',    'Eventos Estrella Ltda.', '800.654.321-0','+57 301 222 3344','ventas@estrella.com',  'Laura Gómez',    'Cliente frecuente'),
('CL-003','Particular', 'María Fernández',        '1.023.456.789','+57 312 333 4455','mfernandez@gmail.com', 'María Fernández','Cliente nuevo'),
('CL-004','Corporativo','Grupo Bancario Andino',  '901.234.567-2','+57 320 444 5566','eventos@gba.com.co',   'Pedro Salcedo',  'Cliente VIP'),
('CL-005','Agencia',    'Show & Business Agency', '802.345.678-3','+57 315 555 6677','contact@showbiz.co',   'Sandra Morales', 'Cliente frecuente');

INSERT IGNORE INTO Eventos VALUES
('EV-2026-001','Cumbre Tecnológica 2026',  'Congreso',   'Tech Summit S.A.',      '2026-04-10','2026-04-12',450,'Confirmado'),
('EV-2026-002','Boda Martínez-López',      'Boda',       'María Fernández',       '2026-05-03','2026-05-03',200,'Confirmado'),
('EV-2026-003','Feria de Innovación',      'Feria',      'Grupo Bancario Andino', '2026-06-15','2026-06-17',700,'Cotización'),
('EV-2026-004','Concierto Noche de Gala',  'Concierto',  'Show & Business Agency','2026-07-20','2026-07-20',750,'En curso'),
('EV-2026-005','Conferencia Liderazgo 2026','Conferencia','Eventos Estrella Ltda.','2026-08-05','2026-08-05',120,'Cotización');

INSERT IGNORE INTO Personal VALUES
('EP-001','Andrés',  'Castillo Vera',  'Coordinador',        '$55.000/hora','EV-2026-001','08:00-18:00','Asignado'),
('EP-002','Patricia','Ríos Mendoza',   'Técnico audiovisual','$45.000/hora','EV-2026-003','09:00-20:00','Asignado'),
('EP-003','Jorge',   'Lozano Peña',    'Camarero',           '$30.000/hora','EV-2026-002','15:00-23:30','Asignado'),
('EP-004','Camila',  'Torres Arango',  'Seguridad',          '$35.000/hora','EV-2026-004','18:00-00:00','Asignado'),
('EP-005','Luis',    'Herrera Soto',   'Chef',               '$70.000/hora','EV-2026-002','12:00-23:00','Disponible');

-- ── STORED PROCEDURES ───────────────────────────────────────────
DROP PROCEDURE IF EXISTS sp_insertar_recinto;
DROP PROCEDURE IF EXISTS sp_actualizar_recinto;
DROP PROCEDURE IF EXISTS sp_eliminar_recinto;
DROP PROCEDURE IF EXISTS sp_buscar_recinto;
DROP PROCEDURE IF EXISTS sp_listar_recintos;
DROP PROCEDURE IF EXISTS sp_insertar_cliente;
DROP PROCEDURE IF EXISTS sp_actualizar_cliente;
DROP PROCEDURE IF EXISTS sp_eliminar_cliente;
DROP PROCEDURE IF EXISTS sp_buscar_cliente;
DROP PROCEDURE IF EXISTS sp_listar_clientes;
DROP PROCEDURE IF EXISTS sp_insertar_evento;
DROP PROCEDURE IF EXISTS sp_actualizar_evento;
DROP PROCEDURE IF EXISTS sp_eliminar_evento;
DROP PROCEDURE IF EXISTS sp_buscar_evento;
DROP PROCEDURE IF EXISTS sp_listar_eventos;
DROP PROCEDURE IF EXISTS sp_insertar_personal;
DROP PROCEDURE IF EXISTS sp_actualizar_personal;
DROP PROCEDURE IF EXISTS sp_eliminar_personal;
DROP PROCEDURE IF EXISTS sp_buscar_personal;
DROP PROCEDURE IF EXISTS sp_listar_personal;

DELIMITER $$

CREATE PROCEDURE sp_insertar_recinto(IN p_codigo VARCHAR(10),IN p_nombre VARCHAR(100),IN p_tipo VARCHAR(30),IN p_ubicacion VARCHAR(100),IN p_capacidad INT,IN p_tarifa VARCHAR(50),IN p_disponibilidad VARCHAR(30))
BEGIN INSERT INTO Recintos VALUES(p_codigo,p_nombre,p_tipo,p_ubicacion,p_capacidad,p_tarifa,p_disponibilidad); END$$

CREATE PROCEDURE sp_actualizar_recinto(IN p_codigo VARCHAR(10),IN p_nombre VARCHAR(100),IN p_tipo VARCHAR(30),IN p_ubicacion VARCHAR(100),IN p_capacidad INT,IN p_tarifa VARCHAR(50),IN p_disponibilidad VARCHAR(30))
BEGIN UPDATE Recintos SET nombre=p_nombre,tipo=p_tipo,ubicacion=p_ubicacion,capacidad_teatro=p_capacidad,tarifa=p_tarifa,disponibilidad=p_disponibilidad WHERE codigo_recinto=p_codigo; END$$

CREATE PROCEDURE sp_eliminar_recinto(IN p_codigo VARCHAR(10))
BEGIN DELETE FROM Recintos WHERE codigo_recinto=p_codigo; END$$

CREATE PROCEDURE sp_buscar_recinto(IN p_termino VARCHAR(100))
BEGIN SELECT * FROM Recintos WHERE codigo_recinto LIKE CONCAT('%',p_termino,'%') OR nombre LIKE CONCAT('%',p_termino,'%'); END$$

CREATE PROCEDURE sp_listar_recintos()
BEGIN SELECT * FROM Recintos; END$$

CREATE PROCEDURE sp_insertar_cliente(IN p_codigo VARCHAR(10),IN p_tipo VARCHAR(20),IN p_razon VARCHAR(100),IN p_doc VARCHAR(20),IN p_tel VARCHAR(20),IN p_correo VARCHAR(80),IN p_contacto VARCHAR(80),IN p_clasificacion VARCHAR(30))
BEGIN INSERT INTO Clientes VALUES(p_codigo,p_tipo,p_razon,p_doc,p_tel,p_correo,p_contacto,p_clasificacion); END$$

CREATE PROCEDURE sp_actualizar_cliente(IN p_codigo VARCHAR(10),IN p_tipo VARCHAR(20),IN p_razon VARCHAR(100),IN p_doc VARCHAR(20),IN p_tel VARCHAR(20),IN p_correo VARCHAR(80),IN p_contacto VARCHAR(80),IN p_clasificacion VARCHAR(30))
BEGIN UPDATE Clientes SET tipo_cliente=p_tipo,razon_social=p_razon,documento_fiscal=p_doc,telefono=p_tel,correo=p_correo,contacto=p_contacto,clasificacion=p_clasificacion WHERE codigo_cliente=p_codigo; END$$

CREATE PROCEDURE sp_eliminar_cliente(IN p_codigo VARCHAR(10))
BEGIN DELETE FROM Clientes WHERE codigo_cliente=p_codigo; END$$

CREATE PROCEDURE sp_buscar_cliente(IN p_termino VARCHAR(100))
BEGIN SELECT * FROM Clientes WHERE codigo_cliente LIKE CONCAT('%',p_termino,'%') OR razon_social LIKE CONCAT('%',p_termino,'%'); END$$

CREATE PROCEDURE sp_listar_clientes()
BEGIN SELECT * FROM Clientes; END$$

CREATE PROCEDURE sp_insertar_evento(IN p_num VARCHAR(15),IN p_titulo VARCHAR(100),IN p_tipo VARCHAR(30),IN p_cliente VARCHAR(100),IN p_fi VARCHAR(20),IN p_ff VARCHAR(20),IN p_asistentes INT,IN p_estado VARCHAR(20))
BEGIN INSERT INTO Eventos VALUES(p_num,p_titulo,p_tipo,p_cliente,p_fi,p_ff,p_asistentes,p_estado); END$$

CREATE PROCEDURE sp_actualizar_evento(IN p_num VARCHAR(15),IN p_titulo VARCHAR(100),IN p_tipo VARCHAR(30),IN p_cliente VARCHAR(100),IN p_fi VARCHAR(20),IN p_ff VARCHAR(20),IN p_asistentes INT,IN p_estado VARCHAR(20))
BEGIN UPDATE Eventos SET titulo=p_titulo,tipo_evento=p_tipo,cliente=p_cliente,fecha_inicio=p_fi,fecha_fin=p_ff,num_asistentes=p_asistentes,estado=p_estado WHERE num_evento=p_num; END$$

CREATE PROCEDURE sp_eliminar_evento(IN p_num VARCHAR(15))
BEGIN DELETE FROM Eventos WHERE num_evento=p_num; END$$

CREATE PROCEDURE sp_buscar_evento(IN p_termino VARCHAR(100))
BEGIN SELECT * FROM Eventos WHERE num_evento LIKE CONCAT('%',p_termino,'%') OR titulo LIKE CONCAT('%',p_termino,'%'); END$$

CREATE PROCEDURE sp_listar_eventos()
BEGIN SELECT * FROM Eventos; END$$

CREATE PROCEDURE sp_insertar_personal(IN p_codigo VARCHAR(10),IN p_nombres VARCHAR(60),IN p_apellidos VARCHAR(60),IN p_especialidad VARCHAR(40),IN p_tarifa VARCHAR(50),IN p_evento VARCHAR(100),IN p_horario VARCHAR(40),IN p_disponibilidad VARCHAR(30))
BEGIN INSERT INTO Personal VALUES(p_codigo,p_nombres,p_apellidos,p_especialidad,p_tarifa,p_evento,p_horario,p_disponibilidad); END$$

CREATE PROCEDURE sp_actualizar_personal(IN p_codigo VARCHAR(10),IN p_nombres VARCHAR(60),IN p_apellidos VARCHAR(60),IN p_especialidad VARCHAR(40),IN p_tarifa VARCHAR(50),IN p_evento VARCHAR(100),IN p_horario VARCHAR(40),IN p_disponibilidad VARCHAR(30))
BEGIN UPDATE Personal SET nombres=p_nombres,apellidos=p_apellidos,especialidad=p_especialidad,tarifa=p_tarifa,evento_asignado=p_evento,horario=p_horario,disponibilidad=p_disponibilidad WHERE codigo_empleado=p_codigo; END$$

CREATE PROCEDURE sp_eliminar_personal(IN p_codigo VARCHAR(10))
BEGIN DELETE FROM Personal WHERE codigo_empleado=p_codigo; END$$

CREATE PROCEDURE sp_buscar_personal(IN p_termino VARCHAR(100))
BEGIN SELECT * FROM Personal WHERE codigo_empleado LIKE CONCAT('%',p_termino,'%') OR nombres LIKE CONCAT('%',p_termino,'%') OR apellidos LIKE CONCAT('%',p_termino,'%'); END$$

CREATE PROCEDURE sp_listar_personal()
BEGIN SELECT * FROM Personal; END$$

DELIMITER ;
