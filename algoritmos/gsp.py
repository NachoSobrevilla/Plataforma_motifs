import collections
from collections import defaultdict
from datetime import datetime
from .clsGntCode import clsGeneticCode as gc
traductor = gc('')

class GSP(object):

    def __init__(self, ds=[], min_sup=2, pos={}, patrones = {}, keys_seqs = [],debug=False, debugTime = False, csv = False, inputType = '', inputName='', initDateTime=0, finDateTime=0):
        self.ds = ds
        self.min_sup = min_sup
        self.pos = pos
        self.patrones = patrones
        self.keys_seqs = keys_seqs
        self.debug = debug
        self.debugTime = debugTime
        self.csv = csv
        self.inputType = inputType
        self.inputName = inputName
        self.initDateTime = initDateTime
        self.finDateTime = finDateTime
    
    def clear(self):
        self.ds.clear()
        self.min_sup = 0
        self.pos.clear()
        self.patrones.clear()
        self.keys_seqs.clear()
        self.debug = False
        self.debugTime = False
        self.csv = False
        self.inputType = ""
        self.inputName = ""
        self.initDateTime = 0
        self.finDateTime = 0
    
    def set_ds(self, ds=[]):
      self.ds = ds

    def get_ds(self):
        return self.ds

    def set_minsup(self, min_sup=0):
        self.min_sup = min_sup

    def get_minsup(self):
        return self.min_sup

    def set_debug(self, debug=False):
        self.debug = debug

    def get_debug(self):
        return self.debug

    def set_debugtime(self, debugTime=False):
        self.debugTime = debugTime

    def get_debugtime(self):
        return self.debugTime

    def set_pos(self, pos={}):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_patrones(self, patrones={}):
        self.patrones = patrones

    def get_patrones(self):
        return self.patrones

    def get_only_patrones(self):
        return self.patrones.keys()

    def get_only_patron_pos(self):
        return self.patrones.values()

    def update_patrones(self, patrones={}):
        self.patrones.update(patrones)

    def set_keys_seqs(self, keys_seqs={}):
        self.keys_seqs = keys_seqs

    def get_keys_seqs(self):
        return self.keys_seqs

    def get_lenpos(self):
        return len(self.pos)

    def get_lendbsequence(self):
        return len(self.ds)
    
    def set_csv(self,csv):
        self.csv = csv
    
    def get_cvs(self):
        return self.csv

    def set_inputType(self, inputType=''):
        self.inputType = inputType
   
    def get_inputType(self):
        return self.inputType
    
    def set_inputName(self, inputName=''):
        self.inputName = inputName
   
    def get_inputName(self):
        return self.inputName
    
    def set_initDateTime(self, initDateTime=datetime.now()):
        self.initDateTime = initDateTime
   
    def get_initDateTime(self):
        return self.initDateTime
    
    def set_finDateTime(self, finDateTime=datetime.now()):
        self.finDateTime = finDateTime
   
    def get_finDateTime(self):
        return self.finDateTime




    def candidates_generator(self, f_k=[]):
        """Función de generar las secuencias candidados de longitud k"""
        for n in 'ACGT':
            for f in f_k:
                yield n+f

    def find_items(self, ds=[], min_sup = 2):
        """Busca los items que conforman la secuencia y superan el min_sup"""
        if len(ds) >= min_sup:
            f = {}
            for s in ds:
                c_list = [c for c, k in collections.Counter(s).items()]
                c_list.sort()
                for n in c_list:
                    if n in f.keys():
                        f[n] += 1
                    elif n == ' ':
                        pass
                    else:
                        f[n] = 1

            f = sorted(f.items(), key=lambda x: x[1], reverse=True)

            return [key for key, value in f if value >= min_sup]
        else:
            return []
        
    def run(self):

        frecuent_list =[]

        frecuent_list.append(self.find_items(ds=self.ds,min_sup=self.min_sup))
        k = 0

        while len(frecuent_list[k]) != 0:

            candidates = {g:0 for g in self.candidates_generator(f_k=frecuent_list[k])}
            loc = candidates.copy()
            pos = defaultdict(list)
            for c in candidates.keys():
                for i in range(len(self.ds)): #d in self.ds:
                    lenc = len(c)
                    for j in range(len(self.ds[i])-(lenc-1)):
                        if self.ds[i][j:lenc+j] == c and lenc+j <= len(self.ds[i]):
                            pos[i].append(j)

                    if len(pos[i]) != 0:
                        candidates[c] += 1

                loc[c] = dict({s:p for s,p in pos.items() if len(p) != 0})
                pos.clear()

                    # Metodo de busqueda binaria no continua
                    # for n in c:
                    #     if len(x) == 1:
                    #         if x == n:
                    #             count += 1
                    #         else:
                    #             break
                    #     else:
                    #         x = x.split(n, maxsplit=1)[len(x)-1]

                    #         if len(x) > 0:
                    #             count += 1
                    #         else:
                    #             break
                        

                        # print(d[x:], end=" ")
                        # x = d[x:].find(n)
                        # print(x,'-',n, end="    |   ")
                        # if x != -1 and x <= len(d):
                        #     pass
                        # x += 1 
                    
                    # if count == len(c):
                    #     candidates[c] += 1
            if self.get_debug == True:
                print(candidates)

            frecuent_list.append([key for key, value in candidates.items() if value>= self.min_sup])

            self.update_patrones({key:value for key,value in loc.items() if len(value)>=self.min_sup})

            
            candidates.clear()
            loc.clear()
            k+=1
            # if k == 3:
            #     break
            # print('\n')
            # print(frecuent_list)
            # break
        

        #frecuent_list.pop()
        if self.get_debug == True:
            print(frecuent_list)

    def traductorCodon(self, codon):
        global traductor
        if len(codon) > 2:
            traductor.setCodon(codon)
            return traductor.getCodonCoded()
        else:
            return ''
    
    def info_patrones(self):
        key_seq = lambda x: self.keys_seqs[x] if len(self.keys_seqs) else x
        return {"Configuracion": {
                                    "Algoritmo": "GSP",
                                    "Siglas": "GSP",
                                    "Min_sup": self.get_minsup(),
                                    "Tipo_Entrada": self.get_inputType(),
                                    "Entrada": self.get_inputName(),
                                    "Sequencias_ananlizadas": '-'.join(self.get_keys_seqs()),
                                    "Num_Sequencias_ananlizadas": len(self.get_ds()),
                                    "Lon_Sequencias_ananlizadas": "-".join(str(len(i)) for i in self.ds),
                                    "Num_Patrones_hallados": len(self.get_patrones()),
                                    "Fecha_Hora_Inicio": '{}'.format(self.get_initDateTime()),
                                    "Fecha_Hora_Fin": '{}'.format(self.get_finDateTime()),
                                    "Duracion": str(self.get_finDateTime() - self.get_initDateTime())
                                },
                "Patrones": [{
                           "Patron": key,
                           "Longitud": len(key),
                           "Ocurrencias": len(values),
                           "Traduccion_aminoacido": self.traductorCodon(key),
                           "Posiciones": [{
                                          "sequencia": key_seq(seq), 
                                          "posicion": p+1} 
                                          for seq, pos in values.items() for p in pos]
                           }for key, values in self.patrones.items()]
            }


