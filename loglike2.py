import pandas as pd
import os
import sys

p = '/home/thibault/M2/' + sys.argv[1] + '/'

if sys.argv[1] == 'Metazoa':
    d = {'Actinopterygii': 'Chordata', 'Amphibia': 'Chordata', 'Anthozoa': 'Cnidaria', 'Appendicularia': 'Chordata', 'Arachnida': 'Arthropoda', 'Archiacanthocephala': 'Acanthocephala', 'Ascidiacea': 'Chordata', 'Asteroidea': 'Echinodermata', 'Aves': 'Chordata', 'Bdelloidea': 'Rotifera', 'Bivalvia': 'Mollusca', 'Branchiopoda': 'Arthropoda', 'Caudofoveata': 'Mollusca', 'Cephalaspidomorphi': 'Chordata', 'Cephalopoda': 'Mollusca', 'Cestoda': 'Platyhelminthes', 'Chilopoda': 'Arthropoda', 'Chromadorea': 'Nematoda', 'Clitellata': 'Annelida', 'Collembola': 'Arthropoda', 'Crinoidea': 'Echinodermata', 'Cubozoa': 'Cnidaria', 'Demospongiae': 'Porifera', 'Diplopoda': 'Arthropoda', 'Diplura': 'Arthropoda', 'Echinoidea': 'Echinodermata', 'Elasmobranchii': 'Chordata', 'Enoplea': 'Nematoda', 'Eoacanthocephala': 'Acanthocephala', 'Eutardigrada': 'Tardigrada', 'Gastropoda': 'Mollusca', 'GastrotrichaCIS': 'Gastrotricha', 'GnathostomulidaCIS': 'Gnathostomulida', 'Gordiida': 'Nematomorpha', 
    'Gymnolaemata': 'Bryozoa', 'Heterotardigrada': 'Tardigrada', 'Hexactinellida': 'Porifera', 'Hexanauplia': 'Arthropoda', 'Holocephali': 'Chordata', 'Holothuroidea': 'Echinodermata', 'Homoscleromorpha': 'Porifera', 'Hoplonemertea': 'Nemertea', 'Hydrozoa': 'Cnidaria', 'Ichthyostraca': 'Arthropoda', 'Insecta': 'Arthropoda', 'KinorhynchaCIS': 'Kinorhyncha', 'Leptocardii': 'Chordata', 'Lingulata': 'Brachiopoda', 'Malacostraca': 'Arthropoda', 'Mammalia': 'Chordata', 'Monogenea': 'Platyhelminthes', 'Monogononta': 'Rotifera', 'Myxini': 'Chordata', 'Myxozoa': 'Cnidaria', 'Myzostomida': 'Annelida', 'Nuda': 'Ctenophora', 'Onychophorida': 'Onychophora', 'Ophiuroidea': 'Echinodermata', 'Ostracoda': 'Arthropoda', 'Palaeacanthocephala': 'Acanthocephala', 'Palaeonemertea': 'Nemertea', 'Pauropoda': 'Arthropoda', 'Phascolosomatidea': 'Sipuncula', 'PhoronidaCIS': 'Phoronida', 'Phylactolaemata': 'Bryozoa', 'Pilidiophora': 'Nemertea', 'Polychaeta': 'Annelida', 'Polyplacophora': 'Mollusca', 'Protura': 'Arthropoda', 'Pycnogonida': 'Arthropoda', 'Remipedia': 'Arthropoda', 'Reptilia': 'Chordata', 'Rhabditophora': 'Platyhelminthes', 'RhombozoaIS': 'Rhombozoa', 'Rhynchonellata': 'Brachiopoda', 'Sagittoidea': 'Chaetognatha', 'Sarcopterygii': 'Chordata', 'Scaphopoda': 'Mollusca', 'Scyphozoa': 'Cnidaria', 'Sipunculidea': 'Sipuncula', 'Staurozoa': 'Cnidaria', 'Tentaculata': 'Ctenophora', 'Thecostraca': 'Arthropoda', 'Trematoda': 'Platyhelminthes', 'Turbellaria': 'Platyhelminthes', 'XenacoelomorphaCIS': 'Xenacoelomorpha'}
if sys.argv[1] == 'Plants':
    d = {'Andreaeopsida':'Bryophyta','Bangiophyceae':'Rhodophyta','Bryopsida':'Bryophyta','Chlorodendrophyceae':'Chlorophyta','Chlorophyceae':'Chlorophyta','Compsopogonophyceae':'Rhodophyta','Cyanidiophyceae':'Rhodophyta','Florideophyceae':'Rhodophyta','Liliopsida':'Magnoliophyta','Magnoliopsida':'Magnoliophyta','Nephroselmidophyceae':'Chlorophyta','Pinopsida':'Pinophyta','Polypodiopsida':'Pteridophyta','Polytrichopsida':'Bryophyta','Psilotopsida':'Pteridophyta','Pteridopsida':'Pteridophyta','Pyramimonadophyceae':'Chlorophyta','Rhodellophyceae':'Rhodophyta','Sphagnopsida':'Bryophyta','Trebouxiophyceae':'Chlorophyta','Ulvophyceae':'Chlorophyta'}
