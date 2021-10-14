import Reader
from algoritmos import BI_n_sequences_copy 


read = Reader(filesnames='Plataforma_motifs\sequencias_prueba\sequence (1).fasta')

list_sequence, headline = read.run()
bi = BI_n_sequences_copy()

bi = bi.basado_indices(min_sup=2)

for sequence, head in list_sequence, headline:
    bi.set_dbsequence(sequence)
    bi.set_pos(bi.find_pos())

    candidates = bi.run()

    print(head)
    print('\n', 'Patrones Hallados: ', ', '.join(str(c) for c in candidates))
    print('\n')
