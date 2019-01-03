SELECT `art_id`, `art_descripcion`, `art_cod_barras`
FROM `articulos`
	JOIN `articulos_de_proveedores` ON `articulos`.`art_id` = `articulos_de_proveedores`.`articulo`
WHERE
	`articulos_de_proveedores`.`proveedor` = 1
    