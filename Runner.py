
# from os import truncate
from prefixspan import PrefixSpan
import glob
import imp
import sys
import os
from click import FileError, exceptions
from numpy import False_
import imp
from tqdm import tqdm
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import time
from flask.json import jsonify
import Reader as r
from algoritmos import BI_n_sequences_copy, BI_copy, gsp
from datetime  import datetime, timedelta
import server as s
import re
import pandas as pd
import json
import Alineador_Patornes, Generador_motifs

x = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\Secuencias ADN\\"
# y = "sequence_citrus_8_150M.fasta"#"test_sequence.fasta"   
z = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\"
z1 = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\motifs\\"
# x1 = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud similar\\"
x1 = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\Empredas por trabajos anteriores\\longitud diferente\\"
y1 = "sequence_XM_011544263.fasta"



def read_file():
    d1 = datetime.now()
    read = r.Reader(x)
    list_sequences, head_sequences, keys_seq = read.run()
    pdt = datetime.now()
    d2 = datetime.now()
    # print('Duración: ', d2-d1)
    df = pd.json_normalize({
        "Nombre_archivo: ": "-",
        "Peso_archivo (MB): ": (os.path.getsize(x)/1000000),
        "Num Aprox de bp: ": os.path.getsize(x),
        'Algoritmo': 'Procesamiento de archivo (PA)',
        "Lista_sequencia_longitud: ": len(list_sequences),
        "Lista_encabezados: ": len(head_sequences),
        "Lista_keys: ": len(keys_seq),
        'Inicio: ': "{}".format(d1),
        'Fin: ': "{}".format(d2),
        'Duracion: ': str(d2-d1)})

    df = pd.json_normalize()
    df.to_csv(z+"log_pruebas.csv",
              mode='a', header=False)
    
    
