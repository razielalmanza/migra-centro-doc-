catTitulos =    """ INSERT INTO cd_cat_titulos 
                    (titulo_original, titulo_en_espa, anio, anio_fin) 
                    VALUES (%s, %s, %s, %s) """
cdItem     =    """ INSERT INTO cd_item 
                    (idcd_cat_personalidades, fechaHoraInsercion, tipo_item, imagen_digital, colocacion, notas, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) """
cdPerson   =    """ INSERT INTO cd_cat_personalidades 
                    (nombre_artistico, nombre_verdadero, sobrenombre, a_r_acervo_repetido )
                    VALUES (%s, %s, %s, %s) """