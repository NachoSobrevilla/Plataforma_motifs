from datetime import datetime
import sys
import os

from .clsGntCode import clsGeneticCode as gc
from collections import defaultdict
traductor = gc('')

class basado_indices_sequencial(object):

   def __init__(self, db_sequence = [], min_sup=2, pos = {}, patrones = {}, keys_seqs = [], debug = False, debugTime = False, csv = False, inputType = '', inputName = '', initDateTime=0, finDateTime=0):
      self.db_sequence = db_sequence
      self.min_sup=min_sup
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
      self.db_sequence.clear()
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

   def set_keys_seqs(self, keys_seqs=[]):
      self.keys_seqs = keys_seqs

   def get_keys_seqs(self):
      return self.keys_seqs

   def get_lenpos(self):
      return len(self.pos)

   def get_lendbsequence(self):
      return len(self.db_sequence)
   
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



   def run(self):
      
      # candidates = []
      #new_pos={}
      #new_pos12 = defaultdict(list)
      #new_pos1 = defaultdict(default_factory=dict, iterable=new_pos12)
      #bases = 'ACTG'
      i=0

      if self.get_lenpos() == 0:
         self.pos = self.find_pos()
      # print(pos, end='\n\n')
      if self.get_debug() == True:
         self.print_candidates(itera=i)
      # candidates.extend(list(pos.keys()))
      # print(pos)
      
      

      while self.get_lenpos() != 0:
         # print('entra iteracion '+str(i))
         
            
         # for key, values in self.pos.items():  # Para cada candidato y sus posiciones
         #    for ids, lpos in values.items():
         #       for p in lpos:  # Para las posiciones
         #          if p+len(key) < len(self.db_sequence[ids]):
         #             new_pos1[key+self.db_sequence[ids][p+len(key)]][p+len(key)].append(p)


 

            # new_pos.update({key+nkey: nvalue for nkey,nvalue in aux.items() if len(nvalue) >= self.min_sup})
            # aux.clear()  
            #  x=self.db_sequence[v+len(key)]
            #       if key+x in new_pos:
            #          new_pos[key+x].append(v)
            #       else:
            #          new_pos[key+x] = [v]

      #       # new_pos.update({nkey: nvalue for nkey, nvalue in new_pos.items() if len(nvalue) >= self.min_sup})
      #       # print(new_pos)

         # if len(new_pos) > 0:
         #    candidates.extend(list(sorted(new_pos.keys(), key=lambda x: x)))
            # candidates.append(list(new_pos.keys()))
         
         

         # self.pos.clear()
         # self.pos = {key: value for key, value in new_pos.items() if len(value) >= self.min_sup}
         # new_pos.clear()x

         # candidates.extend(self.find_next_pos_v1())
         self.find_next_pos_v2()
         # candidates.extend(self.find_next_pos_v2())

         # i+=1
         
         if self.get_debug() == True:
            self.print_candidates(itera=i)
         # print('Candidatos Encontrados: ', *list(self.pos.keys()), '\n')

         # self.print_candidates(pos,len(self.db_sequence))
         
         
         # if self.get_lenpos() > 0:
         #    candidates.extend(list(sorted(self.pos.keys(), key=lambda x: x)))
         
         # print(candidates)
         # if i == 2:
         #    break
         # print("#patron_hallados: "+str(len(self.patrones.keys())))
         i+=1

         if self.get_debug() == True:
            print('\n', 'Patrones Hallados: ', ', '.join(str(c) for c in self.get_only_patrones()))
      
     
      # return candidates
      
      

   def find_pos(self, bases = 'ACGT'):
      """Función dedicada a la busqueda inicial 
      de las posiciones de los nucleotidos en 
      las secuencias de ADN"""
      return {n: 
               {i: 
                  [pos for pos in range(len(self.db_sequence[i])) 
                  if self.db_sequence[i][pos] == n]
                  for i in range(self.get_lendbsequence())} 
               for n in bases}
      # r_value = {}
      # list_pos = []
      

      # for i in range(len(ds)):
      #    for n in bases:
      #       p = 0
      #       while p != -1:
      #          p = ds[i].find(n,p)
      #          if p != -1:
      #             list_pos.append((i,p))
      #             p+=1

      #       if n not in r_value:
      #          r_value[n] = list(list_pos)
      #       else:
      #          r_value[n].extend(list(list_pos))
      #       list_pos.clear()
         
      #    i += 1

      
      
      # r_value = sorted(r_value, key=lambda x: x[0])
      # return r_value
   
   # def print_inter_candidates(self, dict_pos={}, len_ds=0, itera=0):
   #    x = ''
   #    pos = ''
   #    line = '-----------------------------------------------------------------------------------------'
   #    for key,value in dict_pos.items():
   #       x += key+':\n'
   #       for i in range(len_ds):
   #          pos += 'Secuencia'+str(i)+': '
   #          for v in value:
   #             if i == v[0]:
   #                pos += str(v[1])+', '
            
   #          pos = pos[:len(pos)-2]
   #          pos += '\n'
   #       x += pos + line + '\n'
      
   #    print(x)


   def print_candidates(self, itera=0):
      pos = ''
      line = '-----------------------------------------------------------------------------------------'
      r_value=''
      # headline='     '+(' '*itera)+'|'

      # for i in range(len_ds):
      #    headline += '  sequence'+str(i+1)+'   |'
      
      # headline+='\n'
      # r_value += headline
      # for key, value in dict_pos.items():
      #    k='|  '+key+'  |'
      #    for i in range(len_ds):
      #       for v in value:
      #          if i == v[0]:
      #             pos += ' '+str(v[1])+','
      #          else:
      #             pos += ' '
                  
      #       pos = pos[:len(pos)-1]
      #       pos += ' |'
      #    pos += '\n'

      #    r_value += k+pos
      #    k=''
      #    pos =''
      
      # print(r_value)

      
      for key, values in self.pos.items():
         k = '|   '+str(key)+'   |\n'
         # pos = 
         # for i in range(value):
         #    pos += '|   sequence '+str(i)+' : '
         #    for v in value:
         #       if i == v[0]:
         #          pos += str(v[1])+', '
         #    pos = pos[:len(pos)-2]
         #    pos += ' |\n'

         for ids, lpos in values.items():
            pos += '|   sequence '+str(ids)+' : '
            pos += ', '.join(str(p) for p in lpos)
            pos += ' |\n'

               
         r_value += k + pos + line +'\n'
         pos=''
         k=''
 
      print('iteracion '+str(itera)+'\n'+r_value)

   # def find_pos_next(self, s='', min_sup=0, pos=[], l=0, n =''):
   #    r_Value = {}
   #    for p in pos:
   #       if p+l <= len(s):
   #          x = s[p+l]
   #          r_Value[x].append(p)
      
   #    return {key+n:value for key,value in r_Value.items() if len(value) >= min_sup}

   def find_next_pos_v1(self):
      r_value = {}

      for key, values in self.pos.items():
          for ids, lpos in values.items():
              for pos in lpos:
                  # v[0] -> s_id, v[1] -> pos
                  if pos+len(key) < len(self.db_sequence[ids]):
                     x = self.db_sequence[ids][pos+len(key)]
                     # print(key, ids, pos, x)
                     if key+x in r_value:
                        if ids in r_value[key+x]:
                           r_value[key+x][ids].append(pos)
                        else:
                           r_value[key+x].update({ids: [pos]})
                     else:
                        r_value[key+x] = {ids: [pos]}

      self.pos.clear()
      self.set_pos(
          {key: values for key, values in r_value.items() if len(values) >= self.min_sup if len(values.values()) >= 1})

      return self.pos.keys()

   def find_next_pos_v2(self, bases ='ACGT'):

      r_value = {key+b: 
                  {ids: 
                     [p for p in lpos if p+len(key) < len(self.db_sequence[ids]) if self.db_sequence[ids][p + len(key)] == b]for ids, lpos in values.items() }
                 for key, values in self.pos.items() 
                  for b in bases 
                     }
      
      r_value = {keys: {key: value for key,value in values.items() if len(value)>0} 
                           for keys, values in r_value.items() if len(values) >= self.min_sup}
      
      # r_value = {keys: values for keys, values in r_value.items() for key,value in values.items() if len(value)>0 if len(values) >= self.min_sup}
      
      # if len(lpos) > 0
      self.pos.clear()
      # self.set_pos({key: values for key, values in r_value.items()
      #               if len(values.values()) > 0 if len(values) >= self.min_sup  })

       
      self.set_pos({keys: values for keys, values in r_value.items() if len(values) >= self.min_sup})

      # self.info_candidates()
      self.update_patrones(self.get_pos())

      # return self.pos.keys()
   

   def find_next_pos_v3(self):
      r_value = defaultdict(dict)
      r_values = defaultdict(list)
      pass

   def traductorCodon(self, codon):
      global traductor
      if len(codon) > 2:
         traductor.setCodon(codon)
         return traductor.getCodonCoded()
      else:
         return ''
      
   def info_patrones(self):
      key_seq = lambda x: self.keys_seqs[x] if len(self.keys_seqs) else x
      
      return { "Configuracion": {
                                 "Algoritmo":"Basado en indices en multiples sequencias",
                                 "Siglas": "BIMS",
                                 "Min_sup": self.get_minsup(),
                                 "Tipo_Entrada": self.get_inputType(),
                                 "Entrada": self.get_inputName(),
                                 "Sequencias_ananlizadas": "-".join(self.get_keys_seqs()),
                                 "Num_Sequencias_ananlizadas": len(self.get_dbsequence()),
                                 "Lon_Sequencias_ananlizadas": "-".join(str(len(i)) for i in self.db_sequence),
                                 "Num_Patrones_hallados": len(self.get_patrones()),
                                 "Fecha_Hora_Inicio": "{}".format(self.get_initDateTime()),
                                 "Fecha_Hora_Fin": "{}".format(self.get_finDateTime()),
                                 "Duracion": str(self.get_finDateTime() - self.get_initDateTime())
                                 },
                  "Patrones": [{
                              "Patron": key,
                              "Longitud": len(key),
                              "Ocurrencias": len(values.items()),
                              "Traduccion_aminoacido": self.traductorCodon(key),   #.getCodonCoded(),
                              "Posiciones": [{
                                             "sequencia": key_seq(seq),
                                             "posicion": p+1}
                                             for seq, pos in values.items() for p in pos]
                              }for key, values in self.patrones.items()]
               }
            #     "Patrones": [{
            #                "Patron": k,
            #                "Longitud": len(k),
            #                "Ocurrencia": (len(v)),
            #                "Posciones": [{
            #                               "sequencia": key, 
            #                               "posicion": pos+1} 
            #                               for  pos in v]
            #                }for key, values in self.patrones.items()
            #                   for k, v in values.items()]
            # }
            #   "Patrones": [{
            #                "Patron": key,
            #                "Longitud": len(key),
            #                "Ocurrencia": car(len(values)),
            #                "Posciones": [{
            #                               "sequencia": seq, 
            #                               "Inicios": pos} 
            #                               for seq, pos in values.items()]
            #                }for key, values in self.patrones.items()]
            # }
           
      # return {"Patrones": [{
      #                      "Patron": key,
      #                      "Longitud": len(key),
      #                      "Ocurrencia": car(len(values)),
      #                      "Posciones": [{
      #                                     "sequencia": seq, 
      #                                     "Inicios": pos} 
      #                                     for seq, pos in values.items()]
      #                      }for key, values in self.patrones.items()]
      #       }
      # self.keys_seqs.update({
      #                      key: [{
      #                          "longitud": len(key),
      #                          "Frecuenicia": len(values),
      #                          "Ocurrencia": car(len(values)),
      #                          "posiciones": [{"sequencia":seq, "posciones":pos} for seq, pos in values.items() ]  #dict(values.items())
      #                      }]
      #                      
      #                      })

# sequence = ['ACGTGTAAAACTCTTGTT', 
#             'CTAAGTCCGTAGCCGACT',
#             'GGATCCAATCGCTAAT-CG']


   
  
# def main():     
#    sequence = ['ACGTGTAAAACTCTTGTT', 
#             'CTAAGTCCGTAGCCGACT']
#    min_sup = 2

#    bi = basado_indices_sequencial(db_sequence=sequence, min_sup=min_sup, debug=True)
#    bi.set_pos(bi.find_pos())
#    bi.run()      
#    # # print("\n")
#    # # print(bi.get_keys_seqs())
#    # print("\n")
#    # print(bi.get_patrones())
#    # print("\n")
#    print(bi.info_patrones())

# if __name__ == '__main__':
#    main()
