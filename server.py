#Py Servidor Flask
#Importaciones
from flask import Flask, render_template, request, jsonify, send_file, url_for
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from Reader import Reader
from algoritmos.BI_n_sequences_copy import basado_indices_secuencial
from algoritmos.BI_copy import basado_indices
from algoritmos.gsp import GSP
import json, os, datetime, csv, re, glob
# import Alineador_Patornes
import Generador_motifs
from datetime import datetime
import pandas as pd
#Variables

app = Flask(__name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'tmp')
EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')
EXP_FOLDER_JSON_PATRONES = join(EXP_FOLDER, 'json')
EXP_FOLDER_CSV_PATRONES = join(EXP_FOLDER, 'CSV')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CURRENTFILEJSON = ''
CURRENTFILECSV = ''
CURRENTFILE = ''

# def setCurrentFile(current):
#     global CURRENTFILE
#     CURRENTFILE = current
    
# def getCurrentFile():
#     return CURRENTFILE

@app.route('/')#decorador
def index(): 
    """
    Renderiza la pagina principal

    Returns:
        template hmtl : renderiza el archivo html 
    """
    return render_template('index.html')


@app.route('/analisisText', methods=['GET', 'POST'])
def analisisTxt():
    # print(request.is_json)
    """
    Recibe los datos de peticion web en json del tipo de entrada en Texto, ejecuta el algoritmo solitado y obtiene 
    los motifs y patrones frecuentes de las secuencias de ADN de entrada
    
    Params (json) : 
        min_sup (int) : El valor minimo soporte (umbral) para patrones frecuentes
        algoritmo (str) : Indica que algoritmo será utilizado
        keys_sequences (list <str>) : Es una lista de los id's de las secuencias de ADN utilizadas en el analisis
        sequence (list <str> ) : Es la lista de secuencias de ADN
        input (str) : Es el tipo de entrada de datos (Manual/Texto)
        longitud_minima (int) : Es la longitud minima que tiene que tener una subsecuencia para que se considere un motif
        tolerancia_delante (int) : Es la tolerancia de nucleotidos hacia la derecha para unir dos patrones frecuentes
        tolerancia_atras (int) : Es la tolerancia de nucleotidos hacia la izquierda para unir dos patrones frecuentes
        imprimir_logo (boolean) : Permite imprimir los graficos (logos) de los motifs
    
    Returns:
        json : La información detallada de los motifs y patrones frecuentes 
    
    Notas:
        - Se toma los detalles de la ejecución para llevar un registro
        - Esta funcion es solo para el modo de entrada 'Texto o Manual'
    """
    dt1 = datetime.now()
    
    request_json = request.get_json()
    min_sup = int(request_json[0]['min_sup'])
    algorithm = request_json[0]['algoritmo']
    keys_seqs = request_json[0]['keys_sequences']
    sequences = request_json[0]['sequence']
    input_type = request_json[0]['input']
    longitud_minima = int(request_json[0]['longtud_minina'])
    tolerancia_delante = int(request_json[0]['tolerancia_delante'])
    tolerancia_atras = int(request_json[0]['tolerancia_atras'])
    imprimir_logo = bool(request_json[0]["imprimir_logo"])
    print(imprimir_logo)
    
    patrones, motifs = find_motifs(sequences, min_sup, input_type, 'texto-plano', algorithm, keys_seq=keys_seqs,
                                           tolerancia_atras=tolerancia_atras, tolerancia_frente=tolerancia_delante, longitud_minina=longitud_minima, imprimir_logo=imprimir_logo)

    
    # return jsonify(patrones)
    if len(patrones['Patrones']) > 0:
        files_generator(patrones, tolerancia_delante,
                        tolerancia_atras, longitud_minima, imprimir_logo)
        

        dt2 = datetime.now()
        df = pd.json_normalize({
            "Nombre_archivo": "Texto-Secuencias",
            "Peso_archivo": (sum([len(x) for x in sequences]) / 1000000),
            "Num_aprox_bp": sum([len(x) for x in sequences]),
            "Num_secuencias": len(keys_seqs),
            "Secuencias": ','.join(keys_seqs),
            "Lon_secuencias": ",".join(str(len(i)) for i in sequences),
            "Tipo_entrada": 'texto-plano',
            "Algoritmo": algorithm,
            "Min_sup": min_sup,
            "Tolerancia_delante": tolerancia_delante,
            "Tolerancia_detras": tolerancia_atras,
            "Longitud_minima": longitud_minima,
            "Impresion_logo": imprimir_logo,
            "Num_patrones": len(patrones['Patrones']),
            "Longitud_max_patrones": patrones['Patrones'][0]["Longitud"],
            "Num_motifs": len(motifs["Alineaciones"]),
            "Longitud_max_motifs": motifs["Alineaciones"][0]["longitud_motif"],
            'Inicio': '{}'.format(dt1),
            'Fin': '{}'.format(dt2),
            'Duracion': dt2-dt1,
            "Nombre_resultados": CURRENTFILE
        })
        
        if os.path.getsize(join(EXP_FOLDER, 'registro.csv')) == 0:
            df.to_csv(join(EXP_FOLDER,'registro.csv'), mode='a', header=True)
        else:
            df.to_csv(join(EXP_FOLDER,'registro.csv'), mode='a', header=False)
        # return jsonify(patrones)
        return jsonify({"Patrones_Frecuentes": patrones, "Motifs": motifs})
    else:
        return jsonify({'Message_error':'Ejecución sin resultados'})

        

