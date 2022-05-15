from glob import glob
import json
import os
import re
import datetime
import xlsxwriter
import json
from zipfile import ZipFile
from graficador import Graficador
from os.path import join, dirname, realpath
from tqdm import tqdm

EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')

class Alineador_multi(object):
    def __init__(self, secuencias = {}, tolerancia_delante = 2, tolerancia_atras = 2, longitud_minima_cre = 6, json_patrones = "", imprimir_logo = False):
        self.secuencias = secuencias
        self.tolerancia_delante = tolerancia_delante
        self.tolerancia_atras = tolerancia_atras
        self.longitud_minina_cre = longitud_minima_cre
        self.json_patrones =  json_patrones
        self.alineamientos = []
        self.motifs = []
        self.imprimir_logo = imprimir_logo
    
    def clear(self):
        self.secuencias = ''
        self.tolerancia_atras = 0
        self.longitud_minina_cre = 0
        self.tolerancia_delante = 0
        self.json_patrones = ''
        self.alineamientos = []
    
    def get_json_patrones(self):
        if type(self.json_patrones) == str:
            return self.extraccion_json()
        else:
            return self.json_patrones
            
              
    def muestra_resultados_json(self, alineamientos =[], posiciones_align=[], patrones=[], aminoacidos = []):
        
        # def buscar_motif_existente(motif = "", posiciones_esp = {}):
        #     return next((i for i, x in enumerate(list_info) if x["motif"] == motif and {j["secuencia"]: [k["posicion"] for k in x["alineamientos"] if j["secuencia"] == k["secuencia"] ] for j in x["alineamientos"]} == posiciones_esp), -1)

        dict_json ={}
        list_info =[]
        
        for i in tqdm(range(len(patrones))):
            x = []
            for s in alineamientos[i].values():
                x += s     
            # print(x)
            # print(type(alineamientos[i]))
            
            df_conteos, df_info ,motif, exp_reg = self.obtener_motif(x, patrones[i])
            # print(patrones[i])
            if motif != "":
                # existsPos = buscar_motif_existente(motif, posiciones_align[i])
                # print(motif)
                # if existsPos == -1:
                list_info.append({
                    "patron":patrones[i],
                    "alineamientos": [{"secuencia": x1,
                                    "alineamiento": y1,
                                    "posicion": z1 }  
                                    for x1 in alineamientos[i].keys()
                                    for y,z in zip(alineamientos[i].items(), posiciones_align[i].items()) 
                                    for y1, z1 in zip(y[1],z[1]) if (y[0] == x1 and z[0] == x1)
                                    ],
                    "matriz_conteo": json.loads(df_conteos.to_json(orient="index")),
                    "matriz_info": json.loads(df_info.to_json(orient="index")),
                    "motif": motif,
                    "longitud_motif": len(motif),
                    "expresion_regular": exp_reg,
                    "ocurrencias_patron": len(alineamientos[i]),
                    "traduccion_aminoacido": aminoacidos[i]
                    
                })
                # else:
                #     list_info[existsPos]["patron"] = patrones[i]
                #     list_info[existsPos]["traduccion_aminoacido"] = aminoacidos[i]


            
        dict_json["Alineaciones"] = list_info
        dict_json["Num_alineaciones"] = len(list_info)
        # print(dict_json)
        return dict_json
        
       
    def obtener_motif(self, alineamiento=[""], patron=""):
        g = Graficador(alineamiento)
        df_conteos, df_info, motif, exp_reg = g.ploteo_logo_seq_align(patron)
        return df_conteos, df_info, motif, exp_reg
    
    def generador_archivos(self, motifs_json, **kargs):

        def archivo_html():
            principal=""""""
            content_principal=""""""
            row_principal =""""""
            col_1 =""""""
            col_row_1 = """"""
            col_row_2 = """"""
            col_2 =""""""
            list_info_motifs = motifs_json['Alineaciones']
                # Recorremos la lista desde donde se quedo o en 0 hasta la longitud de la lista
            print("html in process")
            for item_dict in tqdm(list_info_motifs):
                # Se toma la imagen del motif actual
                filenamepng = os.path.join(
                    EXP_FOLDER, "motifs_html","img", (item_dict["patron"]+".png"))
                
                #Despues el alineamiento: posicion y secuencia de se alineo
                
                tabla1 = """"""  
                tabla1 += """   <p class="font-weight-bold">Alineamiento</p> """   
                
                x = """"""
                x += """ 
                <tr>
                    <th>secuencia</th>
                    <th>posicion</th>
                    <th>alineamiento</th>
                </tr>
                """ 
                #ciclo while para escribir las secuencias que se estan alineando
                for pos in item_dict["alineamientos"]:              
                    x += """ 
                    <tr>
                        <th>{secuencia}</th>
                        <th>{posicion}</th>
                        <th>{ali}</th>
                    </tr>
                    """.format(secuencia = str(pos["secuencia"]), posicion= str(pos["posicion"]), ali = str(pos["alineamiento"]))
                    
                tabla1 += """ 
                    <table class="table table-active">
                        {tabla_contenido} 
                    </table>
                """.format(tabla_contenido = x)
                    
                col_row_1 +="""
                    <div class ="row my-2 justify-content-center">
                        {tabla} 
                    </div>
                """.format(tabla = tabla1)

                
                #Se escribe la matriz de conteo
                
                #Se escribe la cabecera
                tabla2 =""""""
                tabla2 += """   <p class="font-weight-bold">Matriz de conteo</p> """  
                
                x = """"""
                x += """ 
                <tr>
                    <th>Posición</th>
                    <th>A</th>
                    <th>C</th>
                    <th>T</th>
                    <th>G</th>
                </tr>
                """
                
                y=""""""
                # Se toma la lista de diccionarios, donde las llaves principales son el numero de fila y los items son diccionarios con la llave de nucleotido y el valor es la frecuencia del nucleotido
                matriz_conteo = item_dict["matriz_conteo"]
                #Ciclo para escribir los valores de la matriz
                for k in range(len(matriz_conteo)):
                    
                    y += """ <th>{pos}</th> 
                    """.format(pos=str(k))
                    # Cada valor se escribe en la posicion que le corresponda
                    for key, value in matriz_conteo[str(k)].items():
                        y += """ <th>{value}</th> 
                    """.format(value=str(value))
                
                    x += """
                    <tr>
                        {datos}
                    </tr>
                    """.format(datos = y)
                    
                    y = """"""
                
                tabla2 += """ 
                    <table class="table table-active">
                        {tabla_contenido} 
                    </table>
                """.format(tabla_contenido = x)
                    
                col_row_2 +="""
                    <div class ="row my-2 justify-content-center">
                        {tabla} 
                    </div>
                """.format(tabla = tabla2)  
                
                col_1 += """
                <div class ="col align-items-center">
                    {row1}
                    {row2}
                </div>
                """.format(row1=col_row_1, row2=col_row_2)
                
                #se inserta la imagen y el motif
                col_2 += """
                    <div class ="col align-items-center">
                        <img class="align-self-center" src = "img/{patron}.png" alt = "{patron}.png">
                        <p class="font-weight-bold"> motif: {motif} </p>
                    </div>
                """.format(patron = item_dict["patron"], motif = item_dict["motif"])
                
                row_principal += """<div class ="row text-center justify-content-center my-2">
                    {col1}
                    {col2}
                </div>""".format(col1=col_1, col2=col_2)

                #Escribe el primero el patron
                content_principal += """
                <section>
                    <h3 class="my-2"> Patron {patron} </h3>
                    {row_prin}
                </section>
                
                """ .format(patron=item_dict["patron"], row_prin = row_principal)
            
                row_principal =""""""
                col_1 =""""""
                col_row_1 = """"""
                col_row_2 = """"""
                col_2 =""""""
                    
            principal += """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                    <title>motifs</title>
                </head>
                <body class="mx-5">
                    <div class=" row  m-5 text-center justify-content-center">
                        <h1>Motifs hallados</h1>
                    </div>
                    {contenido}
                </body>
            </html>
            """.format(contenido = content_principal)

            return principal
                    
        def archivo_excel(excel_writer=xlsxwriter.Workbook()):
            items = 0
            #La intencion de ponerlo en un while es para evitar que toda la informacion se ponga en una sola hoja,
            #para eso se recorrera por partes la lista se fuese necesario, el limite por el momento es 100000 filas
            #y se repartira la infromacion en en diferentes
            #Y se utiliza xlsx para insertar las graficas obtenidas
            while True:  # mientras se verdadero
                paper = excel_writer.add_worksheet()  # Se agreaga una nueva hoja de calculo
                #posiciones para escribir en la hora
                row = 0
                col = 0
                #addciones a las posiciones
                i = 0
                j = 0
                # Se toma la lista de alineaciones
                list_info_motifs = motifs_json['Alineaciones']
                # Recorremos la lista desde donde se quedo o en 0 hasta la longitud de la lista
                for itm in tqdm(range(items, len(list_info_motifs))):
                    # Se toma la imagen del motif actual
                    filenamepng = os.path.join(
                        EXP_FOLDER, "motifs_png", (list_info_motifs[itm]["patron"]+".png"))
                    #Escribe el primero el patron
                    j += 1
                    paper.write(row, col, "Patron")
                    paper.write(row, col+j, list_info_motifs[itm]["patron"])
                    paper.write(row+1, col, "Motif")
                    paper.write(row+1, col+j, list_info_motifs[itm]["motif"])
                    paper.write(row+2, col, "Expresion Regular")
                    paper.write(
                        row+2, col+j, list_info_motifs[itm]["expresion_regular"])
                    paper.write(row+3, col, "Longitud motif")
                    paper.write(row+3, col+j, list_info_motifs[itm]["longitud_motif"])
                    
                    #Despues el alineamiento: posicion y secuencia de se alineo
                    i += 5
                    paper.write(row+i, col+j, "Alineamiento")
                    i += 1
                    paper.write(row+i, col+j, "secuencia")
                    paper.write(row+i, col+j+1, "posicion")
                    paper.write(row+i, col+j+2, "alineamiento")
                    #ciclo while para escribir las secuencias que se estan alineando
                    for pos in list_info_motifs[itm]["alineamientos"]:
                        i += 1
                        paper.write(row+i, col+j, str(pos["secuencia"]))
                        paper.write(row+i, col+j+1, str(pos["posicion"]))
                        paper.write(row+i, col+j+2, str(pos["alineamiento"]))

                    #recolocacion de posciones
                    i = 5
                    j = 5
                    #Se escribe la matriz de conteo
                    # Se toma la lista de diccionarios, donde las llaves principales son el numero de fila y los items son diccionarios con la llave de nucleotido y el valor es la frecuencia del nucleotido
                    matriz_conteo = list_info_motifs[itm]["matriz_conteo"]
                    #Se escribe la cabecera
                    paper.write(row+i, col+j, "Matriz de conteo")
                    i += 1
                    #modificar 
                    paper.write(row+i, col+j, "Posición")
                    paper.write(row+i, col+j+1, "A")
                    paper.write(row+i, col+j+2, "C")
                    paper.write(row+i, col+j+3, "T")
                    paper.write(row+i, col+j+4, "G")
                    #Ciclo para escribir los valores de la matriz
                    for k in range(len(matriz_conteo)):
                        i += 1
                        paper.write(row+i, col+j, str(k))
                        # Cada valor se escribe en la posicion que le corresponda
                        for key, value in matriz_conteo[str(k)].items():
                            if key == "A":
                                paper.write(row+i, col+j+1, value)
                            elif key == "C":
                                paper.write(row+i, col+j+2, value)
                            elif key == "T":
                                paper.write(row+i, col+j+3, value)
                            elif key == "G":
                                paper.write(row+i, col+j+4, value)
                    
                    #recolocacion de posciones
                    i = 5
                    j = 12  # se recorren hasta la columna 14
                    # Se toma la lista de diccionarios, donde las llaves principales son el numero de fila y los items son diccionarios con la llave de nucleotido y el valor es la frecuencia del nucleotido
                    matriz_info = list_info_motifs[itm]["matriz_info"]
                    #Se escribe la cabecera
                    paper.write(row+i, col+j, "Matriz de informacion")
                    i += 1
                    paper.write(row+i, col+j, "Posición")
                    paper.write(row+i, col+j+1, "A")
                    paper.write(row+i, col+j+2, "C")
                    paper.write(row+i, col+j+3, "T")
                    paper.write(row+i, col+j+4, "G")
                    #Ciclo para escribir los valores de la matriz
                    for k in range(len(matriz_info)):
                        i += 1
                        paper.write(row+i, col+j, str(k))
                        # Cada valor se escribe en la posicion que le corresponda
                        for key, value in matriz_info[str(k)].items():
                            if key == "A":
                                paper.write(row+i, col+j+1, value)
                            elif key == "C":
                                paper.write(row+i, col+j+2, value)
                            elif key == "T":
                                paper.write(row+i, col+j+3, value)
                            elif key == "G":
                                paper.write(row+i, col+j+4, value)

                    if self.imprimir_logo == True:
                        i = 5
                        j = 19  # se recorren hasta la columna 19
                        
                        #se inserta la imagen al 50% de si proporcion
                        paper.insert_image(
                            row+2, col+j, filenamepng, {'x_scale': 0.5, 'y_scale': 0.5})
                        #por ultimo se escribe el motif
                    
                    #se suma la longitud de la matriz de conteo mas 10 para escribir los nuevos datos
                    row += len(list_info_motifs[itm]["alineamientos"]) + len(matriz_conteo) +10
                    col = 0
                    
                    if itm == len(motifs_json['Alineaciones'])-1:
                        paper.write(row+i+3, col, "Numero de alineaciones")
                        paper.write(row+i+3, col+1, motifs_json["Num_alineaciones"])

                    i = 0
                    j = 0
                    
                    
                        
                    #items es el contador principal dentro del while, por ese motivo se le asigna itm
                    items = itm
                    
                    #Se sobrepasa las 100000 filas se rompe el ciclo for
                    if row > 100000:  # 1000000 :
                        break
                #Si items llega  al longitud de los motifs menos uno, entonces se rompe el ciclo while
                if items == len(motifs_json['Alineaciones'])-1:
                    break

            excel_writer.close()

        #Formacion del nombre del archivo, tal como lo hace el server
        x = ""
        x += "EXP_"+str(kargs['Siglas']) + '_' +\
            str(kargs['Min_sup']) + '_' + \
            str(kargs['Tipo_Entrada']) + '_' + \
            str(kargs['Entrada']).replace(".fasta","") + '_' + \
            str(kargs['Num_Sequencias_ananlizadas']) + '_' + \
            str(kargs['Num_Patrones_hallados']) + '_'

        dt = datetime.datetime.strptime(
            kargs['Fecha_Hora_Inicio'], '%Y-%m-%d %H:%M:%S.%f')

        x += str(dt.day)+"d"+str(dt.month)+"d"+str(dt.year)+"&" + \
            str(dt.hour)+"-"+str(dt.minute)+"-"+str(dt.second)+"_"

        sdt = str(kargs['Duracion'])
        x1 = [i for i in re.split("[ ,:.]", sdt)
              if i.isdigit() or i.isdecimal()]

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
        # filenamehtml = os.path.join(EXP_FOLDER, "motifs_html")

        files_dir_png = os.path.join(EXP_FOLDER, "motifs_png", "*.png")

        try:
            if os.path.isfile(filename+(".json")):
                with open(filename+(".json"), 'w') as file_object_json:
                    json.dump(motifs_json, file_object_json,
                              sort_keys=True, indent=4)
            else:
                with open(filename+(".json"), 'x') as file_object_json:
                    json.dump(motifs_json, file_object_json,
                              sort_keys=True, indent=4)

            if os.path.isfile(filenamexlsx+'.xlsx'):
                with xlsxwriter.Workbook(filenamexlsx+'.xlsx') as excel_writer:
                    archivo_excel(excel_writer)
            else:
                with xlsxwriter.Workbook(filenamexlsx+'.xlsx') as excel_writer:
                    archivo_excel(excel_writer)
            
            # if os.path.isfile(filenamehtml+os.path.sep+"index.html"):
            #     with open(filenamehtml+os.path.sep+"index.html","w") as file_html:
            #         file_html.write(archivo_html())
                
            #     with ZipFile(filenamehtml +os.path.sep + x+".zip","w") as zip_file:
            #         zip_file.write(filenamehtml +os.path.sep+"img")
            #         zip_file.write(filenamehtml+os.path.sep+"index.html")
                
            # else:
            #     with open(filenamehtml+os.path.sep+"index.html","x") as file_html:
            #         file_html.write(archivo_html())
                
            #     #Se crea un archivo zip que contiene el html  
            #     with ZipFile(filenamehtml +os.path.sep + x+".zip","x") as zip_file:
            #         zip_file.write(filenamehtml +os.path.sep+"img")
            #         zip_file.write(filenamehtml+os.path.sep+"index.html")
            
                
            #remoción de los archivos png (LOGOS) generados
            files_png = glob(files_dir_png)
            for f in files_png:
                os.remove(f)
            # os.remove(filenamehtml+os.path.sep+"index.html")
            
            
        except IOError as e:
            print(f'Hubo un error en la escritura del archivo \n'+str(e))

        # except FileNotFoundError as fn:
        #     print(f'Hubo un error en el archivo: No se encontro o no existe. \n'+str(fn))

        # except FileExistsError as fe:
        #     print (f'Hubo un error en el archivo: '+str(fe)+'\n')

        else:
            print("Success!, file created")

    def muestra_resultados_txt(self, alineamientos, posciones, patrones):
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
            # print(muestras)
            
        try:
            with open("alineador_multiple.txt",'x') as file_object:
                file_object.write(muestras)
                
        except Exception as e:
            print(str(e))
            
    def adiccion_frente_patron(self, patron_original = "", dict_posiciones = [{}]):
        i=0
        ban = True  # Ban restar la tolerancia
        ban_brk = True  # Ban para quebrar el while cuando: algunas de las posiciones llega al limite o las torelancia abaco
        pos_delante = self.tolerancia_delante  # tolerancia hacia delante
        pre_ali = {}  # Prealineamiento
        rec_ali = {}  # Record  de los alineamientos
        # Booleano para indicar que si el patron no cumple con una poscion menor a la longitud de la secuencia
        brk_menor_seis = True
        while(pos_delante > 0):  # Busqueda hacia delante
            last_let = ""  # ultima letra
            aux_let = ""  # letra aux -> letra actual
            # Va por cada posicion en especifico del patron {secuencia: "", posicion}
            patron_evaluar = patron_original
            
            for pos in dict_posiciones: #info_patron["Posiciones"]:
                # patron_evaluar = patron_original
                
                #Si la longitud del patron es menos a 6
                # if len(patron_evaluar) < self.longitud_minina_cre and (pos["posicion"]-1)+self.longitud_minina_cre < len(self.secuencias[pos["sequencia"]])-1:
                #     # Se le agregan otras seis posiciones
                #     patron_evaluar = self.secuencias[pos["sequencia"]][(pos["posicion"]-1):(pos["posicion"]-1)+self.longitud_minina_cre]
                # # si la longitud es menor a  6 pero la(s) posiciones
                # elif (pos["posicion"]-1)+self.longitud_minina_cre >= len(self.secuencias[pos["sequencia"]])-1 and len(patron_evaluar) < self.longitud_minina_cre:
                #     #Sino se rompe el ciclo
                #     pos_delante = 0
                #     ban = False
                #     brk_menor_seis = False
                #     break
                
                # si la posicion no sobrepasa a longitud de la secuencia
                if i+(pos["posicion"]-1)+len(patron_evaluar) <= len(self.secuencias[pos["sequencia"]])-1:
                    if i == 0:  # Si el indicador es igual a cero
                        # pre_ali.append(patron_evaluar+self.secuencias[(pos["posicion"]-1)+len(patron_evaluar)+i])
                        # Si no esta la key de la secuencia en los prealineamientos
                        if pos["sequencia"] not in pre_ali:
                            # Si existe algo en el last_let (ultima letra)
                            if last_let:
                                aux_let = self.secuencias[pos["sequencia"]][(
                                    pos["posicion"]-1)+len(patron_evaluar)+i]  # Debe de tomar la ultima letra el aux
                            else:  # Si hay algo en en last_pre
                                # last_let toma la ultima letra al ser la primera iteracion
                                last_let = self.secuencias[pos["sequencia"]][(
                                    pos["posicion"]-1)+len(patron_evaluar)+i]
                        

                            pre_ali[pos["sequencia"]] = [patron_evaluar+self.secuencias[pos["sequencia"]][(pos["posicion"]-1)+len(
                                patron_evaluar)+i]]  # Se añade la secuencia y el patron a pre_ali (prealineamiento)
                        else:  # Si ya existe el patron dentro de pre_ali
                            pre_ali[pos["sequencia"]].append(patron_evaluar+self.secuencias[pos["sequencia"]][(
                                pos["posicion"]-1)+len(patron_evaluar)+i])  # Agrega la poscion dentro de la lista correspondiente
                            # Toma la letra siguiente al patron o alineamiento
                            aux_let = self.secuencias[pos["sequencia"]][(
                                pos["posicion"]-1)+len(patron_evaluar)+i]

                    else:  # Si el indicar no es igual a cero
                        # Se verifica que el key/codigo de la secuencia este en pre_ali, En caso de que exista
                        if pos["sequencia"] in pre_ali:
                            #Se agrega el patron a el alineamiento a la lista correspondiente
                            pre_ali[pos["sequencia"]].append(patron_evaluar+self.secuencias[pos["sequencia"]][(
                                pos["posicion"]-1)+len(patron_evaluar):(pos["posicion"]-1)+len(patron_evaluar)+i+1])
                            #Se toma la ultima leta para aux_let que le quiere agregar al patron desde la secuencia y poscion especifica
                            aux_let = self.secuencias[pos["sequencia"]][(
                                pos["posicion"]-1)+len(patron_evaluar)+i]
                            #Nota: La pos["posicion"] se le resta -1 porque es la que se muestra al usuario
                        else:  # no esta el codigo de la secuencia en pre_ali
                            #Se añande la key y la lista de poscion con el primer elemento
                            pre_ali[pos["sequencia"]] = [patron_evaluar+self.secuencias[pos["sequencia"]][(
                                pos["posicion"]-1)+len(patron_evaluar):(pos["posicion"]-1)+len(patron_evaluar)+i+1]]

                            if last_let:  # si hay algo en last_let
                                #Se toma la letra seguiente al patron/alineacion dentro de la secuencia especifico
                                aux_let = self.secuencias[pos["sequencia"]][(
                                    pos["posicion"]-1)+len(patron_evaluar)+i]
                            else:  # En caso que no tenga nada last_let
                                #Se toma la letra seguiente al patron/alineacion dentro de la secuencia especifico
                                last_let = self.secuencias[pos["sequencia"]][(
                                    pos["posicion"]-1)+len(patron_evaluar)+i]

                    if aux_let != "":  # Si  aux_let es diferente a nada
                        if last_let != aux_let:  # Si aux_let y last_let son diferentes
                            ban = False  # Se activa el ban, que indica que TODAS las letas que se agregan al patron no son iguales
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

                    # if len(pre_ali)> 1:
                        # print(pre_ali.values())
                        # print(list(pre_ali.values())[0][0][-1])
                        # if list(pre_ali.values())[0][0][-1] != list(pre_ali.values()[-1][0][-1]):
                            #
                else:  # Si sobre pasa la poscion del patron/alineacion la longitud de la secuencia
                    # Las posiciciones hacia delante es igual a 0 (Ya no se añande nada)
                    pos_delante = 0
                    ban = False  # Ban es igual a False
                    ban_brk = False  # Ban_brk es igual a False, por ende, se rompe el while
                    break  # Se romple el ciclo de las posiciones
                
                patron_evaluar = patron_original
                    
            if ban_brk == False:
                if len(rec_ali) == 0: # En caso de que rec_ali no tenga nada que retornar
                    rec_ali = { pi["sequencia"]: [ patron_evaluar for i in range(len(dict_posiciones)) 
                                              if dict_posiciones[i]["sequencia"] == pi["sequencia"] ] for pi in dict_posiciones}
                break  # Romple el ciclo while

            if ban == False:
                ban = True
                pos_delante -= 1
            else: #incremento si encuenta algun patorn    
                pos_delante = self.tolerancia_delante
            
            if brk_menor_seis == False: #si es menor a seis
                #mandamos 
                rec_ali = { pi["sequencia"]: [ patron_evaluar for i in range(len(dict_posiciones)) 
                                              if dict_posiciones[i]["sequencia"] == pi["sequencia"] ] for pi in dict_posiciones}
                
                break

            #Si no hay anomalias
            i += 1  # Se suma i indicador de posiciones
            rec_ali.clear()  # Se limpia rec_ali
            rec_ali = pre_ali.copy()  # Se compia el contenido de pre_ali y se pasa rec_ali
            pre_ali.clear()  # Se limpia pre_ali

        return rec_ali
    
    
    
    def adiccion_atras_patron(self,  dict_alineaciones = {}, dict_posiciones = {}):        
        #------------------------------------------------------------------------------------
        #SEGUNDA FASE: SE AGREGAN LETRAS HACIA ATRAS DE LOS PATRONES
        #----------------------------------------------------------------------------------
        # indicador i igual a 1 (Ahora para recortar posiciones hacia atras)
        i = 1
        pre_ali = dict_alineaciones  # copiamos lo que tiene rec_ali a pre_ali. Cambiamos el rol, ahora rec_ali va ir ciclo por ciclo para recolectar los patrones y pre_ali los resguarda
        rec_ali = {}  # se limpia rec_ali
        aux = {}  # diccionario auxiliar -> aqui le pontran todas las alineacion resultantes de cada ciclo
        new_posiciones = {} #las nuevas posiciones con respeocto
        pos_atras = self.tolerancia_atras  # tolerancia hacia atras
        ban = True  # Ban restar la tolerancia
        ban_brk = True  # Ban para quebrar el while cuando: algunas de las posiciones llega al limite o las torelancia abaco
        brk_menor_seis = True # Ban para romper el ciclo si el patron es menor a seis
        #Nota: Ban de Bandera, no se porque tengo esa concepcion
        while(pos_atras > 0):  # Si la posicion hacia atras de mayor a 0
            fst_let = ""  # Se limpia la primera letra
            aux_let = ""  # Se pondran todas las
            for key, pos in dict_posiciones.items():  # se recorren cada key(codigo de la secuencia) y la lista posiciones
                for k in range(len(pos)):  # se recorre la lista en base a si index
                    alineamiento = pre_ali[key][k] # se toma el patron alineado compuesto
                    pos_align = pos[k]
                    #Crecimiento para igual la longitud minima
                    #Si la posicion menos las pociones hacia atras que necesite el patron/secuencia alineada para llegar a una longitud de 6 y si el mismo patron/secuencia es menor a seis 
                    # if pos_align-(self.longitud_minina_cre-len(alineamiento)) > 0 and len(alineamiento) < self.longitud_minina_cre:
                    #     # Si es menor a 6, se le acompletara con las letras detras del patron hasta llegar a 6
                    #     # Primero toma la posicion modificada
                    #     pos_align = pos[k] - \
                    #         (self.longitud_minina_cre-len(alineamiento))
                    #     alineamiento = self.secuencias[key][pos_align:pos[k]] + str(alineamiento) # y despues el nuevo alineamiento
                        
                        
                    # #Si la posicion menos las pociones hacia atras que necesite el patron/secuencia alineada para llegar a una longitud de 6 y si el mismo patron/secuencia es menor a seis
                    # elif pos_align-(self.longitud_minina_cre-len(alineamiento)) <= 0 and len(alineamiento) < self.longitud_minina_cre:
                    #     pos_atras = 0
                    #     brk_menor_seis = False
                    #     break 
                    
                    if (pos_align-i >= 0):  # Si la posicion menos el indicador sea mayores a 0    
                        if i == 1:  # si es igual a 0
                            #*Actualizacion de posciones y alineamientos*
                            if key not in rec_ali:  # si la key de la secuencia no esta em rec_ali
                                if fst_let:  # si fst_let tiene algo
                                    # Se obtiene la letra anterior al patron
                                    aux_let = self.secuencias[key][pos_align-i]
                                else:
                                    # Se obtiene la letra anterior al patron
                                    fst_let = self.secuencias[key][pos_align-i]

                                # Se guarda la key de la secuencia y la posicion
                                rec_ali[key] = [self.secuencias[key][pos_align-i]+alineamiento] 
                                # Se agrega la key y la lista con la primera posicion conocida
                                new_posiciones[key] = [pos_align-1]
                            
                            else:  # si ya esta la key dentro de rec_ali
                                # se agrega a la lista dependiendo del codigo en espeficio
                                rec_ali[key].append(self.secuencias[key][pos_align-i]+alineamiento)    
                                # Se agrega la posicion con la key correspondiente
                                new_posiciones[key].append(pos_align-1)
                                # se obtiene la letra anterior al patron o alineamiento
                                aux_let = self.secuencias[key][pos_align-i]
                                

                            # new_posiciones.append(posiciones[k]-1)
                        else:  # Si es diferente a 1
                            if key not in rec_ali:  # si la key no esta dentor de rec_ali
                                # Se guarda la key de la secuencia y la posicion actualizada
                                rec_ali[key] = [
                                    self.secuencias[key][pos_align-i:pos_align]+alineamiento]

                                if fst_let:  # Si fst_let si tiene algo
                                    # aux_let se toma ultima letra insertada
                                    aux_let = self.secuencias[key][pos_align-i]
                                else:  # Si no tiene
                                    # fst_let toma la ultima letra insertada atras
                                    fst_let = self.secuencias[key][pos_align-i]
                            else:  # si esta la key de la secuencia
                                # se agrega a la lista dependiendo del codigo en espeficio
                                rec_ali[key].append(
                                    self.secuencias[key][pos_align-i:pos_align]+alineamiento)
                                # aux_let se toma ultima letra insertada
                                aux_let = self.secuencias[key][pos_align-i]

                            # Se agrega la posicion con la key correspondiente
                            new_posiciones[key][k] = new_posiciones[key][k]-1

                        # if len(rec_ali) > 1:
                        #     if rec_ali[0][0] != rec_ali[-1][0]:
                        #         ban = False
                        # else:
                        if aux_let != '':  # Si  aux_let es diferente a nada
                            if fst_let != aux_let:  # Si aux_let y last_let son diferentes
                                ban = False  # Se activa el ban, que indica que TODAS las letas que se agregan al patron no son iguales
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
                                fst_let = aux_let
                                #se limpia aux_let
                                aux_let = ""

                        # else:

                        #     aux_let = ""

                    else:  # Si el indicador es menor 0
                        pos_atras = -1  # pos_atras menos
                        ban = False  # booleano para romper el ciclo for interno
                        ban_brk = False  # booleano para rompper el ciclo while
                        break
                    
                    
                if brk_menor_seis == False:  # si el patron es menor a 6
                    break

            if ban_brk == False:  # si ban_brk es falso
                if len(aux) == 0:  # En caso de que rec_ali no tenga nada que retornar
                    #se mandan las mismas posiciones y alineaciones de entrada
                    aux.clear
                    aux = dict_alineaciones.copy()
                    new_posiciones.clear
                    new_posiciones = dict_posiciones.copy()

                break  # break al while funcional

            if ban == False:  # si ban es False
                ban = True #Ban a su estado original
                pos_atras -= 1  # pos_atras menos unos
            else:
                pos_atras = self.tolerancia_atras

            if brk_menor_seis == False:  # si el patron es menor a 6
                #se mandan las mismas posiciones y alineaciones de entrada
                aux.clear
                aux = dict_alineaciones.copy()
                new_posiciones.clear
                new_posiciones = dict_posiciones.copy()
                break
            
            aux.clear()  # limpia el auxiliar
            aux = rec_ali.copy()  # aux guarda lo que tenga rec_ali
            rec_ali.clear()  # limpia lo que tenga rec_ali

            i += 1  # aumenta mas uno el indicardor
        
        #Retorno de resultados
        return aux, new_posiciones

                
    def extraccion_json(self):
        try:
            with open(self.json_patrones, 'r') as jsonpatrones:
                x = json.load(jsonpatrones)
                return x
        except Exception as e:
            print("Error en el Archivo: " + str(e))
    
    def alineador(self):
        patrones = self.get_json_patrones()  # se extrae la informacion del archivo JSON
        alineamiento_retorno = [] #Para guardar todos los alineamientos encontrados
        list_posiciones = [] #Para guardar las posiciones en especifico
        list_animoacidos = [] #lista de los aninoaciodos
        list_patrones=[] #Para la lista de patrones
        
        def comprobar_lugar_alineaciones(posiciones_actuales):
            return next((i for i, x in enumerate(list_posiciones) if x == posiciones_actuales),  -1 )
            #     return next((i for i, x in enumerate(list_info) if x["motif"] == motif and {j["secuencia"]: [k["posicion"] for k in x["alineamientos"] if j["secuencia"] == k["secuencia"] ] for j in x["alineamientos"]} == posiciones_esp), -1)
        
        for info_patron in tqdm(patrones["Patrones"]):
            rec_ali = {} #Record  de los alineamientos
            # posiciones = {p["sequencia"]: [p["posicion"]] if p["sequencia"] is posiciones else p["sequencia"].append(p["posicion"]) for p in info_patron["Posiciones"]}  # [p["posicion"]-1 for p in info_patron["Posiciones"]]
            posiciones = {p["sequencia"]: [ pj["posicion"]-1 for pj in info_patron["Posiciones"] if pj["sequencia"] == p["sequencia"]] for p in info_patron["Posiciones"]}  # [p["posicion"]-1 for p in info_patron["Posiciones"]] #Obtenermos las posiciones
            
            #PRIMER FASE: ADICIÓN DE LETRAS HACIA DELANTE DE LOS PATRONES
            rec_ali = self.adiccion_frente_patron(info_patron["Patron"], info_patron["Posiciones"])
            #print("Primera Fase: ",rec_ali)
            
            if len(rec_ali) == len(posiciones): #Si la longitud de rec_ali es igual al de las posiciones
                
                #SEGUNDA FASE: ADICION DE LETRAS HACIA ATRAS DE LOS PATRONES
                aux, new_posiciones = self.adiccion_atras_patron(rec_ali, posiciones)
                # print("Segunda Fase",aux,"\n",new_posiciones,"\n")
                
                if (len(aux) == len(rec_ali)) and (len(new_posiciones) == len(posiciones)): #Si las longitudes de las alienaciones de enfrente son iguales a las de atras 
                    # print(aux.copy()) #imprime lo que tienes de las alienaciones completas
                    # el patron alineado es mayor a 6 nucleotidos or es un multiplo de 3
                    # or (len(list(aux.values())[0][0]) % 3 == 0):
                    if(len(list(aux.values())[0][0]) >= self.longitud_minina_cre):
                        cla = comprobar_lugar_alineaciones(new_posiciones) #Se compueban las alineaciones para evitar redundancia en las posiciones y por ende los patrones
                        #para ello cla indicara el lugar de la redundancia
                        if cla == -1: #si no existen esas posiciones 
                            alineamiento_retorno.append(aux.copy()) #Agregalo a la lista grande
                            list_posiciones.append(new_posiciones.copy()) #se agrega la que tiene las posiones que retrocediron
                            list_patrones.append(info_patron["Patron"]) #Agrega al patron
                            list_animoacidos.append(info_patron["Traduccion_aminoacido"])
                        else: #en caso contrario 
                            #Se reemplaza el patron con su respectivo traduccion
                            list_patrones[cla] = info_patron["Patron"]
                            list_animoacidos[cla] = info_patron["Traduccion_aminoacido"]
                
                else: #sino
                    # print(pre_ali.copy()) #imprime lo resultante de enfrente                                    if((aux.get.values()[0][0]) >= 6) or ((aux.get.values()) % 3 == 0):
                    # or (len(list(rec_ali.values()[0][0])) % 3 == 0):
                    if(len(list(rec_ali.values()[0][0])) >= self.longitud_minina_cre):
                        # Se compueban las alineaciones para evitar redundancia en las posiciones y por ende los patrones
                        cla = comprobar_lugar_alineaciones(posiciones)#Se compueban las alineaciones para evitar redundancia en las posiciones y por ende los patrones
                        #para ello cla indicara el lugar de la redundancia
                        if cla == -1: #si no existen esas posiciones 
                            alineamiento_retorno.append(rec_ali.copy()) #copialo a la lista grande
                            #quedate con las posiciones originales
                            list_posiciones.append(posiciones) 
                            # Agrega al patron
                            list_patrones.append(info_patron["Patron"])
                            list_animoacidos.append(info_patron["Traduccion_aminoacido"])
                        else: #en caso contrario 
                            #Se reemplaza el patron con su respectivo traduccion
                            list_patrones[cla] = info_patron["Patron"]
                            list_animoacidos[cla] = info_patron["Traduccion_aminoacido"]
                            
                           
            else:  # Si la longitud de rec_ali no fue igual de las posiciones
                #Se toma el patron tal cual junto con las posiciones actuales
                # or (len(info_patron["Patron"]) % 3 == 0)):
                if (len(info_patron["Patron"]) >= self.longitud_minina_cre):
                    # Se compueban las alineaciones para evitar redundancia en las posiciones y por ende los patrones
                    cla = comprobar_lugar_alineaciones(posiciones)
                    #para ello cla indicara el lugar de la redundancia
                    if cla == -1: #si no existen esas posiciones 
                        alineamiento_retorno.append(info_patron["Patron"])
                        list_posiciones.append(posiciones)
                        list_patrones.append(info_patron["Patron"])# Agrega al patron
                        list_animoacidos.append(info_patron["Traduccion_aminoacido"])
                else:
                    #en caso contrario 
                    #Se reemplaza el patron con su respectivo traduccion
                    list_patrones[cla] = info_patron["Patron"]
                    list_animoacidos[cla] = info_patron["Traduccion_aminoacido"]
                            
            
            
            rec_ali.clear()
            aux.clear()
            
        json_resultados = self.muestra_resultados_json(
            alineamiento_retorno, list_posiciones, list_patrones, list_animoacidos)
        self.generador_archivos(json_resultados, **patrones["Configuracion"])
        return json_resultados
        # print(alineamiento_retorno)
        # print(list_posiciones)
            
        # self.muestra_resultados(alineamiento_retorno, list_posiciones, list_patrones)
            #           p  
                # pre_ali = [ptr+self.secuencias[p+len(ptr)] if (p+len(ptr)<=len(self.secuencias)-1) else ban=False for ptr in pre_ali for p in posiciones ]
        
