catTitulos  = """ INSERT INTO cd_cat_titulos 
                  (titulo_original, titulo_en_espa, anio, anio_fin) 
                  VALUES (%s, %s, %s, %s) """
cdItem      = """ INSERT INTO cd_item 
                  (idcd_cat_titulos, fechaHoraInsercion, tipo_item, imagen_digital, foto_old_interpretes, colocacion, notas, activo)
                  VALUES (%s,%s, %s, %s, %s, %s, %s, %s) """
itemStills  = """ INSERT INTO cd_item_stills (idcd_item, a_r_, a_f_total_ejemplares )
                  VALUES (%s,%s, %s) """

cdPersonas =  """ INSERT INTO cd_personas 
               (nombre, tipo_persona) 
               VALUES (%s, %s) """

transPersonas = """ INSERT IGNORE INTO cd_trans_personas_cat_titulos
               (idcd_cat_titulos, idcd_personas, rol) 
               VALUES (%s, %s, %s) """