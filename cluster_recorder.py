import os
import pandas as pd
from collections import defaultdict

# Set paths
BASE_PATH =  os.getcwd().replace('/Scripts', '')
OUTPUT_PATH = os.path.join(BASE_PATH, 'Output/')

# Find all directories ending with '_failed_trees'
failed_trees_folders = [f for f in os.listdir(OUTPUT_PATH) if f.endswith('_failed_trees')]

# Read class-phylum mapping
classes_and_phyla = pd.read_csv(os.path.join(BASE_PATH, 'classes-and-phyla.csv'), index_col = 'Class')

# Intialise a dictionary to store cluster information
clusters_data = defaultdict(dict)

# Loop through all '_failed_trees' folders
for folder in failed_trees_folders:
    class_name = folder.replace('_failed_trees', '')  # Extract class name
    working_path = os.path.join(OUTPUT_PATH, folder)

    # Get phylum for this class
    if class_name not in classes_and_phyla.index:
        phylum = 'NAN'
        print(f'Warning: Class {class_name} not found in classes-and-phyla.csv')
    else:
        phylum = classes_and_phyla.loc[class_name, 'Phylum']

    # Get cluster files
    cluster_files = sorted([f for f in os.listdir(working_path) if f.endswith('.clusters')])

    # Process each cluster file
    for cluster_file in cluster_files:
        genus = cluster_file.replace('.clusters', '')

        # Ensure uniqueness: Append phylum if genus name exists
        unique_genus = f'{genus} ({phylum})' if genus in clusters_data else genus

        # Read the cluster file
        with open(os.path.join(working_path, cluster_file)) as fp:
            contents = fp.read()
            info = [c.strip() for c in contents.splitlines()[5:]]

            # Extract cluster frequencies
            nclusts, freqclusts = [], []
            for line in info:
                nclust, freqclust = map(int, line.split(':'))
                nclusts.append(nclust)
                freqclusts.append(freqclust)

            # Store the cluster frequencies in a dictionary
            clusters_data[unique_genus] = {
                'class': class_name,
                'phylum': phylum,
                **{f'{n} clust': freq for n, freq in zip(nclusts, freqclusts)}
            }

    # Log
    print(f'All clusters recorded for {class_name}.')

# Convert dictionary to DataFrame
clusters_df_total = pd.DataFrame.from_dict(clusters_data, orient = 'index').fillna(0)

# Ensure column order
fixed_columns = ['class', 'phylum']  # First columns
cluster_columns = sorted([col for col in clusters_df_total.columns if 'clust' in col], key = lambda x: int(x.split()[0]))
ordered_columns = ['genus'] + fixed_columns + cluster_columns  # 'genus' will be the reset index name

# Reset index, rename, and reorder columns
clusters_df_total = clusters_df_total.reset_index().rename(columns = {'index': 'genus'})[ordered_columns]

# Save to Excel
cluster_log_path = os.path.join(BASE_PATH, 'Sheets/cluster_log.xlsx')
clusters_df_total.to_excel(cluster_log_path, index = False)
print(f'Results saved to {cluster_log_path}')