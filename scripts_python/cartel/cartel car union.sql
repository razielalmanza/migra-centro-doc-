-- Script to make UNION car and cartel tables.
-- Add the type of table to the corresponding tables
ALTER TABLE cd_test.car ADD COLUMN car_consulta TINYINT(1) DEFAULT 1;
ALTER TABLE cd_test.cartel ADD COLUMN car_consulta TINYINT(1) DEFAULT 0;
-- Add the type of origin of the export to the new table.
ALTER TABLE mydb.cd_item_cartel ADD COLUMN car_consulta TINYINT(1);

-- make the UNION adding some rows to make the UNION possible.
-- THIS IS USED AS THE SCRIPT TO EXPORT TO JSON THE CAR AND CARTEL TABLES.
		-- THIS DO NOT WORK BEACUSE THE TOTAL REGISTERS OF car and cartel are 9000 and 10000+
		-- WHEN SELECTING SEPARATELY IT SHOWS THE CORRECT VALUES FOR car_consulta
		-- WHEN USING THE UNION WE GET THAT ONLY 518 REGISTERS ARE equal to var_consulta = 0, which is incorrect. 
				SELECT count(idReg) FROM (
					SELECT 
						*,
						NULL AS IMAGEN_DIGITAL,
						NULL AS COLECCION,
						NULL AS DISENIADOR
					FROM `cd_test`.`car`
					UNION ALL
					SELECT 
						*,
						NULL AS INVENTARIO_UNAM,
						NULL AS DA
					FROM `cd_test`.`cartel`) AS T
				WHERE car_consulta = 0;

-- END UP USING TWO DIFFERENT EXPORTS WITH EQUAL ROWS:
SELECT 
		*,
		NULL AS IMAGEN_DIGITAL,
		NULL AS COLECCION,
		NULL AS DISENIADOR
	FROM `cd_test`.`car`;
SELECT 
		*,
		TITULO_EN_ESPANOL as TITULO_EN_ESPA,
		NULL AS INVENTARIO_UNAM,
		NULL AS DA
	FROM `cd_test`.`cartel`;
-- We add to cd_item_cartel the rows 'danios' and 'inventario_unam'
USE mydb;
ALTER TABLE cd_item_cartel ADD COLUMN danios VARCHAR(100);
ALTER TABLE cd_item_cartel ADD COLUMN inventario_unam VARCHAR(1);

-- ALTER TABLE cd_test.car DROP COLUMN car_consulta;
-- ALTER TABLE cd_test.cartel DROP COLUMN car_consulta;