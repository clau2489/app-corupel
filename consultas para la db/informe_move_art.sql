use corupel;
select 
	articulos.art_id, art_descripcion, move_cantidad, egr_fecha  
    from articulos, movimientos_egreso
	join egresos on egresos.egr_id= movimientos_egreso.egr_id
	where articulos.art_id = movimientos_egreso.art_id
    AND egr_fecha BETWEEN '2017-10-11' AND '2017-10-20';
    AND movimientos_egreso.art_id = 1214;