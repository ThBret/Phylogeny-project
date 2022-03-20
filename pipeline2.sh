k=Metazoa
p=/home/thibault
p1=$p/M1/$k
p2=$p/M2/$k
for t in Actinopterygii Amphibia Anthozoa Appendicularia Arachnida Archiacanthocephala Ascidiacea Asteroidea Aves Bdelloidea Bivalvia Branchiopoda Caudofoveata Cephalaspidomorphi Cephalopoda Cestoda Chilopoda Chromadorea Clitellata Collembola Crinoidea Cubozoa Demospongiae Diplopoda Diplura Echinoidea Elasmobranchii Enoplea Eoacanthocephala Eutardigrada Gastropoda GastrotrichaCIS GnathostomulidaCIS Gordiida Gymnolaemata Heterotardigrada Hexactinellida Hexanauplia Holocephali Holothuroidea Homoscleromorpha Hoplonemertea Hydrozoa Ichthyostraca Insecta KinorhynchaCIS Leptocardii Lingulata Malacostraca Mammalia Monogenea Monogononta Myxini Myxozoa Myzostomida Nuda Onychophorida Ophiuroidea Ostracoda Palaeacanthocephala Palaeonemertea Pauropoda Phascolosomatidea PhoronidaCIS Phylactolaemata Pilidiophora Polychaeta Polyplacophora Protura Pycnogonida Remipedia Reptilia Rhabditophora RhombozoaIS Rhynchonellata Sagittoidea Sarcopterygii Scaphopoda Scyphozoa Sipunculidea Staurozoa Tentaculata Thecostraca Trematoda Turbellaria XenacoelomorphaCIS
do
cd $p1
mkdir $p2/${t}_iq2
python3 $p/Scripts/cropper2.py $t $k
for i in $(ls $t)
do
    $p/Software/mafft-7.487-without-extensions/core/mafft $p2/${t}_iq2/${i}_cropped > $p2/${t}_iq2/$i.aln
    $p/Software/iqtree -s $p2/${t}_iq2/$i.aln -m GTR+G
    rm $p2/${t}_iq2/$i.aln.bionj
    rm $p2/${t}_iq2/$i.aln.ckp.gz
    rm $p2/${t}_iq2/$i.aln.log
    rm $p2/${t}_iq2/$i.aln.iqtree
    rm $p2/${t}_iq2/$i.aln.mldist
    rm $p2/${t}_iq2/$i.aln.uniqueseq.phy
done
mkdir $p2/${t}_node_trees2
python3 $p/Scripts/collapser2.py $t $k
cd $p2/${t}_iq2
for i in $(ls *.treefile)
do if [ -z "$(ls -A $p2/${t}_node_trees2/"${i//.fas.aln.treefile}"_node_trees)" ]
    then
        echo ${i//.fas.aln.treefile}"_node_trees is empty and was thus deleted"
        rmdir $p2/${t}_node_trees2/"${i//.fas.aln.treefile}"_node_trees
    else
        cd $p2/${t}_node_trees2/"${i//.fas.aln.treefile}"_node_trees
        for j in $(ls *.nwk)
        do 
            $p/Software/iqtree -m GTR+G -s $p2/${t}_iq2/${i//.treefile} -te $j -pre tree${j//.nwk}
            rm tree${j//.nwk}.ckp.gz
            rm tree${j//.nwk}.treefile
            rm tree${j//.nwk}.log
        done
    fi
done
cd $p2/${t}_iq2
for i in $(ls *.treefile)
do
    $p/Software/iqtree -m GTR+G -s ${i//.treefile} -te $i -pre ${i//.fas.aln.treefile}
    rm ${i//.fas.aln.treefile}.ckp.gz
    rm ${i//.fas.aln.treefile}.treefile
    rm ${i//.fas.aln.treefile}.log
done
done