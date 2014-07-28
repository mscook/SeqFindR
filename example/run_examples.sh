SeqFindr Antibiotic_markers.fa assemblies/ -o run1 -l 
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run2 -l
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run3 -l -r
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run4 -l -r --index_file dummy.order
SeqFindr Antibiotic_markers.fa assemblies/ -o run5 -l --careful 0.1
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run6 -l -r --index_file dummy.order --invert
