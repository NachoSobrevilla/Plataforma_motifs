import collections

class GSP(object):

    def __init__(self, ds=[], min_sup=2):
        super().__init__()
        self.ds = ds
        self.min_sup = min_sup

    def candidates_generator(self, f_k=[], l_item=[]):
        """Función de generar las secuencias candidados de longitud k"""
        for f in f_k:
            for n in l_item:
                yield f+n

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

            candidates = {g:0 for g in self.candidates_generator(f_k=frecuent_list[k], l_item=frecuent_list[0])}
            for d in self.ds:
                for c in candidates.keys():
                    count = 0
                    # x = 0
                    print(c, end=": ")
                    x = d
                    for n in c:
                        # if len(x) == 1:
                        #     if x == n:
                        #         count += 1
                        #     else:
                        #         break
                        # else:
                        #     x = x.split(n, maxsplit=1)[len(x)-1]

                        #     if len(x) > 0:
                        #         count += 1
                        #     else:
                        #         break
                        

                        print(d[x:], end=" ")
                        x = d[x:].find(n)
                        print(x,'-',n, end="    |   ")
                        if x != -1 and x <= len(d):
                            
                        x += 1 
                    
                    if count == len(c):
                        candidates[c] += 1

            # print(candidates)
            frecuent_list.append([key for key, value in candidates.items() if value>= self.min_sup])
            candidates.clear()
            k+=1
            if k == 3:
                break
            # print('\n')
            # print(frecuent_list)
            # break
        

        #frecuent_list.pop()
        print(frecuent_list)


        

ds1 = ['ATTAAAGGTTTATACC',  # TTCC',  # CAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
       'CGAACTTTAAAATCTG']  # TGTG']  # GCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
#   'TAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTGCAGGCTGCTTACGGTTTCGTCCGTG',
#   'TTGCAGCCGATCATCAGCACATCTAGGTTTCGTCCGGGTGTGACCGAAAGGTAAGATGGAGAGCCTTGTC',
#   'CCTGGTTTCAACGAGAAAACACACGTCCAACTCAGTTTGCCTGTTTTACAGGTTCGCGACGTGCTCGTAC']
min_sup1 = 2


x = GSP(ds1, min_sup1)
x.run()










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