if sys.argv[1] == 'Fungi':
    d = {'Agaricomycetes':'Basidiomycota','Agaricostilbomycetes':'Basidiomycota','Arthoniomycetes':'Ascomycota','AscomycotaCIS':'Ascomycota','BasidiomycotaIS':'Basidiomycota','Chytridiomycetes':'Chytridiomycota','Cystobasidiomycetes':'Basidiomycota','Dacrymycetes':'Basidiomycota','Dothideomycetes':'Ascomycota','Eurotiomycetes':'Ascomycota','Exobasidiomycetes':'Basidiomycota','Glomeromycetes':'Glomeromycota','Lecanoromycetes':'Ascomycota','Leotiomycetes':'Ascomycota','Microbotryomycetes':'Basidiomycota','Pezizomycetes':'Ascomycota','Phycomycota':'Myxomycota','Pneumocystidomycetes':'Ascomycota','Pucciniomycetes':'Basidiomycota','Saccharomycetes':'Ascomycota','Sordariomycetes':'Ascomycota','Taphrinomycetes':'Ascomycota','Tremellomycetes':'Basidiomycota','Ustilaginomycetes':'Basidiomycota','Wallemiomycetes':'Basidiomycota','Zygomycetes':'Zygomycota','ZygomycotaIS':'Zygomycota'}

lr_df_total = pd.DataFrame(columns=['genus','class','phylum','number of non sig','number of sig','total','number of spp'])

for c, ph in d.items():
    path_nd = p + c + '_node_trees2/'
    path_or = p + c + '_iq2/'
    #Get log-likelihood values for the node trees
    if not os.path.exists(path_nd):
        print('no _node_trees folder for ' + c)
    else:
        genera_nd = sorted([f for f in os.listdir(path_nd) if not f.startswith('.')])
        loglikes_nd = {}
        for gen in genera_nd:
            l = []
            for tree in sorted([t for t in os.listdir(path_nd + gen + '/') if t.endswith('.iqtree')]):
                with open(path_nd + gen + '/' + tree) as fp:
                    contents = fp.read()
                    for entry in contents.splitlines():
                        if 'Log-likelihood of the tree' in entry:
                            l.append(entry.split(' ')[4])
            loglikes_nd[gen.replace('_node_trees','')] = l

        #Get log-likelihood values for the original trees
        genera_or = sorted([f for f in os.listdir(path_or) if f.endswith('.iqtree')])
        loglikes_or = {}
        for gen in genera_or:
            with open(path_or + gen) as fp:
                contents = fp.read()
                for entry in contents.splitlines():
                    if 'Log-likelihood of the tree' in entry:
                        loglikes_or[gen.replace('.iqtree','')] = entry.split(' ')[4]

        #Calculate LR values
        lr_values = {}
        for g in loglikes_nd.keys():
            l = []
            for lnL2 in loglikes_nd[g]:
                lnL1 = float(loglikes_or[g])
                LR = 2 * (lnL1 - float(lnL2))
                l.append(LR)
            lr_values[g] = l

        #Number of significant trees per genus
        non_sig_list = [] ; sig_list = []
        for lrs in lr_values.values():
            cns = 0 ; cs = 0
            for lr in lrs:
                if lr < 3.84:
                    cns += 1
                else:
                    cs +=1
            non_sig_list.append(cns)
            sig_list.append(cs)
        lr_df = pd.DataFrame({'genus':[g.replace('_node_trees','') for g in genera_nd],'class':[c]*len(genera_nd),'phylum':[ph]*len(genera_nd),'number of non sig':non_sig_list,'number of sig':sig_list})
        lr_df['total'] = lr_df['number of non sig'] + lr_df['number of sig']

        #Number of spp
        spp_gen_all = pd.read_excel(p.replace('M2/' + sys.argv[1] + '/','') + 'Sheets/log_' + sys.argv[1] + '.xlsx', usecols=[0,1,2,3,4])
        spp_gen = spp_gen_all.loc[spp_gen_all['class'] == c]
        spp_numbers = []
        for g in spp_gen.sort_values('genus')['genus']:
            if g in list(lr_df['genus']):
                spp_numbers.append(spp_gen.loc[spp_gen['genus'] == g, 'number of spp'].iloc[0])

        lr_df['number of spp'] = spp_numbers
        correlation = lr_df.corr()
        print(c + ": Pearson's correlation coefficient betwen the number of non-significant branch lengths and the number of species per genus: {}".format(correlation.loc['number of non sig', 'number of spp']))
        lr_df_total = lr_df_total.append(lr_df, ignore_index=True)
lr_df_total.to_excel(p.replace('M2/' + sys.argv[1] + '/','') + 'Sheets/lr_df_log_' + sys.argv[1] + '_M2.xlsx', index = False)