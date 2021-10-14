from io import FileIO



class Reader():
    """Esta clase esta enfocada a la lectura de archivos fasta para el analsis de sequencias"""
    def __init__(self, filesnames = '', debug = False, debugTime = False, csv = False):
        self.filenames = filesnames
        self.debug = debug
        self.debugTime = debugTime
        self.csv = csv
    
    def set_filesnames(self, filesnames = ''):
        self.filenames = filesnames
    
    def get_filesnames(self):
        return self.filenames

    def set_debug(self, debug=False):
        self.debug = debug

    def get_debug(self):
        return self.debug

    def set_debugtime(self, debugTime=False):
        self.debugTime = debugTime

    def get_debugtime(self):
        return self.debugTime
    
    def set_csv(self,csv):
      self.csv = csv
   
    def get_cvs(self,csv):
      return self.csv


# for file in filenames:



    def matrix_format(self, lines = []):
        r_value = []
        headlines = []
        keys=[]
        sequence_line = ''
        for line in lines:
            if line != '\n':
                if line[0] != '>':
                    sequence_line += line.replace('\n','')
                else:
                    headlines.append(line.replace('\n',''))
                    keys.append(line.split(sep=' ', maxsplit=1)[0][1:])
            else:
                if len(sequence_line)>0:
                    sequence_line.strip()
                    r_value.append(sequence_line.upper())
                    sequence_line = ''
                else:
                    continue
        
        if len(sequence_line) > 0:
            r_value.append(sequence_line)
            sequence_line = ''
        # r_value = [[(lambda x: x+ if x[0] != '>' ] for line in lines if line != '\n']

        return r_value, headlines, keys

    def run(self):
        # for file in self.filenames:
        try:
            with open(self.filenames) as file_object:
                lines = file_object.readlines()
                # print(lines)

        
        except FileNotFoundError as e:
            return (f'Hubo un error en el archivo {self.get_filesnames()}: No se encontro o no existe. \n'+str(e)), 'Error: archivo no encontrado' 
        except FileExistsError as e:
            return (f'Hubo un error en el archivo {self.get_filesnames()}: '+str(e)+'\n'), 'Error dentro del archivo'
        else:
            list_sequence, headlines, keys_seq = self.matrix_format(lines)
            # for line in file_object:
            #     print(line.rstrip()
            if self.debug == True:
                print('Sequencias: \n', '\n'.join(str(ls) for ls in list_sequence))
            
            return list_sequence, headlines, keys_seq

    # r_value = [[line.split() if line[0] != '>' or line != '\n'] in line for lines if line[0] != '>' or line != '\n']


# read = Reader("Plataforma_motifs\\tmp\\test_sequqnce.fasta")
# list, head = read.run()
# print(head)
# print(list)