# if __name__ == '__main__':
#     # x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud diferente\\"
#     #x = "C:\\Users\\sobre\\Desktop\\"
#     x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\motifs\\multi\\json\\"
#     y = {"MN273335.1": "ACCCCCGTCCCGGGATCAGAGTCACGTACGGTTATCATATGGACCATTGGATCAAAAGGACACGTGTTCGATCAGGATCTGTGATTCGTTCAACGAATCTGACGGAAGATCGTACACTTTATGCTTTTACGCGTGGCAAGCTGTTATTGGTTCTTTAAGGCGTCGTTGCTTTTTTCACGCGTTTTCTTTTTGCGCCGTTGTTTTGGCAGCTGGAAAGCATATGCTTTCCTTAGCTGTTAAGTATTTTTTTTTGTGGTGTGCATACGAAGCTTCGTTTGAGTTTGCCTATAAATAACAGTGCATCGTCTTCAACCTCATACACAACCATGGCTGAGTGGTTTTCAAGTCCTGTGAAAACATGTACACATGTTTGTGACTTTCCTTCTCTCTCTTCTTCTTCTACTGAGCAACAAATAAGGTGTTGTGATACTATGAAGGACAAGTTGCAAGATTCAAGGAGGGTGTTGCTCGTAAGTTGCAGTGTCAGCTTCAATGGCAGTTTCTATGGAGGTAATAGGAATGTTCGTGGTCAACTGCAACTATCAATGGAGGAAGACGATGGTGTTCTTAGACCAATTGGATTTATTCCAATTGGAGGTTATTTGTACCATAATGATTATGGGTATTATCAAGGTGAGAAGACATTTAATCTGGATGTGGAGTCTCAATACTTGAAGGCAGATGAAGATTACAACAAACTGTTCGTGGTAAATATTTTGAATGAAAATGGATTAGATGATAGATGTGATTTGAAGGTGTTTGTTGTTCATACACTTAGAATCAAGGTGTAATTAGTACATCAGTGTAATTAATGTTAATTAATGAATATTTATTATTTTAAGTGTTGTTAATGAATATAATTATTGATTGATATTGTTTTTAATAACTCCGCGAAGCGATATGGATCAGCCCAATAGGCCCAATAGTTAATAGGCCCAATATAAATGGGGATCAGCTGACGTCAGCTGATCCCGTGACAGCCTGGGACGGGGCTTAGTATT",
#          "MN273334.1": "ACCCCCGCCCCAGGATCAGCGGAGTCATCACGTGACTCCCACGTGCTTTGTGCGTGAACTGTAGCGTGTAGGGTCCCACATACGCACTAACTGAACAACGTTGTGAGGACGACGAATACTTCGTCGTGAAGTAAAGTAAACCCACTTCAGTGGGTTTGCTTTATACTTTATTCGTTGTTTGTTGCTTTTGAATGAATGGCTCAGATTGAATCTAAATTAATGCGTACATGGTACGCCTTGTTGTGTGGTGATTATAAATAGCGAGTGGTTCTGAAATTGAATCATCGTCTTCCTCTTCTCACCTGCTTCGTTTGTTTAATTGTTCCATTATAATATTCATTTTAATGGGGGATCAAGGTCAAGGTTATTATGCAGGTTATCAAGCAGACGATGAGGGACAATCATCCAATAATCACCAGGTATTAAATATTATAGGTATAGTATTATTAATAATACTATGTATTAGTGGTATCTGGGTTTGTATTATGTTAGCCTGTTATATACCTGGGTTTGTTAAGAAGACATTAGATGCTTGGTTAAGTTCATCATCAATTATGAAGAGGAGGTTAGCTGCTACTATAACAAGAACACCATATGAAGAAACAGGCCCTGAGAGAGAAAGAAGATGGAGTGCTAGAAGGAATCAAGCTGAAGGAGGTGTTCAAGGGAATAATAATGCTTCTGGGTTTAGTTAGTTAGGTAGTTTGTGTTCTTGTAATTGTCAACATCAGTATGTAATGATTCAAGGAATTAATAAAATATTATTTTATTAATGTGTTGTAGTTGTTTGTTATGTTGTTCTTTGTTGAATAATGTTTATGTGTAAGGAAGACGATGATGAATAATAAGAATATGTTGTTTTTGATTTTAAAACTCCGCGAAGCGGTATGGTTCGGTGTTTGTGTTGACATATATGCCCTTCATTAATGAAGGGGTAATGTCCAAATTACCCCTTGTGACGTCATTTGATCCCGTGCTGAGCTGGGGCGGGGCTTAGTATT",
#          "MN273324.1": "ACCCCCGTCCCGGGATCAGAGTCACGTACGGTTATCATATGGACCATTGGATCAAAAGGACACGTGTTCGATCAGGATCTGTGATTCGTTCAACGAATCTGACGGAAGATCGTACACTTAATGCTTTTACGCGTGGCAAGCTGTGATTGGTTCTTTAAGGCGACGTTGCTTTTTTCACGCGCTTTCTTTTTGCGCCGTTGTTTTGGCAGCTGGAAAGCATATGCTTTCCTTAGCTGTTAAGTATTTCTTTTTGTGGTGTGCATAGGAAGCTTCGTGTGAGTTTGCCTATAAATAACAGTGCATCGTCTTCAACCTCATACACAACCATGGCTGAGTGGTTTTCAAGTCCTGTGAAAACATGTACACATGTTTGTGACTTTCCTTCTCTCTCTTCTTCTTCTACTGAGCAACAAATAAGGTGTTGTGATACTATGAAGGACAAGTTGCAAGATTCAAGGAGGGTGTTGCTCGTAAGTTGCAGTGTCAGCTTCAATGGTAGTTTCTATGGAGGTAATAGGAATGTTCGTGGTCAACTGCAACTATCAATGGAGGAAGACGATGGTGTTCTTAGACCAATTGGATTTATTCCAATTGGAGGTTATTTGTACCATAATGATTATGGGTATTATCAAGGTGAGAAGACATTTAATCTGGATGTGGAGTCTCAATACTTGAAGGCAGATGAAGATTACAACAAACTGTTCGTGGTAAATATTTTGAATGAAAATGGATTAGATGATAGATGTGATTTGAAGGTGTTTGTTGTTCATACACTTAGAATCAAGGTGTAATTAGTACATCAGTGTAATTAATGTTAATTAATGAATATTTATTATTTTAAGTGTTGTTAATGAATATAATTATAGATTGATATTGTTTTTAATAACTCCGCGAAGCGGTATGGATCAGCCCAATAGGCCCAATAGTTAATAGGCCCAATATAAATGGGGATCAGCTGACGTCAGCTGATCCCGTGACAGCCTGGGACGGGGCTTAGTATT",
#          "LC521492.1": "GAGAGGCGGCATAGTATTACCCGCCTCTCATCCCTCACCTTTCATCCCGGTCCCACCATGCCAACTGTGCAATCCACTTGTTGGGTGTTCACACTTAACTTTAAAGGCGAAATTCCTATTTTGCCCTTTAATGACCGCGTTCAGTACGCCTGTTGGCAACACGAAAGAGTGGGCCATGACCATTTACAGGGCTTTATTCAGATGAAGGCCCAACAATCTTTGGGCCAAATGAAGGCCATTATTCCTGGAGCCCATTTTGAGAAAATGAGGGCATTAAATACAGACCAGGCTAAGGCTTACGCTATGAAGGAAGACACACGAATAGAAGGACCATGGGAGTATGGTTTATACATTAAGAAGGGATCGCATAAGAGAAAAATTATGGAGCGATTTGAAGATGACCCAGAAGAAATGAAGATTGAAGATCCCTCACTATATCGTCGGTGTTTATCAAGGAAGATGACAGAAGAACAACGATCAACTGCAGAGTGGAATTACGACATGAGGCCATGGCAAGACCAAGTCATACAAGAGATAGAAGAGACACCTGATTACCGAAAGATTATCTGGGTTTACGGCCCCAAAGGAGGTGAAGGAAAGAGTACGTTTGCCAGGTACCTTTCACTCAAACAAGGTTGGGGTTATTTACCTGGTGGTAAGACGCATGACATGATGCATATCATCAGTGGAGAACCGAAGAACAACTGGGTCTTTGACATCCCAAGAGTAGCGTCTGAGTATGTGAACTATGGTGTATTAGAGCAGGTTAAAAATAGAGTTATGGTTAATACTAAGTACGAGCCAATAGTAATTAGGGATGATAATCATCCTGTTCATGTAATTGTGTTTGCTAATTGTATGCCAGACTTCACAAAAATAAGTGAAGATCGAATGAAAATAGTCCATTGTTAAGAAATATGTTGTTTTTGAAATTACGCGAAGCGAAGTCCCACATCGAATAGGTTGGAGAACTGAGCGAGGGATGAAAGCAATAAATAGG",
#          "MN273341.1": "ACCCCGCCTTGGAACACCTCCTTGGAACGGGTATAAAAATAAATGAAAAATAAAATTAATTAATGGCTTGTGCGAATTGGGTTTTCACGCGTAACTTTGAAGGTGCTCTCCCTTCTCTCTCGTTCGACGAGAGAGTTCAATATGCATCCTGGCAACATGAGAGAGGATCACATGATCATATCCAGGGAGTAATTCAACTGAAGAAGAAGGCAAGAATATCAACTGTGAAGGAGTTAATTGGTGGAAATCCTCATCTGGAGAAGATGAAGGGTACAATTGAAGAAGCTACTGCTTATTCCCAGAAAGAAGAAACACGAGTTGCAGGTCCATGGAGTTATGGGGAAATTTTAAAGAAAGGAAGTCATAAGAGGAAGACGATGGAGAGATACTTAGAAGATCCAGAAGAAATGAGATTGAGGGATCCTGATACTGCTCTTCGATGTAAGGCGAAGAAATTAAAGGAAGAATATTGTTCTTCCTTTTCTGGGTTCAAGCTTCGTCCATGGCAGGTTGAGCTTCATAGAGCTTTAATGGCAGAACCAGACAACCGGACAATTATCTGGGTTTATGGTCCTGATGGAGGAGAAGGAAAATCAACGTTTGCTAAGGAATTAATTAAATATAATTGGTTTTATTCAGCAGGAGGGAAGACTCAAGACGTTCTGTATATGTATGCACAAGATCCAGAAAGAAATATTGCCTTTGATGTGCCCAGATGTTCTTCGGAGATGATGAACTATCAAGCGATGGAGATGATGAAAAATAGATGCTTTGCAAGTACAAAATATAGGCCCGTAGATCTTTGTGTTATGAAAAATGTACATTTAATTGTGTTTGCCAACGTGGCACCGGACCCCACAAAAATAAGTGAGGACAGAATTGTAATTATTAATTGTTGAATTTGAATTTTAAAACTTCGCGAAGCGCCAATTTTCCCGCTCTTTATGCGTTTTATCAAAACGCAGTCGTTTTTACCTTGGACCAAGGCGGGTTGAGTATT",
#          "MN273331.1": "ACCCCGCCTTGGAACACCTCCTTGGAACGGGTATAAAAATAAATGAAAAATAAAATTAATTAATGGCTTGTGCGAATTGGGTTTTCACGCGTAACTTTGAAGGTGCTCTCCCTTCTCTCTCGTTCGACGAGAGAGTTCAATATGCATCCTGGCAACATGAGAGAGGATCACATGATCATATCCAGGGAGTAATTCAACTGAAGAAGAAGGCAAGAATATCAACTGTGAAGGAGTTAATTGGTGGAAATCCTCATCTGGAGAAGATGAAGGGTACAATTGAAGAAGCTACTGCTTATTCCCAGAAAGAAGAAACACGAGTTGCAGGTCCATGGAGTTATGGGGAAATTTTAAAGAAAGGAAGTCATAAGAGGAAGACGATGGAGAGATACTTAGAAGATCCAGAAGAAATGAGATTGAGGGATCCTGATACTGCTCTTCGATGTAAGGCGAAGAAATTAAAGGAAGAATATTGTTCTTCCTTTTCTGGGTTCAAGCTTCGTCCATGGCAGGTTGAGCTTCATAGAGCTTTAATGGCAGAACCAGACAACCGGACAATTATCTGGGTTTATGGTCCTGATGGAGGAGAAGGAAAATCAACGTTTGCTAAGGAATTAATTAAATATAATTGGTTTTATTCAGCAGGAGGGAAGACTCAAGACGTTCTGTATATGTATGCACAAGATCCAGAAAGAAATATTGCCTTTGATGTGCCCAGATGTTCTTCGGAGATGATGAACTATCAAGCGATGGAGATGATGAAAAATAGATGCTTTGCAAGTACAAAATATAGGCCCGTAGATCTTTGTGTTATGAAAAATGTACATTTAATTGTGTTTGCCAACGTGGCACCGGACCCCACAAAAATAAGTGAGGACAGAATTGTAATTATTAATTGTTGAATTTGAATTTTAAAACTTCGCGAAGCGCCAATTTTCCCGCTCTTTATGCGTTTTATCAAAACGCAGTCGTTTTTACCTTGGACCAAGGCGGGTTGAGTATT", 
#          "LC010784.1": "ACCCGCCTCTCATCCCTCACCTTTCATCCCGGTCCCACCATGCCAACTGTGCAATCCACTTGTTGGGTGTTCACACTTAACTTTAAAGGCGAAATTCCTATTTTGCCCTTTAATGACCGCGTTCAGTACGCCTGTTGGCAACACGAAAGAGTGGGCCATGACCATTTACAGGGCTTTATTCAGATGAAGGCCCAACAATCTTTGGGCCAAATGAAGGCCATTATTCCTGGAGCCCATTTTGAGAAAATGAGGGCATTAAATACAGACCAGGCTAAGGCTTACGCTATGAAGGAAGACACACGAATAGAAGGACCATGGGAGTATGGTTTATACATTAAGAAGGGATCGCATAAGAGAAAAATTATGGAGCGATTTGAAGATGACCCAGAAGAAATGAAGATTGAAGATCCCTCACTATATCGTCGGTGTTTATCAAGGAAGATGACAGAAGAACAACGATCAACTGCAGAGTGGAATTACGACATGAGGCCATGGCAAGACCAAGTCATACAAGAGATAGAAGAGACACCTGATTACCGAAAGATTATCTGGGTTTACGGCCCCAAAGGAGGTGAAGGAAAGAGTACGTTTGCCAGGTACCTTTCACTCAAACAAGGTTGGGGTTATTTACCTGGTGGTAAGACGCATGACATGATGCATATCATCAGTGGAGAACCGAAGAACAACTGGGTCTTTGACATCCCAAGAGTAGCGTCTGAGTATGTGAACTATGGTGTATTAGAGCAGGTTAAAAATAGAGTTATGGTTAATACTAAGTACGAGCCAATAGTAATTAGGGATGATAATCATCCTGTTCATGTAATTGTGTTTGCTAATTGTATGCCAGACTTCACAAAAATAAGTGAAGATCGAATGAAAATAGTCCATTGTTAAGAAATATGTTGTTTTTGAAATTACGCGAAGCGAAGTCCCACATCGAATAGGTTGGAGAACTGAGCGAGGGATGAAAGCAATAAATGGGGAGAGGCGGCATAGTATT",
#          "NC_003648.1": "CTGGGGCGGGGCTTAGTATTACCCCCGCCCAGGATCAGCGGAGTCATCACGTGACCCGCACATGCCATTAGTCTATATATAGCTCAAGTTGTAATATTTTATCATTCATGAATAAAATATGGCTCGGCAAGTTATATGCTGGTGCTTTACATTAAATAATCCTCTCTCTCCTCTTTCTCTTCATGAATTAATGAAGTACCTTGTTTATCAAAGAGAACAAGGTGAAGCTGGAAATATTCATTTCCAGGGTTATATTGAGATGAAGAAACGCACGTCTCTTGCAGGTATGAAGAAATTAATCCCAGGTGCCCACTTCGAAAAGAGGAGAGGTACTCAAGGTGAAGCTAGAGCTTACGCCATGAAGGAAGACACCCGTCTTGAAGGTCCATGGGAGTATGGGGAGTTCATCCCCACCATTGAAGATAAGCTCAGAGAAGTTATGAACGACATGAAGATTACAGGTAAGAGACCTATTGAGTATATAGAAGAGTGTTGTAATACATATGATAAATCTGCGAGTACTCTAAGGGAATTCAGAGGTGAGTTGAAGAAGAAGAAGGCAATTATAAGTTGGGAGTTGCAGAGGAAGCCATGGATGGACGAGGTTGATACCTTGCTTCAAGAGAGAGATGGAAGACGAATCATTTGGGTGTATGGCCCACAAGGTGGAGAAGGGAAAACCTCTTACGCTAAGCATCTTGTGAAAACGCGTGATGCTTTTTATTCGACAGGTGGAAAGACAGCCGACATTGCTTTTGCGTGGGACCACCAAGAGTTAGTGCTGTTCGACTTTCCTCGAAGCTTCGAGGAGTATGTCAATTACGGAGTAATTGAGCAATTAAAAAATGGAATAATACAGTCTGGCAAGTATCAAAGTGTAATTAAGTATAGTGATTATGTGGAAGTGATTGTATTTGCTAATTTTACTCCGCGTAGCGGCATGTTTAGTGACGATAGGATTGTGTATGTATATGCATGACGTCATATGATCCCTTGCTGAG", 
#          "NC_003640.1": "GAGAGGCGGCATAGTATTACCCGCCTCTCATCCCTCACCTTTCATCCCGGTCCCACCATGCCAACTGTGCAATCCACTTGTTGGGTGTTCACACTTAACTTTAAAGGGGAAATTCCTATTTTGCCCTTTAATGAACGCGTTCAGTACGCCTGTTGGCAACACGAAAGAGTGGGCCATGACCACTTACAGGGCTTTATTCAGATGAAGGCCCAACAATCTTTGGGCCAAATGAAGGCCATTATTCCTGGAGCCCATTTTGAGAAAATGAGGGCATTAAATTCAGACCAGGCTAAGGCTTACGCTATGAAGGAAGACACACGAATAGAAGGACCATGGGAGTATGGAAAATACATTAAGAAGGGATCGCATAAGAGAAAAATTATGGAGCGATTTGAAGACGACCCAGAAGAAATGAAGATTGAAGATCCCTCACTATATCGTCGTTGTCTATCAAGGAAGATGACAGAAGAACAACGATCAACTGCAGAGTGGAATTACGATATGAAGCCATGGCAAGACCAAGTCATACAAGAGATAGAAGAGACACCTGATTACCGAAAGATTATATGGGTTTACGGCCCCAAAGGAGGTGAAGGAAAGAGTACGTTTGCCAGGTACCTTTCACTCAAACAAGGTTGGGGTTATTTACCTGGTGGTCCGACGCATGACATGCTGCATATCATCAGTGGAGAACCGAAGAACAACTGGGTCTTTGACATCCCAAGAGTAGCGTCTGAGTATGTGAATTATGGTGTATTAGAACAGGTTAAAAATAGAGTTATGGTTAATACTAAGTATGAGCCAATAGTAATTAGGGATGATAATCATCCTGTTCATGTAATTGTGTTTGCTAATTGTATGCCAGACTTCACAAAAATAAGTGAAGATCGAATGAAAATAGTCCATTGTTAAGAAATATGTTGTTTTTAAAACTACGCGAAGCGAAGTCCCACATCGAATAGGTTGGAGAACTGAGCGAGGGATGAAAGCAATAAATAGG",
#          "MW959719.1": "GAATGTAAAATTTTTATAACAAATAAAAACTTTCAACAACGGATCTCTTGGCTCTCGCATCGATGAAGAACGCAGCGAAATGCGATACGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCATCTTGCGCTCTCTGGTATTCCGGAGAGCATGTCTGTTTGAGTGTCATGAATTCTTCAACCCAACTGTTTCTTGTAAACAGCTGGTGTTTGGATTCTGAGCGCTGCTGGCTTCGTGCCTAGCTCGTTCGTAATACATCAGCATCCCTAATACAAGTTTGGATTGACTTGGCGTAATAGACTATTCGCTAAGGATTCAATGTTCGCATTGAGCCAACTTAATTATGGAAGCTTCTAATTGAAAAGTCTACCTTTAGATTAGATCTCAAATCAGGCAGGATTACCCGCTGAACTTAAGCATATCAATAAGCGGAGGAAAAGAAACTAACAAGGATTCCCCTAGTAGCGGCGAGCGAAGCGGGAAAAGCTCAAATTTGTAATCTGGCGTCTACGACGTCCGAGTTGTAATCTCGAGAAGTGTTTTCCGTGATAGACCGCATACAAGTCTCTTGGAACAGAGCGTCATAGTGGTGAGAACCCAGTACACGATGCGGATGCCTATTACTTTGTGATACACTTTCGAAGAGTCGAGTTGTTTGGGAATGCAGCTCAAATTGGGTGGTAAATTCCATCTAAAGCTAAATATTGGCGAGAGACCGATAGCGAACAAGTACCGTGAGGGAAAGATGAAAAGCACTTTGGAAAGAGAGTTAACAGTACGTGAAATTGTTGGAAGGGAAACACATGCAGCCAGACTTGCTATTCGGGGCAACTCGATTGGCAGGCCCGCATCAGTTTTTCGGGGCGGAAAAGCATAGAGAGAAGGTAGCAATTTCGGTTGTGTTATAGCTCTTTATTGGATTCGCCCTGGGGGACTGAGGAACGCAGCGTGCTTTTAGCATAAGCTTCGGCTTATCCACGCTTAGGAT"}
#     # z = "exp-000000-000001-000002_14_12_2021_0_21_33.json"
#     z = "secuencies100-BIMS-test-2022-03-31_15h16m37s57794ms.json"
#     align = Alineador_multi(secuencias=y, tolerancia_atras=2, tolerancia_delante=2, json_patrones= os.path.join(x, z))
#     align.alineador()
