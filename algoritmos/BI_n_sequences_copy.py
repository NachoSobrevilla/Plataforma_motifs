from collections import defaultdict


class basado_indices(object):

   def __init__(self, db_sequence = [], min_sup=2, pos ={}, debug = False, debugTime = False, csv = False):
      self.db_sequence = db_sequence
      self.min_sup=min_sup
      self.pos = pos
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

   def get_lenpos(self):
      return len(self.pos)

   def get_lendbsequence(self):
      return len(self.db_sequence)
   
   def set_csv(self,csv):
      self.csv = csv
   
   def get_cvs(self,csv):
      return self.csv



   def run(self):
      
      candidates = []
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
         print('entra')
         
            
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
         candidates.extend(self.find_next_pos_v2())

         i+=1
         
         if self.get_debug() == True:
            self.print_candidates(itera=i)
         # print('Candidatos Encontrados: ', *list(self.pos.keys()), '\n')

         # self.print_candidates(pos,len(self.db_sequence))
         
         
         # if self.get_lenpos() > 0:
         #    candidates.extend(list(sorted(self.pos.keys(), key=lambda x: x)))
         
         # print(candidates)
         if i == 2:
            break

      if self.get_debug() == True:
         print('\n', 'Patrones Hallados: ', ', '.join(str(c) for c in candidates))
      
      return candidates
      
      

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

      return self.pos.keys()
   

   def find_next_pos_v3(self,):
      r_value = defaultdict(dict)
      r_values = defaultdict(list)
      pass
         

sequence = ['ACGTGTAAAACTCTTGTT', 
            'CTAAGTCCGTAGCCGACT',
            'GGATCCAATCGCTAATCG']

# # sequence = ['ACGTGTAAAACTCTTGTT', 
#           'CTAAGTCCGTAGCCGACT']
min_sup = 2

bi = basado_indices(db_sequence=sequence, min_sup=min_sup, debug=True)
bi.set_pos(bi.find_pos())
print(bi.get_pos())
bi.run()      
