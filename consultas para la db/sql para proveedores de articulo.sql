SELECT `prov_id`, `prov_nombre`, `prov_telefono`
FROM `proveedores`
	JOIN `articulos_de_proveedores` ON `proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`
WHERE
	`articulos_de_proveedores`.`articulo` = 5
    