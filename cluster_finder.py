import os
import sys

# Set paths
OUTPUT_PATH = os.getcwd().replace('/Scripts', '')
PATH_ND = os.path.join(OUTPUT_PATH, f'{sys.argv[1]}_node_trees/')
PATH_OR = os.path.join(OUTPUT_PATH, f'{sys.argv[1]}_iq/')
PATH_NEW = os.path.join(OUTPUT_PATH, f'{sys.argv[1]}_failed_trees/')

#Get log-likelihood values for the node trees
if not os.path.exists(PATH_ND):
    print(f'No "_node_trees" folder for class: {sys.argv[1]}')
else:
    genera_nd = sorted([f for f in os.listdir(PATH_ND) if not f.startswith('.')])
    loglikes_nd = {}
    for gen in genera_nd:
        l = []
        trees = []
        for tree in sorted([t for t in os.listdir(f'{PATH_ND}{gen}/') if t.endswith('.iqtree')]):
            with open(f'{PATH_ND}{gen}/{tree}') as fp:
                contents = fp.read()
                for entry in contents.splitlines():
                    if 'Log-likelihood of the tree' in entry:
                        l.append(entry.split(' ')[4])
                        trees.append(tree)
        loglikes_nd[gen.replace('_node_trees','')] = {trees[0].replace('.iqtree',''):l[0]}
        for i in range(1,len(trees)):
            loglikes_nd[gen.replace('_node_trees','')][trees[i].replace('.iqtree','')] = l[i]

    #Get log-likelihood values for the original trees
    genera_or = sorted([f for f in os.listdir(PATH_OR) if f.endswith('.iqtree')])
    loglikes_or = {}
    for gen in genera_or:
        with open(PATH_OR + gen) as fp:
            contents = fp.read()
            for entry in contents.splitlines():
                if 'Log-likelihood of the tree' in entry:
                    loglikes_or[gen.replace('.iqtree','')] = entry.split(' ')[4]

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
    non_sig_nb, sig_nb = [], []
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
    os.mkdir(PATH_NEW)
    for k, v in non_sig_trees.items():
        if v != [] and len(v) > 1:
            failed_LRT = []
            for t in v:
                with open(os.path.join(PATH_ND, f'{k}_node_trees', f'{t.replace('tree', '')}.nwk')) as fp:
                    contents = fp.read()
                    failed_LRT.append(contents.replace('\n',''))
            with open(os.path.join(PATH_NEW,f'{k}.failed_LRT'), 'a') as f:
                f.write('\n'.join(failed_LRT))

print(f'All clusters found in class {sys.argv[1]}')