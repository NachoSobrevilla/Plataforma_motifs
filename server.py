#Py Servidor Flask
#Importaciones
from types import MethodType
from flask import Flask, render_template, request, jsonify, send_file, url_for
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename, send_from_directory
from werkzeug.wrappers import response
from Reader import Reader
from algoritmos.BI_n_sequences_copy import basado_indices_sequencial
from algoritmos.BI_copy import basado_indices
from algoritmos.gsp import GSP
import json, os, datetime, csv, re, pandas as pd, glob
#Variables

app = Flask(__name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'tmp')
EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CURRENTFILEJSON = ''
CURRENTFILECSV = ''

# def setCurrentFile(current):
#     global CURRENTFILE
#     CURRENTFILE = current
    
# def getCurrentFile():
#     return CURRENTFILE

@app.route('/')#decorador
def index(): #funcion para mostrar la pagina
    return render_template('index.html')


@app.route('/analisisText', methods=['GET', 'POST'])
def analisisTxt():
    # print(request.is_json)
    request_json = request.get_json()
    min_sup = int(request_json[0]['min_sup'])
    algorithm = request_json[0]['algoritmo']
    keys_seqs = request_json[0]['keys_sequences']
    sequences = request_json[0]['sequence']
    input_type = request_json[0]['input']

    # input_type =  input_type + str(datetime.datetime.now())
    
    # print("Algoritmos:",algorithm)
    
    # patrones = {}

    # if algorithm == 'bi':
    #     bi = basado_indices(sequences, min_sup)
    #     bi.set_pos(bi.find_pos())
    #     bi.run()
    #     patrones.update(bi.info_patrones())

    # elif algorithm == 'bi+':
    #     bis = basado_indices_sequencial(sequences, min_sup)
    #     bis.set_pos(bis.find_pos())
    #     bis.run()
    #     bis.set_keys_seqs()
    #     patrones = bis.info_patrones()

    # elif algorithm == 'gsp':
    #     print('en gsp')
    #     gsp = GSP(sequences, min_sup, inputType=input_type, debug=True)
    #     gsp.run()
    #     patrones = gsp.info_candidates()
        
    # else:
    #     pass
    

    patrones  =  find_motifs(sequences, min_sup, input_type, 'texto-plano', algorithm, keys_seq= keys_seqs)
    files_generator(patrones)
    return jsonify(patrones)
    # return json.dumps({'Candidatos':candidates})

    # sequence = request.get_data()
    # print(request_json)
    
    # if request_json:
    #     print(request_json)
    #     return 
    # else:
    #     return json.dumps({{'Error': 'Error en el proceso'}})
        

@app.route('/analisisFile', methods=['GET', 'POST'])
def analisisFile():
    # request.get_data()
    algorithm = request.form["Algoritmo"]
    print(algorithm)
    min_sup = int(request.form["min_sup"])
    file = request.files['file']
    input_type = request.form['input']
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
    input_name = filename.replace('.fasta','')
    input_name = input_name.replace('_','-')
    print(input_name)
    read = Reader(absolutepath)
    list_sequences, head_sequences, keys_seq = read.run()
    # if algorithm == 'bi':
    #     for sequences in list_sequences: #Modificar
    #         # bi = basado_indices(list_sequences[0], min_sup, inputType= input_type)
    #         bi = basado_indices(sequences, min_sup, inputType= input_type)
    #         bi.set_pos(bi.find_pos())
    #         bi.run()
    #         patrones.update(bi.get_infopos())
    #         # candidates = bi.run()

    # elif algorithm == 'bi+':
    #     bis = basado_indices_sequencial(list_sequences, min_sup, inputType=input_type)
    #     bis.set_pos(bis.find_pos())
    #     bis.run()
    #     print(bis.get_patrones())
    #     bis.set_keys_seqs(keys_seq)
    #     patrones = bis.info_patrones()

    
    # elif algorithm == 'gsp':
    #     gsp = GSP(list_sequences, min_sup, inputType=input_type)
    #     gsp.run()
    #     patrones = gsp.info_candidates()
        # print(patrones)
        # candidates = bis.run()

    # Metodo de busqueda binaria no continua 
    # print(list, head)
    # print(request.get_data(), '', request.is_json, request.files , request)
    
    # file = request.get_json()
    # print(file)
    # if file:
    #     return json.dumps({'Success': 'Proceso con exito'})
    # else:
    #     return json.dumps({{'Error': 'Error en el proceso'}})

    # r_value = json.dumps({"Encabezados":head_sequences, "Candidatos":candidates})
    # print(type(r_value))
    # print(r_value)
    # return r_value, 200, {"Content-Type": "application/json"}
    patrones = find_motifs(list_sequences, min_sup, input_type, input_name, algorithm, keys_seq)
    if len(patrones['Patrones']) > 0:
        files_generator(patrones, keys_seq)
        return jsonify(patrones)
    else:
        return jsonify({'Message_error':'Ejecución sin resultados'})
    # return jsonify([{"Encabezados": head_sequences, "Candidatos": candidates}])

