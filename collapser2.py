from Bio import Phylo
import sys
import os

p = '/home/thibault/M2/' + sys.argv[2] + '/'

def tabulate_names(tree):
	'''
	Give unique id to all internal nodes
	'''
	names = {}

	for idx, clade in enumerate(tree.find_clades()):
		if clade.name:
			continue
		else:
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
	for dirpath, dirnames, filenames in os.walk(path, topdown=False):
		if not dirnames and not filenames:
			print(dirpath.replace(path,'') + ' is empty and was thus removed')
			os.rmdir(dirpath)

path = p + sys.argv[1]

os.chdir(path + '_iq2')
for t in sorted([f for f in os.listdir(path + '_iq2/') if not f.startswith('.') if f.endswith('.treefile')]):
	if os.path.getsize(t):
		tree = Phylo.read(t, "newick")
		tabulate_names(tree)
		clades = get_internodes(tree)
		Phylo.draw_ascii(tree)
		os.mkdir(path + '_node_trees2/' + t.replace('.fas.aln.treefile','') + '_node_trees')
		for i in range(len(clades)):
			tree.collapse(target=clades[i])
			Phylo.write(tree, path + '_node_trees2/' + t.replace('.fas.aln.treefile','') + '_node_trees/' + str(i) + ".nwk", "newick")
			Phylo.draw_ascii(tree)
			tree = Phylo.read(t, "newick")
			tabulate_names(tree)
			clades = get_internodes(tree)