@app.route('/analisisFile', methods=['GET', 'POST'])
def analisisFile():
    # request.get_data()
    """
    Recibe los datos de peticion web en json del tipo de entrada en Archivo, ejecuta el algoritmo solitado y obtiene
    los motifs y patrones frecuentes de las secuencias de ADN de entrada

    Params (json) :
        min_sup (int) : El valor minimo soporte (umbral) para patrones frecuentes
        algoritmo (str) : Indica que algoritmo será utilizado
        keys_sequences (list <str>) : Es una lista de los id's de las secuencias de ADN utilizadas en el analisis
        sequence (list <str> ) : Es la lista de secuencias de ADN
        input (str) : Es el tipo de entrada de datos (Archivo)
        longitud_minima (int) : Es la longitud minima que tiene que tener una subsecuencia para que se considere un motif
        tolerancia_delante (int) : Es la tolerancia de nucleotidos hacia la derecha para unir dos patrones frecuentes
        tolerancia_atras (int) : Es la tolerancia de nucleotidos hacia la izquierda para unir dos patrones frecuentes
        imprimir_logo (boolean) : Permite imprimir los graficos (logos) de los motifs

    Returns:
        json : La información detallada de los motifs y patrones frecuentes

    Notas:
        - Se toma los detalles de la ejecución para llevar un registro
        - Esta funcion es solo para el modo de entrada 'Archivo'
        - La forma de la solicitud web es diferente que en la funcion analisisTxt
    """

    dt1 = datetime.now()
    
    algorithm = request.form["Algoritmo"]
    print(algorithm)
    min_sup = int(request.form["min_sup"])
    file = request.files['file']
    input_type = request.form['input']
    longitud_minima = int(request.form['longtud_minina'])
    tolerancia_delante = int(request.form['tolerancia_delante'])
    tolerancia_atras = int(request.form['tolerancia_atras'])
    imprimir_logo = bool(request.form['imprimir_logo'])
    print(imprimir_logo)
    
    patrones = {}
    # 
    # print()
    # print(request.form["file"])
    fn = file.name
    print('nombre',fn)
    filename  = secure_filename(file.filename)
    
    input_type = input_type
    
    absolutepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(absolutepath)
    file.close()
    head, tail =  os.path.split(filename)
    tail = tail.replace(".fasta","")
    tail = tail.replace(".","")
    tail = tail.replace('-','_')
    input_name = tail
    print(input_name)
    read = Reader(absolutepath)
    list_sequences, head_sequences, keys_seq = read.run()
    patrones, motifs = find_motifs(list_sequences, min_sup, input_type, input_name, algorithm, keys_seq, tolerancia_atras, tolerancia_delante, longitud_minima, imprimir_logo)
    if len(patrones['Patrones']) > 0:
        files_generator(patrones, tolerancia_delante, tolerancia_atras, longitud_minima, imprimir_logo)
        # return jsonify(patrones)
        dt2 = datetime.now()
        df = pd.json_normalize({
            "Nombre_archivo": tail+".fasta",
            "Peso_archivo":  (os.path.getsize(absolutepath)/1000000),
            "Num_Aprox_bp": sum([len(x) for x in list_sequences]),
            "Num_Secuencias": len(keys_seq),
            "Secuencias": ','.join(keys_seq),
            "Lon_secuencias": ",".join(str(len(i)) for i in list_sequences),
            "Tipo_entrada": 'texto-plano',
            "Algoritmo": algorithm,
            "Min_sup": min_sup,
            "Tolerancia_delante": tolerancia_delante,
            "Tolerancia_detras": tolerancia_atras,
            "Longitud_minima": longitud_minima,
            "Impresion_logo": imprimir_logo,
            "Num_Patrones": len(patrones['Patrones']),
            "Longitud_max_patrones": patrones['Patrones'][0]["Longitud"],
            "Num_motifs": len(motifs["Alineaciones"]),
            "Longitud_max_motifs": motifs["Alineaciones"][0]["longitud_motif"],
            'Inicio': '{}'.format(dt1),
            'Fin': '{}'.format(dt2),
            'Duracion': dt2-dt1,
            "Nombre_Resultados": CURRENTFILE
        })
        
        if os.path.getsize(join(EXP_FOLDER, 'registro.csv')) == 0:
            df.to_csv(join(EXP_FOLDER,'registro.csv'), mode='a', header=True)
        else:
            df.to_csv(join(EXP_FOLDER,'registro.csv'), mode='a', header=False)
        
        
        return jsonify({"Patrones_Frecuentes": patrones, "Motifs": motifs})
    else:
        return jsonify({'Message_error':'Ejecución sin resultados'})
    # return jsonify([{"Encabezados": head_sequences, "Candidatos": candidates}])

