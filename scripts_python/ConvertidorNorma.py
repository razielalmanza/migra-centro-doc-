class ConvertidorNorma: 
    def getNorma(self, entrada):
        row = entrada.strip().upper()
        if row == "JNTSC" or row == "NTSV" or row == "MTSC" or row == "SNTC" or row == "NSTC" or row == "NTCS":
            return "NTSC"
        if row == "":
            return "SD"#"ErrorSD (temporal)"    
        elif row[0] == "N" and len(row) >= 4:
            if row[:4] == "NTSC":
                return "NTSC"
        elif row[0] == "P" and len(row) >= 3:
            if row[:3] == "PAL":
                return "PAL"
        return "SD"#"ErrorSD (temporal)"