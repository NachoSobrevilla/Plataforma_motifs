from glob import glob
import json, os, re, datetime, xlsxwriter, json
from graficador import Graficador
from os.path import join, dirname, realpath
from tqdm import tqdm

EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')
#Notas
# se incluiran las alineaciones que no tengan motifs?
# se podran configurar el crecimiento para alcanzar cierta longitud? actual es de 6 
# se podran configurar las tolerancias? actual de dos por lado 
class Alineador(object):
    def __init__(self, secuencia = '', tolerancia_delante = 0, tolerancia_atras = 0, json_patrones = ""):
        self.secuencia = secuencia
        self.tolerancia_delante = tolerancia_delante
        self.tolerancia_atras = tolerancia_atras
        self.json_patrones =  json_patrones
        self.alineamientos = []
        self.motifs = []
    
    def clear(self):
        self.secuencia = ''
        self.tolerancia_atras = 0
        self.tolerancia_delante = 0
        self.json_patrones = ''
        self.alineamientos = []
    
    def get_json_patrones(self):
        if type(self.json_patrones) == str:
            return self.extraccion_json()
        else:
            return self.json_patrones
    
    def muestra_resultados_txt(self, alineamientos, posciones, patrones):
    
    
        """Esta funcion muestra los resultados obtendios por el alineamento
        y lo guarda en un archivo TXT por el momento"""
        muestras = ""
        muestras = f"Informacion\n Tolerancia hacia delante: {self.tolerancia_delante}\n Tolerancia hacia atras: {self.tolerancia_atras}\n\n"
        for i in tqdm(range(len(alineamientos))):
            pd_conteos, motif = self.obtener_motif(alineamientos[i])
            
            
            
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

                    x += str(alineamientos[i][j]) + " "

                    if posciones[i][j]+len(alineamientos[i][j])+7 <= len(self.secuencia):
                        x += self.secuencia[posciones[i][j] + len(alineamientos[i][j])+1: posciones[i][j]+len(
                            alineamientos[i][j])+7] + " "
                    else:
                        x += self.secuencia[posciones[i][j] +
                                            len(alineamientos[i][j])+1: len(self.secuencia)] + " "

                    muestra += x + "\n"
                    x = ""
           
            
            muestras += muestra+"\n"+("-"*30)+"\n\n" 
            muestras += "motif obtenido: \t"+motif+"\n\n"
            muestras += str(pd_conteos) + "\n\n\n\n"
            # print(muestras)
            
        try:
            with open("alineador3.txt",'x') as file_object:
                file_object.write(muestras)
                
        except Exception as e:
            print(str(e))
            
    def muestra_resultados_json(self, alineamientos =[], posiciones_align=[], patrones=[]):
        dict_json ={}
        list_info =[]
        for i in range(len(patrones)):
            pd_conteos, motif = self.obtener_motif(
                alineamientos[i], patrones[i])
            if motif != "":
                list_info.append({
                    "patron":patrones[i],
                    "alineamientos": [{"alineamiento": alineamiento,
                                    "posicion": posicion }  
                                    for alineamiento, posicion in zip(alineamientos[i], posiciones_align[i])],
                    "matriz_conteo": json.loads(pd_conteos.to_json(orient="index")) ,
                    "motif": motif           
                })

        dict_json["Alineaciones"] = list_info
        dict_json["Num_alineaciones"] = len(list_info)
        # print(dict_json)
        return dict_json
        
    def generador_archivos(self, motifs_json ,**kargs):
        
        def archivo_excel(excel_write=xlsxwriter.Workbook()):
            items = 0
            #La intencion de ponerlo en un while es para evitar que toda la informacion se ponga en una sola hoja,
            #para eso se recorrera por partes la lista se fuese necesario, el limite por el momento es 100000 filas
            #y se repartira la infromacion en en diferentes
            #Y se utiliza xlsx para insertar las graficas obtenidas
            while True: #mientras se verdadero
                paper = excel_writer.add_worksheet() #Se agreaga una nueva hoja de calculo
                #posiciones para escribir en la hora
                row = 0 
                col = 0
                #addciones a las posiciones
                i = 0
                j = 0
                list_info_motifs = motifs_json['Alineaciones'] #Se toma la lista de alineaciones
                for itm in tqdm(range(items, len(list_info_motifs))): #Recorremos la lista desde donde se quedo o en 0 hasta la longitud de la lista 
                    filenamepng = os.path.join(EXP_FOLDER, "motifs_png", ( list_info_motifs[itm]["patron"]+".png") ) #Se toma la imagen del motif actual
                    #Escribe el primero el patron
                    j += 1 
                    paper.write(row, col, "Patron")
                    paper.write(row, col+j, list_info_motifs[itm]["patron"])
                    #Despues el alineamiento: posicion y secuencia de se alineo
                    i += 2
                    paper.write(row+i, col+j, "Alineamiento")
                    i += 1
                    paper.write(row+i, col+j, "posicion")
                    paper.write(row+i, col+j+1, "alineamiento")
                    #ciclo while para escribir las secuencias que se estan alineando 
                    for pos in list_info_motifs[itm]["alineamientos"]:
                        i += 1
                        paper.write(row+i, col+j, str(pos["posicion"]))
                        paper.write(row+i, col+j+1, str(pos["alineamiento"]))

                    #recolocacion de posciones
                    i = 2
                    j = 5
                    #Se escribe la matriz de conteo 
                    matriz_conteo = list_info_motifs[itm]["matriz_conteo"]#Se toma la lista de diccionarios, donde las llaves principales son el numero de fila y los items son diccionarios con la llave de nucleotido y el valor es la frecuencia del nucleotido
                    #Se escribe la cabecera
                    paper.write(row+i, col+j, "Matriz de conteo")
                    i += 1
                    paper.write(row+i, col+j, "Posición")
                    paper.write(row+i, col+j+1, "A")
                    paper.write(row+i, col+j+2, "C")
                    paper.write(row+i, col+j+3, "T")
                    paper.write(row+i, col+j+4, "G")
                    #Ciclo para escribir los valores de la matriz
                    for k in range(len(matriz_conteo)):
                        i += 1
                        paper.write(row+i, col+j, str(k))
                        for key, value in matriz_conteo[str(k)].items():#Cada valor se escribe en la posicion que le corresponda
                            if key == "A":
                                paper.write(row+i, col+j+1, value)
                            elif key == "C":
                                paper.write(row+i, col+j+2, value)
                            elif key == "T":
                                paper.write(row+i, col+j+3, value)
                            elif key == "G":
                                paper.write(row+i, col+j+4, value)
                        

                    
                    j = 14 #se recorren hasta la columna 14
                    #se inserta la imagen al 50% de si proporcion 
                    paper.insert_image(row+2, col+j, filenamepng, {'x_scale': 0.5, 'y_scale': 0.5})
                    #por ultimo se escribe el motif
                    paper.write(row+i+2, col, "motif")
                    paper.write(row+i+2, col+1, list_info_motifs[itm]["motif"])
                    if itm == len(motifs_json['Alineaciones'])-1:
                        paper.write(row+i+3, col, "Numero de alineaciones")
                        paper.write(row+i+3, col+1,
                                    motifs_json["Num_alineaciones"])
                    #se suma la longitud de la matriz de conteo mas 10 para escribir los nuevos datos
                    row += len(matriz_conteo) + 10
                    col = 0
                    i = 0
                    j = 0
                    #items es el contador principal dentro del while, por ese motivo se le asigna itm 
                    items = itm
                    #Se sobrepasa las 100000 filas se rompe el ciclo for 
                    if row > 100000: #1000000 :
                        break
                #Si items llega  al longitud de los motifs menos uno, entonces se rompe el ciclo while 
                if items == len(motifs_json['Alineaciones'])-1:
                    break

            excel_writer.close()
            
        #Formacion del nombre del archivo, tal como lo hace el server    
        x=""
        x += "EXP_"+str(kargs['Siglas']) + '_' +\
               str(kargs['Min_sup']) + '_' + \
               str(kargs['Tipo_Entrada']) + '_' + \
               str(kargs['Entrada']).split(".fasta")[0] + '_' + \
               str(kargs['Num_Sequencias_ananlizadas']) + '_' + \
               str(kargs['Num_Patrones_hallados']) + '_'

        dt = datetime.datetime.strptime(kargs['Fecha_Hora_Inicio'], '%Y-%m-%d %H:%M:%S.%f')

        x += str(dt.day)+"d"+str(dt.month)+"d"+str(dt.year)+"&" + \
            str(dt.hour)+"-"+str(dt.minute)+"-"+str(dt.second)+"_"

        sdt = str(kargs['Duracion'])
        x1 = [i for i in re.split("[ ,:.]", sdt) if i.isdigit() or i.isdecimal()]

        if len(x1) < 5:
            x1.insert(0, '0')
            x1.append('0')

        seconds = (int(x1[0])*86400) + (int(x1[1])*3600) + \
            (int(x1[2])*60) + int(x1[3])
        # print(sdt, ' ', x1[4])
        x += 'D-'+str(seconds)+'&'+x1[4]

        #se asigna la ruta completa tanto para el nombre del archivo json y xlsx
        filename = os.path.join(EXP_FOLDER, "motifs_json", x)
        filenamexlsx = os.path.join(EXP_FOLDER, "motifs_excel", x)
        
        files_dir_png = os.path.join(EXP_FOLDER, "motifs_png","*.png")
        
        
        try:
            if os.path.isfile(filename+(".json")):
                with open(filename+(".json"), 'w') as file_object_json:
                    json.dump(motifs_json, file_object_json, sort_keys = True, indent = 4)
            else:
                with open(filename+(".json"),'x') as file_object_json:
                    json.dump(motifs_json, file_object_json, sort_keys = True, indent = 4)
            
            if os.path.isfile(filenamexlsx+'.xlsx'):
                with xlsxwriter.Workbook(filenamexlsx+'.xlsx') as excel_writer:
                    archivo_excel(excel_writer)
            else:
                with xlsxwriter.Workbook(filenamexlsx+'.xlsx') as excel_writer:
                    archivo_excel(excel_writer)
            
            #remoción de los archivos png (LOGOS) generados 
            files_png = glob(files_dir_png)
            for f in files_png:
                os.remove(f)
            
        except IOError as e:
            print(f'Hubo un error en la escritura del archivo \n'+str(e))
            
        # except FileNotFoundError as fn:
        #     print(f'Hubo un error en el archivo: No se encontro o no existe. \n'+str(fn))
        
        # except FileExistsError as fe:
        #     print (f'Hubo un error en el archivo: '+str(fe)+'\n')
        
        else:
            print("Success!, file created")
    
    
    def obtener_motif(self,alineamiento = [""], patron=""):
        g = Graficador(alineamiento)
        
        pd_conteos, motif = g.ploteo_logo_seq_align(g.get_list_align_plt(), patron) 
        return pd_conteos, motif      
    
                    
    def extraccion_json(self):
        try:
            with open(self.json_patrones, 'r') as jsonpatrones:
                x = json.load(jsonpatrones)
                return x
        except Exception as e:
            print("Error en el Archivo: " + str(e))
    
    
    
    def adiccion_frente_patron(self, patron_original = "", lista_posiciones = []):
        """Funcion para calcular las posibles mutaciones que pueda tener el patron frecuente a motif """
        ban = True  # Boolano para indicar y la columna es homogenia o no
        ban_brk = True  # Booleano para indicar si hay que romper el while
        brk_menor_seis = True #Booleano para indicar que si el patron no cumple con una poscion menor a la longitud de la secuencia
        pre_ali = [] # Captura al principio las primeras alineaciones hacia delante (posiciones)
        rec_ali = []  # guarda las posciones de pre ali (record)
        pos_delante = self.tolerancia_delante
        i = 0
        while(pos_delante > 0):  # Busqueda hacia delante
              # Se pone el patron dentro de la variable
            patron_evaluar = patron_original

            for p in lista_posiciones:  # por cada posicion
                # si la longitud del patron es menor a 6 y la posicion mas 6 no arrebasa la longitud de la secuencia
                if len(patron_evaluar) < 6 and p+6 < len(self.secuencia)-1:
                    # Se le agregan otras seis posiciones
                    patron_evaluar = self.secuencia[p:p+6]
                elif p+6 >= len(self.secuencia)-1 and len(patron_evaluar) < 6: # si la longitud es menor a  6 pero la(s) posiciones 
                    pos_delante = 0
                    ban = False
                    brk_menor_seis = False
                    break

                # Si lo que vamos a buscar despues del patron no sobrepasa a la longitud de la secuencia
                if i+p+len(patron_evaluar) <= len(self.secuencia)-1:
                    if i == 0:  # Si i es igual a cero
                        # Se añade a la lista preliminar (pre_ali) el patron mas el nucleotido que este enfrente
                        pre_ali.append(
                            patron_evaluar+self.secuencia[p+len(patron_evaluar)+i])
                        #patron = patron+self.secuencia[p+len(patron)+i]
                    else:  # si no
                        # Se añade a la lista preliminar (pre_ali) el patron con tolerancia mas el nucleotido que este enfrente
                        pre_ali.append(
                            patron_evaluar+self.secuencia[p+len(patron_evaluar):p+len(patron_evaluar)+i+1])
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

                patron_evaluar = patron_original

            if ban_brk == False:  # break para romper el WHILE
                if len(rec_ali) == 0: # En caso de que rec_ali no tenga nada que retornar
                    rec_ali = [patron_evaluar for i in range(
                        len(lista_posiciones))]
                break

            if ban == False:  # break para romper
                ban = True
                pos_delante -= 1
            
            if brk_menor_seis == False:
                rec_ali=[patron_evaluar for i in range(len(lista_posiciones))]
                break

            i += 1
            rec_ali.clear()
            # A medida que crecen los patrones en el alineamiento se tienen que guardar en la lista rec_ali
            rec_ali = pre_ali[:]
            pre_ali.clear()
        
        return rec_ali
        #fin de la funcion
    
    def adiccion_atras_patron(self, lista_alineaciones = [], lista_posiciones = []):
        i = 1
        ban = True  # Boolano para indicar y la columna es homogenia o no
        ban_brk = True  # Booleano para indicar si hay que romper el while
        brk_menor_seis = True #Booleano para indicar que si el patron no cumple con una poscion menor a la longitud de la secuencia
        pre_ali = lista_alineaciones #Se reciben nuevas posiciones
        new_posiciones = [] #listas de nuevas posiciones
        rec_ali =[] #record ieterativo de los alineamientos
        aux = [] #record final de los alineamientos
        pos_atras= self.tolerancia_atras
        
        while(pos_atras > 0): 
            for k in range(len(lista_posiciones)): #se recore la lista de posiciones
                alineamiento = pre_ali[k] # se toma el patron alineado compuesto
                pos_align = lista_posiciones[k] # se toma la posicion actual
                # Si es menor a 6, se le acompletara con las letras detras del patron hasta llegar a 6
                if pos_align-(6-len(alineamiento)) > 0 and len(alineamiento) < 6:
                    pos_align = pos_align-(6-len(alineamiento))
                    alineamiento = self.secuencia[pos_align:lista_posiciones[k]] + str(alineamiento)
                
                #Si la posicion menos las pociones hacia atras que necesite el patron/secuencia alineada para llegar a una longitud de 6 y si el mismo patron/secuencia es menor a seis
                elif pos_align-(6-len(alineamiento)) <= 0 and len(alineamiento) < 6:
                    #Se rompe el ciclo
                    pos_atras = 0
                    brk_menor_seis = False
                    break 
                     
                if (pos_align-i >= 0):
                    if i==1: # si la posicion esta dentro de la lista de new_posiciones
                        #Se les añade a los alineamientos la letra anterior y se recorre al posicion a -1
                        rec_ali.append(
                            self.secuencia[pos_align-i]+str(alineamiento))
                        new_posiciones.append(pos_align-1)
                    
                    else: 
                        #se añaden las letras anteriores corespondientes detras de patron 
                        rec_ali.append(self.secuencia[pos_align-i:pos_align]+str(alineamiento))
                        #Se actualiza la posicion
                        new_posiciones[k] = new_posiciones[k]-1 
                        
                    #Se verifica la longitud de rec_ali y si es mayor a 1
                    if len(rec_ali) > 1:
                        #Si primer elemento de rec_ali tiene la primera letra diferente a la primera letra del ultimo elemento añadido de rec_ali
                        if rec_ali[0][0] != rec_ali[-1][0]:
                            ban = False #Ban igual a False => posiciones permitidas hacia atras decrementan a -1
                            

                else:#Si la posicion -1 es inferior 0
                    pos_atras = -1
                    ban = False
                    ban_brk = False
                    break

            if ban_brk == False: #booleano para romper el ciclo si la posicion en inferior a cero
                if len(aux) == 0:  # En caso de que rec_ali no tenga nada que retornar
                    aux.clear
                    aux = lista_alineaciones[:]
                    new_posiciones.clear
                    new_posiciones = lista_posiciones[:] 
                    
                break

            if ban == False: #booleano para romper el ciclo
                ban = True
                pos_atras -= 1
            
            if brk_menor_seis == False: #si el patron es menor a 6
                #se mandan las mismas posiciones y alineaciones de entrada 
                aux.clear
                aux = lista_alineaciones[:]
                new_posiciones.clear
                new_posiciones = lista_posiciones[:]
                break
                

            aux.clear()
            aux = rec_ali[:]
            rec_ali.clear()

            i += 1
        
        return aux, new_posiciones
    
    def alineador(self):
        patrones = self.get_json_patrones()
        alineamiento_retorno = []
        list_posiciones = []
        list_patrones=[]
        
        for info_patron in tqdm(patrones["Patrones"]):
            pre_ali = [] #Captura al principio las primeras alineaciones hacia delante (posiciones)
            # rec_ali = [] #guarda las posciones de pre ali  
            posiciones = [p["posicion"]-1 for p in info_patron["Posiciones"]] #lista para recuperar todas las posiciones (posiciones -1)
            new_posiciones = []
            
            rec_ali = self.adiccion_frente_patron(
                info_patron["Patron"], posiciones)  # Ahora a la funcion
            # print("Salida"+str(rec_ali))
            if len(rec_ali) == len(posiciones): #Se asume que la longitud de un 
                
                aux, new_posiciones = self.adiccion_atras_patron(rec_ali, posiciones)

                if len(aux) == len(rec_ali) and len(new_posiciones) == len(posiciones): # Si la longitud de rec_ali es igual a aux
                    if ((len(aux[0]) >= 6) or (len(aux[0]) % 3 == 0)): # el patron alineado es mayor a 6 nucleotidos or es un multiplo de 3 
                        #Puse el or len para admitir mas patrones pero creo que se va a cambiar
                        alineamiento_retorno.append( aux[:] )
                        list_posiciones.append(new_posiciones)
                        list_patrones.append(info_patron["Patron"])
                        #se "guardan" las las alieneaciones completas (frontal y posterior) junto con
                        #las nuevas posicoines
                    
                else:
                    if ((len(rec_ali[0]) >= 6) or (len(rec_ali[0]) % 3 == 0)):
                        alineamiento_retorno.append(rec_ali[:])
                        list_posiciones.append(posiciones)
                        list_patrones.append(info_patron["Patron"])
                        #se "guardan" las las alieneaciones con modificacion hacia delante junto con
                        #las posiciones originales

                          
            else:
                #
                if ((len(info_patron["Patron"]) >= 6) or (len(info_patron["Patron"]) % 3 == 0)):
                    alineamiento_retorno.append(info_patron["Patron"])
                    list_posiciones.append(posiciones)
                    list_patrones.append(info_patron["Patron"])
                    #se "guardan" los patrones originales junto con
                    #las nuevas posiciones
            
            
            pre_ali.clear()
            rec_ali.clear()
            
        # self.muestra_resultados_txt(alineamiento_retorno, list_posiciones, list_patrones)
        json_resultados = self.muestra_resultados_json(alineamiento_retorno, list_posiciones, list_patrones)
        self.generador_archivos(json_resultados,**patrones["Configuracion"])
            #           p  
                # pre_ali = [ptr+self.secuencia[p+len(ptr)] if (p+len(ptr)<=len(self.secuencia)-1) else ban=False for ptr in pre_ali for p in posiciones ]
        
# if __name__ == '__main__':
#     x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud diferente\\"
#     y = "GCTTCACATGCCGCTGTGANACAGTGGTTTCGTGTGAGGGCTACGTCGTTAAGAGAATAACGATGAGCCCAGGCCTTTATGGAAAAACCACAGGGTATGCGGTAACCCACCACGCAGA"
#     z = "sequence_HL714398-BI-test-2022-02-05_21h47m23s927286ms.json"
#     align = Alineador(secuencia=y, tolerancia_atras=2, tolerancia_delante=2, json_patrones= os.path.join(x, z))
#     align.alineador()