def find_motifs(list_sequences= [], min_sup = 0, input_type='', input_name = '', algorithm = '', keys_seq=[], tolerancia_atras = 2, tolerancia_frente = 2, longitud_minina=6, imprimir_logo = False): 
     
    """Funcion que contiene los algoritmos para hallar motifs

    Params:
        list_sequences = [] (list <str>) : Es la lista de secuencias de ADN
        min_sup = 2 (int) : El valor minimo soporte (umbral) para patrones frecuentes
        input_type = '' (str) : Es el tipo de entrada de datos (Archivo o Entrada Manual)
        input_name = '' (str) : Es el nombre del archivo en que caso que se utilize el modo 
        algorithm = '' (str) : Indica que algoritmo será utilizado
        keys_seq = [] (list <str>) : Es una lista de los id's de las secuencias de ADN utilizadas en el analisis
        tolerancia_atras = 2 (int) : Es la tolerancia de nucleotidos hacia la izquierda para unir dos patrones frecuentes
        tolerancia_frente = 2 (int) : Es la tolerancia de nucleotidos hacia la derecha para unir dos patrones frecuentes
        longitud_minina = 6 (int) : Es la longitud minima que tiene que tener una subsecuencia para que se considere un motif
        imprimir_logo (boolean) : Permite imprimir los graficos (logos) de los motifs
    
    Varibles:
        patrones  = {} (dict) 
        motifs = {} (dict) 
     
    Returns:
        patrones  = {} (dict) : Retorna la información de los patrones frecuentes a partir del analisis de las secuencias de ADN.
        motifs = {} (dict) : Retorna la información de los motifs a partir del analisis de las secuencias de ADN.
    
    Notes:
        - Cada algoritmo llama a su función correspondiente.
    """
    patrones = {}
    motifs = {}
    
    if algorithm == 'bi':
        bi = basado_indices(inputType = input_type, inputName = input_name)
        bi.set_initDateTime(datetime.now())
        for i in range(len(list_sequences)):
            bi.set_sequence(list_sequences[i])
            bi.set_minsup(min_sup)
            bi.set_seqCode(i+1)
            bi.set_pos(bi.find_pos())
            bi.run()
        
        bi.set_finDateTime(datetime.now())
        bi.set_keys_seqs(keys_seq)

        patrones.update(bi.info_patrones())


    elif algorithm == 'bi+':
        head, tail = os.path.split(input_name)
        tail = tail.replace(".fasta", "")
        tail = tail.replace(".", "")
        
        bis = basado_indices_secuencial(
            list_sequences, min_sup, inputType=input_type, inputName=input_name)
        bis.set_initDateTime(datetime.now())
        bis.set_pos(bis.find_pos())
        bis.run()
        bis.set_finDateTime( datetime.now())
        bis.set_keys_seqs(keys_seq) #aunque sea mandar un listado de numeros cuando sean manual
        
        patrones = bis.info_patrones()
        
        # apm = Generador_motifs.Generador(
        #     secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_delante=tolerancia_frente, tolerancia_atras=tolerancia_atras, longitud_minima_cre=longitud_minina, json_patrones=patrones)
        # motifs.update(apm.alineador())

    elif algorithm == 'gsp':
        gsp = GSP(list_sequences, min_sup,
                  inputType=input_type, inputName=input_name)
        gsp.set_initDateTime( datetime.now())
        gsp.run()
        gsp.set_finDateTime( datetime.now())
        gsp.set_keys_seqs(keys_seq)
        patrones = gsp.info_patrones()
        # apm = Generador_motifs.Generador(
        #     secuencias=dict(zip(keys_seq, list_sequences)),
        #     tolerancia_delante= tolerancia_frente, 
        #     tolerancia_atras= tolerancia_atras, longitud_minina_cre= longitud_minina, json_patrones=patrones)
        # motifs.update(apm.alineador())
    
    else:
        print('Error, sin algoritmo selecioando')
    
    patrones["Patrones"].sort(key=lambda dicts: dicts["Longitud"], reverse=True)
    # list_info.sort(key=lambda dicts: dicts["longitud_motif"], reverse=True)
    
    alineador = Generador_motifs.Generador(
        secuencias=dict(zip(keys_seq, list_sequences)),
        tolerancia_delante=tolerancia_frente,
        tolerancia_atras=tolerancia_atras, 
        longitud_minima_cre = longitud_minina, 
        json_patrones=patrones, 
        imprimir_logo= imprimir_logo)
    motifs.update(alineador.alineador())

        
    return patrones, motifs


