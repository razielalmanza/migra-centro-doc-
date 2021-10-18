"""
Este script usa el 'person.json' obtenido de usar el wizard de export mysql Workbench.
Usando ese query.
    SELECT idReg, fechaHoraInsercion AS 'fechaHoraInsercion(cd_item)',
    NOMBRE_ARTISTICO AS 'nombre_artistico(cd_item_personalidades)',
    NOMBRE_VERDADERO AS 'nombre_verdadero(cd_item_personalidades)',
    SOBRENOMBRE AS 'sobrenombre(cd_item_personalidades)',COLOCACION AS 'colocacion(cd_item)',
    A_R_ACERVO_REPETIDO AS 'a_r_acervo_repetido(cd_item_personalidades)',IMAGEN_DIGITAL AS 'imagen_digital(cd_item)',
    NOTAS AS 'notas(cd_item)',ACTIVO AS 'activo(cd_item)' FROM cd_test.person 

El proceso para la nueva base será, primero  insertar a la tabla cd_item y luego, preguntar por
INSERT INTO table_name (col1, col2,...) VALUES ('val1', 'val2'...);
SELECT LAST_INSERT_ID(); te da el últmo de la conexión y por usuario, SI SIRVE
Usar ese id para insertar ya en cd_item_person

# Idea: User el formato 'parametro(tabla)' para hacer mas rapido inserts.

"""
import json, sys
import personSql as sqlStrings 
from datetime import datetime

# Trims and check if it contains idp, and returns as int.
def cleanIds (input):
    if input.startswith('IDP'):
      input = input[3:]
    input = int(input) if input != '' else 0
    return input

def getDataFromJSON(file):
# We get the file and change given fields.
    with open(file) as json_file:
        return json.load(json_file) 
    #return data   

# change given fields.
def cleanData(data):
    for d in data:
        # Trim to 100 characters and trim white spaces.
        d['nombre_artistico(cd_item_personalidades)'] = d['nombre_artistico(cd_item_personalidades)'][0:100].strip()
        d['nombre_verdadero(cd_item_personalidades)'] = d['nombre_verdadero(cd_item_personalidades)'][0:100].strip()
        d['sobrenombre(cd_item_personalidades)'] = d['sobrenombre(cd_item_personalidades)'][0:100].strip()
        d['colocacion(cd_item)'] = d['colocacion(cd_item)'][0:30].strip()
        d['a_r_acervo_repetido(cd_item_personalidades)'] = cleanIds(d['a_r_acervo_repetido(cd_item_personalidades)'])
        d['imagen_digital(cd_item)'] = cleanIds(d['imagen_digital(cd_item)'])
        d['activo(cd_item)'] = cleanIds(d['activo(cd_item)'])
        d['notas(cd_item)'] = d['notas(cd_item)'][0:350]


#### SQL STUFF ###
#############################
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
Recibe la cadena que contiene el INSERT INTO, y los parámetros a insertar.
'''
def insertToTable(tableString, params):
    try:
        dbCursor.execute(tableString,params)
    except Exception as e:
        print("Falló en " + str(e))
        print( params)


''' Importante, busca cojncidencia si el a_r_acervo_repetido y el nombre artistico hacen match. '''
def existe_personalidad(data_entidad):
  dbCursor.execute(
  """SELECT idcd_cat_personalidades
  FROM cd_cat_personalidades
  WHERE 
  nombre_artistico = %s AND 
  a_r_acervo_repetido = %s """, 
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
    for d in data:
        ''' cd_cat_personalidades '''
        valPerson = (
          d['nombre_artistico(cd_item_personalidades)'],
          d['nombre_verdadero(cd_item_personalidades)'],
          d['sobrenombre(cd_item_personalidades)'],
          d['a_r_acervo_repetido(cd_item_personalidades)'])
        cdPersonID = existe_personalidad([
            d['nombre_artistico(cd_item_personalidades)'],
            d['a_r_acervo_repetido(cd_item_personalidades)']
        ])
        if not cdPersonID:
            insertToTable(sqlStrings.cdPerson, valPerson)
            cdPersonID = getIdLastInserted()
        #else:
        #    print("ya existe", cdPersonID)
        ''' cd_item '''
        fecha = datetime.strptime(d['fechaHoraInsercion(cd_item)'], "%Y-%m-%d %H:%M:%S")
        valCdItem = (cdPersonID,
                    fecha,
                    "person", 
                    d['imagen_digital(cd_item)'], 
                    d['colocacion(cd_item)'],
                    d['notas(cd_item)'],
                    d['activo(cd_item)'])
        insertToTable(sqlStrings.cdItem, valCdItem)
        

if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
      print("No has introducido la contraseña de la BD.\n\t ****** Usage: python cartel.py [DB_password] ****")
      sys.exit()
    data = getDataFromJSON('person.json') # Global ref to data.
    cleanData(data)                       # Cleaned data
    dbConnection = createConnectionDB("root", sys.argv[1], "127.0.0.1", "documentacion")
    dbCursor = dbConnection.cursor(buffered=True)
    data = data[0:10] # Made for testing
    insertIntoDB(data)
    #testSelect("cd_item")
    #emptyTable("cd_cat_titulos")
    dbConnection.commit()






########################## We can use already use the dict 'data' to insert to some database.
# Export to json with unicode characters ( :( )
"""
with open('person_cleaned_with_unicode.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile)
## This is to import the json to csv without unicode characters
import pandas as pd
df = pd.read_json (r'./person_cleaned_with_unicode.json')
df.to_csv (r'./person_clean_without_unicode.csv', index = None)
"""

"""
Time stuff to manage format time, if needed.
import datetime
import time

fecha = "2014-06-27 13:14:18"
fecha = time.mktime(datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").timetuple())
print (fecha)
print(datetime.datetime.utcfromtimestamp(fecha).strftime('%Y-%m-%d %H:%M:%S'))

"""



        
   