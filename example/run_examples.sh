SeqFindr Antibiotic_markers.fa assemblies/ -o run1 -l 
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run2 -l
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run3 -l -r
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run4 -l -r --index_file dummy.order
SeqFindr Antibiotic_markers.fa assemblies/ -o run5 -l --careful 0.1
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run6 -l -r --index_file dummy.order --invert
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run7 -l --index_file dummy.order --invert
SeqFindr Antibiotic_markers.fa assemblies/ -o run8 -l --index_file dummy.order --invert
# New option --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -o run9 -l --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run10 -l --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run11 -l -r --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run12 -l -r --index_file dummy.order --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -o run13 -l --careful 0.1 --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run14 -l -r --index_file dummy.order --invert --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -m consensus/ -o run15 -l --index_file dummy.order --invert --remove_empty_cols
SeqFindr Antibiotic_markers.fa assemblies/ -o run16 -l --index_file dummy.order --invert --remove_empty_cols
