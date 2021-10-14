from collections import Counter
from typing import Generator


class freespan(object):
    
    def __init__(self, ds, max_len, min_sup):
        """funcion constructora"""
        self.ds = ds
        self.max_len = max_len
        self.min_sup = min_sup

    def generator_f_list(self):
        """Función para encontrar a los candidatos dentro de las secuencias"""
        f = {}
        
        for s in self.ds:
            x=[key for key in Counter(s).keys()]
       
            for n in x:
                if n in f.keys():
                    f[n] += 1
                else:
                    f[n] = 1


        f.update({key:value for key,value in f.items() if value >= self.min_sup})

        return f

    def db_proyecction(self, ite=[]):
        db = []
        y = ''
        
        for s in self.ds:
           pass
        

    def count_candidates(self, Ds, c_list):
        pass


    


                
        return 


    def run(self):
        """Funcón principal del algoritmo"""
        
        f_k = self.generator_f_list()
        
    

    
def main():
    k = 10
    # ds = ['ATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
    #       'CGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
    ds = ['ACGTGTAAAACTCTTGTT',
          'CTAAGTCCGTAGCCGACT',
          'GGATCCAATCGCTAATCG']
    min_sup = 2

    x = freespan(ds, k, min_sup)
    x.run()

if __name__ == "__main__":
    main()
