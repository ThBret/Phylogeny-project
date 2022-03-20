k=Metazoa
p=/home/thibault
p2=$p/M1/$k
for t in Actinopterygii Amphibia Anthozoa Appendicularia Arachnida Archiacanthocephala Ascidiacea Asteroidea Aves Bdelloidea Bivalvia Branchiopoda Caudofoveata Cephalaspidomorphi Cephalopoda Cestoda Chilopoda Chromadorea Clitellata Collembola Crinoidea Cubozoa Demospongiae Diplopoda Diplura Echinoidea Elasmobranchii Enoplea Eoacanthocephala Eutardigrada Gastropoda GastrotrichaCIS GnathostomulidaCIS Gordiida Gymnolaemata Heterotardigrada Hexactinellida Hexanauplia Holocephali Holothuroidea Homoscleromorpha Hoplonemertea Hydrozoa Ichthyostraca Insecta KinorhynchaCIS Leptocardii Lingulata Malacostraca Mammalia Monogenea Monogononta Myxini Myxozoa Myzostomida Nuda Onychophorida Ophiuroidea Ostracoda Palaeacanthocephala Palaeonemertea Pauropoda Phascolosomatidea PhoronidaCIS Phylactolaemata Pilidiophora Polychaeta Polyplacophora Protura Pycnogonida Remipedia Reptilia Rhabditophora RhombozoaIS Rhynchonellata Sagittoidea Sarcopterygii Scaphopoda Scyphozoa Sipunculidea Staurozoa Tentaculata Thecostraca Trematoda Turbellaria XenacoelomorphaCIS
do
cd $p2
mkdir ${t}_iq
touch ${t}_iq/record.txt
echo -e "Less than 4 sequences after crop (empty cropped file):\n\n\nMore than 4 sequences after crop:" >> ${t}_iq/record.txt
for i in $(ls $t)
do
    $p/Software/mafft-7.487-without-extensions/core/mafft $t/$i > ${t}_iq/$i.aln
    $p/Software/iqtree -s ${t}_iq/$i.aln -m GTR+G
    rm ${t}_iq/$i.aln.bionj
    rm ${t}_iq/$i.aln.ckp.gz
    rm ${t}_iq/$i.aln.log
    rm ${t}_iq/$i.aln.iqtree
    rm ${t}_iq/$i.aln.mldist
    rm ${t}_iq/$i.aln.uniqueseq.phy
    $p/Software/nt-ng/newick-tools --bipartitions --tree ${t}_iq/$i.aln.treefile | tail -n+6 > ${t}_iq/$i.bipartition
done
mkdir ${t}_to_crop
python3 $p/Scripts/cropper.py $t $k
for i in $(ls $t)
do
    if [ -s ${t}_to_crop/$i.to_crop ]
    then $p/Software/nt-ng/newick-tools --prune_labels `cat ${t}_to_crop/$i.to_crop` --tree ${t}_iq/$i.aln.treefile --output ${t}_iq/$i.cropped_tree
    else cp ${t}_iq/$i.aln.treefile ${t}_iq/$i.cropped_tree
    fi
    if [ ! -s ${t}_iq/$i.cropped_tree ]
    then 
        sed "/^Less than 4 sequences after crop (empty cropped file):/a"${i//.fas} ${t}_iq/record.txt > ${t}_iq/intermediate.txt && mv ${t}_iq/intermediate.txt ${t}_iq/record.txt
        rm ${t}_iq/$i.cropped_tree
    fi
    if [ -s ${t}_iq/$i.cropped_tree ]
    then sed "/^More than 4 sequences after crop:/a"${i//.fas} ${t}_iq/record.txt > ${t}_iq/intermediate.txt && mv ${t}_iq/intermediate.txt ${t}_iq/record.txt
    fi
done
mkdir ${t}_node_trees
python3 $p/Scripts/collapser.py $t $k
cd ${t}_iq
for i in $(ls *.cropped_tree)
do if [ -z "$(ls -A $p2/${t}_node_trees/"${i//.fas.cropped_tree}"_node_trees)" ]
    then
        echo ${i//.fas.cropped_tree}"_node_trees is empty and was thus deleted"
        rmdir $p2/${t}_node_trees/"${i//.fas.cropped_tree}"_node_trees
    else
        cd $p2/${t}_node_trees/"${i//.fas.cropped_tree}"_node_trees
        for j in $(ls *.nwk)
        do 
            $p/Software/iqtree -m GTR+G -s $p2/${t}_iq/${i//.cropped_tree}.aln_cropped -te $j -pre tree${j//.nwk}
            rm tree${j//.nwk}.ckp.gz
            rm tree${j//.nwk}.treefile
            rm tree${j//.nwk}.log
        done
    fi
done
for i in $(ls *.fas.cropped_tree)
do
    $p/Software/iqtree -m GTR+G -s ${i//.cropped_tree}.aln_cropped -te $i -pre ${i//.cropped_tree}
    rm ${i//.cropped_tree}.ckp.gz
    rm ${i//.cropped_tree}.treefile
    rm ${i//.cropped_tree}.log
done
done