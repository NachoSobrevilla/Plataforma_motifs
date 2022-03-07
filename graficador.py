from cProfile import label
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston

class Graficador(object):
    
    def __init__(self, list_align_ptt = [[]]):
        self.list_align_ptt = list_align_ptt
    
    def contador(self):
        count_a = [0 for i in range(len(self.list_align_ptt[0]))]
        count_c = [0 for i in range(len(self.list_align_ptt[0]))]
        count_g = [0 for i in range(len(self.list_align_ptt[0]))]
        count_t = [0 for i in range(len(self.list_align_ptt[0]))]
        count_head = ["Columna" +str(i+1) for i in range(len(self.list_align_ptt[0]))]
        
        for ptt in self.list_align_ptt:
            for j in range(len(ptt)):
                if ptt[j] == "A":
                    count_a[j] +=1
                elif ptt[j] == "C":
                    count_c[j] += 1
                elif ptt[j] == "G":
                    count_g[j] += 1
                elif ptt[j] == "T":
                    count_t[j] += 1
                else:
                    count_a[j] += 1
                    count_c[j] += 1
                    count_g[j] += 1
                    count_t[j] += 1
        
        print(count_a)
        print(count_c)
        print(count_g)
        print(count_t)
        
        indice = np.arange(len(count_head))
        
        plt.bar(indice, count_a, label = "A")    
        plt.bar(indice, count_c, label = "C", bottom = np.array(count_a))    
        plt.bar(indice, count_g, label="G", bottom = np.array(count_c) + np.array(count_a))
        plt.bar(indice, count_t, label="T", bottom= np.array(count_g) + np.array(count_c) + np.array(count_a))
        plt.xticks(indice, count_head)
        plt.ylabel("Apariciones")    
        plt.xlabel("Columnas")
        plt.title("Apariciones por columna")
        plt.legend(loc= "lower left")
        
        plt.show() 
 
 


if __name__ == '__main__':
    list_ptt = ["AACCACAG",
                "CACCACGC"]
    g = Graficador(list_align_ptt=list_ptt)
    g.contador()
    
       
