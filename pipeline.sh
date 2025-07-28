#!/bin/bash

# ----- SETUP ----- #
# Paths
p=/home/thibault
p1=$p/Taxa
p2=$p/Output
cd $p

# Create dir for analysis outpout
mkdir -p "Output"

# Delete empty class directories and shorten long names
for t in Taxa/*; do
    # If $t is an empty directory, delete it
    if [ -d "$t" ] && [ -z "$(ls -A "$t")" ]; then
        rmdir "$t"
        echo "Deleted empty directory: $(basename "$t")"
    # Rename _class_incertae_sedis to _CIS for readability
    elif [[ "$t" == *"_class_incertae_sedis"* ]]; then
        mv "$t" "${t/_class_incertae_sedis/_CIS}"
    # Rename _incertae_sedis to _IS for readability
    elif [[ "$t" == *"_incertae_sedis"* ]]; then
        mv "$t" "${t/_incertae_sedis/_IS}"
    fi
done

# ----- BEGINNING OF PIPELINE ----- #
for t in Taxa/*; do
    t=$(basename "$t")

    # Create "_iq" output dir for the current taxon unless it already exists
    if [ ! -d "$p2/${t}_iq" ]; then
        mkdir "$p2/${t}_iq"
    else
        echo "Directory ${t}_iq already exists"
    fi

    # Processing taxon : X
    echo "Processing taxon: $t"

    # Crop the genus files to only keep 1 sequence per species
    python3 $p/Scripts/cropper.py $t

    # Align the sequences and construct the genus trees ▼
    for i in $(ls $p1/$t); do
        $p/Software/mafft-7.487-without-extensions/core/mafft $p2/${t}_iq/${i}_cropped > $p2/${t}_iq/$i.aln
        $p/Software/iqtree -s $p2/${t}_iq/$i.aln -m GTR+G
        # Clean up
        rm $p2/${t}_iq/$i.aln.bionj \
            $p2/${t}_iq/$i.aln.ckp.gz \
            $p2/${t}_iq/$i.aln.log \
            $p2/${t}_iq/$i.aln.iqtree \
            $p2/${t}_iq/$i.aln.mldist \
            $p2/${t}_iq/$i.aln.uniqueseq.phy
    done

    # Create "_node_trees" output dir for the current taxon unless it already exists
    if [ ! -d "$p2/${t}_node_trees" ]; then
        mkdir "$p2/${t}_node_trees"
    else
        echo "Directory ${t}_node_trees already exists"
    fi

    # Collapse the trees into node trees
    python3 $p/Scripts/collapser.py $t

    # Compare collapsed trees with cropped alignement files ▼
    # Navigate to the "_iq" directory for the current taxon
    cd $p2/${t}_iq
    for i in $(ls *.treefile) ; do
        # Find and delete empty "_node_trees" directories
        if [ -z "$(ls -A $p2/${t}_node_trees/"${i//.fas.aln.treefile}"_node_trees)" ] ; then
            echo ${i//.fas.aln.treefile}"_node_trees is empty and was thus deleted"
            rmdir $p2/${t}_node_trees/"${i//.fas.aln.treefile}"_node_trees
        else
            # If not empty, navigate to the "_node_trees" directory
            cd $p2/${t}_node_trees/"${i//.fas.aln.treefile}"_node_trees
            # Loop through each .nwk file
            for j in $(ls *.nwk) ; do 
                # Run iqtree using the .nwk file as a guide tree (-te option)
                $p/Software/iqtree -m GTR+G -s $p2/${t}_iq/${i//.treefile} -te $j -pre tree${j//.nwk}
                # Clean up
                rm tree${j//.nwk}.ckp.gz \
                    tree${j//.nwk}.treefile \
                    tree${j//.nwk}.log
            done
        fi
    done

    # Return to the "_iq" directory for the current taxon
    cd $p2/${t}_iq
    # Loop through each .treefile file
    for i in $(ls *.treefile); do
        # Run iqtree using the .treefile file as a guide tree (-te option)
        $p/Software/iqtree -m GTR+G -s ${i//.treefile} -te $i -pre ${i//.fas.aln.treefile}
        # Clean up
        rm ${i//.fas.aln.treefile}.ckp.gz \
            ${i//.fas.aln.treefile}.treefile \
            ${i//.fas.aln.treefile}.log
    done
done