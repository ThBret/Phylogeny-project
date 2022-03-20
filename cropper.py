import pandas as pd
import os
import sys

path = '/home/thibault/M1/' + sys.argv[2] + '/'

genera = sorted([f for f in os.listdir(path + sys.argv[1] + '/') if not f.startswith('.')])
all_mono_spec = []
monos_prop = []
paras_prop = []
monos_count = []
paras_count = []
all_d = []
for gen in genera:
    #From the fasta file:
    spp = []
    all_labels = []
    with open(path + sys.argv[1] + '/' + gen) as fp:
        contents2 = fp.read()
        for entry in contents2.split('>')[1:]:
            sub2 = entry.rsplit('\n')[0]
            all_labels.append(sub2)
            spp.append('_'.join(sub2.rsplit('_')[1:]))
    df = pd.DataFrame({'label':all_labels, 'species':spp})
    df.sort_values('species', inplace = True)
    #print(df)
    d = {}
    for spec in df['species'].unique():
        spps = []
        for sppx in df[df['species'] == spec].label:
            spps.append(sppx)
        d[spec] = spps
    all_d.append(d)
    #From the bipartitions:
    list_of_bip = []
    with open(path + sys.argv[1] + '_iq/' + gen + '.bipartition') as fp:
        contents = fp.read()
        for entry in contents.splitlines():
            sub = [s.split('_') for s in entry.split(',')]
            sub_x  = ['_'.join([str(c) for c in lst]) for lst in sub]
            list_of_bip.append(sub_x)
    #Comparison
    count_monophyletic = 0
    mono_spec = []
    for species in d:
        for i in range(len(list_of_bip)):
            reverse_list_of_bips = [x for x in all_labels if x not in list_of_bip[i]]
            d[species].sort()
            list_of_bip[i].sort()
            reverse_list_of_bips.sort()
            if d[species] == list_of_bip[i] or d[species] == reverse_list_of_bips:
                count_monophyletic += 1
                mono_spec.append(species)
            else:
                continue
    all_mono_spec.append(mono_spec)
    #Results
    count_paraphyletic = len(df['species'].unique()) - count_monophyletic
    print('Genus ' + gen.replace('.fas', '') + ': ')
    mono_prop = count_monophyletic/len(df['species'].unique())
    print('Proportion of monophyletic species: {}'.format(mono_prop))
    monos_prop.append(mono_prop) ; monos_count.append(count_monophyletic)
    para_prop = count_paraphyletic/len(df['species'].unique())
    print('Proportion of paraphyletic species: {}'.format(para_prop))
    paras_prop.append(para_prop) ; paras_count.append(count_paraphyletic)
    print('\n')

results = pd.DataFrame({'monophyletic prop':monos_prop, 'paraphyletic prop':paras_prop, 'monophyletic count':monos_count, 'paraphyletic count':paras_count,'genus':[g.replace('.fas', '') for g in genera]})
#results.to_excel('/Users/thibaultbret/bip_results.xlsx', sheet_name = sys.argv[1], index = False)

#isolate paraphyletic sequences
for d in all_d:
    for i in all_mono_spec:
        for j in i:
            if j in d.keys():
                del(d[j])

#save paraphyletic sequences to separate files
index_count = -1
all_para_to_crop = {}
for d in all_d:
    index_count += 1
    para_list = list(d.values())
    para_list = [item for sublist in para_list for item in sublist]
    all_para_to_crop[[g.replace('.fas','') for g in genera][index_count]] = para_list

#Get duplicate species sequences
index_count = -1
all_to_crop = {}
for gen in genera:
    #From the fasta file:
    spp = []
    all_labels = []
    with open(path + sys.argv[1] + '/' + gen) as fp:
        contents = fp.read()
        for entry in contents.split('>')[1:]:
            sub = entry.rsplit('\n')[0]
            all_labels.append(sub)
            spp.append('_'.join(sub.rsplit('_')[1:]))
    df = pd.DataFrame({'label':all_labels, 'species':spp})
    df.sort_values('species', inplace = True)
    duplicates = list(df[df.duplicated(['species'], keep='first')].label)
    #CROP FILES
    to_crop = list(set(all_para_to_crop[gen.replace('.fas','')] + duplicates))
    index_count += 1
    all_to_crop[[g.replace('.fas','') for g in genera][index_count]] = to_crop
    with open(path + sys.argv[1] + '_to_crop/' + gen.replace('.fas','') + '.fas.to_crop', 'a') as f:
        f.write(','.join(to_crop))

#Crop alignment files
for gen in genera:
    cropped_aln = ''
    with open(path + sys.argv[1] + '_iq/' + gen + '.aln') as fp:
        contents = fp.read()
        for entry in contents.split('>')[1:]:
            sub = entry.rsplit('\n')
            if sub[0] not in all_to_crop[gen.replace('.fas','')]:
                cropped_aln += '>' + sub[0] + '\n'
                for l in range(1,len(sub)):
                    if sub[l] != '':
                        cropped_aln +=  sub[l] + '\n'
    with open(path + sys.argv[1] + '_iq/' + gen.replace('.fas','') + '.fas.aln_cropped', 'w') as f:
        f.write(cropped_aln)
