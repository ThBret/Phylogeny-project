k=Fungi
p=/home/thibault
p2=$p/M2/$k
for c in Agaricomycetes Agaricostilbomycetes Arthoniomycetes AscomycotaCIS BasidiomycotaIS Chytridiomycetes Cystobasidiomycetes Dacrymycetes Dothideomycetes Eurotiomycetes Exobasidiomycetes Glomeromycetes Lecanoromycetes Leotiomycetes Microbotryomycetes Pezizomycetes Phycomycota Pneumocystidomycetes Pucciniomycetes Saccharomycetes Sordariomycetes Taphrinomycetes Tremellomycetes Ustilaginomycetes Wallemiomycetes Zygomycetes ZygomycotaIS
do
cd $p2
for g in $(ls ${c}_failed_trees2)
do
cd $p2/${c}_failed_trees2
$p/Software/raxmlHPC-PTHREADS-AVX2 -m GTRGAMMA -J MRE -z $g -n con
rm RAxML_info.con
sed "s/1\.0//g" RAxML_MajorityRuleExtendedConsensusTree.con | sed "s/\[//g" | sed "s/\]//g" > con.ed
$p/Software/nt-ng/newick-tools --rapid 99 --tree con.ed > ${g//.failed_LRT}.clusters
rm RAxML_MajorityRuleExtendedConsensusTree.con
rm con.ed
done
done

#for c in Actinopterygii Amphibia Anthozoa Appendicularia Arachnida Archiacanthocephala Ascidiacea Asteroidea Aves Bdelloidea Bivalvia Branchiopoda Caudofoveata Cephalaspidomorphi Cephalopoda Cestoda Chilopoda Chromadorea Clitellata Collembola Crinoidea Cubozoa Demospongiae Diplopoda Diplura Echinoidea Elasmobranchii Enoplea Eoacanthocephala Eutardigrada Gastropoda GastrotrichaCIS GnathostomulidaCIS Gordiida Gymnolaemata Heterotardigrada Hexactinellida Hexanauplia Holocephali Holothuroidea Homoscleromorpha Hoplonemertea Hydrozoa Ichthyostraca Insecta KinorhynchaCIS Leptocardii Lingulata Malacostraca Mammalia Monogenea Monogononta Myxini Myxozoa Myzostomida Nuda Onychophorida Ophiuroidea Ostracoda Palaeacanthocephala Palaeonemertea Pauropoda Phascolosomatidea PhoronidaCIS Phylactolaemata Pilidiophora Polychaeta Polyplacophora Protura Pycnogonida Remipedia Reptilia Rhabditophora RhombozoaIS Rhynchonellata Sagittoidea Sarcopterygii Scaphopoda Scyphozoa Sipunculidea Staurozoa Tentaculata Thecostraca Trematoda Turbellaria XenacoelomorphaCIS
#for c in Andreaeopsida Bangiophyceae Bryopsida Chlorodendrophyceae Chlorophyceae Compsopogonophyceae Cyanidiophyceae Florideophyceae Liliopsida Magnoliopsida Nephroselmidophyceae Pinopsida Polypodiopsida Polytrichopsida Psilotopsida Pteridopsida Pyramimonadophyceae Rhodellophyceae Sphagnopsida Trebouxiophyceae Ulvophyceae
#for c in Agaricomycetes Agaricostilbomycetes Arthoniomycetes AscomycotaCIS BasidiomycotaIS Chytridiomycetes Cystobasidiomycetes Dacrymycetes Dothideomycetes Eurotiomycetes Exobasidiomycetes Glomeromycetes Lecanoromycetes Leotiomycetes Microbotryomycetes Pezizomycetes Phycomycota Pneumocystidomycetes Pucciniomycetes Saccharomycetes Sordariomycetes Taphrinomycetes Tremellomycetes Ustilaginomycetes Wallemiomycetes Zygomycetes ZygomycotaIS