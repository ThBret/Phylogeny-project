import pandas as pd
import os
import sys

path = '/home/thibault/M1/' + sys.argv[2] + '/'

genera = sorted([f for f in os.listdir(path + sys.argv[1] + '/') if not f.startswith('.')])
#Get duplicate species sequences
index_count = -1
all_to_crop = {}
for gen in genera:
    #From the fasta file:
    spp = []
    all_labels = []
    all_seqs = []
    with open(path + sys.argv[1] + '/' + gen) as fp:
        contents = fp.read()
        for entry in contents.split('>')[1:]:
            sub = entry.rsplit('\n')
            seq = entry.rsplit('\n')[1]
            all_labels.append(sub[0])
            all_seqs.append(seq)
            spp.append('_'.join(sub[0].rsplit('_')[1:]))
    df = pd.DataFrame({'species':spp, 'label':all_labels, 'sequence':all_seqs})
    df.sort_values(by="sequence", key=lambda x: x.str.len(), ascending = False, inplace = True)
    df_cropped = df.drop_duplicates('species')
    keeps = df_cropped['label'].to_list()
    #CROP FILES
    cropped_file = ''
    with open(path + sys.argv[1] + '/' + gen) as fp:
        contents = fp.read()
        for entry in contents.split('>')[1:]:
            sub = entry.rsplit('\n')
            if sub[0] in keeps:
                cropped_file += '>' + sub[0] + '\n'
                for l in range(1,len(sub)):
                    if sub[l] != '':
                        cropped_file +=  sub[l] + '\n'
    with open(path.replace('M1','M2') + sys.argv[1] + '_iq2/' + gen.replace('.fas','') + '.fas_cropped', 'w') as f:
        f.write(cropped_file)