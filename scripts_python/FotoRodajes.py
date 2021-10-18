import mysql.connector
import pymysql
import json, sys, csv
from datetime import datetime
import re

'''

SELECT
idReg, TAMA as 'tama(cd_item_fotos_rodaje)', COLOR as 'color(cd_item_fotos_rodaje)', fechaHoraInsercion as 'fechaHoraInsercion(cd_item)', 'fotografía de rodaje' as 'tipo_item(cd_item)', IMAGEN_DIGITAL as 'imagen_digital(cd_item)', INTERPRETES as 'foto_old_interpretes(cd_item)', ACTIVO as 'activo(cd_item)', COLOCACION as 'colocacion(cd_item)', NOTAS as 'notas(cd_item)', TITULO AS 'titulo_original(cd_cat_titulos)', '' AS 'titulo_en_espa(cd_cat_titulos)', ANIO as 'anio(cd_cat_titulos)', REALIZADOR as 'nombre(cd_personas)'
FROM cd_test.foto;

0: idReg
1: tama(cd_item_fotos_rodaje)   
2: color(cd_item_fotos_rodaje)  
3: fechaHoraInsercion(cd_item)  
4: tipo_item(cd_item)
5: imagen_digital(cd_item)      
6: foto_old_interpretes(cd_item)
7: activo(cd_item)
8: colocacion(cd_item)
9: notas(cd_item)
10: titulo_original(cd_cat_titulos)
11: titulo_en_espa(cd_cat_titulos)
12: anio(cd_cat_titulos)
13: nombre(cd_personas)
'''
def createConnectionDB(user, password, host, db):
    mydb = mysql.connector.connect(
        host=host,
        user="root",
        password=password,
        database=db
        )
    return mydb


def getIdLastInsertedFromTable(nameTable,nameId):
    sql =  "SELECT * FROM "+nameTable+" WHERE "+nameId+" = (SELECT LAST_INSERT_ID())" #"SELECT MAX( "+nameId+" ) FROM "+ nameTable
    dbCursor.execute(sql)
    result = dbCursor.fetchall()
    for row in result:
        return row[0]

def quita_ultima_coma(cadena):
    try:
        if cadena[-1] == ",":
            return cadena[:len(cadena) -1]
        else:
            return cadena
    except:
        return ""
'''
Recibe el id del cd_item y la cadena con los interpretes.
Separa a los interpretes por un número, por cada uno se crea la relación 
cd_trans_item_interpretes.
'''
def insert_interpretes(id_cd_item, interpretes):
  cdInterpretes = """ INSERT IGNORE INTO cd_interpretes
                (nombre)
                VALUES (%s) """
  transInterpre = """ INSERT IGNORE INTO cd_trans_item_interpretes
                  (idcd_item, nombre)
                  VALUES (%s, %s) """ 
  nombres_array = re.split("\d", interpretes)
  badInputs = ["", " ", "NO IDENTIFICADO(S)", "NO IDENTIFICADO", "no identificado", None]
  for nombre in nombres_array:
      if nombre in badInputs:
        continue
      nombre = nombre.strip()
      nombre = quita_ultima_coma(nombre)
      # Insertamos a cd_interpretes.
      insert(cdInterpretes, (nombre))
      # Insertamos a cd_trans_item_interpretes
      params = (id_cd_item, nombre)
      insert(transInterpre, params)

def insert(sql, val):
    try:
        dbCursor.execute(sql,val)
    except Exception as e:
        print("Falló en " + str(e))
        print( val)

'''
  Busca si existe ya un título en cd_cat_titulos con los datos de la entidad recibida.
  Si existe, regresa el idcd_cat_titulos encontrado. y evita hacer la inserción, si no lo encuentra, regresa
  None, provocando que cuando se use esa función haya que insertar (pues aún no existe esta entidad en la base.)
  NOTA: Usa solo titulo_original y año para encontrar una coincidencia.
'''
def existe_titulo(data_entidad):
  
  dbCursor.execute(
  """ SELECT idcd_cat_titulos 
  FROM cd_cat_titulos 
  WHERE 
  titulo_original = %s 
  AND anio = %s 
  """, 
  data_entidad)
  found_rows = dbCursor.fetchmany(size=1)
  dbCursor.fetchall() # Necesario para desechar el fetch anterior
  #print(found_rows)
  # found_rows es una lista con las tuplas a encontrar, pedimos la primera [0], 
  # que es la primera entidad encontrada, luego el atributo [0] que es el id 
  if len(found_rows) != 0:
    return found_rows[0][0]
  return None

