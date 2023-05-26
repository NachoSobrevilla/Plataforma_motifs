class basado_indices(object):

   def __init__(self, ds = [], min_sup=2):
      self.db_sequence=ds
      self.min_sup=min_sup


   def run(self):
      
      candidates = []
      new_pos={}
      aux = {}
      i=0

      pos = self.find_pos(self.db_sequence, self.min_sup)
      # print(pos, end='\n\n')

      self.print_candidates(dict_pos=pos,len_ds=len(self.db_sequence),itera=i)
      # candidates.extend(list(pos.keys()))
      # print(pos)
      
      while len(pos) != 0:

         for key, values in pos.items():
            for v in values:
               if v[1]+len(key) < len(self.db_sequence[v[0]]): #v[0] -> s_id, v[1] -> pos
                  x = self.db_sequence[v[0]][v[1]+len(key)]
                  if key+x in new_pos:
                     new_pos[key+x].append(v)
                  else:
                     new_pos[key+x] = [v]

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
         
         i+=1
         self.print_candidates(
             dict_pos=new_pos, len_ds=len(self.db_sequence), itera=i)

         pos.clear()
         pos = {key: value for key, value in new_pos.items() if len(value) >= self.min_sup}.copy()
         new_pos.clear()

         print('Candidatos Encontrados: ', *list(pos.keys()), '\n')

         # self.print_candidates(pos,len(self.db_sequence))
         
         if len(pos) > 0:
            candidates.extend(list(sorted(pos.keys(), key=lambda x: x)))
         
         # print(candidates)

      print('\n', 'Patrones Hallados: ', ', '.join(str(c) for c in candidates))
      
      

   def find_pos(self, ds=[], min_sup=2):
      """Función dedicada a la busqueda inicial 
      de las posiciones de los nucleotidos en 
      las secuencias de ADN"""

      r_value = {}
      list_pos = []
      bases= ['A','C','G','T']

      for i in range(len(ds)):
         for n in bases:
            p = 0
            while p != -1:
               p = ds[i].find(n,p)
               if p != -1:
                  list_pos.append((i,p))
                  p+=1

            if n not in r_value:
               r_value[n] = list(list_pos)
            else:
               r_value[n].extend(list(list_pos))
            list_pos.clear()
         
         i += 1
      
      # r_value = sorted(r_value, key=lambda x: x[0])
      return r_value
   
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


   def print_candidates(self, dict_pos ={}, len_ds=0, itera=0):
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


      for key, value in dict_pos.items():
         k = '|   '+str(key)+'   |\n'
         # pos = 
         for i in range(len_ds):
            pos += '|   sequence '+str(i)+' : '
            for v in value:
               if i == v[0]:
                  pos += str(v[1])+', '
            pos = pos[:len(pos)-2]
            pos += ' |\n'
               
         r_value += k + pos + line +'\n'
         pos=''
         k=''
 
      print('iteracion '+str(itera)+'\n'+r_value)

      

   def find_pos_next(self, s='', min_sup=0, pos=[], l=0, n =''):
      r_Value = {}
      for p in pos:
         if p+l <= len(s):
            x = s[p+l]
            r_Value[x].append(p)
      
      return {key+n:value for key,value in r_Value.items() if len(value) >= min_sup}
         

sequence = ['ACGTGTAAAACTCTTGTT', 
            'CTAAGTCCGTAGCCGACT',
            'GGATCCAATCGCTAATCG']
min_sup = 2
bi = basado_indices(sequence, min_sup)
bi.run()      



# import collections

# class basado_indices(object):
#    def __init__(self, ds=[], min_sup = 2):
#       self.ds = ds
#       self.min_sup = min_sup

   
#    def run(self):
#       index_items = self.find_index_items(self.ds)
#       maps_items= self.mapeo_candidatos(index_items)
      
#       #for s in self.ds:
      
               


#    def find_index_items(self, ds=''):
#       """Busca los items de las secuencias"""
#       f = [] 
#       i=0
#       #for s in ds:
#       c_list = [c for c, k in collections.Counter(ds).items()]
#       c_list.sort()
#       if c_list != f:
#          if len(f) != 0:
#             f = list(c_list)
#          else:
#             f.extend([c for c in c_list if c not in f])

#       f.sort()

#       d = (dict(zip(range(len(f)),f)))
#       print(d)
#       return d #(dict((i,x) for x in i,f))


#    def mapeo_candidatos(self, index_items={}):
#       r =[]
#       for values in index_items.values():
#          x = []
#          for i in range(len(self.ds)):
#             if self.ds[i] == values:
#                i += 1
#                x.append((i, self.ds[i]))

#          r.append(x)
#          x.clear()
      
#       return x




# ds1 = 'ATTAAAGGTTTATACC'#,  # TTCC',  # CAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAA',
#       # 'CGAACTTTAAAATCTG']  # TGTG']  # GCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAAC']
# #   'TAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTGCAGGCTGCTTACGGTTTCGTCCGTG',
# #   'TTGCAGCCGATCATCAGCACATCTAGGTTTCGTCCGGGTGTGACCGAAAGGTAAGATGGAGAGCCTTGTC',
# #   'CCTGGTTTCAACGAGAAAACACACGTCCAACTCAGTTTGCCTGTTTTACAGGTTCGCGACGTGCTCGTAC']
# min_sup1 = 2


# x = basado_indices(ds1, min_sup1)
# x.run()
