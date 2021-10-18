import pymysql
import csv
import sys
from ManejadorPaises import ManejadorPaises
from ConvertidorColor import ConvertidorColor
from ConvertidorFormatoPelicula import ConvertidorFormatoPelicula
from ConvertidorRegionPelicula import ConvertidorRegionPelicula
from ConvertidorNorma import ConvertidorNorma
from ConvertidorAudio import ConvertidorAudio

#Crear el ambiente virtual: $python.exe -m venv env_migracion_BD_centro_Doc

class conectorBD:

    def __init__(self, _host, _port, _user, _passwd, _db):
        """Recibimos los parametros necesarios para realizar la conexion
        a la base de datos deseada"""
        self.db = pymysql.connect(host=_host, port=_port, user=_user,
        passwd=_passwd, db=_db)

'''
Tabla unica:
[0]= idReg  [1]=fechaHoraInsercion [2]=TITULO_ORIGINAL  [3]=TITULO_EN_ESPA   [4]=REALIZADOR [5]=PAIS_DE_REALIZACION
[6]=A (anio)    [7]=FORMATO  [8]=COLOR   [9]=AUDIO [10]=NORMA [11]=DURACION [12]=REGION [13]=PANTALLA
[14]=COLOCACION [15]=OBSERVACIONES [16]=EXTRAS [17]=ACTIVO 
'''

if __name__ == '__main__':
    if (len(sys.argv) < 2 ):
        print("No has introducido la contraseña de la BD.\n\t ****** Usage: python PeliculasConexionDB.py [DB_password] ****")
        sys.exit()
    #'Realizamos la captura de datos para la conexion a la base de datos'
    host="localhost"
    #port=3307
    port=3306
    user="root"
    #passwd="root"
    passwd = sys.argv[1]
    #db="centro-doc-pruebas"
    db="cd_test"
    BD = conectorBD(host, port, user, passwd, db)
    cursor = BD.db.cursor()


    try:
        
        header=["idReg","formato(cd_vhs_dvd)","color(cd_vhs_dvd)","audio(cd_vhs_dvd)",
                "idioma(cd_vhs_dvd)","subtitulos(cd_vhs_dvd)","intertitulos(cd_vhs_dvd)","norma(cd_vhs_dvd)",
                "duracion(cd_vhs_dvd)","region(cd_vhs_dvd)","pantalla(cd_vhs_dvd)","observaciones(cd_vhs_dvd)",
                "pais_de_realizacion(cd_cat_titulos)","extras(cd_vhs_dvd)",
                "fechaHoraInsercion(cd_item)","tipo_item(cd_item)",
                "imagen_digital(cd_item)","foto_old_interpretes(cd_item)","activo(cd_item)","colocacion(cd_item)","notas(cd_item)","titulo_original(cd_cat_titulos)",
                "titulo_en_espa(cd_cat_titulos)","anio(cd_cat_titulos)","nombre(cd_personas)"]

        query="SELECT * FROM unica"# WHERE idReg >= '%d' AND idReg <= '%d' " % (1,500)
        cursor.execute(query)

        resultados=cursor.fetchall()
        
        with open('cd_vhs_dvd.csv', mode='w',newline='',encoding="utf-8") as peliculas_file:
            peliculas_file.write('\ufeff')
            peliculas_writer = csv.writer(peliculas_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            peliculas_writer.writerow(header)
            converterColor= ConvertidorColor(",")
            converterFormato = ConvertidorFormatoPelicula()
            converterRegion = ConvertidorRegionPelicula()
            converterNorma = ConvertidorNorma()
            converterAudio = ConvertidorAudio()
            
            for item in resultados:
                '''
                En este paso, donde se exporta toda la tabla unica procesada a csv, se extrad
                los audios del campo audio, la conversión a su correcto ISO ocurre en otro lugar.
                Dependerá de si es un cambio directo en la base, o solo dentro del front end.
                '''
                converterAudio.procesaAudio(item[9]) #("SS ESP SUBT ENG")
                
                converterPaises=ManejadorPaises(item[5],",")
                idReg=item[0]
                formato_cd_vhs_dvd= converterFormato.getFormato(item[7])[0:10] #item[7]
                color_cd_vhs_dvd= converterColor.getColor(item[8])[0:20] #item[8]
                audio_cd_vhs_dvd=" ".join(converterAudio.audio_cd) #item[9]
                idioma_cd_vhs_dvd= " ".join(converterAudio.dialogos)
                subtitulos_cd_vhs_dvd=" ".join(converterAudio.subtitulos)
                intertitulos_cd_vhs_dvd=" ".join(converterAudio.intertitulos)
                norma_cd_vhs_dvd=converterNorma.getNorma(item[10])#item[10]
                duracion_cd_vhs_dvd=item[11]        
                region_cd_vhs_dvd=converterRegion.getRegion(item[12])#item[12]
                pantalla_cd_vhs_dvd=item[13]
                observaciones_cd_vhs_dvd=item[15]
                pais_de_realizacion_cd_cat_titulos=converterPaises.getIsoAlpha3().upper() #item[5]
                extras_cd_vhs_dvd=item[16]
                fechaHoraInsercion_cd_item=item[1].strftime("%d-%m-%Y %H:%M:%S") #item[1]
                tipo_item_cd_item="video"
                imagen_digital_cd_item="NA"
                foto_old_interpretes_cd_item="NA"
                activo_cd_item=item[17]
                colocacion_cd_item=item[14][0:49]
                notas_cd_item=""
                titulo_original_cd_cat_titulos=item[2]
                titulo_en_espa_cd_cat_titulos=item[3]
                anio_cd_cat_titulos=item[6]
                nombre_cd_personas=item[4]

                row=[idReg, formato_cd_vhs_dvd,color_cd_vhs_dvd,audio_cd_vhs_dvd,idioma_cd_vhs_dvd,subtitulos_cd_vhs_dvd,
                intertitulos_cd_vhs_dvd,norma_cd_vhs_dvd,duracion_cd_vhs_dvd,region_cd_vhs_dvd,pantalla_cd_vhs_dvd,observaciones_cd_vhs_dvd,
                pais_de_realizacion_cd_cat_titulos,extras_cd_vhs_dvd,fechaHoraInsercion_cd_item,tipo_item_cd_item,imagen_digital_cd_item,
                foto_old_interpretes_cd_item,activo_cd_item,colocacion_cd_item,notas_cd_item,titulo_original_cd_cat_titulos,
                titulo_en_espa_cd_cat_titulos,anio_cd_cat_titulos,nombre_cd_personas]

                peliculas_writer.writerow(row)
                
        print(len(resultados))

    except Exception as error:
        print("Paso algo raro en la consulta:", error)