def files_generator(patrones={}, tolerancia_delante=2, tolerancia_detras=2, longitud_min=6, logos=False):
    global CURRENTFILECSV, CURRENTFILEJSON, CURRENTFILE
    
    x = "EXP_"+str(patrones['Configuracion']['Entrada']) + '_'+ str(patrones['Configuracion']['Tipo_Entrada']) + '_'+str(patrones['Configuracion']['Siglas']) + '_' +str(patrones['Configuracion']['Min_sup']) + '_' + str(tolerancia_delante) + '_'+ str(tolerancia_detras)+'_'+ str(longitud_min) + '_'+str(logos)+'_'
        
    
    dt =  datetime.strptime(patrones['Configuracion']['Fecha_Hora_Inicio'], '%Y-%m-%d %H:%M:%S.%f')
    
    x += str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)+"_"+str(dt.hour)+"-"+str(dt.minute)+"-"+str(dt.second)
    
    CURRENTFILE = x
    
    # sdt = str(patrones['Configuracion']['Duracion'])
    # x1 = [i for i in re.split("[ ,:.]",sdt) if i.isdigit() or i.isdecimal()]

    # if len(x1) < 5:
    #     x1.insert(0,'0')
    #     x1.append('0')
    
    # seconds = (int(x1[0])*86400) + (int(x1[1])*3600) + (int(x1[2])*60) + int(x1[3])
    # print(sdt,' ', x1[4])
    # x += 'D-'+str(seconds)+'&'+x1[4]
    
    # print(x)
    
    # keys = "-".join(k for k in keys_seqs)
    # dt =  datetime.now()
    # n = str(dt.day)+"_"+str(dt.month)+"_" +str(dt.year)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
    # EXP_FOLDER+"/exp-"+keys+"_"+n+".json"
    # if len(keys_seqs)!=0:
    #     # filenamejson = os.path.join(EXP_FOLDER,"json\\", "exp-"+keys+"_"+n)  #+".json")
    #     # filenamecsv = os.path.join(EXP_FOLDER,"csv\\", "exp-"+keys+"_"+n)  #+".json")  
    # else:
    #     filenamejson = os.path.join(EXP_FOLDER,"json\\","exp-txt"+"_"+n) #+".json")
    #     filenamecsv = os.path.join(EXP_FOLDER, "csv\\", "exp-txt"+"_"+n)  # +".json")
    #     CURRENTFILEJSON = filenamejson+".json"
    #     CURRENTFILECSV = filenamecsv+".csv"
    
    filenamejson = os.path.join(EXP_FOLDER, "json", x)  
    print(filenamejson)
    filenamecsv = os.path.join(EXP_FOLDER, "csv", x)  
    CURRENTFILEJSON = filenamejson+".json"
    CURRENTFILECSV = filenamecsv+".csv"    
    # print(filename)
    # CURRENTFILE = filename
    # print(CURRENTFILE)
    #print(os.scandir(os.path.join(EXP_FOLDER)))
    # patrones = json.dumps(patrones, sort_keys=True, indent=4)
    try:
        with open(filenamejson+(".json"),'x') as file_object_json:
            json.dump(patrones, file_object_json, sort_keys = True, indent = 4)

        with open(filenamecsv+(".csv"), 'x') as file_object_csv:
            writer = csv.writer(file_object_csv)
            
            for kp, vp in patrones.items() :
                if kp == "Configuracion":
                    writer.writerow([kp])
                    for k,v in vp.items():
                        writer.writerow(['',k, v])
                    writer.writerow(['\n'])
        
                elif kp == "Patrones":
                    writer.writerow([kp])
                    writer.writerow([list(vp[0].keys())])
                    for i in range(len(vp)):
                        writer.writerow([vp[i]["Patron"], vp[i]["Longitud"], vp[i]["Ocurrencias"]])
                        for elem in vp[i]["Posiciones"]:
                            writer.writerow(['','','',elem])
                            
                        writer.writerow(['\n'])
            
            
    except IOError as e:                
        return (f'Hubo un error en la escritura del archivo \n'+str(e))
    except FileNotFoundError as e:
        return (f'Hubo un error en el archivo: No se encontro o no existe. \n'+str(e))
    except FileExistsError as e:
        return (f'Hubo un error en el archivo: '+str(e)+'\n')
    else:
        print("Success!, file created")


