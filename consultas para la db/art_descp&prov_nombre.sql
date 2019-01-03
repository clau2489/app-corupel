SELECT `art_descripcion`, `prov_nombre`
FROM `proveedores`, `articulos`
	JOIN `articulos_de_proveedores` ON `articulos`.`art_id` = `articulos_de_proveedores`.`articulo`
WHERE
	`articulos_de_proveedores`.`articulo` = 2
    