def find_n_patterns_bims():
    '''Funcion para probar bims con diferentes archivos'''
    # archivos = glob.glob(os.path.join(
    #     z1, "multi"+os.path.sep)+'*.fasta')
    
    archivos = glob.glob(os.path.join(
        z1, "multi"+os.path.sep)+'*.fasta')
    
    i = 0
    for archivo in tqdm(archivos):
        head, tail = os.path.split(archivo)
        tail = tail.replace(".fasta", "")
        tail = tail.replace(".", "")
        print(tail)
        
        print("leyendo archivos")      
        read = r.Reader(archivo)
        list_sequences, head_sequences, keys_seq = read.run()
        print("lectura terminada")
        pdt = datetime.now()
        print("iniciando analisis")
        
        d1 = datetime.now()
        pf = BI_n_sequences_copy.basado_indices_secuencial(db_sequence=list_sequences, min_sup=2, keys_seqs=keys_seq ,inputType='archivo', inputName=tail)
        pf.set_initDateTime(pdt)
        tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())
        data_pf = pf.info_patrones()
        d2 = datetime.now()
        print(len(data_pf["Patrones"]))
    
        # align = Generador_motifs.Generador(
            # secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=2, tolerancia_delante=2, json_patrones=pf.info_patrones(), imprimir_logo=True)
        # align.alineador()
        
        print("analisis finalizado")
        try:
            with open(z1+"multi"+os.path.sep+tail+'_BIMS_test_'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(data_pf, file_object_json, sort_keys=True, indent=4)
                
        except FileError as e:                
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
            # del(pf)
        
        dtBI = {
            "Secuencias": "-".join(keys_seq),
            "longitud": "-".join(str(len(i)) for i in list_sequences),
            "patrones_obtenidos": len(pf.get_only_patrones()),
            "duracion": '{}'.format(pf.get_finDateTime() - pf.get_initDateTime()),
            "duracion_seg": str(pf.get_finDateTime() - pf.get_initDateTime())
        }
            
        # print('Duración: ', d2-d1)
        df = pd.json_normalize({
            "Nombre_archivo: ": tail+".fasta",
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'BIMS(MULTI)',
            "Lista_sequencia_longitud: ": len(list_sequences),
            "Lista_encabezados: ": len(head_sequences),
            "Lista_keys: ": len(keys_seq),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})

        df.to_csv(z+"log_pruebas.csv",
                mode='a', header=False)
        
        pf.clear()
        del(pf)
        dfbi = pd.json_normalize(dtBI)
        dfbi.to_csv(z+"log_cap_bims.csv", mode='a', header=False)
        
        
        i += 1
        
        

def find_n_patterns_gsp():
    '''Funcion para probar bims con diferentes archivos'''
    
    # archivos = glob.glob(os.path.join(
    #     z1, "multi"+os.path.sep)+'*.fasta')
    archivos = glob.glob(os.path.join(
        z1, "multi"+os.path.sep)+'*.fasta')
    
    # archivos = glob.glob(os.path.join(
    #     z, "adicional multi"+os.path.sep)+'*.fasta')
    i = 0
    for archivo in tqdm(archivos):
        
        print("Inicio")
        head, tail = os.path.split(archivo)
        tail = tail.replace(".fasta", "")
        tail = tail.replace(".", "")
        print(tail)
        # d1 = datetime.now()
        print("leyendo archivos")
        read = r.Reader(archivo)
        list_sequences, head_sequences, keys_seq = read.run()
        print("lectura terminada")
        pdt = datetime.now()
        print("iniciando analisis")

        
        d1 = datetime.now()
        pf = gsp.GSP(
            ds=list_sequences, min_sup=2, keys_seqs=keys_seq, inputType='archivo', inputName="tail")
        pf.set_initDateTime(pdt)
        # tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())        
        data_pf = pf.info_patrones()
        # align = Generador_motifs.Generador(
        #     secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=2, tolerancia_delante=2, json_patrones=pf.info_patrones(), imprimir_logo=True)
        # align.alineador()
        d2 = datetime.now()
        try:
            with open(z1+"multi"+os.path.sep+tail+'_GSP_test_'+'-'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(data_pf, file_object_json,
                          sort_keys=True, indent=4)

        except FileError as e:
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
            # del(pf)
        
        # x = [y for y in range(100000)]
        dtBI = {
            "Secuencias": "-".join(keys_seq),
            "longitud": "-".join(str(len(i)) for i in list_sequences),
            "patrones_obtenidos": len(pf.get_only_patrones()),
            "duracion": '{}'.format(pf.get_finDateTime() - pf.get_initDateTime()),
            "duracion_seg": str(pf.get_finDateTime() - pf.get_initDateTime())
        }

        print("analisis finalizado")
        
        dfbi = pd.json_normalize(dtBI)
        dfbi.to_csv(z+"log_cap_gsp.csv", mode='a', header=False)
        # d2 = datetime.now()
        
        # print('Duración: ', d2-d1)
        df = pd.json_normalize({
            "Nombre_archivo: ":  tail + ".fasta", #archivo, #y
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'GSP(MULTI)',
            "Lista_sequencia_longitud: ": len(list_sequences),
            "Lista_encabezados: ": len(head_sequences),
            "Lista_keys: ": len(keys_seq),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})

        df.to_csv(z+"log_pruebas.csv",
                  mode='a', header=False)

        pf.clear()
        del(pf)
        

        i += 1


def find_n_patterns_Prefix():
    '''Funcion para probar bims con diferentes archivos'''

    # archivos = glob.glob(os.path.join(
    #     z1, "multi"+os.path.sep)+'*.fasta')
    archivos = glob.glob(os.path.join(
        z1, "multi"+os.path.sep)+'*.fasta')

    # archivos = glob.glob(os.path.join(
    #     z, "adicional multi"+os.path.sep)+'*.fasta')
    i = 0
    max_len = [74,118,30,223,36,35,64]
    for archivo in tqdm(archivos):
        

        print("Inicio")
        head, tail = os.path.split(archivo)
        tail = tail.replace(".fasta", "")
        tail = tail.replace(".", "")
        print(tail)
        # d1 = datetime.now()
        print("leyendo archivos")
        read = r.Reader(archivo)
        list_sequences, head_sequences, keys_seq = read.run()
        print("lectura terminada")
        pdt = datetime.now()
        print("iniciando analisis")
        print(list_sequences)
        d1 = datetime.now()
        ps = PrefixSpan(list_sequences)
        ps.minlen = 2
        ps.maxlen = max_len[i]
        ps_result = ps.frequent(2)
        d2 = datetime.now()
        
        dict_result = {
            "configuracion":{   "Algoritmo": "Basado en indices",
                                "Siglas": "BI",
                                "Min_sup": 2,
                                "Tipo_Entrada": "Archivo",
                                "Entrada":tail,
                                "Secuencias_analizadas": '-'.join(keys_seq),
                                "Longitud_Secuencias": '-'.join(len(ks) for ks in keys_seq),
                                "Num_secuencias_analizadas": len(keys_seq),
                                "Num_patrones_hallados": len(ps_result),
                                "Fecha_Hora_Inicio": '{}'.format(d1),
                                "Fecha_Hora_Fin": '{}'.format(d2),
                                "Duracion": str(d2 - d1)},
            "Patrones": ps_result.sort(key=lambda tps: len(tps[1]),reverse=True)
        }
        
        try:
            with open(z1+"multi"+os.path.sep+tail+'_PrefixSpan_test_'+'-'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump( dict_result , file_object_json,
                          sort_keys=True, indent=4)

        except FileError as e:
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
            # del(pf)

        # x = [y for y in range(100000)]
        dtBI = {
            "Secuencias": "-".join(keys_seq),
            "longitud": "-".join(str(len(i)) for i in list_sequences),
            "patrones_obtenidos": len(ps_result),
            "duracion": '{}'.format(d1 - d1),
            "duracion_seg": str(d1 - d1)
        }

        print("analisis finalizado")

        dfbi = pd.json_normalize(dtBI)
        dfbi.to_csv(z+"log_cap_prefixspan.csv", mode='a', header=False)
        # d2 = datetime.now()

        # print('Duración: ', d2-d1)
        df = pd.json_normalize({
            "Nombre_archivo: ":  tail + ".fasta",  # archivo, #y
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'PREFIXSPAN(MULTI)',
            "Lista_sequencia_longitud: ": len(list_sequences),
            "Lista_encabezados: ": len(head_sequences),
            "Lista_keys: ": len(keys_seq),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})

        df.to_csv(z+"log_pruebas.csv",
                  mode='a', header=False)

        ps_result.clear()
        del(ps_result)
        dict_result.clear()
        del(dict_result)

        i += 1


def find_patterns_bi():
    '''Funcion para probar bims con diferentes archivos'''
    archivos = glob.glob(os.path.join(z1,"una"+os.path.sep)+'*.fasta')
    # archivo = os.path.join(x1, "sequence_NM_007169.fasta")
    i = 0
    # print(archivos)
    for archivo in tqdm(archivos):
        head, tail =  os.path.split(archivo)
        tail = tail.replace(".fasta","")
        tail = tail.replace(".","")
        
        print("leyendo archivos")      
        read = r.Reader(archivo)
        list_sequences, head_sequences, keys_seq = read.run()
        print("lectura terminada")
        pdt = datetime.now()
        print("iniciando analisis")
        d1 = datetime.now()
        pf = BI_copy.basado_indices(
            s=list_sequences[0], min_sup=2, keys_seqs=keys_seq, inputType='archivo', inputName=tail)
        # pf = BI_n_sequences_copy.basado_indices_secuencial(db_sequence=list_sequences, min_sup=5, keys_seqs=keys_seq ,inputType='archivo', inputName=y)
        pf.set_initDateTime(pdt)
        tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())
        dataBi = pf.info_patrones()
        d2 = datetime.now()
        # align = Generador_motifs.Generador(
        #     secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=2, tolerancia_delante=2, json_patrones=dataBi, imprimir_logo=F)
        # align.alineador()
        
        # align = Alineador_Patornes.Alineador(
        #     secuencia=list_sequences[0], tolerancia_atras=2, tolerancia_delante=2, json_patrones=dataBi, imprimir_logo=True)
        # align.alineador()

        print("analisis finalizado")
        try:
            with open(z1+"una"+os.path.sep+tail+'-BI-test-'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(dataBi, file_object_json, sort_keys=True, indent=4)
                
        except FileError as e:                
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
        
        dtBI = {
            "Sequencia":dataBi["Configuracion"]["Secuencias_analizadas"],
            "longitud": dataBi["Configuracion"]["Longitud_Secuencias"],
            "patrones_obtenidos": dataBi["Configuracion"]["Num_patrones_hallados"],
            "duracion": '{}'.format(dataBi["Configuracion"]["Duracion"]),
            "duracion_seg": str(pf.get_finDateTime() - pf.get_initDateTime())
        }    
        # d2 = datetime.now()
        # print('Duración: ', d2-d1)
        df = pd.json_normalize({
            "Nombre_archivo: ": tail+".fasta", #"sequence_experimental_1_1000_"+str(i),
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'BI(UNA)',
            "Lista_sequencia_longitud: ": len(list_sequences),
            "Lista_encabezados: ": len(head_sequences),
            "Lista_keys: ": len(keys_seq),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})
        
        

        df.to_csv(z+"log_pruebas.csv",
                mode='a', header=False)
        
        dfbi = pd.json_normalize(dtBI)
        dfbi.to_csv(z+"log_cap_bi.csv", mode ='a', header=False)
        
        pf.clear()
        
        i+=1



def bims_stand_alone():
    # sequence = ['ACGTGTAAAACTCTTNNNNNNNNNNNNNNNGTT',
    #             'CNNNNNNNNNNNNNNNNTAAGTCCGTAGCCGACT',]
    sequence = ['ACGTGTAAAACTCTTGTT',
                'CTAAGTCCGTAGCCGACT',]
    min_sup = 2

    bi = BI_n_sequences_copy.basado_indices_secuencial(
        db_sequence=sequence, min_sup=min_sup, debug=True)
    bi.set_pos(bi.find_pos())
    bi.run()
    # # print("\n")
    # # print(bi.get_keys_seqs())
    # print("\n")
    # print(bi.get_patrones())
    # print("\n")
    # print(bi.info_patrones())
    

if __name__ == '__main__':
    # find_patterns_bi()
    # find_n_patterns_bims()
    # find_n_patterns_gsp()
    find_n_patterns_Prefix()




# x = "Plataforma_motifs\\Secuencias_prueba\\sequences_flu.fasta"
# d1 = datetime.now()
# read = r.Reader(x)
# list_sequences, head_sequences, keys_seq = read.run()
# d2 = datetime.now()
# print('Duración: ',d2-d1)

# datos_pruebas = {
#     "Nombre_archivo: ": x,
#     "Peso_archivo (MB): ": (os.path.getsize(x)/1000000),
#     "Num Aprox de bp: ": os.path.getsize(x),
#     'Algoritmo': 'Procesamiento de archivo (PA)',
#     "Lista_sequencia_longitud: ": len(list_sequences),
#     "Lista_encabezados: ": len(head_sequences),
#     "Lista_keys: ": len(keys_seq),
#     'Inicio: ': d1,
#     'Fin: ': d2,
#     'Duracion: ': d2-d1
# }

# df = pd.json_normalize(datos_pruebas)
# df.to_csv("C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\No funcionales\\backend\\log_pruebas.csv", mode='a', header=False)

# sequence = []
# min_sup = 3
# b = BI_n_sequences_copy.basado_indices_secuencial(db_sequence=sequence, min_sup=3, debug=True, csv=True)
# b.run()
# # json_result = json.loads(json.dumps(b.info_patrones()))
# # df = pd.json_normalize(json_result)
# # df.to_csv("busqueda_errores.csv")
# # print("".join("{}\t".format(b.info_patrones())))

# try:
#     with open(''+(".json"), 'x') as file_object_json:
#         json.dump(b.info_patrones(), file_object_json,
#                   sort_keys=True, indent=4)
# except IOError as e:                
#     print(f'Hubo un error en la escritura del archivo \n'+str(e))




# read = Reader(filesnames='Plataforma_motifs\Secuencias_prueba\sequence (1).fasta')

# list_sequence, headline = read.run()
# bi = BI_n_sequences_copy()

# bi = bi.basado_indices(min_sup=2)

#     for sequence, head in list_sequence, headline:
#         bi.set_dbsequence(sequence)
#         bi.set_pos(bi.find_pos())

#         candidates = bi.run()

#         print(head)
#         print('\n', 'Patrones Hallados: ', ', '.join(str(c) for c in candidates))
#         print('\n')

####-Otra prueba
# sequence = ['ACGTGTAAAACTCTTGTT', 'CTAAGTCCGTAGCCGACT', 'GGATCCAATCGCTAATCG']
# min_sup = 3
# b = BI_copy.basado_indices()

# b = bi.basado_indices()


# for i in range(len(sequence)):
#     b.set_sequence(sequence[i])
#     b.set_minsup(min_sup)
#     b.set_seqCode(i)
#     b.set_pos(b.find_pos())
#     b.run()

# b.set_sequence(sequence[0])
# b.set_minsup(min_sup)
# b.set_pos(b.find_pos())
# b.run()

# patrones = b.get_patrones()
# # print(b.get_patrones())

# resultado = {  "Patrones1": [{
#             "Patron": k,
#             "Longitud": len(k),
#             "Ocurrencias": len(v),
#             "Posiciones": [{"sequencia": key,
#                             "posicion": pos+1}
#                             for pos in v]
#         } for key, values in patrones.items()
#             for k, v in values.items()
#         ]
#     }

# print(resultado)




# patrones = {}  
# gsp = gsp.GSP(sequence, min_sup, inputType="prueba",
#               initDateTime=datetime.now())
# gsp.run()
# gsp.set_finDateTime(datetime.now())
# patrones = gsp.info_candidates()

# print(patrones)


# dt = datetime.strptime("2022-01-02 22:11:34.237049", '%Y-%m-%d %H:%M:%S.%f')
# dt1 = datetime.strptime("2022-01-04 22:10:34.237041", '%Y-%m-%d %H:%M:%S.%f')
# dt2 = dt1-dt
# print(dt2)
# print(dt2.seconds)
# print(dt2.days*86400)

# sdt = str(dt2)
# x = [i for i in re.split("[ ,:.]",sdt) if i.isdigit() or i.isdecimal()]
# print(x)
# print(int(x[0])*86400)
# print(int(x[1])*3600)
# print(int(x[2])*60)
# print(x[3])
# print()
# ms = str(x[4])
# ms += '00'
# print(ms[:4])
# ms1 = '9'
# print(ms1[:4])
# dt3 = timedelta(days=x[0], hours= x[1], minutes= x[2], seconds= x[3], milliseconds=x[4])
# dt3 = timedelta(seconds=((x[0]*86400)+(x[1]*3600)+(x[2]*60)+x[3]))
# print(str(dt3))

