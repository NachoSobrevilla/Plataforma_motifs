from flask import Flask, render_template, request, jsonify
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from Reader import Reader
from algoritmos.BI_n_sequences_copy import basado_indices_sequencial
from algoritmos.BI_copy import basado_indices
from algoritmos.gsp import GSP
import json
import os
import datetime
app = Flask(__name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'tmp')
EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')#decorador
def index(): #funcion para mostrar la pagina
    return render_template('index.html')


@app.route('/analisisText', methods=['GET', 'POST'])
def analisisTxt():
    # print(request.is_json)
    request_json = request.get_json()
    min_sup = int(request_json[0]['min_sup'])
    algorithm = request_json[0]['algoritmo']
    sequences = request_json[0]['sequence']
    candidates = []
    patrones = {}

    if algorithm == 'bi':
        if len(sequences) == 1:
            bi = basado_indices(sequences, min_sup)
            bi.set_pos(bi.find_pos())
            bi.run()
            patrones.update(bi.info_patrones())
        else: 
            pass

    elif algorithm == 'bi+':
        bis = basado_indices_sequencial(sequences, min_sup)
        bis.set_pos(bis.find_pos())
        bis.run()
        bis.set_keys_seqs()
        patrones = bis.info_patrones()

    elif algorithm == 'GSP':
        gsp = GSP(sequences,min_sup)
        gsp.run()
        patrones = gsp.info_candidates()

    else:
        pass

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
def analisisFle():
    # request.get_data()
    algorithm = request.form["Algoritmo"]
    min_sup = int(request.form["min_sup"])
    file = request.files['file']
    patrones = {}
    # 
    # print()
    # print(request.form["file"])
    
    filename  = secure_filename(file.filename)
    absolutepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(absolutepath)
    file.close()

    read = Reader(absolutepath)
    list_sequences, head_sequences, keys_seq = read.run()
    if algorithm == 'bi':
        if len(list_sequences) == 1:
            bi = basado_indices(list_sequences, min_sup)
            bi.set_pos(bi.find_pos())
            bi.run()
            patrones.update(bi.get_infopos())
            # candidates = bi.run()
        else:
            pass

    elif algorithm == 'bi+':
        bis = basado_indices_sequencial(list_sequences, min_sup)
        bis.set_pos(bis.find_pos())
        bis.run()
        print(bis.get_patrones())
        bis.set_keys_seqs(keys_seq)
        patrones = bis.info_patrones()

    
    elif algorithm == 'gsp':
        gsp = GSP(list_sequences,min_sup)
        gsp.run()
        patrones = gsp.info_candidates()
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
    files_generator(patrones, keys_seq)
    
    return jsonify(patrones)
    # return jsonify([{"Encabezados": head_sequences, "Candidatos": candidates}])


def files_generator(patrones={}, keys_seqs = []):
    keys = "-".join(k for k in keys_seqs)
    dt = datetime.datetime.now()
    n = str(dt.day)+"_"+str(dt.month)+"_" +str(dt.year)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
    # EXP_FOLDER+"/exp-"+keys+"_"+n+".json"
    if len(keys_seqs)!=0:
        filename = os.path.join(EXP_FOLDER, "exp-"+keys+"_"+n+".json")
    else:
        filename = os.path.join(EXP_FOLDER, "exp-txt"+"_"+n+".json")
    print(filename)
    #print(os.scandir(os.path.join(EXP_FOLDER)))
    try:
        with open(filename,'x') as file_object:
            json.dump(patrones, file_object)

        
    except FileNotFoundError as e:
        return (f'Hubo un error en el archivo {filename}: No se encontro o no existe. \n'+str(e)), 'Error: archivo no encontrado' 
    except FileExistsError as e:
        return (f'Hubo un error en el archivo {filename}: '+str(e)+'\n'), 'Error dentro del archivo'
    else:
        print("Success!, file created")


@app.route('/mostrarArchivos', methods=['GET', 'POST'])
def mostrarFicheros():
    r_value = []
    try:
        with os.scandir(EXP_FOLDER) as ficheros:
            # ficheros.sort(os.path.getctime())
            for f in ficheros:
                r_value.append(f.name)
    except FileNotFoundError as e:
        return (f'Hubo un error en la lectura de ficheros: No se encontro o no existe. \n'+str(e)), 'Error: archivo no encontrado'
    except FileExistsError as e:
        return (f'Hubo un error en la lectura de ficheros: '+str(e)+'\n'), 'Error dentro del archivo'
    else:
        return jsonify(r_value[::-1])

if __name__ == '__main__':
    app.run() #port=8000, debug = flase