@app.route('/mostrarArchivos', methods=['GET', 'POST'])
def mostrarFicheros():
    # archivos = None
    
    # print(os.path.join(EXP_FOLDER, "json"+os.path.sep))
    try:
        # archivos = glob.glob(os.path.join(EXP_FOLDER, "json"+os.path.sep)+'*.json')
        # archivos.sort(key = os.path.getctime, reverse=True)
        # archivos = [os.path.splitext(str(archivo).replace(os.path.join(EXP_FOLDER, "json"+os.path.sep),''))[0] for archivo in archivos]
        
        # print(archivos)
        # with os.scandir(os.path.join(EXP_FOLDER, "json"+os.path.sep)) as ficheros:
            
        #     # ficheros.sort(key = os.path.getctime())
        #     # ficheros.sort(key = os.path.getctime())
        #     # print(ficheros)
            
        #     r_value = [os.path.splitext(f.name)[0]  for f in ficheros]
        #     print(r_value)
            # r_value.sort(key = os.path.getctime)
            
            # for f in ficheros[::-1]:
            #     # print(f.name)
            #     # print(list(os.path.splitext(f.name)))
                
            #     r_value.append(os.path.splitext(f.name)[0])
        df = pd.read_csv(join(EXP_FOLDER, 'registro.csv'),  header=0)
        archivos = json.loads(df.to_json(orient="values"))

    except FileNotFoundError as e:
        return (f'Hubo un error en la lectura de ficheros: No se encontro o no existe. \n'+str(e), 'Error: archivo no encontrado')
    except FileExistsError as e:
        return (f'Hubo un error en la lectura de ficheros: '+str(e)+'\n', 'Error dentro del archivo')
    else:
        # r_value.sort(key=os.path.getctime())
        return jsonify(archivos)

