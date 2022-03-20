import os
import sys

if sys.argv[2] == 'M1':
    p = '/home/thibault/M1/' + sys.argv[1] + '/'
else:
    p = '/home/thibault/M2/' + sys.argv[1] + '/'

if sys.argv[1] == 'Metazoa':
    d = {'Actinopterygii': 'Chordata', 'Amphibia': 'Chordata', 'Anthozoa': 'Cnidaria', 'Appendicularia': 'Chordata', 'Arachnida': 'Arthropoda', 'Archiacanthocephala': 'Acanthocephala', 'Ascidiacea': 'Chordata', 'Asteroidea': 'Echinodermata', 'Aves': 'Chordata', 'Bdelloidea': 'Rotifera', 'Bivalvia': 'Mollusca', 'Branchiopoda': 'Arthropoda', 'Caudofoveata': 'Mollusca', 'Cephalaspidomorphi': 'Chordata', 'Cephalopoda': 'Mollusca', 'Cestoda': 'Platyhelminthes', 'Chilopoda': 'Arthropoda', 'Chromadorea': 'Nematoda', 'Clitellata': 'Annelida', 'Collembola': 'Arthropoda', 'Crinoidea': 'Echinodermata', 'Cubozoa': 'Cnidaria', 'Demospongiae': 'Porifera', 'Diplopoda': 'Arthropoda', 'Diplura': 'Arthropoda', 'Echinoidea': 'Echinodermata', 'Elasmobranchii': 'Chordata', 'Enoplea': 'Nematoda', 'Eoacanthocephala': 'Acanthocephala', 'Eutardigrada': 'Tardigrada', 'Gastropoda': 'Mollusca', 'GastrotrichaCIS': 'Gastrotricha', 'GnathostomulidaCIS': 'Gnathostomulida', 'Gordiida': 'Nematomorpha', 
    'Gymnolaemata': 'Bryozoa', 'Heterotardigrada': 'Tardigrada', 'Hexactinellida': 'Porifera', 'Hexanauplia': 'Arthropoda', 'Holocephali': 'Chordata', 'Holothuroidea': 'Echinodermata', 'Homoscleromorpha': 'Porifera', 'Hoplonemertea': 'Nemertea', 'Hydrozoa': 'Cnidaria', 'Ichthyostraca': 'Arthropoda', 'Insecta': 'Arthropoda', 'KinorhynchaCIS': 'Kinorhyncha', 'Leptocardii': 'Chordata', 'Lingulata': 'Brachiopoda', 'Malacostraca': 'Arthropoda', 'Mammalia': 'Chordata', 'Monogenea': 'Platyhelminthes', 'Monogononta': 'Rotifera', 'Myxini': 'Chordata', 'Myxozoa': 'Cnidaria', 'Myzostomida': 'Annelida', 'Nuda': 'Ctenophora', 'Onychophorida': 'Onychophora', 'Ophiuroidea': 'Echinodermata', 'Ostracoda': 'Arthropoda', 'Palaeacanthocephala': 'Acanthocephala', 'Palaeonemertea': 'Nemertea', 'Pauropoda': 'Arthropoda', 'Phascolosomatidea': 'Sipuncula', 'PhoronidaCIS': 'Phoronida', 'Phylactolaemata': 'Bryozoa', 'Pilidiophora': 'Nemertea', 'Polychaeta': 'Annelida', 'Polyplacophora': 'Mollusca', 'Protura': 'Arthropoda', 'Pycnogonida': 'Arthropoda', 'Remipedia': 'Arthropoda', 'Reptilia': 'Chordata', 'Rhabditophora': 'Platyhelminthes', 'RhombozoaIS': 'Rhombozoa', 'Rhynchonellata': 'Brachiopoda', 'Sagittoidea': 'Chaetognatha', 'Sarcopterygii': 'Chordata', 'Scaphopoda': 'Mollusca', 'Scyphozoa': 'Cnidaria', 'Sipunculidea': 'Sipuncula', 'Staurozoa': 'Cnidaria', 'Tentaculata': 'Ctenophora', 'Thecostraca': 'Arthropoda', 'Trematoda': 'Platyhelminthes', 'Turbellaria': 'Platyhelminthes', 'XenacoelomorphaCIS': 'Xenacoelomorpha'}
if sys.argv[1] == 'Plants':
    d = {'Andreaeopsida':'Bryophyta','Bangiophyceae':'Rhodophyta','Bryopsida':'Bryophyta','Chlorodendrophyceae':'Chlorophyta','Chlorophyceae':'Chlorophyta','Compsopogonophyceae':'Rhodophyta','Cyanidiophyceae':'Rhodophyta','Florideophyceae':'Rhodophyta','Liliopsida':'Magnoliophyta','Magnoliopsida':'Magnoliophyta','Nephroselmidophyceae':'Chlorophyta','Pinopsida':'Pinophyta','Polypodiopsida':'Pteridophyta','Polytrichopsida':'Bryophyta','Psilotopsida':'Pteridophyta','Pteridopsida':'Pteridophyta','Pyramimonadophyceae':'Chlorophyta','Rhodellophyceae':'Rhodophyta','Sphagnopsida':'Bryophyta','Trebouxiophyceae':'Chlorophyta','Ulvophyceae':'Chlorophyta'}
