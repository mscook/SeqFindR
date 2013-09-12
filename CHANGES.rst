SeqFindR changelog
==================

2013-08-16 Mitchell Stanton-Cook <m.stantoncook@gmail.com>:
    * General refactors & code cleaning/optimisations
    * Split into: blast.py, config.py, imaging.py, SeqFindR.py & util.py
    * fixed meta information
    * fixed argparse. Required options are now required not optional (database 
      & ass_dir)
    * output & output_prefix now do something...
    * New option -s/--strip (will strip off the 1st and last N bases from the 
      mapping consensuses and database to avoid uncalled bases at the start and
      end of runs
    * New option -e/--existing_run load in a BLAST XML results file. 
      Can thus reformat the plot without having to re-run BLAST.

2013-07-16 Nabil-Fareed Alikhan <n.alikhan@uq.edu.au>:
    * Added Ability to use amino acid sequences as Virluence factors
    * Added helper method to automatically detect type of sequence file 
       (nucl or pro)
    * Added commandline override option for above auto-detection ( -R )
    * Replaced a number of system calls and pathnames with cross platform 
    friendly alternatives
    * Added support for fasta file extensions .fna, .fas, .fa; rather than just 
    .fas (For query sequences)
    * Added tBLASTx functionality and option to trigger it ( -X ) 