@app.route('/mostrarArchivoExp', methods=['GET', 'POST'])
def mostrarArchivoAct(): #filename=''):
    fn = request.get_json()['filename']
    datareturn = ''
    # print(fn)
    try:
        with open(os.path.join(EXP_FOLDER, "json", fn)) as file_object:
            txt = file_object.readlines()
        
        # print(txt)
        
        for t in txt:
            datareturn += t
        
    except FileExistsError as e:
        return (f'Hubo un error en la lectura de ficheros: '+str(e)+'\n'), 'Error dentro del archivo'
    else:
        return  datareturn 
# @app.route('/descargaArchivo', methods = ['GET', 'POST'])
# def descargar():
#     if app.debug == True:
#         print("request:", str(request.get_json()))
    
    
#     request_file = request.get_json()
#     print(request_file)
#     filename = request_file[0]['filename']
#     filetype = request_file[0]['filetype']

#     if filetype == 'json':
#         return send_file(os.path.join(EXP_FOLDER, filename), as_attachment=True)
#     elif filetype == 'csv':
#         return send_file(os.path.join(EXP_FOLDER, filename), as_attachment=True)
#     elif filetype == 'currentJSON':
#         return send_file(CURRENTFILE, as_attachment=True)
#     elif filetype == 'currentCSV':
#         return send_file(CURRENTFILE)
#     else:
#         return jsonify({'Error': 'Error en el proceso'})

    # return send_file(os.path.join(EXP_FOLDER, filename), as_attachment=True, attachment_filename=filename, mimetype=filetype)

    
@app.route('/descarga/experimentos/<filetype>/', methods=['GET', 'POST'])
@app.route('/descarga/experimentos/<filetype>/<filename>/', methods=['GET', 'POST'])
def getExpetimento(filetype = "currentJSON", filename = ""):
    if app.debug == True:
        print('type',filetype, ' name', filename)
        print('descarga json', CURRENTFILEJSON)
        print('descarga csv', CURRENTFILECSV)
        print(EXP_FOLDER)
        #os.path.join(EXP_FOLDER, "json", x)
    if filetype == 'currentJSON':
        return send_file(CURRENTFILEJSON, as_attachment=True)
    elif filetype == 'currentCSV':
        return send_file(CURRENTFILECSV, as_attachment=True)
    elif filetype == 'currentJSONMotif':
        return send_file(os.path.join(EXP_FOLDER, "motifs_json", "MOTIFS_"+CURRENTFILE)+'.json', as_attachment=True)
    elif filetype == 'currentXLSX':
        return send_file(os.path.join(EXP_FOLDER, "motifs_excel", "MOTIFS_"+CURRENTFILE)+'.xlsx', as_attachment=True)
    elif filetype == 'JSON':
        return send_file(os.path.join(EXP_FOLDER,'json\\', filename)+'.json', as_attachment=True)
    elif filetype == 'CSV':
        return send_file(os.path.join(EXP_FOLDER,'csv\\', filename)+'.csv', as_attachment=True)
    elif filetype == 'JSONMotif':
        return send_file(os.path.join(EXP_FOLDER, 'motifs_json\\', "MOTIFS_"+filename)+'.json', as_attachment=True)
    elif filetype == 'XLSX':
        return send_file(os.path.join(EXP_FOLDER,'motifs_excel\\', "MOTIFS_"+filename)+'.xlsx', as_attachment=True)
    
    else:
        return -1 
        # return send_from_directory(directory= EXP_FOLDER, filename = CURRENTFILENAME)
    


if __name__ == '__main__':
    app.run(debug = True)  #port=8000, 


