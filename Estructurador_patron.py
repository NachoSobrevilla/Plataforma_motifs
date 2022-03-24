

import numpy as np, pandas as pd

class Estructurador(object):
    """Clase Estructurador, Tiene la finalidad de formar un motif en base de una matriz de conteo se que se pase"""
    def __init__(self, alineaciones = pd.DataFrame):
        self.alineaciones = alineaciones
                                # UNA BASE-------| DOS BASES-------------| TRES BASES----| CUATRO BASES | CERO BASES |
                                #-BASICOS(1)-----|----(2)----------------|------(3)------|-4-|-0-|
        self.lista_nucleotidos = ["A","C","G","T","W","S","M","K","R","Y","B","D","H","V","N","Z"] #lista de bases
        self.lista_complemento = ["T","G","C","A","W","S","K","M","Y","R","V","H","D","B","N","Z"] #Lista de completentos 
        self.lista_nucleotidos_basicos = ["A","C","G","T"]
        #Tabla de resetacion de las bases/simbolos
        self.tabla_representacion = np.array([
        #    A|C|G|T
            [1,0,0,0], #A
            [0,1,0,0], #C
            [0,0,1,0], #G
            [0,0,0,1], #T
            [1,0,0,1], #W
            [0,1,1,0], #S
            [1,1,0,0], #M
            [0,0,1,1], #K
            [1,0,1,0], #R
            [0,1,0,1], #Y
            [0,1,1,1], #B
            [1,0,1,1], #D
            [1,1,0,1], #H
            [1,1,1,0], #V
            [1,1,1,1], #N
            [0,0,0,0]  #Z
        ])
        #https://es.wikipedia.org/wiki/Secuencia_de_ADN
    def get_alineaciones(self):
        """Retorna las alineaciones"""
        return self.alineaciones
        
    def set_alineaciones(self, alineaciones=pd.DataFrame):
        """Ingreso de alineaciones"""
        self.alineaciones = alineaciones
    
    def get_letra_dict(self, x=""):
        pass
    
    def get_combinacion_letras(self, ltr = ""):
        pass
    
    def get_estructura(self):
        com = ""
        for i in range(len(self.alineaciones)):
            for j in range(len(self.tabla_representacion)):
                np_array_ali = self.alineaciones.iloc[i]>0
                if np.array_equal(np_array_ali,self.tabla_representacion[j]):
                    com += self.lista_nucleotidos[j]
                    break
        
        return com
            
        
        

