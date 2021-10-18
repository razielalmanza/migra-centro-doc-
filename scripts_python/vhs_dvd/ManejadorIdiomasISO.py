import json
from ConvertidorAudio import ConvertidorAudio
import copy

''' 
	Esta clase al llamarla debería asignar a 'self.idiomasEnISO'
	el diccionario con estructura que se menciona en procesarAudios().
	El cual bastaría consultar direcamente con el idReg para obtener la listas de audios procesados con su ISO
'''
class ManejadorIdiomasISO:
    def __init__(self):
      self.audiosOriginal = self.getDataFromJSON('audio_unica.json')
      self.classExtraeIdiomas = ConvertidorAudio()
      self.idiomasExtraidos = dict()

      # Tal vez podríamos usar otra clase:
      self.idiomasIntermedio = self.getDataFromJSON('idiomas_inter.json')
      self.diccionarioISO = dict()
      self.getDataFromFile('ISO639-2_spa.csv') 

      self.conjuntoIdiomas = []
      # Obtenemos el iso
      self.idiomasEnISO = None 
      self.conteoConflictos = 0

    ''' Iteramos sobre todos los valores de los diccionarios.
        Es decir, en cada lista de idiomas extraida.
     '''
    def procesaISO(self):
      self.idiomasEnISO = copy.deepcopy(self.idiomasExtraidos) # Mantener una copia clara de los idiomas extraidos antes y despues del ISO
      for item in self.idiomasEnISO.values():
        # Procesamos las entradas 1, 2 y 3. (diaologos, subs, inter)
        # La entrada cd_item que es la 0 se queda igual.
        self.procesa(item[1])
        self.procesa(item[2])
        self.procesa(item[3])


    def procesaISOLenguaje(self,cadena_idiomas):
      '''
        Este es una adaptacion cuando esta clase es invocada desde VhsDvd.
        El parametro cadena_idiomas es de tipo "ESP USA FRA"
        En este metodo se convierte en un arreglo y ya se procesaria consultando en
        otra clase para que nos devuelva la cadena con los lenguajes ya convertidos
      '''
      lista_idioma = cadena_idiomas.split()
      #print("SE pretende convertir a ISO63 la lisa: ",lista_idioma) 
      # Manda a llamar a procesa, que usa listas de idiomas.
      lista_procesada = self.procesa(lista_idioma)
      return lista_procesada
      
    
    ''' Recibe una lista de idiomas: listas de subtitulos, dialogos, etc
    Casos: 
          1: El idioma ya existe en nuestro diccionario con ISO válido, se deja como va. ('por', 'eng', 'spa')
          2: El idioma pasa por nuestro diccionario intermedio. (typos: 'mex', 'usa', 'spanol')
          3: El idioma se escribió en español y se busca en el diccionario en el iso por llave. ('español', 'ingles')  
    
    Regresa una lista de idiomas procesados en ISO o especificando que no hay.
    '''
    def procesa(self, listaIdiomas):
      FLAG_NOT_FOUND = "NO SE ENCONTRÓ MATCH: "
      for i in range(len(listaIdiomas)):
        #if (listaIdiomas[i] not in self.conjuntoIdiomas):
        #  self.conjuntoIdiomas.append(listaIdiomas[i]) 
        idioma = None
        # Caso 1
        if (self.isLanguajeValidISO(listaIdiomas[i])):
          idioma = listaIdiomas[i]
        # Caso 2
        if (not idioma):
          idioma = self.getKeyFromLanguaje(listaIdiomas[i])
        # Caso 3
        if (not idioma):
          try:
            idioma = self.diccionarioISO[listaIdiomas[i]]['iso639_2']
          except:
            idioma = FLAG_NOT_FOUND + listaIdiomas[i]
            listaIdiomas[i] = idioma
            self.conteoConflictos += 1
        #print(idioma)
        listaIdiomas[i] = idioma

      return listaIdiomas 
    
    def isLanguajeValidISO(self, idioma):
      for dicc in self.diccionarioISO.values():
        if idioma == dicc['iso639_2']:
          return True
      return False
    
    ''' Busca si un idioma está dentro de nuestro diccionario intermedio 
        si existe regresa el idoma en iso correcto, si no, un None.
    '''
    def getKeyFromLanguaje(self, languaje):
      i = 0
      for valores in self.idiomasIntermedio.values():
        if languaje in valores:
          return list(self.idiomasIntermedio.keys())[i]
        i +=1
      return None

    def getDataFromJSON(self, file):
    # We get the file and change given fields.
        with open(file) as json_file:
            return json.load(json_file)

    ''' Este método jala la info de la pagina que se encuentra en google. (Es especifico a este archivo).
        El cual carece de formato como csv, pues es el copy/paste mal formateado de la tabla.
        Abrir archivo para detalles.
        Pero tiene en español la información necesaria. '''
    def getDataFromFile(self, file):
      file1 = open(file, 'r',  encoding="utf8") 
      Lines = file1.readlines() 
      for line in Lines: 
          lineAsList = line.split()
          # Hago uso de comentarios en el archivo fuente con '#' en idiomas conflicitivos.
          if lineAsList[0] == "#":
            continue
          # Como las lineas son de la forma:
          # Nombres idiomas en español  iso-1  iso-2
          # Donde las últimas dos palabras son los codigos y el resto del inicio son nombres, se hace:
          iso639_2 = lineAsList.pop()
          iso639_1 = lineAsList.pop()
          # lineAsList es la ahora la lista de nombres de ese idioma, ahora
          # a cada idioma en español le agregamos sus codigos.
          for idioma in lineAsList:
            idioma = self.elimina_comas(idioma)
            idioma = self.classExtraeIdiomas.elimina_tildes(idioma)
            self.diccionarioISO[idioma] = {"iso639_1": iso639_1, "iso639_2": iso639_2} 

    def elimina_comas(self, cadena):
        s = cadena.replace(",", " ")
        return " ".join(s.split()).lower()
      

    '''
    Utiliza el json audio_unica para procesar los audios de cada idReg de la tabla orignal 'unica'.
    Regresa diccionario con estructura:
        { idReg: [ [audio], [dialogos], [subtitulos], [intertitulos] ] }
    '''
    def procesarAudios(self):
        #self.audiosOriginal = self.audiosOriginal[0:100] # Acortamos para pruebas
        for item in self.audiosOriginal:
            self.classExtraeIdiomas.procesaAudio(item["AUDIO"])
            self.idiomasExtraidos[item["idReg"]] = [self.classExtraeIdiomas.audio_cd ,self.classExtraeIdiomas.dialogos, self.classExtraeIdiomas.subtitulos, self.classExtraeIdiomas.intertitulos]

