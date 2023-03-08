from tempfile import SpooledTemporaryFile
import Generador_motifs
import Alineador_Patornes
import json
import pandas as pd
import re
import server as s
from datetime import datetime, timedelta
from algoritmos import BI_n_sequences_copy, BI_copy, gsp
import Reader as r
import time
from prefixspan import PrefixSpan
import glob
import gc 
import sys
import os
from click import FileError, exceptions
from numpy import False_
# import imp
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

z = "C:\\Users\\sobre\\Documents\\MCCAyE\\Tesis\\pruebas\\parametros\\mas\\"

def Test_umbral(support = 2):
    '''Funcion para realizar diferentes ejecuciones de support de BIMS'''
    # archivos = glob.glob(os.path.join(
    #     z1, "multi"+os.path.sep)+'*.fasta')
    
    archivos = glob.glob(z+'*.fasta')
    
    
    for archivo in tqdm(archivos):
        # archivo = os.path.join(z, "multi"+os.path.sep)+'*.fasta'
        # archivo = os.path.join(z, "sequence_human_multi_2000-200_1.fasta")
        
        head, tail = os.path.split(archivo)
        tail = tail.replace(".fasta", "")
        tail = tail.replace(".", "")
        print(tail)
        
        print("leyendo archivos")      
        read = r.Reader(archivo)
        list_sequences, head_sequences, keys_seq = read.run()
        print(len(list_sequences))
        print("lectura terminada")
        pdt = datetime.now()
        print("iniciando analisis")
        

        d1 = datetime.now()
        pf = BI_n_sequences_copy.basado_indices_secuencial(db_sequence=list_sequences, min_sup=support, keys_seqs=keys_seq ,inputType='archivo', inputName=tail)
        pf.set_initDateTime(pdt)
        tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())
        data_pf = pf.info_patrones()
        
        print(len(data_pf["Patrones"]))
        
        align = Generador_motifs.Generador(secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=2, tolerancia_delante=2,
                                            longitud_minima_cre=6, json_patrones=pf.info_patrones(), imprimir_logo=False)
        data_m = align.alineador()
        
        d2 = datetime.now()
        
        print("analisis finalizado")
        try:
            with open(z+tail+'_BIMS_test_sup_'+str(support)+'_'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(data_pf, file_object_json, sort_keys=True, indent=4)
                
        except FileError as e:                
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
            # del(pf)
        
        # dtBI = {
        #     "Secuencias": "-".join(keys_seq),
        #     "longitud": "-".join(str(len(i)) for i in list_sequences),
        #     "patrones_obtenidos": len(pf.get_only_patrones()),
        #     "duracion": '{}'.format(pf.get_finDateTime() - pf.get_initDateTime()),
        #     "duracion_seg": str(pf.get_finDateTime() - pf.get_initDateTime())
        # }
            
        # print('Duración: ', d2-d1)
        len_m = lambda x: data_m["Alineaciones"][0]["longitud_motif"] if len(x) > 0 else 0
        df = pd.json_normalize({
            "Nombre_archivo: ": tail+".fasta",
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'BIMS-Support-'+str(support),
            "Lista_keys: ": len(keys_seq),
            "Secuencias": "-".join(keys_seq),
            "Longitudes": "-".join(str(len(i)) for i in list_sequences),
            "Min_Sup": str(support),
            "Longitud_min": 6,
            "Tolerancia_delante": 2,
            "Tolerancia_atras": 2,
            "Max_Lon_Patrones_Frec": data_pf["Patrones"][0]["Longitud"],
            "Num_patrones": len(data_pf["Patrones"]),
            "Max_Lon_motif": len_m(data_m["Alineaciones"]),
            "Num_motifs": len(data_m["Alineaciones"]),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})
        # "Max_Lon_motif": data_m["Alineaciones"][0]["longitud_motif"],
        if os.path.exists(z+"log_pruebas.csv"):
            df.to_csv(z+"log_pruebas.csv", mode='a',
                    header=False)
        else:
            df.to_csv(z+"log_pruebas.csv",
                    header=True)
            

        pf.clear()
        gc.collect()
        # del(pf)
            # data_m.clear()
            # del(pf)
            # dfbi = pd.json_normalize(dtBI)
            # dfbi.to_csv(z+"log_cap_bims.csv", mode='a', header=False)
        
        


def Test_tolerancias(tolerancias = 2):
    '''Funcion para realizar diferentes ejecuciones de tolerancias de BIMS'''
    # archivos = glob.glob(os.path.join(
    #     z1, "multi"+os.path.sep)+'*.fasta')

    archivos = glob.glob(z+'*.fasta')

    # archivos = glob.glob(os.path.join(z, "multi"+os.path.sep)+'*.fasta')
    
    for archivo in tqdm(archivos):
        # archivo = os.path.join(z, "multi"+os.path.sep)+'*.fasta'
        # archivo = os.path.join(z, "sequence_human_multi_2000-200_1.fasta")
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
        pf = BI_n_sequences_copy.basado_indices_secuencial(
            db_sequence=list_sequences, min_sup=2, keys_seqs=keys_seq, inputType='archivo', inputName=tail)
        pf.set_initDateTime(pdt)
        tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())
        data_pf = pf.info_patrones()
        
        print(len(data_pf["Patrones"]))

        align = Generador_motifs.Generador(secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=tolerancias, tolerancia_delante=tolerancias,
                                            longitud_minima_cre=6, json_patrones=pf.info_patrones(), imprimir_logo=False)
        data_m = align.alineador()
        d2 = datetime.now()
        print("analisis finalizado")
        try:
            with open(z+tail+'_BIMS_test_tol_'+str(tolerancias)+'_'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(data_pf, file_object_json, sort_keys=True, indent=4)

        except FileError as e:
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")
            # del(pf)

        # dtBI = {
        #     "Secuencias": "-".join(keys_seq),
        #     "longitud": "-".join(str(len(i)) for i in list_sequences),
        #     "patrones_obtenidos": len(pf.get_only_patrones()),
        #     "duracion": '{}'.format(pf.get_finDateTime() - pf.get_initDateTime()),
        #     "duracion_seg": str(pf.get_finDateTime() - pf.get_initDateTime())
        # }

        # print('Duración: ', d2-d1)
        len_m = lambda x: data_m["Alineaciones"][0]["longitud_motif"] if len(x) > 0 else 0
        df = pd.json_normalize({
            "Nombre_archivo: ": tail+".fasta",
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'BIMS-tolerancias-'+str(tolerancias),
            "Lista_keys: ": len(keys_seq),
            "Secuencias": "-".join(keys_seq),
            "Longitudes": "-".join(str(len(i)) for i in list_sequences),
            "Min_Sup": 2,
            "Longitud_min": 6,
            "Tolerancia_delante": tolerancias,
            "Tolerancia_atras": tolerancias,
            "Max_Lon_Patrones_Frec": data_pf["Patrones"][0]["Longitud"],
            "Num_patrones": len(data_pf["Patrones"]),
            "Max_Lon_motif": len_m(data_m["Alineaciones"]),
            "Num_motifs": len(data_m["Alineaciones"]),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})

        if os.path.exists(z+"log_pruebas.csv"):
            df.to_csv(z+"log_pruebas.csv", mode='a',
                header=False)
        else:
            df.to_csv(z+"log_pruebas.csv",
                    header=True)

        pf.clear()
        gc.collect()
        # del(pf)
        
        # del(pf)
        # dfbi = pd.json_normalize(dtBI)
        # dfbi.to_csv(z+"log_cap_bims.csv", mode='a', header=False)

        


def Test_len(lon = 2):
    '''Funcion para realizar diferentes ejecuciones de tolerancias de BIMS'''
    # archivos = glob.glob(os.path.join(z, "multi"+os.path.sep)+'*.fasta')
    archivos = glob.glob(z+'*.fasta')

    for archivo in tqdm(archivos):
    # archivo = os.path.join(z, "multi"+os.path.sep)+'*.fasta'
    # archivo = os.path.join(z, "sequence_human_multi_2000-200_1.fasta")
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
        pf = BI_n_sequences_copy.basado_indices_secuencial(
            db_sequence=list_sequences, min_sup=2, keys_seqs=keys_seq, inputType='archivo', inputName=tail)
        pf.set_initDateTime(pdt)
        tqdm(pf.set_pos(pf.find_pos()))
        tqdm(pf.run())
        pf.set_finDateTime(datetime.now())
        data_pf = pf.info_patrones()
        
        print(len(data_pf["Patrones"]))

        align = Generador_motifs.Generador(secuencias=dict(zip(keys_seq, list_sequences)), tolerancia_atras=2, tolerancia_delante=2,
                                            longitud_minima_cre=lon, json_patrones=pf.info_patrones(), imprimir_logo=False)
        data_m = align.alineador()
        d2 = datetime.now()
        print("analisis finalizado")
        try:
            with open(z+tail+'_BIMS_test_len_'+str(lon)+'_'+'{}'.format(d1.date())+'_'+str(d1.hour)+'h'+str(d1.minute)+'m'+str(d1.second)+'s'+str(d1.microsecond)+'ms'+".json", 'x') as file_object_json:
                json.dump(data_pf, file_object_json, sort_keys=True, indent=4)

        except FileError as e:
            print('Hubo un error en la escritura del archivo \n'+str(e))

        else:
            print("Success!, file created")

        def len_m(x): return data_m["Alineaciones"][0]["longitud_motif"] if len(
            x) > 0 else 0
        df = pd.json_normalize({
            "Nombre_archivo: ": tail+".fasta",
            "Peso_archivo (MB): ": (os.path.getsize(archivo)/1000000),
            "Num Aprox de bp: ": os.path.getsize(archivo),
            'Algoritmo': 'BIMS-Longitud-'+str(lon),
            "Lista_keys: ": len(keys_seq),
            "Secuencias": "-".join(keys_seq),
            "Longitudes": "-".join(str(len(i)) for i in list_sequences),
            "Min_Sup": 2,
            "Longitud_min": lon,
            "Tolerancia_delante": 2,
            "Tolerancia_atras": 2,
            "Max_Lon_Patrones_Frec": data_pf["Patrones"][len(data_pf["Patrones"])-1]["Longitud"],
            "Num_patrones": len(data_pf["Patrones"]),
            "Max_Lon_motif": len_m(data_m["Alineaciones"]),
            "Num_motifs": len(data_m["Alineaciones"]),
            'Inicio: ': '{}'.format(d1),
            'Fin: ': '{}'.format(d2),
            'Duracion: ': d2-d1})

        if os.path.exists(z+"log_pruebas.csv"):
            df.to_csv(z+"log_pruebas.csv", mode='a',
                    header=False)
        else:
            df.to_csv(z+"log_pruebas.csv",
                    header=True)

        pf.clear()
        gc.collect()

        # dfbi = pd.json_normalize(dtBI)
        # dfbi.to_csv(z+"log_cap_bims.csv", mode='a', header=False)




if __name__ == '__main__':
    # i= 2
    # while i <= 15:
    #   print("umbral:"+str(i))
    #   Test_umbral(i)
    #   gc.collect()
    #   i += 1
      
    
    # i = 6
    # while i <= 20:
    #     # print("umbral: "+str(i)) 
    #     # Test_umbral(i)
    #     print("min_len: "+str(i))
    #     Test_len(i)
    #     gc.collect()
    #     i+=1
    
    # gc.collect()

        
    i = 2
    while i <= 11:
        print("tolerancia: "+str(i))
        Test_tolerancias(i)
        i+=1
        gc.collect()
    # Test_len()
