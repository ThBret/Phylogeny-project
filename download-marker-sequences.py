import pandas as pd
import os
import sys
from tqdm import tqdm

# Set working directory (local/HPC)
if len(sys.argv) < 2 or sys.argv[1] == 'local':
    BASE_PATH = '/Users/thibaultbret'
else:
    BASE_PATH = '/home/thibault'

# Set output path
OUT_PATH = os.path.join(BASE_PATH, 'Taxa')
os.mkdir(OUT_PATH)

# ---------- Helper Functions ----------
def writefile(path, class_name, genus, df):
    """
    Write a FASTA file for a given genus, containing all its species sequences.
    """
    genus_df = df[df['genus'] == genus] # get subset of rows matching the genus
    genus_txt = ''.join([
        f'>{genus_df.index[i]}_{genus_df.species[i]}\n{genus_df.sequence[i]}\n'
        for i in range(len(genus_df))
        ])
    FILE_PATH = os.path.join(path, class_name, f'{genus}.fas')
    with open(FILE_PATH, 'w') as f:
        f.write(genus_txt)


def delfolder(path):
    """
    Delete all empty subdirectories in a given directory.
    """
    for dirpath, dirnames, filenames in os.walk(path, topdown = False):
        if not dirnames and not filenames:
            print(f'{dirpath[len(path):]} is empty and was removed')
            os.rmdir(dirpath)   


# ---------- Taxonomic Reference ----------

# METAZOAN TAXA
Metazoan_phyla = {
    "Acanthocephala": ['Archiacanthocephala', 'Eoacanthocephala', 'Palaeacanthocephala'],
    "Annelida": ['Clitellata', 'Polychaeta', 'Sipuncula'],
    "Arthropoda": ['Arachnida', 'Branchiopoda', 'Cephalocarida', 'Chilopoda', 'Collembola', 'Copepoda', 'Diplopoda', 'Diplura', 'Ichthyostraca', 'Insecta','Malacostraca', 'Merostomata', 'Oligostraca_class_incertae_sedis', 'Ostracoda', 'Pauropoda', 'Protura', 'Pycnogonida', 'Remipedia', 'Symphyla', 'Thecostraca'],
    "Brachiopoda": ['Craniata', 'Lingulata', 'Rhynchonellata'],
    "Bryozoa": ['Gymnolaemata', 'Phylactolaemata', 'Stenolaemata'],
    "Chaetognatha": ['Sagittoidea'],
    "Chordata": ['Actinopterygii', 'Amphibia', 'Appendicularia', 'Ascidiacea', 'Aves', 'Elasmobranchii', 'Holocephali', 'Leptocardii', 'Mammalia', 'Myxini', 'Petromyzonti', 'Reptilia', 'Sarcopterygii', 'Thaliacea'],
    "Cnidaria": ['Anthozoa', 'Cubozoa', 'Hydrozoa', 'Myxozoa', 'Scyphozoa', 'Staurozoa'],
    "Ctenophora": ['Nuda', 'Tentaculata'],
    "Cycliophora": ['Eucycliophora'],
    "Echinodermata": ['Asteroidea', 'Crinoidea', 'Echinoidea', 'Holothuroidea', 'Ophiuroidea'],
    "Entoprocta": ['Entoprocta_class_incertae_sedis'],
    "Gastrotricha": ['Gastrotricha_class_incertae_sedis'],
    "Gnathostomulida": ['Gnathostomulida_class_incertae_sedis'],
    "Hemichordata": ['Enteropneusta', 'Graptolithoidea'],
    "Kinorhyncha": ['Allomalorhagida', 'Cyclorhagida'],
    "Mollusca": ['Bivalvia', 'Caudofoveata', 'Cephalopoda', 'Gastropoda', 'Monoplacophora', 'Polyplacophora', 'Scaphopoda', 'Solenogastres'],
    "Nematoda": ['Chromadorea', 'Enoplea'],
    "Nematomorpha": ['Gordioida'],
    "Nemertea": ['Hoplonemertea', 'Palaeonemertea', 'Pilidiophora'],
    "Onychophora": ['Udeonychophora'],
    "Phoronida": ['Phoronida_class_incertae_sedis'],
    "Placozoa": ['Placozoa_class_incertae_sedis', 'Polyplacotomia'],
    "Platyhelminthes": ['Catenulida', 'Cestoda', 'Monogenea', 'Platyhelminthes_incertae_sedis', 'Rhabditophora', 'Trematoda'],
    "Porifera": ['Calcarea', 'Demospongiae', 'Hexactinellida', 'Homoscleromorpha'],
    "Priapulida": ['Priapulida_class_incertae_sedis', 'Priapulimorpha'],
    "Rhombozoa": ['Rhombozoa_incertae_sedis'],
    "Rotifera": ['Bdelloidea', 'Monogononta', 'Pararotatoria'],
    "Tardigrada": ['Eutardigrada', 'Heterotardigrada'],
    "Xenacoelomorpha": ['Acoelomorpha', 'Xenacoelomorpha_class_incertae_sedis']
    # 'Kinorhyncha_incertae_sedis', 'Nematoda_class_incertae_sedis', 'Nemertea_incertae_sedis' --> classes with no public records 
}

# Classes that require special handling due to size
Problematic_classes = ['Insecta', 'Actinopterygii']


# ---------- Main Downloader Function ----------