def find_motifs(list_sequences= [], min_sup = 0, input_type='', input_name = '', algorithm = '', keys_seq=[]): 
    '''Funcion que contiene los algoritmos para hallar motifs'''
    patrones = {}
    if algorithm == 'bi':
        bi = basado_indices(inputType = input_type, inputName = input_name)
        bi.set_initDateTime(datetime.datetime.now())
        for i in range(len(list_sequences)):
            bi.set_sequence(list_sequences[i])
            bi.set_minsup(min_sup)
            bi.set_seqCode(i+1)
            bi.set_pos(bi.find_pos())
            bi.run()
        
        bi.set_finDateTime(datetime.datetime.now())
        bi.set_keys_seqs(keys_seq)
        # bi = basado_indices(list_sequences[0], min_sup, inputType= input_type)
        # bi = basado_indices(list_sequences, min_sup, inputType=input_type)
        # bi.set_pos(bi.find_pos())
        # bi.run()
        patrones.update(bi.info_patrones())
        # candidates = bi.run()

    elif algorithm == 'bi+':
        bis = basado_indices_sequencial(
            list_sequences, min_sup, inputType=input_type, inputName=input_name)
        bis.set_initDateTime(datetime.datetime.now())
        bis.set_pos(bis.find_pos())
        bis.run()
        bis.set_finDateTime(datetime.datetime.now())
        bis.set_keys_seqs(keys_seq) #aunque sea mandar un listado de numeros cuando sean manual
        patrones = bis.info_patrones()

    elif algorithm == 'gsp':
        gsp = GSP(list_sequences, min_sup,
                  inputType=input_type, inputName=input_name)
        gsp.set_initDateTime(datetime.datetime.now())
        gsp.run()
        gsp.set_finDateTime(datetime.datetime.now())
        gsp.set_keys_seqs(keys_seq)
        patrones = gsp.info_patrones()
    
    else:
        print('Error, sin algoritmo selecioando')
        
    return patrones

# def json_generator(algoritmo, min_sup, inputType, nomArch, keySeq, sequences):
#     def key_seq(x): return keySeq[x] if len(keySeq) else x
#     return {
#             "Configuracion": {
#                 "Algoritmo": algoritmo,
#                 "Min_sup": min_sup,
#                 "Tipo_Entrada": inputType,
#                 "Entrada": nomArch,
#                 "Sequencias_ananlizadas": str(keySeq),
#                 "Num_Sequencias_ananlizadas": len(self.get_ds()),
#                 "Num_Patrones_hallados": len(self.get_patrones()),
#                 "Fecha_Hora_Inicio": '{}'.format(self.get_initDateTime()),
#                 "Fecha_Hora_Fin": '{}'.format(self.get_finDateTime()),
#                 "Duracion": str(self.get_finDateTime() - self.get_initDateTime())
#             },
#             "Patrones": [{
#                 "Patron": key,
#                 "Longitud": len(key),
#                 "Ocurrencias": len(values),
#                 "Posiciones": [{
#                     "sequencia": key_seq(seq),
#                     "posicion": p+1}
#                     for seq, pos in values.items() for p in pos]
#             }for key, values in self.patrones.items()]
#     }

def files_generator(patrones={}, keys_seqs = []):
    global CURRENTFILECSV, CURRENTFILEJSON
    
    x = "EXP_"+str(patrones['Configuracion']['Siglas']) + '_' +\
        str(patrones['Configuracion']['Min_sup']) + '_' + \
        str(patrones['Configuracion']['Tipo_Entrada']) + '_'+ \
        str(patrones['Configuracion']['Entrada']) + '_'+ \
        str(patrones['Configuracion']['Num_Sequencias_ananlizadas']) + '_'+ \
        str(patrones['Configuracion']['Num_Patrones_hallados']) + '_'
    
    dt = datetime.datetime.strptime(patrones['Configuracion']['Fecha_Hora_Inicio'], '%Y-%m-%d %H:%M:%S.%f')
    
    x += str(dt.day)+"d"+str(dt.month)+"d"+str(dt.year)+"&"+str(dt.hour)+"-"+str(dt.minute)+"-"+str(dt.second)+"_"
    
    sdt = str(patrones['Configuracion']['Duracion'])
    x1 = [i for i in re.split("[ ,:.]",sdt) if i.isdigit() or i.isdecimal()]
    
    if len(x1) < 5:
        x1.insert(0,'0')
        x1.append('0')
    
    seconds = (int(x1[0])*86400) + (int(x1[1])*3600) + (int(x1[2])*60) + int(x1[3])
    print(sdt,' ', x1[4])
    x += 'D-'+str(seconds)+'&'+x1[4]
    
    # print(x)
    
    # keys = "-".join(k for k in keys_seqs)
    # dt = datetime.datetime.now()
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
    archivos = None
    # print(os.path.join(EXP_FOLDER, "json"+os.path.sep))
    try:
        archivos = glob.glob(os.path.join(EXP_FOLDER, "json"+os.path.sep)+'*.json')
        archivos.sort(key = os.path.getctime, reverse=True)
        archivos = [os.path.splitext(str(archivo).replace(os.path.join(EXP_FOLDER, "json"+os.path.sep),''))[0] for archivo in archivos]
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
        
    if filetype == 'currentJSON':
        return send_file(CURRENTFILEJSON, as_attachment=True)
    elif filetype == 'currentCSV':
        return send_file(CURRENTFILECSV, as_attachment=True)
    elif filetype == 'JSON':
        return send_file(os.path.join(EXP_FOLDER,'json\\', filename), as_attachment=True)
    elif filetype == 'CSV':
        return send_file(os.path.join(EXP_FOLDER,'csv\\', filename), as_attachment=True)
    else:
        return -1 
        # return send_from_directory(directory= EXP_FOLDER, filename = CURRENTFILENAME)
    


if __name__ == '__main__':
    app.run(debug = True)  #port=8000, 


