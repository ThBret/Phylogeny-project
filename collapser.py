from Bio import Phylo
import sys
import os

# Define base path
BASE_PATH = '/home/thibault/Output/'

def tabulate_names(tree):
	'''
	Give unique id to all internal nodes
	'''
	names = {}

	# Iterate through all clades in the tree
	for idx, clade in enumerate(tree.find_clades()):
		# Skip clades that already have names
		if clade.name:
			continue
		else:
			# Assign a unique name to the internal clade
			clade.name = str(idx)
		names[clade.name] = clade
	return names

def get_internodes(tree):
	'''
	store all internal nodes in a list
	'''
	clades = []
	for i in range(1, len(tree.get_nonterminals())):
		clades.append(tree.get_nonterminals()[i])
	return clades

def del_empty_folders(path):
	'''
	delete empty folders
	'''
	for dirpath, dirnames, filenames in os.walk(path, topdown = False):
		if not dirnames and not filenames:
			# Print and remove empty directory
			print(f'{dirpath.replace(path, "")} is empty and was thus removed')
			os.rmdir(dirpath)

# Define taxon path from command line argument
Taxon_path = f'{BASE_PATH}/{sys.argv[1]}'

# Change directory to the taxon tree directory
os.chdir(f'{Taxon_path}_iq')
for t in sorted([f for f in os.listdir(f'{Taxon_path}_iq') if f.endswith('.treefile') and not f.startswith('.')]):
	if os.path.getsize(t): # Skip empty files
		tree = Phylo.read(t, 'newick')
		tabulate_names(tree)
		clades = get_internodes(tree)
		Phylo.draw_ascii(tree)

        # Create output directory for node trees
		output_dir = f'{Taxon_path}_node_trees/{t.replace(".fas.aln.treefile", "")}_node_trees'
		os.makedirs(output_dir, exist_ok = True)
	
		# Iterate over each internal node and create collapsed trees
		for i in range(len(clades)):
			tree.collapse(target = clades[i])

			# Write the collapsed tree to a file
			Phylo.write(tree, f'{output_dir}/{str(i)}.nwk', 'newick')

			# Visualise the collapsed tree
			Phylo.draw_ascii(tree)

			# Reset tree to original state
			tree = Phylo.read(t, 'newick')
			tabulate_names(tree)
			clades = get_internodes(tree)
