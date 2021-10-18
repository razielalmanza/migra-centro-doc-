import mysql.connector
import pymysql
import json, sys, csv

'''
SELECT 
idReg, EJEMPLARES as 'ejemplares(cd_item_fotomontajes)' , PAIS as 'pais(cd_item_fotomontajes)' 
,fechaHoraInsercion as 'fechaHoraInsercion(cd_item)', 'fmontaje' as 'tipo_item(cd_item)', 
IMAGEN_DIGITAL as 'imagen_digital(cd_item)', INTERPRETES as 'foto_old_interpretes(cd_item)', 
ACTIVO as 'activo(cd_item)' , COLOCACION as 'colocacion(cd_item)', NOTAS as 'notas(cd_item)', 
TITULO_ORIGINAL as 'titulo_original(cd_cat_titulos)', TITULO_EN_ESPA as 'titulo_en_espa(cd_cat_titulos)', 
A as 'anio(cd_cat_titulos)', REALIZADOR as 'nombre(cd_personas)'
from cd_test.fomo;

0: idReg
1: ejemplares(cd_item_fotomontajes)
2: pais(cd_item_fotomontajes)      
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

def getIdLastInserted():
    sql = "SELECT LAST_INSERT_ID()"
    dbCursor.execute(sql)
    for row in dbCursor:
        return row[0]

def getIdLastInsertedFromTable(nameTable,nameId):
    sql =  "SELECT * FROM "+nameTable+" WHERE "+nameId+" = (SELECT LAST_INSERT_ID())" #"SELECT MAX( "+nameId+" ) FROM "+ nameTable
    dbCursor.execute(sql)
    result = dbCursor.fetchall()
    for row in result:
        return row[0]

'''
Recibe el id del cd_item y la cadena con los interpretes.
Separa a los interpretes por comas en una lista, por cada uno se crea la relación 
cd_trans_item_interpretes.
'''
def insert_interpretes(id_cd_item, interpretes):
  cdInterpretes = """ INSERT IGNORE INTO cd_interpretes
                (nombre)
                VALUES (%s) """
  transInterpre = """ INSERT IGNORE INTO cd_trans_item_interpretes
                  (idcd_item, nombre)
                  VALUES (%s, %s) """ 
  nombres_array = interpretes.split(",")
  for nombre in nombres_array:
      nombre = nombre.strip()
      if nombre == "":
        continue
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
    TIPO_ITEM = "fomo"
    #AGREGAR LOS DATOS DE FOTOMONTAJES  -> comentario por Berna, no veo a qué se refiere.
    ''' 
        Agregamos a cd cat títulos si no existe uno ya.
    '''
    sql = """ INSERT INTO cd_cat_titulos 
               (titulo_original, titulo_en_espa, anio) 
               VALUES (%s, %s, %s) """
    anio = data[12]
    if(data[12] == "" or data[12] == "SD" or data[12] is None or not data[12].isnumeric() ):
        anio = 0
    val = (data[10], data[11], anio)
    idToInsertCatTitulos = existe_titulo([data[10], anio])
    if not idToInsertCatTitulos:
        insert(sql, val)
        idToInsertCatTitulos = getIdLastInsertedFromTable("cd_cat_titulos","idcd_cat_titulos")
    '''
        insertamos a cd_item 
    '''
    queryInsertarItem = "INSERT INTO cd_item (idcd_cat_titulos, fechaHoraInsercion,tipo_item, imagen_digital, foto_old_interpretes,activo,colocacion, notas) VALUES (%s,%s, %s, %s, %s, %s,%s,%s) "    
    valorNewItem =(idToInsertCatTitulos,data[3], TIPO_ITEM ,data[5],data[6],data[7],data[8],data[9])
    insert(queryInsertarItem,valorNewItem)
    idToInsertFotomontajes = getIdLastInsertedFromTable("cd_item","idcd_item")
    '''
        insertamos a cd_item_fotomontajes 
    '''
    queryInsertarFotomontaje = "INSERT INTO cd_item_fotomontajes (idcd_item, ejemplares, pais) VALUES (%s,%s,%s) "
    valorNewFotomontaje= (idToInsertFotomontajes, data[1], data[2])
    insert(queryInsertarFotomontaje,valorNewFotomontaje)
    '''
        insertamos a cd_personas si no existe  
    '''
    queryInsertarCdPersonas = "INSERT INTO cd_personas (nombre, tipo_persona) VALUES (%s,%s) "
    valorCdPersonas = (data[13], "F")
    idLastCdPersonas = existe_persona(valorCdPersonas)
    if not idLastCdPersonas:
        insert(queryInsertarCdPersonas,valorCdPersonas)
        idLastCdPersonas = getIdLastInsertedFromTable("cd_personas","idcd_personas")
    '''
        insertamos a trans 
    '''
    queryInsertTransPersonasTitulos= "INSERT IGNORE INTO cd_trans_personas_cat_titulos (idcd_cat_titulos,idcd_personas,rol) VALUES (%s,%s,%s) "
    valorTransPersonasTitulos = (idToInsertCatTitulos,idLastCdPersonas, "Realizador")
    insert(queryInsertTransPersonasTitulos, valorTransPersonasTitulos)

    ''' inserta interpretes a cd_interpretes '''
    insert_interpretes(idToInsertFotomontajes, data[6])

if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
        print("No has introducido la contraseña de la BD.\n\t ****** Usage: python fotomontajes.py [DB_password] ****")
        sys.exit()
    host = "localhost"
    port = 3306
   # port = 14792
    user = "root"
    passwd = sys.argv[1]
    db = "documentacion"
    connection = pymysql.connect(host=host, port=port, user=user,
        passwd=passwd, db=db)
    dbCursor = connection.cursor()   

    with open('cd_fotomontajes.csv', newline='',encoding="utf-8") as csvfile:
        fotomontajesReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for item in enumerate(fotomontajesReader):
            if item[0] >= 1 and item[0] <= 10:
                insertIntoDB(item[1])
                #print("idx-> "+item[0])
    connection.commit()
    