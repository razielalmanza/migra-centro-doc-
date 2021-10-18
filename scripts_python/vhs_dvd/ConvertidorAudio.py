import re
import unicodedata
import json
class ConvertidorAudio:

    def procesaAudio(self, audio):
        self.audio = self.elimina_tildes(audio).lower() 
        self.audio = self.elimina_signos_raros(self.audio)
        self.lista_audio= self.audio.split()
        self.idx_dialogo=-1
        self.idx_subtitulo=-1
        self.idx_intertitulo=-1
        self.audio_cd=[]
        self.dialogos = []
        self.subtitulos = []
        self.intertitulos = []
        self.keyInterWords = ["intertitulos", "inter"] # Aparece 'SINTER' en algunos casos
        self.keySubtWords = ["subtitulos", "subt", "s", "sub", "subr"]
        self.keyAudioWords = ["dialogos", "d","musica","m","silente","narracion","n"] #No sé si agregar aqui "ss" ya que se encuentra en  stopWords
        self.stopWords = ["co", "con", "d", "ss"] + self.keyInterWords + self.keySubtWords + self.keyAudioWords
        self.skipWords = ["en", "e" , "y", "(inicio)", "continuacion", "t"] # "audio EN español, etc'
        #print(self.audio)
        #print("*****************************************")
        #print("Caso: ", self.audio)

        self.extraeIdiomas()

    def extraeIdiomas(self):
        idx = 0
        while idx < len(self.lista_audio):
            if self.find_idx_dialogo(self.lista_audio[idx]):
                #print("Se encontró dialogos en idx", idx)
                #if self.lista_audio[idx] == "silente" or self.lista_audio[idx] == "ss":
                #    self.dialogos.append("SS") 
                salto = self.innerSearchLang("dial", idx)
                self.audio_cd.append(self.lista_audio[idx])
                self.idx_dialogo = idx
                idx += salto

            elif self.find_idx_subtitulo(self.lista_audio[idx]):
                #print("Se encontró subtitulos en idx", idx)
                salto = self.innerSearchLang("subt", idx)
                self.idx_dialogo = idx
                idx += salto

            elif self.find_idx_intersubtitulo(self.lista_audio[idx]):
                #print("Se encontró intersubtitulo en idx", idx)
                salto = self.innerSearchLang("inter", idx)
                self.idx_dialogo = idx
                idx += salto
            idx += 1
        #print("Audio encontrado: ",self.audio_cd)
        #print("Idiomas encontrados: ", self.dialogos)
        #print("Subtítulos encontrados: ", self.subtitulos)
        #print("Intertítulos encontrados: ", self.intertitulos)

    def find_idx_dialogo(self,item):
        #dialogos = re.findall("(^([dD])+(ialogos)*)", item)
        return item in self.keyAudioWords #dialogos or silente or musica
    
    def find_idx_subtitulo(self, item):
        return item in self.keySubtWords

    def find_idx_intersubtitulo(self, item):
        return item in self.keyInterWords
    
    ''' Itera sobre la lista de idiomas, a partir del siguiente item donde apareció un token
        Usa el contador 'salto' para regresar el numero de posiciones las cuales la iteración original
        debe evitar iterar de nuevo.
    '''
    def innerSearchLang(self, tipo, indexInicio):
        lista = self.lista_audio[indexInicio + 1:]
        salto = 0
        for item in lista:
            if item in self.stopWords:
                return salto
            elif item in self.skipWords:
                pass
            # Agrega a la lista según sea el tipo de busqueda
            else:
                if tipo == "dial":
                    self.dialogos.append(item)
                elif tipo == "subt":
                    self.subtitulos.append(item)
                elif tipo == "inter":
                    self.intertitulos.append(item)
            salto += 1
        return salto

    def elimina_tildes(self,cadena):
        '''
        Elimina Acentos y la letra enie por n jejeje
        '''
        s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
        return s
    def elimina_signos_raros(self, cadena):
        s = cadena.replace(",", " ")
        s = s.replace(".", " ")
        s = s.replace("`", " ")
        s = s.replace("/", " ")
        return " ".join(s.split())
#### END MAIN CLASS ####


''' Metodos para probar dentro de la clase el json completo '''
def getDataFromJSON(file):
# We get the file and change given fields.
    with open(file) as json_file:
        return json.load(json_file) 

def pruebaCompleta():
    data = getDataFromJSON('audio_unica.json')
    #data = data[0:100]
    for d in data:
        classAudio.procesaAudio(d["AUDIO"])


if __name__ == "__main__":
    # Algunos casos
    classAudio = ConvertidorAudio() 
    classAudio.procesaAudio("dialogos usa sas ass as aseww as con SUBT esp inter ger")
    classAudio.procesaAudio("dialogos usa con SUBT ingles")
    classAudio.procesaAudio("SUBT esp D esp")
    classAudio.procesaAudio("INTER english D esp")
    # Probamos todo. al sacar el output completo para leer mejor a un txt sale que no hubo excepciones, al menos.
    pruebaCompleta()

'''
Esto era de los casos de prueba que lidié al intentar con indices, me hice bolas :(
 Caso en el que tiene las 3 
id0 = 0
id1 = 3
id2 = 5
case1 = ["dialogos", "a", "b", "subt", "e", "inter", "o"]

print(case1[id0 +1: id1])
print(case1[id1 +1: id2])
print(case1[id2 +1])

Caso en el que tiene solo dial 
id0 = -1
id1 = 3
id2 = -1
case1 = ["dialogos", "a", "b", "subt", "e", "inter", "o"]

if (id1 == -1 == id2 == id0):
    # Asignar nada
    print("no se encontró nada")

inidicesAudio = (id0 +1, id1)
#if (id0 == -1)
indicesSubt = (id1 +1, id2)
indicesInter = (id2 +1)

'''