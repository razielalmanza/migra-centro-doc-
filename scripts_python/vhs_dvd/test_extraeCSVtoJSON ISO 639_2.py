# Clase para extraer la lista de idiomas 'ISO639-2_spa.csv' a una lista de jsons usable en el front end.
class Prueba:
  def __init__(self):
    self.listaISO = []

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
          self.listaISO.append({"value": idioma, "code": iso639_2})

  def elimina_comas(self, cadena):
      s = cadena.replace(",", " ")
      return " ".join(s.split()).lower()

  def elimina_tildes(self,cadena):
    '''
    Elimina Acentos y la letra enie por n jejeje
    '''
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s

if __name__ == "__main__":
  clasePrueba = Prueba()
  clasePrueba.getDataFromFile('ISO639-2_spa.csv') 
  print(clasePrueba.listaISO) 

