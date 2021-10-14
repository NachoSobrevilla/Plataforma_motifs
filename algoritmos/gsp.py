import collections
from collections import defaultdict

class GSP(object):

    def __init__(self, ds=[], min_sup=2, pos={}, patrones = {}, keys_seqs ={},debug=False, debugTime = False, csv = False):
        self.ds = ds
        self.min_sup = min_sup
        self.pos = pos
        self.patrones = patrones
        self.keys_seqs = keys_seqs
        self.debug = debug
        self.debugTime = debugTime
        self.csv = csv
    
    def set_dbsequence(self, db_sequence=[]):
      self.db_sequence = db_sequence

    def get_dbsequence(self):
        return self.db_sequence

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

    def set_key_seq(self, keys_seqs={}):
        self.keys_seqs = keys_seqs

    def get_key_seq(self):
        return self.keys_seqs

    def get_lenpos(self):
        return len(self.pos)

    def get_lendbsequence(self):
        return len(self.db_sequence)
    
    def set_csv(self,csv):
        self.csv = csv
    
    def get_cvs(self,csv):
        return self.csv






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

    def info_candidates(self):
        key_seq = lambda x: self.keys_seqs[x] if len(self.keys_seqs) else x
        return {"Configuracion": {
                                "Algoritmo": "GSP",
                                "min_sup": self.get_minsup(),
                                "Realizado en": "text/archivo FASTA",
                                "No. de sequencias ananlizadas": len(self.get_dbsequence()),
                                "No. Patrones Hallados": len(self.get_patrones())},
                "Patrones": [{
                           "Patron": key,
                           "Longitud": len(key),
                           "Ocurrencias": len(values),
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
