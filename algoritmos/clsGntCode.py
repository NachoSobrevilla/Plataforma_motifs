class clsGeneticCode:
    def __init__(self,codon):
        self.__codon=codon
        self.__alfabeto=["T","C","A","G"]
        self.__tabla1=[
                 [
                     ["Phe","Phe","Leu","Leu"]
                    ,["Ser","Ser","Ser","Ser"]
                    ,["Tyr","Tyr","END","END"]
                    ,["Cys","Cys","END","Trp"]
                ]
                ,[
                     ["Leu","Leu","Leu","Leu"]
                    ,["Pro","Pro","Pro","Pro"]
                    ,["His","His","Gln","Gln"]
                    ,["Arg","Arg","Arg","Arg"]
                ]
                ,[
                     ["Ile","Ile","Ile","Met"]
                    ,["Thr","Thr","Thr","Thr"]
                    ,["Asn","Asn","Lys","Lys"]
                    ,["Ser","Ser","Arg","Arg"]
                ]
                ,[
                     ["Val","Val","Val","Val"]
                    ,["Ala","Ala","Ala","Ala"]
                    ,["Asp","Asp","Glu","Glu"]
                    ,["Gly","Gly","Gly","Gly"]
                ]
            ]
        self.__tabla2=[
                 [
                     ["F","F","L","L"]
                    ,["S","S","S","S"]
                    ,["Y","Y","*","*"]
                    ,["C","C","*","W"]
                ]
                ,[
                     ["L","L","L","L"]
                    ,["P","P","P","P"]
                    ,["H","H","Q","Q"]
                    ,["R","R","R","R"]
                ]
                ,[
                     ["I","I","I","M"]
                    ,["T","T","T","T"]
                    ,["N","N","K","K"]
                    ,["S","S","R","R"]
                ]
                ,[
                     ["V","V","V","V"]
                    ,["A","A","A","A"]
                    ,["D","D","E","E"]
                    ,["G","G","G","G"]
                ]
            ]
    def getAlfabeto(self):
        return self.__alfabeto
    def getTabla1(self):
        return self.__tabla1

    def setCodon(self,codon):
        self.__codon=codon
    def getCodon(self):
        return self.__codon

    def getCodonCoded(self):
        ubicacion=[]
        for base in self.__codon:
            ubicacion.append(self.__alfabeto.index(base))

        return self.__tabla1[ubicacion[0]][ubicacion[1]][ubicacion[2]]

    def getCodonCodedMin(self):
        ubicacion=[]
        for base in self.__codon:
            ubicacion.append(self.__alfabeto.index(base))
        
        return self.__tabla2[ubicacion[0]][ubicacion[1]][ubicacion[2]]
            
if __name__ == '__main__':
    pass
        