# ds1 = ['ATTAAAGGTTTATACC',  # TTCC',  # CAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
#        'CGAACTTTAAAATCTG']  # TGTG']  # GCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
# #   'TAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTGCAGGCTGCTTACGGTTTCGTCCGTG',
# #   'TTGCAGCCGATCATCAGCACATCTAGGTTTCGTCCGGGTGTGACCGAAAGGTAAGATGGAGAGCCTTGTC',
# #   'CCTGGTTTCAACGAGAAAACACACGTCCAACTCAGTTTGCCTGTTTTACAGGTTCGCGACGTGCTCGTAC']
# ds = ['ACGTGTAAAACTCTTGTT', 'CTAAGTCCGTAGCCGACT']
# ds = ['ACGTGTAAAACTCTTGTT', 'CTAAGTCCGTAGCCGACT', 'GGATCCAATCGCTAATCG']
# min_sup1 = 2


# x = GSP(ds, min_sup1)
# x.run()
# print(x.info_candidates())
# print(x.get_patrones())









# import collections


# def find_candidates(ds=[], item='', min_sup=2):
#     """Busca candidatos"""
#     if len(ds) >= min_sup:
#         f = {}
#         for s in ds:
#             c_list = [c for c, k in collections.Counter(s).items()]
#             c_list.sort()
#             for n in c_list:
#                 if n in f.keys():
#                     f[n] += 1
#                 else:
#                     f[n] = 1
#         f = sorted(f.items(), key=lambda x: x[1], reverse=True)

#         return [key for key, value in f if value >= min_sup]
#     else:
#         return []


# def candidates_generator(f_k=[]):
#     """Función de generar las secuencias candidados de longitud k"""
#     for f in f_k:    
#         for n in 'ACGT':
#             yield f+n


# def run():
#     """Funcón principal del algoritmo"""
#     k = 2
#     min_sup = 2
#     ds = ['ATTAAAGGTTTATACC',
#           'CGAACTTTAAAATCTG']  
#         #['ATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
#         #'CGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
#     f_k=[]
#     f_k.append(find_candidates(ds=ds, min_sup=min_sup))
#     print(f_k)
    
#     log= ''
#     log2= ''

#     while len(f_k[k-2]) != 0:
#         C_k = {g:0 for g in candidates_generator(f_k[k-2])}
#         for d in ds:   
#             for c in C_k.keys():
#                 a=0
#                 for i in range(len(d)-(k-1)): 
#                     if d[i:k+i] == c and k+i <= len(d):
#                         a+=1 
#                 C_k[c]=a

#         # log = log + 'k = '+str(k)+' ;  Candidados: '+str(C_k)+'\n\n'

#         f_k.append([key for key, value in C_k.items() if value>= min_sup])
#         print(f_k)
#         C_k.clear()
        
#         # log2 = log2 + 'k = '+str(k)+' ;  Resultados: '+str(f_k[k-1])+'\n\n'
#         k+=1

#     f_k.pop()
#     # print(C_k)
#     # for key in C_k.keys():
#     #     if C_k[key]>= min_sup: 
#     #         print(key, C_k[key])
#     print(log)
#     print(log2)

# if __name__ == "__main__":
#     """Funcón de inicio"""
#     run()
