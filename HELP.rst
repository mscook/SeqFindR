SeqFindR -h
===========

Something like this::

    usage: SeqFindR [-h] [-R {nucl,prot}] [-X] [-v] [-o OUTPUT] [-p OUTPUT_PREFIX]
                    [-t TOL] [-m CONS] [-l] [-r] [-g] [--index_file INDEX_FILE]
                    [--color COLOR] [--DPI DPI] [--seed SEED] [--size SIZE]
                    [-s STRIP] [--EXISTING_MATRIX] [--BLAST_THREADS BLAST_THREADS]
                    seqs_of_interest assembly_dir

    SeqFindR v0.1 - A tool to easily create informative genomic feature plots
    (http://github.com/mscook/SeqFindR)

    positional arguments:
      seqs_of_interest      Full path to FASTA file containing a set of sequences
                            of interest
      assembly_dir          Full path to directory containing aset of assemblies
                            in FASTA format

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         verbose output

    Optional algorithm options:
      Options relating to the SeqFindR algorithm

      -t TOL, --tol TOL     Similarity cutoff [default = 0.95]
      -m CONS, --cons CONS  Full path to directory containing mapping consensuses
                            [default = None]. See manual for more info
      -r, --reshape         Differentiate between mapping and assembly hits in the
                            figure [default = no differentiation]
      --index_file INDEX_FILE
                            Maintain the y axis strain order according to order
                            given in this file. Otherwise clustering by row
                            similarity. [default = do clustering]. See manual for
                            more info
      -s STRIP, --strip STRIP
                            Strip the 1st and last N bases of mapping consensuses
                            & database [default = 10]

    Optional input/output options:
      Options relating to input and output

      -o OUTPUT, --output OUTPUT
                            Output the results to this location
      -p OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX
                            Give all result files this prefix
      --EXISTING_MATRIX     Use existing SeqFindR matrix (reformat the plot)
                            [default = False]

    Figure options:
      Options relating to the output figure

      -l, --label_genes     Label the x axis with the query identifier [default =
                            False]
      -g, --grid            Figure has grid lines [default = True]
      --color COLOR         The color index [default = None]. See manual for more
                            info
      --DPI DPI             DPI of figure [default = 300]
      --seed SEED           Color generation seed
      --size SIZE           Size of figure [default = 10x12 (inches)]

    BLAST options:
      Options relating to BLAST

      -R {nucl,prot}, --reftype {nucl,prot}
                            Reference Sequence type. If not given will try to
                            detect it
      -X, --tblastx         Run tBLASTx rather than BLASTn
      --BLAST_THREADS BLAST_THREADS
                            Use this number of threads in BLAST run [default = 1]

    Licence: ECL 2.0 by Mitchell Stanton-Cook <m.stantoncook@gmail.com>
