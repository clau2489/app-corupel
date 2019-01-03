CREATE TABLE `articulos` (
  `art_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_cod_barras` varchar(20) NULL UNIQUE KEY,
  `art_descripcion` varchar(100) NOT NULL,
  `art_marca` varchar(20) NOT NULL,
  `art_destino` int(16) UNSIGNED,
  `art_agrupacion` varchar(20) ,
  `art_stock_minimo` int(8) NOT NULL,
  `art_stock_actual` int(8) UNSIGNED NOT NULL  DEFAULT 0,
  `art_activo` tinyint (1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `operarios` (
  `ope_legajo` int(16) NOT NULL PRIMARY KEY,
  `ope_nombre` varchar(20) NOT NULL,
  `ope_apellido` varchar(20) NOT NULL,
  `ope_puesto` varchar(20) NOT NULL,
  `ope_dni` int(13)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `proveedores` (
  `prov_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_nombre` varchar(60) NOT NULL,
  `prov_razon_social` varchar(60) NOT NULL,
  `prov_cuit` varchar(20),
  `prov_direccion` varchar(60),
  `prov_nombre_contacto` varchar(30),
  `prov_telefono` varchar(30),
  `prov_telefono_dos` varchar(30),
  `prov_email` varchar(40),
  `prov_notas` tinytext,
  `prov_activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `articulos_de_proveedores` (
  `articulo` int(16) UNSIGNED NOT NULL,
  `proveedor` int(16) UNSIGNED NOT NULL,
  PRIMARY KEY (`articulo`, `proveedor`),
  CONSTRAINT `constr_articulos_de_proveedores_articulo_fk`
        FOREIGN KEY `articulo_fk` (`articulo`) REFERENCES `articulos` (`art_id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `constr_articulos_de_proveedores_proveedor_fk`
        FOREIGN KEY `proveedor_fk` (`proveedor`) REFERENCES `proveedores` (`prov_id`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `agrupaciones` (
  `ag_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ag_nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `destinos` (
  `des_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `des_maquina` varchar(20) NOT NULL,
  `des_descripcion` varchar(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `movimientos_ingreso` (
  `movi_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_id` int(16) UNSIGNED NOT NULL ,
  `ing_id` int(16) UNSIGNED NOT NULL ,
  `movi_cantidad` int(20) UNSIGNED NOT NULL,
  `movi_restante` int(20) UNSIGNED NOT NULL,
  `movi_costo` decimal(20, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `movimientos_egreso` (
  `move_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_id` int(16) UNSIGNED NOT NULL,
  `move_destino` int(16) UNSIGNED,
  `move_sector` varchar(20),
  `egr_id` int(16) UNSIGNED NOT NULL,
  `move_cantidad` int(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ingresos` (
  `ing_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_id` int(16) UNSIGNED NOT NULL,
  `ing_fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `egresos` (
  `egr_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ope_legajo` int(16) NOT NULL,
  `egr_fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `comprobantes` (
  `comp_prefijo` varchar(10) NOT NULL,
  `comp_numero` int(20) NOT NULL,
  `comp_fecha` date NOT NULL,
  `ing_id` int(16) UNSIGNED NOT NULL,
  PRIMARY KEY (`comp_prefijo`, `comp_numero`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
