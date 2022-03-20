import pandas as pd
import os
from tqdm import tqdm

#function that writes the data for a given genus as a file correspondingly named
def writefile(c, genus):
    genus_df = df[df['genus'] == genus]
    genus_txt = ''.join(['>' + genus_df.index[i] + '_' + genus_df.species[i] + '\n' + genus_df.sequence[i] + '\n' for i in range(len(genus_df))])
    with open('/Users/thibaultbret/'+ c + '/' + genus + '.fas', 'w') as f:
        f.write(genus_txt)

#function that deletes empty folders in a given directory
def delfolder(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        if not dirnames and not filenames:
            print(dirpath.replace(path,'') + ' is empty and was thus removed')
            os.rmdir(dirpath)   

#log datadrame to keep track of number of spp per genus and the hierarchy of each genus
log = pd.DataFrame(columns = ['genus','number of spp','number of sq','class'])

#METAZOA
Acanthocephala = ['Archiacanthocephala','Eoacanthocephala','Palaeacanthocephala','Polyacanthocephala']
Annelida = ['Clitellata','Polychaeta','Myzostomida']
Arthropoda = ['Arachnida','Branchiopoda','Cephalocarida','Chilopoda','Collembola','Diplopoda','Diplura','Hexanauplia','Ichthyostraca','Insecta','Malacostraca','Merostomata','Oligostraca_class_incertae_sedis','Ostracoda','Pauropoda','Protura','Pycnogonida','Remipedia','Symphyla','Thecostraca']
Brachiopoda = ['Craniata','Lingulata','Rhynchonellata']
Bryozoa = ['Gymnolaemata','Phylactolaemata','Stenolaemata']
Chaetognatha = ['Sagittoidea']
Chordata = ['Actinopterygii','Amphibia','Appendicularia','Ascidiacea','Aves','Cephalaspidomorphi','Elasmobranchii','Holocephali','Leptocardii','Mammalia','Myxini','Reptilia','Sarcopterygii','Thaliacea']
Cnidaria = ['Anthozoa','Cubozoa','Hydrozoa','Myxozoa','Scyphozoa','Staurozoa']
Ctenophora = ['Nuda','Tentaculata']
Echinodermata = ['Asteroidea','Crinoidea','Echinoidea','Holothuroidea','Ophiuroidea']
Gastrotricha = ['Gastrotricha_class_incertae_sedis']
Gnathostomulida = ['Gnathostomulida_class_incertae_sedis']
Kinorhyncha = ['Kinorhyncha_incertae_sedis']
Mollusca = ['Aplacophora','Bivalvia','Caudofoveata','Cephalopoda','Gastropoda','Monoplacophora','Polyplacophora','Scaphopoda','Solenogastres']
Nematoda = ['Chromadorea','Enoplea','Nematoda_class_incertae_sedis']
Nematomorpha = ['Gordiida','Nectonematoida']
Nemertea = ['Hoplonemertea','Palaeonemertea','Pilidiophora']
Onychophora = ['Onychophorida']
Phoronida = ['Phoronida_class_incertae_sedis']
Platyhelminthes = ['Cestoda','Monogenea','Platyhelminthes_incertae_sedis','Rhabditophora','Trematoda','Turbellaria']
Porifera = ['Calcarea','Demospongiae','Hexactinellida','Homoscleromorpha']
Rhombozoa = ['Rhombozoa_incertae_sedis']
Rotifera = ['Bdelloidea','Monogononta']
Sipuncula = ['Phascolosomatidea','Sipunculidea']
Tardigrada = ['Eutardigrada','Heterotardigrada']
Xenacoelomorpha = ['Xenacoelomorpha_class_incertae_sedis']

#PLANTAE
Bryophyta = ['Andreaeobryopsida','Andreaeopsida','Bryopsida','Oedipodiopsida','Polytrichopsida','Sphagnopsida','Takakiopsida']
Chlorophyta = ['Chlorodendrophyceae','Chlorophyceae','Chlorophyta_incerta_sedis','Chloropicophyceae','Mamiellophyceae','Nephroselmidophyceae','Palmophyllophyceae','Pedinophyceae','Prasinophyceae','Pyramimonadophyceae','Trebouxiophyceae','Ulvophyceae']
Magnoliophyta = ['Amborellanae','Liliopsida','Magnoliopsida']
Pinophyta = ['Pinopsida']
Pteridophyta = ['Polypodiopsida','Psilotopsida','Pteridopsida']
Rhodophyta = ['Bangiophyceae','Compsopogonophyceae','Cyanidiophyceae','Florideophyceae','Rhodellophyceae','Stylonematophyceae']

#FUNGI
Ascomycota = ['Archaeorhizomycetes','Arthoniomycetes','Ascomycetes','Ascomycota_class_incertae_sedis','Ascomycota_incertae_sedis','Dothideomycetes','Eurotiomycetes','Laboulbeniomycetes','Lecanoromycetes','Leotiomycetes','Lichinomycetes','Neolectomycetes','Pezizomycetes','Pezizomycotina_incertae_sedis','Pneumocystidomycetes','Saccharomycetes','Schizosaccharomycetes','Sordariomycetes','Taphrinomycetes','Xylonomycetes']
Basidiomycota = ['Agaricomycetes','Agaricostilbomycetes','Atractiellomycetes','Basidiomycota_incertae_sedis','Cystobasidiomycetes','Dacrymycetes','Entorrhizomycetes','Exobasidiomycetes','Microbotryomycetes','Mixiomycetes','Pucciniomycetes','Tremellomycetes','Tritirachiomycetes','Ustilaginomycetes','Wallemiomycetes']
Chytridiomycota = ['Chytridiomycetes','Monoblepharidomycetes']
Glomeromycota = ['Glomeromycetes']
Myxomycota = ['Myxomycetes','Phycomycota']
Zygomycota = ['Mucoromycotina','Zygomycetes','Zygomycota_incertae_sedis']

#Give the list of phyla to download (plant phyla in this example)
phyla = [Bryophyta,Chlorophyta,Magnoliophyta,Pinophyta,Pteridophyta,Rhodophyta] 

#DOWNLOADER
#create directory for the class
os.chdir('/Users/thibaultbret')
for p in phyla:
    for c in p:
        #1) DOWNLOAD THE SEQUENCES FROM BOLDSYSTEMS
        downloader = 'curl -o ' + c + '.fas ' + '"http://v3.boldsystems.org/index.php/API_Public/sequence?taxon={}&marker=rbcL"'.format(c)
        #for metazoans --> downloader = 'curl -o ' + c + '.fas ' + '"http://v3.boldsystems.org/index.php/API_Public/sequence?taxon={}&marker=COI-5P"'.format(c)
        #for fungi --> downloader = 'curl -o ' + c + '.fas ' + '"http://v3.boldsystems.org/index.php/API_Public/sequence?taxon={}&marker=rbcL"'.format(c)
        os.system(downloader)
        #2) CONVERT .FAS CLASS FILE TO A FOLDER CONTAINING .FAS FILES FOR ALL THE GENERA CONTAINED IN THE CLASS
        path = '/Users/thibaultbret/'+ c
        species = []
        sequences = []
        ids = []
        #create class folder
        os.makedirs(path)
        #get all the needed data from the original file
        with open(path + '.fas') as fp:
            contents = fp.read()
            for entry in contents.split('>')[1:]:
                #for metazoans --> if 'COI-5P' in entry and 'sp.' not in entry:
                #for fungi --> if 'ITS' in entry and 'sp.' not in entry:
                if 'rbcL' in entry and 'sp.' not in entry:
                    sub = entry.rsplit('|')
                    id = sub[0]
                    sp = sub[1].replace(' ','_')
                    seq = sub[-1].strip('\n')
                    ind = seq.find('\n') + 1
                    seq = seq[ind:]
                    ids.append(id)
                    species.append(sp)
                    sequences.append(seq)
        #convert the newly acquired data into a dataframe for clarity and easier data manipulation
        df = pd.DataFrame({'species':species,'sequence':sequences,'id':ids})
        df = df.set_index('id',ids)
        all_genera = []
        for i in tqdm(df.species):
            g = i.split('_')[0]
            all_genera.append(g)
        df['genus'] = all_genera
        df.sort_values('genus', inplace = True)
        #write .fas file for each genus contained in the class
        for g in tqdm(df.genus.unique()):
            writefile(c,g)
        #delete the original (now redundant) .fas file
        os.remove(path + '.fas')
        #3) FILTER OUT GENERA WITH AN INSUFFICIENT NUMBER OF SPECIES OR SEQUENCES
        genera = []
        nb_spp = []
        nb_sq = []
        for genus in tqdm(sorted(os.listdir(path))):
            if not genus.startswith('.'):
                genera.append(genus.replace('.fas',''))
                with open(path + '/' + genus) as fp:
                    contents = fp.read()
                    sppgen = []
                    for s in contents.split('>')[1:]:
                        s = s.splitlines()[0]
                        sppgen.append(' '.join(s.split('_')[1:]))
                    nb_spp.append(len(set(sppgen)))
                    nb_sq.append(contents.count('>'))
        #add resuslts to dataframe    
        df_to_export = pd.DataFrame({'genus':genera,'number of spp':nb_spp,'number of sq':nb_sq,'class':([c]*len(genera)),'phylum':([p]*len(genera)),'kept in analysis':['Yes']*len(genera)})
        #delete the files corresponding to the genera containing less than 3 species/4 sequences
        too_few_spp = df_to_export[df_to_export['number of spp'] < 3]['genus'].tolist()
        too_few_seq = df_to_export[df_to_export['number of sq'] < 4]['genus'].tolist()
        for genus in [g.replace('.fas', '') for g in sorted(os.listdir(path)) if not g.startswith('.')]:
                if genus in too_few_spp or genus in too_few_seq:
                    os.remove(path + '/' + genus + '.fas')
                    df_to_export.loc[df_to_export.genus == genus, 'kept in analysis'] = 'No'
        #export results to an Excel spreadsheet  
        log = log.append(df_to_export, ignore_index=True)
        #output message to confirm success of operation
        print(c + ' has been fully downloaded and formatted')
#export the log to an excel file
log.to_excel('/Users/thibaultbret/log_' + c + '.xlsx', sheet_name = c, index = False)