import collections

class PrefixSpan(object):
    def __init__(self, ds = [], min_sup = 2):
        self.ds = ds
        self.min_sup = min_sup
    

    def run(self):
        f_list = self.find_candidates(self.ds, self.min_sup)
        candidates = self.find_subsets(self.ds, f_list, self.min_sup)

        print(candidates)
        

    def find_candidates(self, ds=[], item ='',min_sup=2):
        """Busca candidatos (sufijos)"""
        if len(ds) >= min_sup:
            f = {}
            for s in ds:
                c_list = [c for c, k in collections.Counter(s).items()]
                c_list.sort()
                for n in c_list:
                    if n in f.keys():
                        f[n] += 1
                    else:
                        f[n] = 1
            f = sorted(f.items(),key = lambda x:x[1], reverse=True)

            return [key for key, value in f if value >= min_sup]
        else:
            return []
         
    
    def find_subsets(self, suffixes = [], preffixes=[], min_sup = 2):
        """Es el metodo recursivo"""
        r = []

        for p in preffixes:
            print(p)
            suf = self.generator_suffixes(suffixes,p)
            print(suf)
            p_list = self.find_candidates(suf, min_sup)
            print(p_list)
            if len(p_list) > 0 and len(suf) >= min_sup:
                x =  self.find_subsets(suf,p_list,min_sup)
                # if len(x) == 0:
                #     r.append(p)
                # else:
                r.extend([str(p+xi) for xi in x])
            else:
                r.append(str(p))
                continue
        
        return r

            

    def generator_suffixes(self, ds=[], p=''):
        r = []
        for s in ds:
            x = s.split(p,maxsplit=1)[1]
            if len(x) > 0:
                r.append(x)
        
        return r
        





ds1 = ['ATTAAAGGTTTATACC',#TTCC',  # CAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
       'CGAACTTTAAAATCTG']#TGTG']  # GCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
#   'TAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTGCAGGCTGCTTACGGTTTCGTCCGTG',
#   'TTGCAGCCGATCATCAGCACATCTAGGTTTCGTCCGGGTGTGACCGAAAGGTAAGATGGAGAGCCTTGTC',
#   'CCTGGTTTCAACGAGAAAACACACGTCCAACTCAGTTTGCCTGTTTTACAGGTTCGCGACGTGCTCGTAC']
min_sup1 = 2



x = PrefixSpan(ds1, min_sup1)
x.run()

#class PrefixSpan(object):

#     def __init__(self, ds='', min_sup=0, min_lenght =0):
#         """Funcion inicial de la clase. ds es el conjunto de secuecias de ADN para el analisis; 
#         min_sup es el soporte minimo de apareciones para que un subconjuto de secuencias sea frecuente;
#         y una min_lenght que inicandidatesa una longitud minima"""
#         self.ds = ds
#         self.min_sup = min_sup
#         self.min_lenght = min_lenght
    
#     def run(self):
#         def imprime_dic(f):
#             for c, locs in f.items():
#                 print(c, end=' ')

#                 for loc, pos in locs:
#                     print(self.ds[loc][pos:], '<<',
#                         self.ds[loc][:pos], '>>', end=' | ')

#                 print("\n", '-----------------------------------------')
            
#         f ={}
#         candidates =[]
#         positions = []
        
        
#         f = self.find_count_candidates()
#         print(f)
#         print()
#         for i in range(self.min_lenght):
#             f = self.find_count_candidates(candidates=f)
#             print(f)
#             print()
        
        
        
        
#         imprime_dic(f)
        



#     def find_count_candidates(self, candidates = {}):
#         """Función para encontrar a los candidatos dentro de las secuencias"""
#         f = {}
#         j = 0
#         if len(candidates) == 0:
#             for i in range(len(self.ds)):
#                 c_list = [c for c, k in collections.Counter(self.ds[i]).items()]
#                 for n in c_list:
#                     j = self.ds[i].find(n)
#                     if j != -1:
#                         if n in f.keys():
#                             f[n].append([i, j+1])
#                         else:
#                             f[n] = [[i, j+1]]

#         else:
#             for c, locs in candidates.items():
#                 for loc, pos in locs:
#                     x = self.ds[loc]
#                     if pos < len(x):
#                         x = x[pos:]
#                         c_list = [c for c, k in collections.Counter(x).items()]
#                         # c_list.sort()
#                         for n in c_list:
#                             j = x.find(n)
#                             if j != -1:
#                                 n = c+n
#                                 if n in f.keys():
#                                     f[n].append([loc, pos+j+1])
#                                 else:
#                                     f[n] = [[loc, pos+j+1]]

#         f = {key: value for key, value in f.items() if len(list(value))>= self.min_sup }
        
#         return f




# def run():
# """Función principal del algoritmo """
    
            
# if '__main__' == __name__:
#     run()
    
    



    

   
    

    

