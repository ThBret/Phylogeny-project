import os
import sys
import pandas as pd

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

clusters_df_total = pd.DataFrame(columns=['genus','class','phylum','1 clust','2 clust','3 clust','4 clust','5 clust','6 clust','7 clust','8 clust','9 clust']).set_index('genus')

for cl, ph in d.items():
    if sys.argv[2] == 'M1':
        path = p + cl + '_failed_trees/'
    else:
        path = p + cl + '_failed_trees2/'
    #Get the number of cluster per genus
    clusters = sorted([f for f in os.listdir(path) if f.endswith('.clusters')])
    clusters_df = pd.DataFrame({'genus':[c.replace('.clusters','') for c in clusters],'class':[cl]*len(clusters),'phylum':[ph]*len(clusters),'1 clust':[0]*len(clusters),'2 clust':[0]*len(clusters),'3 clust':[0]*len(clusters),'4 clust':[0]*len(clusters),'5 clust':[0]*len(clusters),'6 clust':[0]*len(clusters),'7 clust':[0]*len(clusters),'8 clust':[0]*len(clusters),'9 clust':[0]*len(clusters)})
    clusters_df.set_index('genus', inplace = True)
    d = dict.fromkeys([c.replace('.clusters','') for c in clusters])
    for cluster in clusters:
        d_nested = {}
        with open(path + cluster) as fp:
            contents = fp.read()
            info = [c.strip() for c in contents.splitlines()[5:]]
            nclusts = []
            freqclusts = []
            for i in range(len(info)):
                nclust = int(info[i][0])
                freqclust = int(info[i][-1])
                d_nested[nclust] = freqclust
                nclusts.append(nclust)
                freqclusts.append(freqclust)
            for c in range(len(nclusts)):
                clusters_df.loc[clusters_df.index == cluster.replace('.clusters',''), str(nclusts[c]) + ' clust'] = freqclusts[c]
        d[cluster.replace('.clusters','')] = d_nested
        clusters_df['clusters'] = d.values()
    clusters_df_total = clusters_df_total.append(clusters_df)
    print(cl + ' has been fully processed')
clusters_df_total.reset_index().to_excel('/home/thibault/Sheets/cluster_log_' + sys.argv[1] + '_' + sys.argv[2] + '.xlsx', index = False)
