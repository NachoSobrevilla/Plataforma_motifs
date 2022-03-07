
from __future__ import with_statement
import json, os

from click import open_file
from more_itertools import last
from numpy import True_


class Alineador_multi(object):
    def __init__(self, secuencias = {}, tolerancia_delante = 0, tolerancia_atras = 0, json_patrones = ""):
        self.secuencias = secuencias
        self.tolerancia_delante = tolerancia_delante
        self.tolerancia_atras = tolerancia_atras
        self.json_patrones =  json_patrones
        self.alineamientos = []
    
    def clear(self):
        self.secuencias = ''
        self.tolerancia_atras = 0
        self.tolerancia_delante = 0
        self.json_patrones = ''
        self.alineamientos = []
              
    
    def muestra_resultados(self, alineamientos, posciones, patrones):
        muestras = ""
        muestras = f"Informacion\n Tolerancia hacia delante: {self.tolerancia_delante}\n Tolerancia hacia atras: {self.tolerancia_atras}\n\n"
        for i in range(len(alineamientos)):
        # for key, value in alineamientos.items():
            # for i in range(len(value)):notio
            muestra = ""
            x = ""
            muestra += patrones[i]+ str("-"*60) +"\n"
            
            if type(alineamientos[i]) != dict:
                for key, values in posciones[i].items():
                    for pos in values:
                        x += "posicion: " + str(pos) +"\t"+ "secuencia: "+ str(key)+ "\t\t "
                        if pos - 6 <= 0:
                            x += self.secuencias[key][0:pos] + " "
                        else:
                            x += self.secuencias[key][pos-6:pos] + " "
                        
                        x += alineamientos[i] + " "
                        
                        if pos+len(alineamientos[i])+7 <= len(self.secuencias[key]):
                            x += self.secuencias[key][pos+ len(alineamientos[i])+1 : pos+len(alineamientos[i])+7] + " "
                        else:
                            x += self.secuencias[key][pos + len(alineamientos[i])+1: len(self.secuencias[key])] + " "
                            
                        muestra += x + "\n"
                        x = ""
            
            
            else:
                # for j in range(len(alineamientos[i])):
                for key, values in (alineamientos[i].items()):
                    for j in range(len(values)):
                        x += "posicion: " + str(posciones[i][key][j]) + " secuencia: "+ str(key)+ "\t\t "
                        if posciones[i][key][j] - 6 <= 0:
                            x += " "*(10-posciones[i][key][j]) + \
                                self.secuencias[key][0:posciones[i][key][j]] + " "
                        else:
                            if posciones[i][key][j] < 10:
                                x += "\t " + \
                                    self.secuencias[key][posciones[i][key]
                                                         [j]-6:posciones[i][key][j]] + " "
                            else:
                                x += self.secuencias[key][posciones[i]
                                                          [key][j]-6:posciones[i][key][j]] + " "

                        x += alineamientos[i][key][j] + " "

                        if posciones[i][key][j]+len(alineamientos[i][key][j])+7 <= len(self.secuencias[key]):
                            x += self.secuencias[key][posciones[i][key][j] + len(
                                alineamientos[i][key][j])+1: posciones[i][key][j]+len(alineamientos[i][key][j])+7] + " "
                        else:
                            x += self.secuencias[key][posciones[i][key][j] +
                                                len(alineamientos[i][key][j])+1: len(self.secuencias[key])] + " "

                        muestra += x + "\n"
                        x = ""
            muestras += muestra+"\n"+("-"*30)+"\n\n"
            print(muestras)
            
        try:
            with open("alineador_multiple.txt",'x') as file_object:
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
    
    def alineador_multi(self):
        patrones = self.extraccion_json() # se extrae la informacion del archivo JSON
        alineamiento_retorno = [] #Para guardar todos los alineamientos encontrados
        list_posiciones = [] #Para guardar las posiciones en especifico
        list_patrones=[] #Para la lista de patrones
        
        for info_patron in patrones["Patrones"]:
            list_patrones.append(info_patron["Patron"]) #Agrega al patron
            ban = True #Ban restar la tolerancia
            ban_brk = True #Ban para quebrar el while cuando: algunas de las posiciones llega al limite o las torelancia abaco
            pos_delante = self.tolerancia_delante #tolerancia hacia delante
            pos_atras = self.tolerancia_atras #tolerancia hacia atras
            pre_ali = {} #Prealineamiento 
            rec_ali = {} #Record  de los alineamientos
            # posiciones = {p["sequencia"]: [p["posicion"]] if p["sequencia"] is posiciones else p["sequencia"].append(p["posicion"]) for p in info_patron["Posiciones"]}  # [p["posicion"]-1 for p in info_patron["Posiciones"]]
            posiciones = {p["sequencia"]: [pj["posicion"] for pj in info_patron["Posiciones"] if pj["sequencia"] == p["sequencia"]] for p in info_patron["Posiciones"]}  # [p["posicion"]-1 for p in info_patron["Posiciones"]] #Obtenermos las posiciones
            new_posiciones = {} #las nuevas posiciones con respeocto
            i=0 #i para indicar cuantos posiciones hacia delante se agregaran
            #PRIMER FASE: ADICIÓN DE LETRAS HACIA DELANTE DE LOS PATRONES
            while(pos_delante>0): #Busqueda hacia delante
                last_let=""  #ultima letra
                aux_let ="" #letra aux -> letra actual
                for pos in info_patron["Posiciones"]: #Va por cada posicion en especifico del patron {secuencia: "", posicion}
                    
                    if i+(pos["posicion"]-1)+len(info_patron["Patron"]) <= len(self.secuencias[pos["sequencia"]])-1: #si la posicion no sobrepasa a longitud de la secuencia 
                        if i==0: #Si el indicador es igual a cero
                            # pre_ali.append(info_patron["Patron"]+self.secuencias[(pos["posicion"]-1)+len(info_patron["Patron"])+i])
                            if pos["sequencia"] not in pre_ali : #Si no esta la key de la secuencia en los prealineamientos
                                if last_let: #Si existe algo en el last_let (ultima letra)
                                    aux_let = self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i] #Debe de tomar la ultima letra el aux
                                else:  #Si hay algo en en last_pre
                                    last_let = self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i] #last_let toma la ultima letra al ser la primera iteracion
                                
                                pre_ali[pos["sequencia"]] = [info_patron["Patron"]+self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i]] #Se añade la secuencia y el patron a pre_ali (prealineamiento)
                            else: #Si ya existe el patron dentro de pre_ali
                                pre_ali[pos["sequencia"]].append(info_patron["Patron"]+self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i]) #Agrega la poscion dentro de la lista correspondiente 
                                aux_let = self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i] #Toma la letra siguiente al patron o alineamiento
       
                        else: #Si el indicar no es igual a cero
                            if pos["sequencia"] in pre_ali: #Se verifica que el key/codigo de la secuencia este en pre_ali, En caso de que exista
                                #Se agrega el patron a el alineamiento a la lista correspondiente
                                pre_ali[pos["sequencia"]].append(info_patron["Patron"]+self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"]):(pos["posicion"]-1)+len(info_patron["Patron"])+i+1])
                                #Se toma la ultima leta para aux_let que le quiere agregar al patron desde la secuencia y poscion especifica
                                aux_let = self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(info_patron["Patron"])+i]
                                #Nota: La pos["posicion"] se le resta -1 porque es la que se muestra al usuario
                            else: #no esta el codigo de la secuencia en pre_ali
                                #Se añande la key y la lista de poscion con el primer elemento
                                pre_ali[pos["sequencia"]] = [info_patron["Patron"]+self.secuencias[pos["sequencia"]][( 
                                    pos["posicion"]-1)+len(info_patron["Patron"]):(pos["posicion"]-1)+len(info_patron["Patron"])+i+1]]
                                
                                if last_let: #si hay algo en last_let
                                    #Se toma la letra seguiente al patron/alineacion dentro de la secuencia especifico
                                    aux_let = self.secuencias[pos["sequencia"]][(
                                        pos["posicion"]-1)+len(info_patron["Patron"])+i]
                                else: #En caso que no tenga nada last_let
                                    #Se toma la letra seguiente al patron/alineacion dentro de la secuencia especifico
                                    last_let = self.secuencias[pos["sequencia"]][(
                                        pos["posicion"]-1)+len(info_patron["Patron"])+i]
                        
                        if aux_let != "": #Si  aux_let es diferente a nada
                            if last_let != aux_let: #Si aux_let y last_let son diferentes
                                ban = False #Se activa el ban, que indica que TODAS las letas que se agregan al patron no son iguales
                                #Ej
                                #Columna 1  Columna 2
                                #   A           C    
                                #   A           T    
                                #   A           G    
                                #   A           C    
                                #   A           A
                                #No se activa ban en la columna uno
                                #Se activa en la columna dos porque todas las letras no so iguales     
                            else: #En caso de que sean iguales
                                #remplaza lo que tenga last_let con aux_let
                                last_let = aux_let 
                                #se limpia aux_let
                                aux_let = ""
                                         
                        # if len(pre_ali)> 1:
                            # print(pre_ali.values())
                            # print(list(pre_ali.values())[0][0][-1])
                            # if list(pre_ali.values())[0][0][-1] != list(pre_ali.values()[-1][0][-1]):
                                # 
                    else: #Si sobre pasa la poscion del patron/alineacion la longitud de la secuencia
                        pos_delante = 0 #Las posiciciones hacia delante es igual a 0 (Ya no se añande nada)
                        ban = False #Ban es igual a False 
                        ban_brk = False #Ban_brk es igual a False, por ende, se rompe el while
                        break #Se romple el ciclo de las posiciones
                    
                  
                if ban_brk == False: 
                    break #Romple el ciclo while
                
                if ban == False:
                    ban = True
                    pos_delante -= 1
                
                #Si no hay anomalias
                i+=1 #Se suma i indicador de posiciones
                rec_ali.clear() #Se limpia rec_ali
                rec_ali = pre_ali.copy() #Se compia el contenido de pre_ali y se pasa rec_ali 
                pre_ali.clear() #Se limpia pre_ali
            
            #------------------------------------------------------------------------------------
            #SEGUNDA FASE: SE AGREGAN LETRAS HACIA ATRAS DE LOS PATRONES
            #----------------------------------------------------------------------------------
            if len(rec_ali) == len(posiciones): #Si la longitud de rec_ali es igual al de las posiciones
                i = 1 # indicador i igual a 1 (Ahora para recortar posiciones hacia atras)
                pre_ali = rec_ali.copy() # copiamos lo que tiene rec_ali a pre_ali. Cambiamos el rol, ahora rec_ali va ir ciclo por ciclo para recolectar los patrones y pre_ali los resguarda
                rec_ali.clear() # se limpia rec_ali 
                aux = {} #diccionario auxiliar -> aqui le pontran todas las alineacion resultantes de cada ciclo
                while(pos_atras>0): #Si la posicion hacia atras de mayor a 0
                    fst_let="" #Se limpia la primera letra
                    aux_let ="" #Se pondran todas las 
                    for key, pos in posiciones.items(): #se recorren cada key(codigo de la secuencia) y la lista posiciones
                        for k in range(len(pos)): #se recorre la lista en base a si index
                            if (pos[k]-i >= 0): #Si la posicion menos el indicador sea mayores a 0
                                if i==1: #si es igual a 0 
                                    
                                    if key not in rec_ali: #si la key de la secuencia esta em rec_ali
    
                                        if fst_let: # si fst_let tiene algo
                                            aux_let = self.secuencias[key][pos[k]-1]  #Se obtiene la letra anterior al patron
                                        else:   
                                            fst_let = self.secuencias[key][pos[k]-1] #Se obtiene la letra anterior al patron
                                        
                                        rec_ali[key] = [self.secuencias[key][pos[k]-1]+pre_ali[key][k]] #Se guarda la key de la secuencia y la posicion
                                    else: # si ya esta la key dentro de rec_ali
                                        rec_ali[key].append(self.secuencias[key][pos[k]-1]+pre_ali[key][k]) #se agrega a la lista dependiendo del codigo en espeficio
                                        
                                        aux_let = self.secuencias[key][pos[k]-1] #se obtiene la letra anterior al patron o alineamiento

                                    #*Actualizacion de posciones*    
                                    if key not in new_posiciones:#Si la key no esta dentro de las nuevas posiciones
                                        new_posiciones[key] = [pos[k]-1] #Se agrega la key y la lista con la primera posicion conocida
                                    else: #Si ya esta la key
                                        new_posiciones[key].append(pos[k]-1) # Se agrega la posicion con la key correspondiente
                                    

                                    # new_posiciones.append(posiciones[k]-1)
                                else:#Si es diferente a 0
                                    if key not in rec_ali:# si la key no esta dentor de rec_ali
                                        rec_ali[key] = [self.secuencias[key][pos[k]-i-1:pos[k]]+pre_ali[key][k]] ##Se guarda la key de la secuencia y la posicion actualizada
                                        
                                        if fst_let: #Si fst_let si tiene algo
                                            aux_let = self.secuencias[key][pos[k]-i-1] #aux_let se toma ultima letra insertada 
                                        else: #Si no tiene
                                            fst_let = self.secuencias[key][pos[k]-i-1] #fst_let toma la ultima letra insertada atras
                                    else: # si esta la key de la secuencia
                                        rec_ali[key].append(self.secuencias[key][pos[k]-i-1:pos[k]]+pre_ali[key][k])  #se agrega a la lista dependiendo del codigo en espeficio
                                        # aux_let se toma ultima letra insertada
                                        aux_let = self.secuencias[key][pos[k]-i-1]
                                    
                                    # Se agrega la posicion con la key correspondiente
                                    new_posiciones[key][k] = new_posiciones[key][k]-i-1
                                    
                                # if len(rec_ali) > 1:
                                #     if rec_ali[0][0] != rec_ali[-1][0]:
                                #         ban = False
                                # else: 
                                if aux_let != '': #Si  aux_let es diferente a nada
                                    if fst_let != aux_let: #Si aux_let y last_let son diferentes
                                        ban = False#Se activa el ban, que indica que TODAS las letas que se agregan al patron no son iguales
                                        #Ej
                                        #Columna 1  Columna 2
                                        #   A           C
                                        #   A           T
                                        #   A           G
                                        #   A           C
                                        #   A           A
                                        #No se activa ban en la columna uno
                                        #Se activa en la columna dos porque todas las letras no so iguales
                                    else:  # En caso de que sean iguales
                                        #remplaza lo que tenga last_let con aux_let
                                        last_let = aux_let
                                        #se limpia aux_let
                                        aux_let = ""
                                
                                
                                # else:
                                    
                                #     aux_let = ""    
                                
                            else: #Si el indicador es menor 0
                                pos_atras = -1 #pos_atras menos
                                ban = False #booleano para romper el ciclo for interno
                                ban_brk = False #booleano para rompper el ciclo while
                                break #
                    
                    if ban_brk == False: #si ban_brk es falso
                        break   #break al while funcional
                    
                    if ban == False: # si ban es False
                        ban = True 
                        pos_atras -= 1 #pos_atras menos unos

                    aux.clear() # limpia el auxiliar
                    aux = rec_ali.copy() #aux guarda lo que tenga rec_ali
                    rec_ali.clear() #limpia lo que tenga rec_ali
                    
                    i+=1  #aumenta mas uno el indicardor

                if len(aux) == len(pre_ali): #Si las longitudes de las alienaciones de enfrente son iguales a las de atras 
                    print(aux.copy()) #imprime lo que tienes de las alienaciones completas
                    alineamiento_retorno.append(aux.copy()) #Agregalo a la lista grande
                    
                else: #sino
                    print(pre_ali.copy()) #imprime lo resultante de enfrente
                    alineamiento_retorno.append(pre_ali.copy()) #copialo a la lista grande
                
                if len(new_posiciones) == len(posiciones): #si las longitudes de las posiciones son iguales
                    #se agrega la que tiene las posiones que retrocediron
                    print(new_posiciones.copy()) 
                    list_posiciones.append(new_posiciones.copy())
                else:#sino
                    #quedate con las posiciones originales
                    print(posiciones)
                    list_posiciones.append(posiciones)        
            else:  # Si la longitud de rec_ali no fue igual de las posiciones
                #Se toma el patron tal cual junto con las posiciones actuales
                alineamiento_retorno.append(info_patron["Patron"])
                list_posiciones.append(posiciones)
            
            
            pre_ali.clear()
            rec_ali.clear()
            
        self.muestra_resultados(alineamiento_retorno,
                                list_posiciones, list_patrones)
            #           p  
                # pre_ali = [ptr+self.secuencias[p+len(ptr)] if (p+len(ptr)<=len(self.secuencias)-1) else ban=False for ptr in pre_ali for p in posiciones ]
        
if __name__ == '__main__':
    # x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud diferente\\"
    x = "C:\\Users\\sobre\\Desktop\\"
    y = {"000000": "ACGTGTAAAACTCTTGTT",
         "000001": "CTAAGTCCGTAGCCGACT", 
         "000002": "GGATCCAATCGCTAATCG"}
    z = "exp-000000-000001-000002_14_12_2021_0_21_33.json"
    align = Alineador_multi(secuencias=y, tolerancia_atras=2, tolerancia_delante=2, json_patrones= os.path.join(x, z))
    align.alineador_multi()
