# ----- SETUP ----- #
# Paths
p=/home/thibault
p1=$p/Taxa
p2=$p/Output

# ----- BEGINNING OF PIPELINE ----- #
for t in Taxa/*; do
    t=$(basename "$t")
    cd $p2

    # Identify clusters in failed trees
    python3 $p/Scripts/cluster_finder.py $t

    # ...
    for g in $(ls $p2/${t}_failed_trees) ; do
        cd $p2/${t}_failed_trees
        $p/Software/raxmlHPC-PTHREADS-AVX2 -m GTRGAMMA -J MRE -z $g -n con
        rm RAxML_info.con
        sed "s/1\.0//g" RAxML_MajorityRuleExtendedConsensusTree.con | sed "s/\[//g" | sed "s/\]//g" > con.ed
        $p/Software/nt-ng/newick-tools --rapid 99 --tree con.ed > ${g//.failed_LRT}.clusters
        rm RAxML_MajorityRuleExtendedConsensusTree.con
        rm con.ed
    done
done

# Record the clusters
python3 $p/Scripts/cluster_recorder.py

# Get loglike values
python3 $p/Scripts/loglike.py

# Get pairwise distances
Rscript $p/Scripts/pairwise-dist.R