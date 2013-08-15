SeqFindR changelog
==================

2013-07-16 Nabil-Fareed Alikhan <n.alikhan@uq.edu.au>
    * Added Ability to use amino acid sequences as Virluence factors
    * Added helper method to automatically detect type of sequence file 
       (nucl or pro)
    * Added commandline override option for above auto-detection ( -R )
    * Replaced a number of system calls and pathnames with cross platform 
    friendly alternatives
    * Added support for fasta file extensions .fna, .fas, .fa; rather than just 
    .fas (For query sequences)
    * Added tBLASTx functionality and option to trigger it ( -X ) 
