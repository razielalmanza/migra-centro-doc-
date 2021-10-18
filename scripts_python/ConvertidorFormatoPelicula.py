import unicodedata

class ConvertidorFormatoPelicula:
    
    def getFormato(self,formatoDB):
        cadena=formatoDB.upper()
        if cadena == "VHS" or cadena == "BETA/VHS" or cadena == "VHS/BETA" or cadena == "VHAS" or cadena == "VHS€" or cadena=="VHYS":
            return "VHS"
        elif cadena == "BETA" or cadena == "VHD" or cadena == "CD" or cadena == "16"  or cadena == "VCD" or cadena == "LASER DISC":
            return cadena
        elif cadena == "DVD" or cadena == "DVDF" or cadena == "DVD.13029/2018" or cadena == "DVDQ":
            return "DVD"
        elif cadena == "35" or cadena =="35MM":
            return "35"
        elif cadena == "BLUE RAY" or cadena == "BLU RAY":
            return "BLU-RAY"
        elif cadena == "" or cadena == "Pelicula":
            return "SD"
        else:
            return "E: Formato Pelicula"
        
         