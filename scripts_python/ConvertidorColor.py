import json
import unicodedata

class ConvertidorColor:
    def __init__(self,separador):
        self.separador=separador
    
    def getColor(self,cadenaOriginal):
        lista=cadenaOriginal.split(self.separador)
        listaProcesada=[]
        #print("*******************************")
        #print(lista)
        for color in lista:
            verificaColor=self.convierte(color.strip())
            listaProcesada=listaProcesada+verificaColor
        return ",".join(listaProcesada)

    def convierte(self,color):

        dato= color.upper()
        if dato == "C" or dato == "COLOR" or dato == "COL" or dato == "SI" or dato == "COLO":
            return ["C"]
        elif dato == "B/N" or dato =="BLANCO Y NEGRO" or dato =="BYN" or dato == "BN" or dato == "BLANCO Y NEGRO":
            return ["BN"]
        elif dato == "B/N Y COLOR" or dato == "BN C" or dato == "C BN" or dato== "C/BN" or dato == "BLANCO Y NEGRO COLOR":
            return ["BN","C"]
        elif dato=="T" or dato == "ENTINTADO":
            return ["T"]
        elif dato == "BN T":
            return ["BN", "T"]
        elif dato == "NO APLICA"  or dato == "":
            return ["NA"]
        return ["Corregir:" + dato]
       
        

        