def existe_persona(data_entidad):
  dbCursor.execute(
  """SELECT idcd_personas
  FROM cd_personas 
  WHERE 
  nombre = %s 
  AND tipo_persona = %s
  """, 
  data_entidad)
  found_rows = dbCursor.fetchmany(size=1)
  dbCursor.fetchall() # Necesario para desechar el fetch anterior
  #print(found_rows)
  # found_rows es una lista con las tuplas a encontrar, pedimos la primera [0], 
  # que es la primera entidad encontrada, luego el atributo [0] que es el id 
  if len(found_rows) != 0:
    return found_rows[0][0]
  return None

def insertIntoDB(data):
    TIPO_ITEM = "foro"
    '''
        Se insertan primero los cat_values
    '''
    sqlCatValue =  """ INSERT IGNORE INTO cat_values 
                        (tname, fname, val, display_value) 
                        VALUES (%s, %s, %s, %s) """
    insert(sqlCatValue, ["foto", "tama", data[1], data[1]] ) # cat_values tama
    insert(sqlCatValue, ["foto", "color", data[2], data[2]] ) # cat_values color

    queryInsertaCatTitulos = """ INSERT INTO cd_cat_titulos 
               (titulo_original, titulo_en_espa, anio) 
               VALUES (%s, %s, %s, %s, %s) """
    anio = data[12]
    if(data[12] == "" or data[12] == "SD" or data[12] is None or not data[12].isnumeric() ):
        anio=0
    valorNewCatTitulo = (data[10], data[11], anio)
    idLastCatTitulos = existe_titulo([data[10], anio])
    if not idLastCatTitulos:
        insert(queryInsertaCatTitulos, valorNewCatTitulo)
        idLastCatTitulos= getIdLastInsertedFromTable("cd_cat_titulos","idcd_cat_titulos")
    queryInsertarItem = "INSERT INTO cd_item (idcd_cat_titulos, fechaHoraInsercion,tipo_item, imagen_digital, foto_old_interpretes,activo,colocacion, notas) VALUES (%s,%s, %s, %s, %s, %s,%s,%s)"
    fecha= datetime.strptime(data[3],"%Y-%m-%d %H:%M:%S")
    valorNewItem =(idLastCatTitulos,fecha,TIPO_ITEM,data[5],data[6],data[7],data[8],data[9])
    dbCursor.execute(queryInsertarItem,valorNewItem)

    idLastItem = getIdLastInsertedFromTable("cd_item","idcd_item")
    queryInsertarFotoRodaje = "INSERT INTO cd_item_fotos_rodaje (idcd_item, tama, color) VALUES (%s,%s,%s) "
    valorNewFotoRodaje = (idLastItem,data[1],data[2])
    dbCursor.execute(queryInsertarFotoRodaje,valorNewFotoRodaje)

    queryInsertarCdPersonas =  "INSERT INTO cd_personas (nombre, tipo_persona) VALUES (%s,%s) "
    valorNewCdPersonas = (data[13], "F")
    idLastCdPersonas = existe_persona(valorNewCdPersonas)
    if not idLastCdPersonas:
        insert(queryInsertarCdPersonas,valorNewCdPersonas)
        idLastCdPersonas = getIdLastInsertedFromTable("cd_personas","idcd_personas")

    queryInsertTransPersonasTitulos= "INSERT IGNORE INTO cd_trans_personas_cat_titulos (idcd_cat_titulos,idcd_personas,rol) VALUES (%s,%s,%s) "
    valorNewTransPersonasTitulos =(idLastCatTitulos,idLastCdPersonas,"Realizador") 
    dbCursor.execute(queryInsertTransPersonasTitulos,valorNewTransPersonasTitulos)

    ''' inserta interpretes a cd_interpretes '''
    insert_interpretes(idLastItem, data[6])
    
if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
        print("No has introducido la contraseña de la BD.\n\t ****** Usage: python FotoRodajes.py [DB_password] ****")
        sys.exit()
    host = "localhost"
    port = 3306 #env raziel
    #port = 14792
    host = "localhost"
    user = "root"
    #passwd="safe-holder"
    passwd = sys.argv[1]
    db = "safe-holder"
    connection = pymysql.connect(host=host, port=port, user=user,
        passwd=passwd, db=db)
    dbCursor = connection.cursor()   

    with open('cd_fotos_rodaje.csv', newline='',encoding="utf-8") as csvfile:
        fotoRodajeReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for item in enumerate(fotoRodajeReader):
            # Esta ejcución toma mucho, aprox 10 mins. evitar correr todo.
             if item[0] >= 1 and item[0] <= 10:
                insertIntoDB(item[1])
                #print("idx-> "+item[0])
    connection.commit()
    
