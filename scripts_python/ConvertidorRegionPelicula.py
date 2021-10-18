class ConvertidorRegionPelicula:
    def getRegion(self, row):
        entrada= row.strip()
        if entrada == "NTSC" or entrada == "WS" or entrada =="2 min" or entrada == "":
            return "SD"
        elif len(entrada) == 1:
            return entrada
        else:
            
            porComas = entrada.split(",")
            if len(porComas) == 1:
                porEspacios = entrada.split()    
                return ",".join(porEspacios)
            else:
                resultado = map(lambda item: item.strip(),porComas)
                porComas= list(resultado)
                return ",".join(porComas)
                
            