# Regresa un conteo total de conflictos.
# Sobre la tabla completa de unica.
def conteoConflcitos():
  clasePrueba.procesarAudios()
  clasePrueba.procesaISO()
  print("Conflictos " + str(clasePrueba.conteoConflictos) + " / " + str(len(clasePrueba.idiomasExtraidos)))

# Usa la lista de idiomas unicos obtenidos e intenta obtener su match, y regresa 
# si hay conflicto o no. 
def verConflictosListaCompleta():
  idiomasUnicos = "francia espanol esp quechua frances ingles portugues por sueco ene spanol ruso usa gbr nld italiano aleman prt rus japones jpn fra tr aus ita dnk swe chn latin deu holandes arabe son afgano thailandes koreano chino coreano mandarin danes finlandes georgiano serbio hebreo hindi vietnamita polaco hungaro checo persa dbl alman noruego tailandes catalan vnm euskera fines tibetano griego turco cantones spa chi eng ger fre pol bul dut psa sze cze ing int tur rumano bulgaro egipcio taiwanes bengali urdu dzongkha jaapones tajiko arabigo espanolcon croata yidis inglescon irlandes nahuatl hindu filipino zapoteco kurdo bosnio suajili tayiko kor francescon totonaco purepecha itaiano k'iche' belga epanol inglesm zulu flamenco corenao es coreno servo-croata tha isr cnh sbl nor ser gre ara nhl eps irn yug bra rom fin mex grc ind sau ndl cog phl srb bel pahl aut egy us fvra dnl geo hun itadnk twn kaz hin ndk isl rrt aubt prtchn arb kopr ukr sut espprt espnfra espjpn eusa pse che est uzb arm bih mng irq zaf ko mkd mprt albanes cmr rwa svn cat ned esloveno malayo islandes neerlandes ucraniano mixteco lingala gallego serbo-croata mongol frnces lituano"
  output = clasePrueba.procesaISOLenguaje(idiomasUnicos)
  for idioma in (output):
    print (idioma)

# Para hacer pruebas individuales.
def pruebaIndividual(idiomas):
  print(clasePrueba.procesaISOLenguaje(idiomas))

# Hace una prueba completa de 0, jala del json de la tabla unica, extrae, pasa a iso y regresa
# diccionario de la forma {idReg: [...]}
def pruebaCompletaDeCero():
  clasePrueba.procesarAudios()
  clasePrueba.procesaISO()
  #print(clasePrueba.idiomasExtraidos)
  print(clasePrueba.idiomasEnISO)

if __name__ == "__main__":
    clasePrueba = ManejadorIdiomasISO() 
    #pruebaCompletaDeCero()
    #conteoConflcitos()
    verConflictosListaCompleta()
    #pruebaIndividual("mex usa ingles")
    