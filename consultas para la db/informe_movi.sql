use corupel;
select 
	articulos.art_id, art_descripcion, movimientos_ingreso.art_id, movi_restante, movi_cantidad, movi_costo, ing_fecha  
    from articulos, movimientos_ingreso
	join ingresos on ingresos.ing_id = movimientos_ingreso.ing_id
	where articulos.art_id = movimientos_ingreso.art_id
    AND movimientos_ingreso.art_id = 1214;