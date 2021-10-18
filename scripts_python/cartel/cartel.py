# Uses the script in 'cartel car union.sql' to get the data used here.

import json, sys
import cartelSql as sqlStrings 
from datetime import datetime

'''
Trims and check if it contains idp, and returns as int.
'''
def cleanIds (input):
    if input.startswith('IDP'):
      input = input[3:]
    if (input == '' or  input == ' '):
      return 0
    return int(input)
    #input = int(input) if input != '' or input != ' ' else 0
    #return input

def getDataFromJSON(file):
# We get the file and change given fields.
    with open(file) as json_file:
        return json.load(json_file) 
    #return data   

#from six.moves import input

'''
  Usado para unificar el campo IMAGEN_DIGITAL a Int y A que corresponde a año.
'''
def getInts(input_user):
  badFormats = [' ', '', 'SD', 'BUENO', 'S', 'FS', 'FSD', 'S-D', 'A', 'D']
  if input_user.startswith('IDC'):
      input_user = input_user[3:]
  if input_user in badFormats:
    return 0
  try:
    return int(input_user) 
  except:
    #a = input("Error en " + input_user + " hagalo manual:")
    #return int(a)
    return 0 #default value for error cases

'''
  No se usa pues en tabla cartel/car no se usa formato de rango de años. 
'''
def getAnios(data):  
    diccionario = dict()   
    for i in data:
      if len(i['A']) > 4:
        print (i['A'])
        anio = int(input("inicio"))
        anioFin = int(input("fin")) 
        diccionario[i['idReg']] = [anio, anioFin]
      else:
        diccionario[i['idReg']] = [i['A'], None]
      
def cleanData(data):  
    for d in data:
        # Trim to n characters and trim white spaces.
        d['A'] = getInts(d['A'])
        d['INSTITUCION'] = d['INSTITUCION'].strip()[0:350] 
        d['COLOCACION'] = d['COLOCACION'][0:16]
        d['DESCRIPTORES'] = d['DESCRIPTORES'][0:120]
        d['NOTAS'] = d['NOTAS'][0:120]
        d['TECNICA'] = d['TECNICA'][0:150]
        d['SOPORTE'] = d['SOPORTE'][0:60]
        d['DA'] = d['DA'][0:100]
        #d['IMAGEN_DIGITAL'] = getInts(d['IMAGEN_DIGITAL'])
        d['IMAGEN_DIGITAL'] = d['IMAGEN_DIGITAL'][0:20]



import mysql.connector
def createConnectionDB(user, password, host, db):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        #port=14792
        port=3306 #env raziel
        )
    return mydb

'''
Recibe la cadena que contiene el INSERT INTO, y los parámetros a insertar.
'''
def insertToTable(tableString, params=None):
    try:
        dbCursor.execute(tableString, params)
    except Exception as e:
        print("Falló en " + str(e))
        print( params)

'''
Recibe el id del cd_item y la cadena con los interpretes.
Separa a los interpretes por comas en una lista, por cada uno se crea la relación 
cd_trans_item_interpretes.
'''
def insert_interpretes(id_cd_item, interpretes):
  nombres_array = interpretes.split(",")
  for nombre in nombres_array:
      nombre = nombre.strip()
      if nombre == "":
        continue
      # Insertamos a cd_interpretes.
      insertToTable(sqlStrings.cdInterpretes, (nombre))
      # Insertamos a cd_trans_item_interpretes
      params = (id_cd_item, nombre)
      insertToTable(sqlStrings.transInterpre, params)


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

def insertIntoDB(data, paisesISO):
    TIPO_ITEM = "cartel"
    for d in data:
        ''' cat_values 'tama' '''
        insertToTable(sqlStrings.catValues, [ "cartel", "tama", d['TAMA'], d['TAMA'] ])
        ''' cd_cat_titulos '''
        ''' circa sigue vacío '''
        data_titulo = [ 
          d['TITULO_ORIGINAL'], 
          d['TITULO_EN_ESPA'], 
          d['A'], 
          paisesISO[d['idReg']]
        ]
        cdCatTitulosID = existe_titulo([ d['TITULO_ORIGINAL'], d['A']])
        if (not cdCatTitulosID):
          insertToTable(sqlStrings.catTitulos, data_titulo)
          cdCatTitulosID = getIdLastInserted()
        ''' cd_personas 'realizador' '''
        data_persona = [ d['REALIZADOR'], 'F' ]
        cdPersonasID = existe_persona(data_persona)
        if not cdPersonasID:
          insertToTable(sqlStrings.cdPersonas, data_persona )
          cdPersonasID = getIdLastInserted()
        ''' cd_trans_personas_cat_titulos'''
        insertToTable(sqlStrings.transPersonas, [ cdCatTitulosID, cdPersonasID, 'Realizador' ])
        ''' cd_item '''
        fecha = datetime.strptime(d['fechaHoraInsercion'], "%Y-%m-%d %H:%M:%S")
        valCdItem = ( cdCatTitulosID,
                    fecha,
                    TIPO_ITEM, 
                    d['IMAGEN_DIGITAL'], 
                    d['INTERPRETES'],
                    d['COLOCACION'],
                    d['NOTAS'],
                    d['ACTIVO'])
        insertToTable (sqlStrings.cdItems, valCdItem)
        cdItemID = getIdLastInserted()
        ''' inserta interpretes a cd_interpretes '''
        insert_interpretes(cdItemID, d['INTERPRETES'])
        # cd_item_cartel
        valCartel = ( cdItemID,  
          d['INSTITUCION'],
          paisesISO[d['idReg']],
          d['TAMA'],
          d['EJEMPLARES'],
          d['TECNICA'],
          d['ESTADO_FISICO'],
          d['DISENIADOR'],
          d['car_consulta'])
        insertToTable(sqlStrings.cdCartel, valCartel)

'''
Util SQL functions
'''
def testSelect(table):
    dbCursor.execute("SELECT * FROM " + table)
    for row in dbCursor:
        print(row)
def emptyTable(table):
    dbCursor.execute("DELETE FROM " + table)
def getIdLastInserted():
    sql = "SELECT LAST_INSERT_ID()"
    dbCursor.execute(sql)
    for row in dbCursor:
        return row[0]

'''
Regresa un diccionario de cada entrada en la base con el forrmato:
{idReg: PAIS}
'''
def countriesAsDict(data):
  diccionario = dict()  
  for i in data:
    diccionario[i['idReg']] = i['PAIS']
  return diccionario

import ManejadorPaises as mp
def obtainCountriesInIsoAlpha3(data):
  paisesComoDict = countriesAsDict(data)
  manejador = mp.ManejadorPaises()
  paisesIsoAlpha3 = manejador.getIsoAlpha3WithDicc(paisesComoDict)
  #print(paisesIsoAlpha3)
  return paisesIsoAlpha3

if __name__ == "__main__":
    if (len(sys.argv) < 3 ):
      print("No has introducido la contraseña de la BD. O el archivo a leer\n\t ****** Usage: python cartel.py [DB_password] cartel/car.json ****")
      sys.exit()
    data = getDataFromJSON(sys.argv[2]) # Remember to run with car.json and cartel.json.
    data = data[0:10] # for testing
    # Se tarda muchísimo ya 30+ mins en prueba completa.
    cleanData(data)                       # Cleaned data
    paisesWithIso3 = obtainCountriesInIsoAlpha3(data)
    dbConnection = createConnectionDB("root", sys.argv[1], "127.0.0.1", "documentacion")
    dbCursor = dbConnection.cursor(buffered=True)
    insertIntoDB(data, paisesWithIso3)
    dbConnection.commit()
