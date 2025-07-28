import os
import pandas as pd

# Set paths
BASE_PATH =  os.getcwd().replace('/Scripts', '')
OUTPUT_PATH = os.path.join(BASE_PATH, 'Output/')

# Find all directories ending with '_node_trees'
node_trees_folders = [f for f in os.listdir(OUTPUT_PATH) if f.endswith('_node_trees')]

# Read class-phylum mapping
classes_and_phyla = pd.read_csv(os.path.join(BASE_PATH, 'classes-and-phyla.csv'), index_col = 'Class')

# Initialise DataFrame
lr_df_total = pd.DataFrame(columns = ['genus', 'class', 'phylum', 'number of non sig', 'number of sig', 'total', 'number of spp'])

# Loop through all '_node_trees' folders
for folder_nd in node_trees_folders:
    class_name = folder_nd.replace('_node_trees', '') # Extract class name
    nd_path = os.path.join(OUTPUT_PATH, folder_nd) # Path to 'node_trees' folders

    # Get phylum for this class
    if class_name not in classes_and_phyla.index:
        phylum = 'NAN'
        print(f'Warning: Class {class_name} not found in classes-and-phyla.csv')
    else:
        phylum = classes_and_phyla.loc[class_name, 'Phylum']

    # Get log-likelihood values for the node trees
    gen_node_trees = sorted([f for f in os.listdir(nd_path) if not f.startswith('.')])
    loglikes_nd = {}
    for gen_node_tree in gen_node_trees:
        genus = gen_node_tree.replace('_node_trees','')
        # Ensure uniqueness: Append phylum if genus name exists
        unique_genus = f'{genus} ({phylum})' if genus in loglikes_nd else genus
        l = []
        for tree in sorted([t for t in os.listdir(os.path.join(nd_path, gen_node_tree)) if t.endswith('.iqtree')]):
            # retrieve log-likelihood value
            with open(os.path.join(nd_path, gen_node_tree, tree)) as fp:
                contents = fp.read()
                for entry in contents.splitlines():
                    if 'Log-likelihood of the tree' in entry:
                        l.append(entry.split(' ')[4])
        loglikes_nd[unique_genus] = l

    # Get log-likelihood values for the original trees
    folder_iq = folder_nd.replace('_node_trees','_iq')
    iqtree_path = os.path.join(OUTPUT_PATH, folder_iq) # Path to 'iqtree' folders
    gen_iqtrees = sorted([f for f in os.listdir(iqtree_path) if f.endswith('.iqtree')])
    loglikes_or = {}
    for gen_iqtree in gen_iqtrees:
        genus = gen_iqtree.replace('.iqtree','')
        # Ensure uniqueness: Append phylum if genus name exists
        unique_genus = f'{genus} ({phylum})' if genus in loglikes_or else genus
        # retrieve log-likelihood value
        with open(os.path.join(iqtree_path, gen_iqtree)) as fp:
            contents = fp.read()
            for entry in contents.splitlines():
                if 'Log-likelihood of the tree' in entry:
                    loglikes_or[unique_genus] = entry.split(' ')[4]

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
    non_sig_list, sig_list = [], []
    genera_list = []
    for genus, lrs in lr_values.items():
        cns, cs = 0, 0
        for lr in lrs:
            if lr < 3.84:
                cns += 1
            else:
                cs += 1
        non_sig_list.append(cns)
        sig_list.append(cs)
        genera_list.append(genus)

    # Record to df
    lr_df = pd.DataFrame({
        'genus': genera_list, 
        'class': [class_name] * len(genera_list), 
        'phylum': [phylum] * len(genera_list), 
        'number of non sig': non_sig_list, 
        'number of sig': sig_list
    })
    lr_df['total'] = lr_df['number of non sig'] + lr_df['number of sig']

    # Number of spp
    taxonomy_log = pd.read_excel(os.path.join(BASE_PATH, 'Sheets/log_Metazoa.xlsx'), usecols = [0, 1, 2, 3, 4])
    spp_gen = taxonomy_log.loc[taxonomy_log['class'] == class_name]
    # Create a dictionary mapping genus to species number
    spp_dict = dict(zip(spp_gen['genus'], spp_gen['number of spp']))
    # Map the species number to each genus in lr_df
    lr_df['number of spp'] = lr_df['genus'].map(spp_dict)
    # Fill any NaN values in 'number of spp' with 0 if no match was found
    lr_df['number of spp'].fillna(0, inplace = True)

    # Number of internal branch lengths
    lr_df['number of internal branch lengths'] = lr_df['number of spp'] - 3

    # Percentage of non sig branches
    lr_df['percentage of non sig'] = lr_df['number of non sig'] / lr_df['number of internal branch lengths']

    # Pearson's correlation
    correlation = lr_df[['number of non sig', 'number of spp']].corr()
    corr_value = correlation.loc['number of non sig', 'number of spp']
    print(f"{class_name}: Pearson's correlation coefficient between the number of non-significant branch lengths and the number of species per genus: {corr_value}")

    # Append class results to total loglike DataFrame
    lr_df_total = pd.concat([lr_df_total, lr_df], axis = 0)

# Save to Excel
lr_df_log_path = os.path.join(BASE_PATH, 'Sheets/lr_df_log.xlsx')
lr_df_total.to_excel(lr_df_log_path, index = False)
print(f'Results saved to {lr_df_log_path}')