def downloader(min_nb_unique_spp, min_nb_seq, phyla = Metazoan_phyla, kingdom = 'Metazoa', marker = 'COI-5P'):
    # Log datadrame keeping track of the number of species per genus and the hierarchy of each genus
    genus_log = pd.DataFrame(columns = ['genus','number of spp','number of sq','class'])

    # Set working directory
    os.chdir(OUT_PATH)

    for phylum, classes in phyla.items():
        for class_name in classes:
            # Define class path
            CLASS_PATH = os.path.join(OUT_PATH, class_name)
            
             # Skip class if directory already exists
            if os.path.isdir(CLASS_PATH):
                print(f'\033[1m/!\ Skipping {class_name} (directory already exists) /!\ \033[0m \n')
                continue

            # ---------- 1. Download Sequences from BOLD Systems ----------
            if not class_name in Problematic_classes:
                os.system(f'curl -# -o {class_name}.fas "http://v3.boldsystems.org/index.php/API_Public/sequence?taxon={class_name}&marker={marker}"')
            
            # Handle large classes (Insecta and Actinopterygii)
            else:
                with open(f'{class_name}-families.txt', 'r') as file:
                    families = file.read().splitlines()
                for index, family in enumerate(families, start = 1):
                    # Download sequence data for each family and append to class '.fas' file
                    os.system(f'curl -# "http://v3.boldsystems.org/index.php/API_Public/sequence?taxon={family}&marker={marker}" >> {class_name}.fas')
                    print(f'{index}/{len(families)}')

            # ---------- 2. Format Sequences ----------
            species, sequences, ids = [], [], []
            os.makedirs(CLASS_PATH) # Create class folder

            # Read the downloaded FASTA file
            with open(f'{class_name}.fas', encoding = 'utf-8', errors = 'ignore') as file:
                contents = file.read()
                for entry in contents.split('>')[1:]:
                    # Check if the entry has the expected format, correct biomarker, and corresponds to a species (two-word name)
                    if '|' in entry and marker in entry:
                        parts = entry.split('|')
                        if len(parts[1].split()) == 2 and 'sp.' not in parts[1]:
                            seq_id = parts[0]
                            species_name = parts[1].replace(' ','_')
                            sequence = parts[-1].split('\n', 1)[-1].strip()
                            ids.append(seq_id)
                            species.append(species_name)
                            sequences.append(sequence)

            # Convert the newly acquired data into a dataframe for clarity and easier data manipulation
            df = pd.DataFrame({'species':species,'sequence':sequences,'id':ids})
            df.set_index('id', inplace = True)
            df['genus'] = df['species'].str.split('_').str[0]
            df.sort_values('genus', inplace = True)

            # Avoid duplicates
            written_genera = set()

            # Write FASTA file for each genus contained in the class
            for genus in tqdm(df.genus.unique(), desc = f'Processing genera from {class_name}'):   
                if genus in written_genera:
                    continue # skip duplicate
                writefile(OUT_PATH, class_name, genus, df)
                written_genera.add(genus)
            
            # Delete the original (now redundant) FASTA file
            os.remove(f'{class_name}.fas')

            # ---------- 3. Filter & Log Genera ----------
            genera_data = []

            for genus_file in tqdm(sorted(os.listdir(CLASS_PATH)), desc = f'Filtering genera from {class_name}'):
                genus_name, ext = os.path.splitext(genus_file)

                # Process only .fas files
                if ext == '.fas' and not genus_file.startswith('.'):
                    with open(os.path.join(CLASS_PATH, genus_file), 'r') as fp:
                        contents = fp.read()

                    # Extract species names and sequences from the .fas file
                    species_names = [
                        ' '.join(entry.split('_')[1:]).splitlines()[0]
                        for entry in contents.split('>')[1:]
                        ]
                    unique_spp_count = len(set(species_names))  # Number of unique species
                    seq_count = contents.count('>')  # Number of sequences

                    # Append data for each genus
                    kept = 'Yes'
                    # Delete files with insufficient species or sequences
                    if unique_spp_count < min_nb_unique_spp or seq_count < min_nb_seq:
                        kept = 'No'
                        try:
                            os.remove(os.path.join(CLASS_PATH, genus_file))
                        except FileNotFoundError:
                            print(f'File not found: {genus_file}')
                        
                    genera_data.append([genus_name, unique_spp_count, seq_count, class_name, phylum, kept])

            # Create a DataFrame for the processed data
            df_to_export = pd.DataFrame(genera_data, columns = ['genus', 'number of spp', 'number of sq', 'class', 'phylum', 'kept in analysis'])

            # Append the results to the log DataFrame
            genus_log = pd.concat([genus_log, df_to_export], ignore_index = True)

            #output message to confirm success of operation
            print(f'{class_name} has been successfully downloaded and processed.\n')
    
    # Export global log to Excel
    LOG_PATH = os.path.join(BASE_PATH, f'log_{kingdom}.xlsx')
    genus_log.to_excel(LOG_PATH, sheet_name = kingdom, index = False)


# For testing:
# downloader(2, 3, phyla = {"Cnidaria": ["Hydrozoa"], "Tardigrada": ['Eutardigrada']}, kingdom = "test")


# ---------- Main Function ----------
if __name__ == "__main__":
    downloader(min_nb_unique_spp = 2, # minimum number of unique species for a genus to be processed
               min_nb_seq = 3, # minimum number of marker sequences for a genus to be processed
               phyla = Metazoan_phyla,
               kingdom = 'Metazoa',
               marker = 'COI-5P')