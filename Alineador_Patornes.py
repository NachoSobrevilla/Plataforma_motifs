
from __future__ import with_statement
import json, os

from click import open_file


class Alineador(object):
    def __init__(self, secuencia = '', tolerancia_delante = 0, tolerancia_atras = 0, json_patrones = ""):
        self.secuencia = secuencia
        self.tolerancia_delante = tolerancia_delante
        self.tolerancia_atras = tolerancia_atras
        self.json_patrones =  json_patrones
        self.alineamientos = []
    
    def clear(self):
        self.secuencia = ''
        self.tolerancia_atras = 0
        self.tolerancia_delante = 0
        self.json_patrones = ''
        self.alineamientos = []
              
    
    def muestra_resultados(self, alineamientos, posciones, patrones):
        """Esta funcion muestra los resultados obtendios por el alineamento
        y lo guarda en un archivo TXT por el momento"""
        muestras = ""
        muestras = f"Informacion\n Tolerancia hacia delante: {self.tolerancia_delante}\n Tolerancia hacia atras: {self.tolerancia_atras}\n\n"
        for i in range(len(alineamientos)):
            muestra = ""
            x = ""
            muestra += patrones[i]+ str("-"*30) +"\n"
            
            if len(alineamientos[i]) == 1:
                for pos in posciones[i]:
                    x += "posicion: " + str(pos) + "\t\t "
                    if pos - 6 <= 0:
                        x += self.secuencia[0:pos] + " "
                    else:
                        x += self.secuencia[pos-6:pos] + " "
                    
                    x += alineamientos[i] + " "
                    
                    if pos+len(alineamientos[i][0])+7 <= len(self.secuencia) :
                        x += self.secuencia[pos + len(alineamientos[i][0])+1 : pos+len(alineamientos[i][0])+7] + " "
                    else:
                        x += self.secuencia[pos +
                                            len(alineamientos[i][0])+1: len(self.secuencia)] + " "

                    muestra += x + "\n"
                    x = ""
            
            else:
                for j in range(len(alineamientos[i])):
                    x += "posicion: " + str(posciones[i][j]) + "\t\t "
                    if posciones[i][j] - 6 <= 0:
                        x += " "*(10-posciones[i][j]) + \
                            self.secuencia[0:posciones[i][j]] + " "
                    else:
                        if posciones[i][j] <10:  
                            x +="\t "+ self.secuencia[posciones[i][j]-6:posciones[i][j]] + " "
                        else:
                            x += self.secuencia[posciones[i][j]-6:posciones[i][j]] + " "

                    x += alineamientos[i][j] + " "

                    if posciones[i][j]+len(alineamientos[i][j])+7 <= len(self.secuencia):
                        x += self.secuencia[posciones[i][j] + len(alineamientos[i][j])+1: posciones[i][j]+len(
                            alineamientos[i][j])+7] + " "
                    else:
                        x += self.secuencia[posciones[i][j] +
                                            len(alineamientos[i][j])+1: len(self.secuencia)] + " "

                    muestra += x + "\n"
                    x = ""
            muestras += muestra+"\n"+("-"*30)+"\n\n"
            print(muestras)
            
        try:
            with open("alineador2.txt",'x') as file_object:
                file_object.write(muestras)
                
        except Exception as e:
            print(str(e))
            
            
                    
    def extraccion_json(self):
        try:
            with open(self.json_patrones, 'r') as jsonpatrones:
                x = json.load(jsonpatrones)
                return x
        except Exception as e:
            print("Error en el Archivo: " + str(e))
    
    
    def creciente_frente(self,patron_original, lista_posiciones):
        """Funcion para calcular las posibles mutaciones que pueda tener el patron frecuente a motif """
        ban = True  # Boolano para indicar y la columna es homogenia o no
        ban_brk = True  # Booleano para indicar si hay que romper el while
        pre_ali = [] # Captura al principio las primeras alineaciones hacia delante (posiciones)
        rec_ali = []  # guarda las posciones de pre ali (record)
        pos_delante = self.tolerancia_delante
        
        while(pos_delante > 0):  # Busqueda hacia delante
              # Se pone el patron dentro de la variable
            patron = patron_original

            for p in lista_posiciones:  # por cada posicion
                # si la longitud del patron es menor a 6 y la posicion mas 6 no arrebasa la longitud de la secuencia
                if len(patron) < 6 and p+6 < len(self.secuencia)-1:
                    # Se le agregan otras seis posiciones
                    patron = self.secuencia[p:p+6]
                elif p+6 < len(self.secuencia)-1:
                    pos_delante = 0
                    ban = False
                    ban_brk = False

                # Si lo que vamos a buscar despues del patron no sobrepasa a la longitud de la secuencia
                if i+p+len(patron) <= len(self.secuencia)-1:
                    if i == 0:  # Si i es igual a cero
                        # Se añade a la lista preliminar (pre_ali) el patron mas el nucleotido que este enfrente
                        pre_ali.append(
                            patron+self.secuencia[p+len(patron)+i])
                        #patron = patron+self.secuencia[p+len(patron)+i]
                    else:  # si no
                        # Se añade a la lista preliminar (pre_ali) el patron con tolerancia mas el nucleotido que este enfrente
                        pre_ali.append(
                            patron+self.secuencia[p+len(patron):p+len(patron)+i+1])
                        # patron = patron + self.secuencia[p+len(patron):p+len(patron)+i+1]
                    if len(pre_ali) > 1:
                        # Asumiendo de que TODOS los patrones se les añade el "mismo" nucleotido, solo se comparan dos, el ultimo elementos del primer patron vs el ultimo elemento del ultimo patron
                        if pre_ali[0][-1] != pre_ali[-1][-1]:
                            ban = False
                else:  # Si se supera la posicion se rompe SOLO EL FOR
                    pos_delante = 0
                    ban = False
                    ban_brk = False
                    break

                patron = patron_original

            if ban_brk == False:  # break para romper el WHILE
                break

            if ban == False:  # break para romper
                ban = True
                pos_delante -= 1

            i += 1
            rec_ali.clear()
            # A medida que crecen los patrones en el alineamiento se tienen que guardar en la lista rec_ali
            rec_ali = pre_ali[:]
            pre_ali.clear()
        
        return rec_ali
        #fin de la funcion
    
    def creciente_atras(self,patron, lista_posiciones):
        pass
    
    def alineador(self):
        patrones = self.extraccion_json()
        alineamiento_retorno = []
        list_posiciones = []
        list_patrones=[]
        
        for info_patron in patrones["Patrones"]:
            list_patrones.append(info_patron["Patron"])
            ban = True #Boolano para indicar y la columna es homogenia o no
            ban_brk = True #Booleano para indicar si hay que romper el while
            pos_delante = self.tolerancia_delante
            pos_atras = self.tolerancia_atras
            pre_ali = [] #Captura al principio las primeras alineaciones hacia delante (posiciones)
            rec_ali = [] #guarda las posciones de pre ali  
            posiciones = [p["posicion"]-1 for p in info_patron["Posiciones"]] #lista para recuperar todas las posiciones (posiciones -1)
            new_posiciones = []
            i=0 # contador
            
            
            
            while(pos_delante>0): #Busqueda hacia delante
                patron = info_patron["Patron"] #Se pone el patron dentro de la variable
                
                for p in posiciones: #por cada posicion
                    if len(patron) < 6 and p+6 < len(self.secuencia)-1: #si la longitud del patron es menor a 6 y la posicion mas 6 no arrebasa la longitud de la secuencia
                        patron = self.secuencia[p:p+6] #Se le agregan otras seis posiciones
                    elif p+6 < len(self.secuencia)-1:
                        pos_delante = 0
                        ban = False
                        ban_brk = False
                    
                        
                                            
                    if i+p+len(patron) <= len(self.secuencia)-1: #Si lo que vamos a buscar despues del patron no sobrepasa a la longitud de la secuencia
                        if i==0: #Si i es igual a cero
                            pre_ali.append(patron+self.secuencia[p+len(patron)+i]) #Se añade a la lista preliminar (pre_ali) el patron mas el nucleotido que este enfrente
                            #patron = patron+self.secuencia[p+len(patron)+i]
                        else: #si no
                            pre_ali.append(patron+self.secuencia[p+len(patron):p+len(patron)+i+1])  # Se añade a la lista preliminar (pre_ali) el patron con tolerancia mas el nucleotido que este enfrente
                            # patron = patron + self.secuencia[p+len(patron):p+len(patron)+i+1]
                        if len(pre_ali)> 1:
                            if pre_ali[0][-1] != pre_ali[-1][-1]: # Asumiendo de que TODOS los patrones se les añade el "mismo" nucleotido, solo se comparan dos, el ultimo elementos del primer patron vs el ultimo elemento del ultimo patron
                                ban = False
                    else: #Si se supera la posicion se rompe SOLO EL FOR 
                        pos_delante = 0
                        ban = False
                        ban_brk = False
                        break
                    
                    
                    patron = info_patron["Patron"]
                  
                if ban_brk == False: #break para romper el WHILE
                    break
                
                if ban == False: #break para romper 
                    ban = True
                    pos_delante -= 1
                
                i+= 1        
                rec_ali.clear()
                rec_ali = pre_ali[:] #A medida que crecen los patrones en el alineamiento se tienen que guardar en la lista rec_ali
                pre_ali.clear()
            
            if len(rec_ali) == len(posiciones): #Se asume que la longitud de un 
                i = 0 
                pre_ali = rec_ali[:] 
                rec_ali.clear()
                aux = []
                while(pos_atras>0):
                    for k in range(len(posiciones)):
                        if (posiciones[k]-i > 0):
                            if i==0:
                                rec_ali.append(self.secuencia[posiciones[k]-1]+pre_ali[k])
                                new_posiciones.append(posiciones[k]-1)
                            else:
                                rec_ali.append(
                                    self.secuencia[posiciones[k]-i-1:posiciones[k]]+pre_ali[k])
                                new_posiciones[k] = new_posiciones[k]-i-1
                                
                            if len(rec_ali) > 1:
                                if rec_ali[0][0] != rec_ali[-1][0]:
                                    ban = False
                        
                        else:
                            pos_atras = -1
                            ban = False
                            ban_brk = False
                            break
                    
                    if ban_brk == False:
                        break
                    
                    if ban == False:
                        ban = True
                        pos_atras -= 1

                    aux.clear()
                    aux = rec_ali[:]
                    rec_ali.clear()
                    
                    i+=1

                if len(aux) == len(pre_ali):
                    alineamiento_retorno.append(aux[:])
                    
                else:
                    alineamiento_retorno.append(pre_ali[:])
                
                if len(new_posiciones) == len(posiciones):
                    list_posiciones.append(new_posiciones)
                else:
                    list_posiciones.append(posiciones)        
            else:
                alineamiento_retorno.append(patron)
                list_posiciones.append(posiciones)
            
            
            pre_ali.clear()
            rec_ali.clear()
            
        self.muestra_resultados(alineamiento_retorno,
                                list_posiciones, list_patrones)
            #           p  
                # pre_ali = [ptr+self.secuencia[p+len(ptr)] if (p+len(ptr)<=len(self.secuencia)-1) else ban=False for ptr in pre_ali for p in posiciones ]
        
if __name__ == '__main__':
    x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud diferente\\"
    y = "GCTTCACATGCCGCTGTGANACAGTGGTTTCGTGTGAGGGCTACGTCGTTAAGAGAATAACGATGAGCCCAGGCCTTTATGGAAAAACCACAGGGTATGCGGTAACCCACCACGCAGA"
    z = "sequence_HL714398-BI-test-2022-02-05_21h47m23s927286ms.json"
    align = Alineador(secuencia=y, tolerancia_atras=1, tolerancia_delante=1, json_patrones= os.path.join(x, z))
    align.alineador()
