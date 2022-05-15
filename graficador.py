import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import Estructurador_patron as eptr
import logomaker, os
from os.path import join, dirname, realpath 

EXP_FOLDER = join(dirname(realpath(__file__)), 'experimentos')
class Graficador(object):
   
    
    def __init__(self, list_align_plt = [[]], imprimirLogo = False):
        self.list_align_plt = list_align_plt
        self.imprimirLogo = imprimirLogo
    
    def set_list_align_plt(self, list_align_plt = [[]]):
        self.list_align_plt = list_align_plt
    
    def get_list_align_plt(self):
        return self.list_align_plt
    
    def set_imprimirLogo(self, impirmirLogo):
        self.imprimirLogo = impirmirLogo
        
    def get_imprimirLogo(self):
        return self.imprimirLogo
    
    def contador(self):
        
        # self.ploteo_logo_seq_align(self.list_align_plt)
        
        dict_conteos = {
            "A": [0 for i in range(len(self.list_align_plt[0]))],
            "C": [0 for i in range(len(self.list_align_plt[0]))],
            "G": [0 for i in range(len(self.list_align_plt[0]))],
            "T": [0 for i in range(len(self.list_align_plt[0]))]
        }
        
        
        # count_head = [str(i+1) for i in range(len(self.list_align_plt[0]))]
        idx=[i for i in range(len(self.list_align_plt[0]))]
        
        
        for ptt in self.list_align_plt:
            for j in range(len(ptt)):
                if ptt[j] == "A":
                    dict_conteos["A"][j] +=1
                    
                elif ptt[j] == "C":
                    dict_conteos["C"][j] +=1
                    
                elif ptt[j] == "G":
                    dict_conteos["G"][j] +=1
                    
                elif ptt[j] == "T":
                    dict_conteos["T"][j] +=1
                    
                else:
                   pass
        
        # print("A: "+str(dict_conteos["A"]))
        # print("C: "+str(dict_conteos["C"]))
        # print("G: "+str(dict_conteos["G"]))
        # print("T: "+str(dict_conteos["T"]))
    
        # indices = np.arange(len(count_head))
        
        data_count = pd.DataFrame(dict_conteos)
        data_count["pos"] = idx
        data_count.set_index("pos", inplace=True)
        
        return data_count
        # print(data_count)
        
        # dict_conteos.clear()
        # count_head.clear()
        
        # motif = self.obtener_motif(data_count)
        # self.ploteo(data_count, motif)
        # self.ploteo_logo(data_count, motif)
        
    
    def obtener_motif(self, dict_conteos ):
        # data_count = pd.DataFrame(dict_conteos)
        # data_count.index = labels_head
        estructurador = eptr.Estructurador(dict_conteos)
        return estructurador.get_estructura()
    
        
        
        
        
    def ploteo(self, dict_conteos=pd.DataFrame, motif = ""):
        logomaker.demo('fig1b')
        crp_df = logomaker.get_example_matrix('crp_energy_matrix', print_description=False)
        # print(crp_df)
        # print(type(crp_df))
        dict_conteos = dict_conteos.sort_index(ascending=False)
        ax = dict_conteos.plot(kind="barh", stacked =True, figsize=(8,6), title = "Matriz de conteo del motif "+ motif) #, y = "columna", x="Nucleotidos")
        ax.set_xlabel("Nucleotidos")
        ax.set_ylabel("Frecuencia")
        xacum = 0
        #Ejes para el plot => Etiquetas de datos
        for y in range(len(dict_conteos)): #y
            for x in range(len(dict_conteos.iloc[y])): # x
                if dict_conteos.iloc[y,x] != 0:
                    xacum += dict_conteos.iloc[y,x]/2
                    ax.text(xacum, y, str(dict_conteos.iloc[y, x]))
                    xacum += dict_conteos.iloc[y,x]/2
            xacum=0
                    
            
        plt.legend(loc=2)

        
        plt.show()
               
        # plt.bar(indices, dict_conteos["A"], label ="A")    
        # plt.bar(indices, dict_conteos["C"], label ="C") #,bottom = np.array(count_a))    
        # plt.bar(indices, dict_conteos["G"], label ="G") #,bottom = np.array(count_c) + np.array(count_a))
        # plt.bar(indices, dict_conteos["T"], label ="T") #,bottom= np.array(count_g) + np.array(count_c) + np.array(count_a))
        # plt.xticks(indices, labels_head)
        # plt.ylabel("Apariciones")    
        # plt.xlabel("Columnas")
        # plt.title("Apariciones por columna")
        # plt.legend(loc= "lower left")
        
        # plt.show() 
 
    def ploteo_logo(self, pd_conteos=pd.DataFrame, motif= ""):
        lgmkr = logomaker.Logo(pd_conteos)
        plt.show()
        
    def ploteo_logo_seq_align(self, patron = ""):
        
        w = len(self.list_align_plt[0])
        # pd_conteos =    logomaker.alignment_to_matrix(seq_ali)
        df_conteos = self.contador()  #logomaker.alignment_to_matrix()
        # print(df_conteos)
        #print(type(df_conteos))
        #print(df_conteos.iloc[0])
        df_info = logomaker.transform_matrix(df_conteos, pseudocount=0.0001, from_type="counts", to_type="information")
        
        motif, exp_reg = self.obtener_motif(df_conteos)
        # print(motif)
        if self.imprimirLogo == True:
            lm = logomaker.Logo(df_info,figsize=(w,4.5))
            lm.ax.set_yticks([0,1,2])
            lm.ax.set_xticks(range(0,w))
            plt.xlabel("Posiciones")
            plt.ylabel("Información (bits)")
        
            if motif != "":
                plt.title("LOGO - "+motif)
                plt.savefig(os.path.join(EXP_FOLDER, "motifs_png", patron)+".png")
                plt.close("all")
            
        # plt.show()
        # else:
        #     plt.title("LOGO - "+patron)
        
        
        
        return df_conteos, df_info, motif, exp_reg

# if __name__ == '__main__':
#     list_ptt = ["CATGCCGCTG",
#                 "GCTGTGANAC",
#                 "TGTGANACAG",
#                 "AGTGGTTTCG",
#                 "CGTGTGAGGG",
#                 "TGTGAGGGCT",
#                 "GATGAGCCCA",
#                 "TATGGAAAAA",
#                 "TATGCGGTAA",
#                 "CATGCCGCTG",      
#                 "GCTGTGANAC",
#                 "TGTGANACAG",
#                 "AGTGGTTTCG",
#                 "CGTGTGAGGG",
#                 "TGTGAGGGCT",
#                 "GATGAGCCCA",
#                 "TATGGAAAAA",
#                 "TATGCGGTAA"]
    # list_ptt = ['ATGCCGCT', 
    #             'ATGAGCCC', 
    #             'ATGGAAAA', 
    #             'ATGCGGTA']
    # list_ptt =[ "TGANACAG",
    #             "CGTGTGAG",
    #             "TCGTTAAG",
    #             "GTTAAGAG",
    #             "ACGATGAG",
    #             "GAGCCCAG",
    #             "AACCACAG",
    #             "CCACGCAG"]
    # g = Graficador(list_align_plt=list_ptt)
    # df_conteos, df_info, motif, exp_reg = g.ploteo_logo_seq_align("TG")
    # print("return")
    # print(df_conteos)
    # print(motif)
    # print(df_info)
    # print(exp_reg)
    
       
