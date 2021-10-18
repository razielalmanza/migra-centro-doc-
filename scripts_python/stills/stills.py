# SELECT idReg, fechaHoraInsercion AS 'fechaHoraInsercion(cd_item)', 
# TITULO AS 'titutlo_original(cd_cat_titulos)', A AS 'anio(cd_cat_titulos)', 
# COLOCACION AS 'colocacion(cd_item)', A_R_ AS 'a_r_(cd_item__stills)' ,NOTAS AS 'notas(cd_item)', 
# REALIZADOR AS 'foto_old_interpretes(cd_item)' ,
# A_F_TOTAL_DE_EJEMPLARES AS 'a_f_total_de_ejemplares(cd_item_stills)',
# IMAGEN_DIGITAL AS 'imagen_digital(cd_item)', ACTIVO AS 'activo(cd_item)' FROM cd_test.stills 
import json, sys
dict_anios_in_fin = dict()
import stillsSql as sqlStrings 
from datetime import datetime

# Trims and check if it contains idp, and returns as int.
def cleanIds (input):
    if input.startswith('IDP'):
      input = input[3:]
    if (input == '' or  input == ' '):
      return 0
    return int(input)
    #input = int(input) if input != '' or input != ' ' else 0
    #return input

def getAnioInFin (anio, idReg):
  # We remove every space if theres any
  anio.replace(" ", "")
  if anio == " " or anio == "" or anio == "vacio" or anio == "S/D":
    dict_anios_in_fin[idReg] = [0,None]
    return 
  guion_index = anio.find("-")
  if guion_index == -1:
    dict_anios_in_fin[idReg] = [int(anio), int(anio)] # Maybe change second param to None
    return 
  dict_anios_in_fin[idReg] = [int(anio[0:guion_index]), int(anio[guion_index + 1:])]

def getDataFromJSON(file):
# We get the file and change given fields.
    with open(file) as json_file:
        return json.load(json_file) 
    #return data   

def cleanData(data):
    for d in data:
        # Trim to n characters and trim white spaces.
        d['titutlo_original(cd_cat_titulos)'] = d['titutlo_original(cd_cat_titulos)'].strip()[0:250]
        # We get the respective start and end year, then add it to an dictionary with the respective idReg
        # So later when inserting, when getting the years, we ask to the dict in the iteration.
        getAnioInFin(d['anio(cd_cat_titulos)'], d['idReg'])
        d['colocacion(cd_item)'] = int(d['colocacion(cd_item)'])
        d['a_r_(cd_item__stills)'] = cleanIds(d['a_r_(cd_item__stills)'])
        d['notas(cd_item)'] = d['notas(cd_item)'].strip()[0:350]
        d['imagen_digital(cd_item)'] = d['imagen_digital(cd_item)'][0:20]
        d['activo(cd_item)'] = cleanIds(d['activo(cd_item)'])

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
def insertToTable(tableString, params):
    try:
        dbCursor.execute(tableString,params)
    except Exception as e:
        print("Falló en " + str(e))
        print( params)

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

def insertIntoDB(data):
    TIPO_ITEM = "still"
    for d in data:
        ''' cd_cat_titulos (circa remains empty ??) '''
        valCatTitulos = (d['titutlo_original(cd_cat_titulos)'], 
               d['titutlo_original(cd_cat_titulos)'], 
               dict_anios_in_fin[d['idReg']][0],
               dict_anios_in_fin[d['idReg']][1]
               )
        catTitulosID = existe_titulo([
                d['titutlo_original(cd_cat_titulos)'], 
                dict_anios_in_fin[d['idReg']][0]
        ])
        if not catTitulosID:
            insertToTable(sqlStrings.catTitulos, valCatTitulos)
            catTitulosID = getIdLastInserted()
        #else: 
        #    print("existe titulo", catTitulosID)
        ''' cd_personas 'realizador' '''
        valPersona =  [ d['foto_old_interpretes(cd_item)'], 'F' ]
        cdPersonasID = existe_persona(valPersona)
        if not cdPersonasID:
            insertToTable(sqlStrings.cdPersonas, valPersona)
            cdPersonasID = getIdLastInserted()
        #else: 
        #    print("existe persona", cdPersonasID)
        ''' cd_trans_personas_cat_titulos'''
        insertToTable(sqlStrings.transPersonas, [ catTitulosID, cdPersonasID, 'Realizador' ])
        ''' cd_item '''
        fecha = datetime.strptime(d['fechaHoraInsercion(cd_item)'], "%Y-%m-%d %H:%M:%S")
        valCdItem = ( catTitulosID,
                    fecha,
                    "still", 
                    d['imagen_digital(cd_item)'], 
                    d['foto_old_interpretes(cd_item)'],
                    d['colocacion(cd_item)'],
                    d['notas(cd_item)'],
                    d['activo(cd_item)'])
        insertToTable(sqlStrings.cdItem, valCdItem)     
        cdItemID = getIdLastInserted()
        ''' Insert to cd_item_stills '''
        valItemStills = ( cdItemID,   
          d['a_r_(cd_item__stills)'],
          d['a_f_total_de_ejemplares(cd_item_stills)'])
        insertToTable(sqlStrings.itemStills, valItemStills)

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

if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
        print("No has introducido la contraseña de la BD.\n\t ****** Usage: python stills.py [DB_password] ****")
        sys.exit()
    data = getDataFromJSON('stills.json') 
    data = data[1000:1011] # For testing
    cleanData(data)                       # Cleaned data
    dbConnection = createConnectionDB("root", sys.argv[1], "127.0.0.1", "documentacion")
    dbCursor = dbConnection.cursor(buffered=True)
    insertIntoDB(data)
    #testSelect("cd_item")
    #emptyTable("cd_cat_titulos")
    dbConnection.commit()


    #print(dict_anios_in_fin)
    #print(data)