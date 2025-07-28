import pandas as pd
from pathlib import Path
import sys

# Define base paths
TAXA_PATH = Path('/home/thibault/Taxa')
OUTPUT_PATH = Path('/home/thibault/Output')

# Define the target and output directories (sys.argv corresponds to the current Taxon)
target_dir = TAXA_PATH / sys.argv[1]
output_dir = OUTPUT_PATH / f'{sys.argv[1]}_iq'

# Ensure output directory exists
output_dir.mkdir(parents = True, exist_ok = True)

# Get list of genera
genera = sorted([f for f in target_dir.iterdir() if f.is_file() and not f.name.startswith('.')])

# Initialise dictionary for sequences to crop
all_to_crop = {}

for gen in genera:
    spp, all_labels, all_seqs = [], [], []

    # Read the fasta file contents
    with open(gen, 'r') as fp:
        contents = fp.read()
        
        for entry in contents.split('>')[1:]:
            lines = entry.splitlines()
            label = lines[0]
            seq = lines[1]
            
            # Extract species name and accumulate data
            species = '_'.join(label.split('_')[1:])
            spp.append(species)
            all_labels.append(label)
            all_seqs.append(seq)
    
    # Create a DataFrame for processing
    df = pd.DataFrame({'species': spp, 'label': all_labels, 'sequence': all_seqs})
    df.sort_values(by = 'sequence', key = lambda x: x.str.len(), ascending = False, inplace = True)
    df_cropped = df.drop_duplicates('species')
    keeps = set(df_cropped['label'])
    
    # Construct the cropped file content
    cropped_file_content = ''
    for entry in contents.split('>')[1:]:
        lines = entry.splitlines()
        label = lines[0]
        if label in keeps:
            cropped_file_content += f'>{label}\n' + '\n'.join(lines[1:]) + '\n'
    
    # Write the cropped sequences to a new file
    output_file = output_dir / f'{gen.stem}.fas_cropped'
    with open(output_file, 'w') as f:
        f.write(cropped_file_content)