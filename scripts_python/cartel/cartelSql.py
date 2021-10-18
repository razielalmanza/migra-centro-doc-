catValues =   """ INSERT IGNORE INTO cat_values 
                        (tname, fname, val, display_value) 
                        VALUES (%s, %s, %s, %s) """

catTitulos =  """ INSERT INTO cd_cat_titulos 
               (titulo_original, titulo_en_espa, anio, pais_de_realizacion) 
               VALUES (%s, %s, %s, %s) """

cdPersonas =  """ INSERT INTO cd_personas 
               (nombre, tipo_persona) 
               VALUES (%s, %s) """

transPersonas = """ INSERT IGNORE INTO cd_trans_personas_cat_titulos
               (idcd_cat_titulos, idcd_personas, rol) 
               VALUES (%s, %s, %s) """

cdItems =      """ INSERT INTO cd_item 
                (idcd_cat_titulos, fechaHoraInsercion, tipo_item, imagen_digital, foto_old_interpretes, colocacion, notas, activo)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s) """

cdCartel =     """ INSERT INTO cd_item_cartel 
                (idcd_item, institucion, pais, tama, ejemplares, tecnica, estado_fisico, diseniador, car_consulta )
                VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s) """

cdInterpretes = """ INSERT IGNORE INTO cd_interpretes
                (nombre)
                VALUES ('{nombre}') """

transInterpre = """ INSERT IGNORE INTO cd_trans_item_interpretes
                  (idcd_item, nombre)
                  VALUES (%s, %s) """ 