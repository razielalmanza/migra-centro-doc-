# -*- coding: utf-8 -*-
import json
import unicodedata
class ManejadorPaises:
    '''
    Recibe un string de paises separados por un guión
    '''
    def __init__(self,cadenaOriginal,separador):
        self.separador= separador
        self.cadenaOriginal=cadenaOriginal.lower()
        with open('countries.json',encoding="utf-8") as f:
            self.listaPaises= json.load(f)["paises"]
        
    def __init__(self):
        with open('countries.json',encoding="utf-8") as f:
            self.listaPaises= json.load(f)["paises"]

    '''
        Devuelve el pais en formato ISO alpha3 utilizando como auxiliar 
        el archivo countries.json en español. 
        En caso de que no funcione lanzara un string advirtiendo el pais que no regresa el formato correctamente
    '''
    def getIsoAlpha3(self):        
        if self.cadenaOriginal == "hong-kong" or self.cadenaOriginal=="hong kong":
            #print("HONG-KONG")
            return "HKG"
        elif self.cadenaOriginal == "gran bretaña" or self.cadenaOriginal == "reino unido":
            #print("HONG-KONG")
            return "GBR"
        elif self.cadenaOriginal == "estados unidos":
            return "USA"
        elif self.cadenaOriginal == "costa rica":
            return "CRI"
        elif self.cadenaOriginal == "puerto rico":
            return "PRI"
        elif self.cadenaOriginal == "corea del sur":
            return "PRI"
        else:
            lista=[]
            print(self.separador)
            lista=self.cadenaOriginal.split(self.separador)
            '''
            if len(lista) == 1:
                lista= lista[0].split()
            if len(lista) == 1:
                lista = lista[0].split("/")
            if len(lista) == 1:
                lista = lista[0].split("-")
            '''
            listaProcesada=[]
            print("*******************************")
            #print(lista)
            for pais in lista:
                verificaPais=self.buscaIso(pais.strip())
                #listaProcesada=listaProcesada+[verificaPais]
                listaProcesada.append(verificaPais)
            #return ",".join(listaProcesada)
            return listaProcesada

    # Recibe un diccionario, donde cada entrada tiene la forma: {idReg: pais}
    # Regresa un diccionario del mismo tipo pero con formato iso en alpha3
    def getIsoAlpha3WithDicc(self, diccionario):
        listaProcesada = dict()
        print("*******************************")
        for entry in diccionario:
            verificaPais = self.buscaIso(diccionario[entry].strip())
            #listaProcesada=listaProcesada+[verificaPais]
            listaProcesada[entry] = verificaPais
        return listaProcesada

    def buscaIso(self,dato):
        sin_tildes = self.elimina_tildes(dato)
        datoLower=sin_tildes.lower()
        #print("Se revisa: "+datoLower)
        for pais in self.listaPaises:
            nombrePaisSinAcentos=self.elimina_tildes(pais["name"])
            if pais["alpha3"].lower() == datoLower:
                #print("\tPais cumple ISO en BD")
                return pais["alpha3"].upper()
            elif nombrePaisSinAcentos.lower() == datoLower:
                #print("\tSe encontro nombre completo del pais. Corregido")
                return pais["alpha3"].upper()
            elif pais["alpha2"].lower() == datoLower:
                #print("\tSe encontro ISO alpha2: "+dato+" pasa a "+pais["alpha3"].upper()+"("+pais["name"]+")"+". Corregido")
                return pais["alpha3"].upper()
            elif datoLower == "uk" or datoLower == "ing" or datoLower == "inglaterra" or datoLower == self.elimina_tildes("gran bretaña") or datoLower == "reino unido":
                return "GBR"
            elif datoLower == "eua" or datoLower == "u.s.a" or  datoLower == "e.u.a" or datoLower == "u.s.a." or datoLower == "e.u.a.":
                return "USA"
            elif datoLower == "yug" or datoLower == "yugoslavia":
                return "YUG"    
            elif datoLower == "ale" or datoLower == "germania" or datoLower == "ddr":
                return "DEU"    
            elif datoLower == "" or datoLower == "desconocido":
                #print("Campo vacio")
                return "SD"
        #print("\tCorregir manual: "+ dato)
        return "Corregir manual: "+ dato

    def elimina_tildes(self,cadena):
        s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
        return s



        
    