if sys.argv[1] == 'Fungi':
    d = {'Agaricomycetes':'Basidiomycota','Agaricostilbomycetes':'Basidiomycota','Arthoniomycetes':'Ascomycota','AscomycotaCIS':'Ascomycota','BasidiomycotaIS':'Basidiomycota','Chytridiomycetes':'Chytridiomycota','Cystobasidiomycetes':'Basidiomycota','Dacrymycetes':'Basidiomycota','Dothideomycetes':'Ascomycota','Eurotiomycetes':'Ascomycota','Exobasidiomycetes':'Basidiomycota','Glomeromycetes':'Glomeromycota','Lecanoromycetes':'Ascomycota','Leotiomycetes':'Ascomycota','Microbotryomycetes':'Basidiomycota','Pezizomycetes':'Ascomycota','Phycomycota':'Myxomycota','Pneumocystidomycetes':'Ascomycota','Pucciniomycetes':'Basidiomycota','Saccharomycetes':'Ascomycota','Sordariomycetes':'Ascomycota','Taphrinomycetes':'Ascomycota','Tremellomycetes':'Basidiomycota','Ustilaginomycetes':'Basidiomycota','Wallemiomycetes':'Basidiomycota','Zygomycetes':'Zygomycota','ZygomycotaIS':'Zygomycota'}

for cl, ph in d.items():
    if sys.argv[2] == 'M1':
        path_nd = p + cl + '_node_trees/'
        path_or = p + cl + '_iq/'
        path_new = p + cl + '_failed_trees/'
    else:
        path_nd = p + cl + '_node_trees2/'
        path_or = p + cl + '_iq2/'
        path_new = p + cl + '_failed_trees2/'
    #Get log-likelihood values for the node trees
    if not os.path.exists(path_nd):
        print('no _node_trees folder for ' + cl)
    else:
        genera_nd = sorted([f for f in os.listdir(path_nd) if not f.startswith('.')])
        loglikes_nd = {}
        for gen in genera_nd:
            l = []
            trees = []
            for tree in sorted([t for t in os.listdir(path_nd + gen + '/') if t.endswith('.iqtree')]):
                with open(path_nd + gen + '/' + tree) as fp:
                    contents = fp.read()
                    for entry in contents.splitlines():
                        if 'Log-likelihood of the tree' in entry:
                            l.append(entry.split(' ')[4])
                            trees.append(tree)
            loglikes_nd[gen.replace('_node_trees','')] = {trees[0].replace('.iqtree',''):l[0]}
            for i in range(1,len(trees)):
                loglikes_nd[gen.replace('_node_trees','')][trees[i].replace('.iqtree','')] = l[i]

        #Get log-likelihood values for the original trees
        genera_or = sorted([f for f in os.listdir(path_or) if f.endswith('.iqtree')])
        loglikes_or = {}
        for gen in genera_or:
            with open(path_or + gen) as fp:
                contents = fp.read()
                for entry in contents.splitlines():
                    if 'Log-likelihood of the tree' in entry:
                        if sys.argv[2] == 'M1': loglikes_or[gen.replace('.fas.iqtree','')] = entry.split(' ')[4]
                        else: loglikes_or[gen.replace('.iqtree','')] = entry.split(' ')[4]

        #Calculate LR values
        lr_values = {}
        for g in loglikes_nd.keys():
            l = []
            trees = []
            c = -1
            values = {}
            for v in loglikes_nd[g]:
                c += 1
                lnL2 = loglikes_nd[g]['tree' + str(c)]
                lnL1 = float(loglikes_or[g])
                LR = 2 * (lnL1 - float(lnL2))
                values[v] = LR
            lr_values[g] = values

        #Finding which trees failed the LRT
        non_sig_nb = [] ; sig_nb = []
        non_sig_trees = dict.fromkeys(list(loglikes_nd.keys()))
        for gen, lrs in lr_values.items():
            non_sig_list = []
            cns = 0 ; cs = 0
            for t, lr in lrs.items():
                if lr < 3.84:
                    cns += 1
                    non_sig_list.append(str(t))
                else:
                    cs += 1
            non_sig_trees[gen] = non_sig_list
            non_sig_nb.append(cns)
            sig_nb.append(cs)

        #Write non sig trees into file called .failed_LRT
        os.mkdir(path_new)
        for k, v in non_sig_trees.items():
            if v != [] and len(v) > 1:
                failed_LRT = []
                for t in v:
                    with open(path_nd + k + '_node_trees/' + t.replace('tree','') + '.nwk') as fp:
                        contents = fp.read()
                        failed_LRT.append(contents.replace('\n',''))
                with open(path_new + k + '.failed_LRT', 'a') as f:
                    f.write('\n'.join(failed_LRT))
    print(cl + ' has been fully processed')
