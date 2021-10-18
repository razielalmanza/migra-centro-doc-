import mysql.connector
import pymysql
import json, sys, csv
from datetime import datetime
from ManejadorIdiomasISO import ManejadorIdiomasISO

'''
    0: idReg
    1: formato(cd_vhs_dvd)
    2: color(cd_vhs_dvd)
    3: audio(cd_vhs_dvd)
    4: idioma(cd_vhs_dvd)
    5: subtitulos(cd_vhs_dvd)
    6: intertitulos(cd_vhs_dvd)
    7: norma(cd_vhs_dvd)
    8: duracion(cd_vhs_dvd)
    9: region(cd_vhs_dvd)
    10: pantalla(cd_vhs_dvd)
    11: observaciones(cd_vhs_dvd)
    12: pais_de_realizacion(cd_cat_titulos)
    13: extras(cd_vhs_dvd)
    14: fechaHoraInsercion(cd_item)
    15: tipo_item(cd_item)
    16: imagen_digital(cd_item)
    17: foto_old_interpretes(cd_item)
    18: activo(cd_item)
    19: colocacion(cd_item)
    20: notas(cd_item)
    21: titulo_original(cd_cat_titulos)
    22: titulo_en_espa(cd_cat_titulos)
    23: anio(cd_cat_titulos)
    24: nombre(cd_personas)
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

def insert(sql, val):
    try:
        dbCursor.execute(sql,val)
    except Exception as e:
        print("Falló en " + str(e))
        print( val)

def readCSV(file):
    dictionary = {}
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')       
        for a in csv_reader:
           try:
             dictionary[int(a[0])] = int(a[1])
           except:
               pass
    return dictionary

'''
    Regresa el time en formato hhh:mm:ss
    Recibe el tiempo en segundos.
'''
def segundos_a_time(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return '{}:{:0>2}:{:0>2}'.format(h, m, s)

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
  nombre = %s AND 
  tipo_persona = %s
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

def insertIntoDB(data, duracion):
    TIPO_ITEM = "vhs_dvd"
    '''
        Aqui se puede realizar el procesamiento de las columnas
        de audio,idioma subtitulos e intertitulos adaptandolo a las ISO's 
        ya que el resto de la información viene ya cumpliendo los requerimientos
        que estan en confluence.
        En unos campos los lee como None ya que estan vacios y
        cuando los insertas a la DB da una excepcion porque algunos
        campos de la nueva BD no te permite agregar nulos. 
    '''
    
    '''
        Se insertan primero los cat_values
    '''
    sqlCatValue =  """ INSERT IGNORE INTO cat_values 
                        (tname, fname, val, display_value) 
                        VALUES (%s, %s, %s, %s) """
    insert(sqlCatValue, ["vhs_dvd", "formato", data[1], data[1]] ) # cat_values formato
    insert(sqlCatValue, ["vhs_dvd", "pantalla", data[10], data[10]] ) # cat_values pantalla
    insert(sqlCatValue, ["vhs_dvd", "extras", data[13], data[13]] ) # cat_values extras

    '''
        Se verifica si existe un título, si no se inserta uno nuevo.
    '''
    sql = """ INSERT INTO cd_cat_titulos 
               (titulo_original, titulo_en_espa, anio, pais_de_realizacion) 
               VALUES (%s, %s, %s, %s) """

    anio = data[23]
    if(data[23] == "" or data[23] is None or not data[23].isnumeric() ):
        anio=0
    val = (data[21], data[22], anio, data[12])
    
    lastIdFromCatTitulos = existe_titulo([data[21], anio])
    
    if not lastIdFromCatTitulos:
        insert(sql, val)
        lastIdFromCatTitulos = getIdLastInsertedFromTable("cd_cat_titulos","idcd_cat_titulos")
    #else: 
    #    print("ya existe titulo", lastIdFromCatTitulos)
    queryInsertarItem = "INSERT INTO cd_item (idcd_cat_titulos, fechaHoraInsercion, tipo_item, imagen_digital, activo,colocacion, notas) VALUES (%s,%s, %s, %s, %s,%s,%s) "
    fecha=datetime.strptime(data[14],"%d-%m-%Y %H:%M:%S")
    valorNewItem = (lastIdFromCatTitulos,fecha,TIPO_ITEM,data[16],data[18],data[19],data[20])
    insert(queryInsertarItem,valorNewItem)
    lastInsertedCdItem = getIdLastInsertedFromTable("cd_item", "idcd_item")
    
    '''
    En este punto, en la inserción a la nueva base, se decide insertar la información como va. Sin ninclur ISOs en idiomas.
    #Aqui se agrega a la tabla de vhs_dvd la informacion
    convertidorIdiomasISO.procesaISOLenguaje(data[4]) #idiomas, faltaria los idiomas de subtitulos e intertitulos. 
    '''
  
    queryInsertarCdPersonas = "INSERT INTO cd_personas (nombre, tipo_persona) VALUES (%s,%s) "
    valorCdPersonas = (data[24], "F")
    idLastCdPersonas = existe_persona(valorCdPersonas)
    if not idLastCdPersonas:
        insert(queryInsertarCdPersonas,valorCdPersonas)
        idLastCdPersonas = getIdLastInsertedFromTable("cd_personas", "idcd_personas")

    queryInsertTransPersonasTitulos= "INSERT IGNORE INTO cd_trans_personas_cat_titulos (idcd_cat_titulos,idcd_personas,rol) VALUES (%s,%s,%s) "
    valorTransPersonasTitulos = (lastIdFromCatTitulos,idLastCdPersonas,"Realizador")
    insert(queryInsertTransPersonasTitulos,valorTransPersonasTitulos)

    queryCdItem = "INSERT INTO cd_vhs_dvd VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    duracion_en_TIME = segundos_a_time(duracion)
    valuesCdItem = (lastInsertedCdItem, data[1], data[2], data[3], data[4], data[5], data[6], data[7], duracion_en_TIME, data[9], data[10], data[11], data[13])
    insert(queryCdItem, valuesCdItem)


if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
        print("No has introducido la contraseña de la BD.\n\t ****** Usage: python VhdDvd.py [DB_password] ****")
        sys.exit()
    host = "localhost"
    port = 3306 #env raziel
    #port=14792
    user = "root"
    #passwd="root"
    passwd = sys.argv[1]
    db = "documentacion"
    duraciones = readCSV("duracion_en_TIME.csv")
    #print(duraciones[12121])
    connection = pymysql.connect(host=host, port=port, user=user,
        passwd=passwd, db=db)
    dbCursor = connection.cursor()   
    convertidorIdiomasISO = ManejadorIdiomasISO()
    with open('cd_vhs_dvd.csv', newline='',encoding="utf-8") as csvfile:
        videosReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for item in enumerate(videosReader):
            if item[0] >= 1 and item[0] <= 10: #Se pone una cota para no procesar toooooda la informacion
                #print(item[1])
                duracion_en_segundos = duraciones[int(item[1][0])] # Obtenemos la duracion según su idReg, item[1][0]
                insertIntoDB(item[1], duracion_en_segundos ) # Enviamos su duracion en segundos
    connection.commit()

