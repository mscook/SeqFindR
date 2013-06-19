SeqFindR
========

.. image:: https://travis-ci.org/mscook/SeqFindR.png?branch=master
        :target: https://travis-ci.org/mscook/SeqFindR

SeqFindR - easily create informative genomic feature plots.

**Please see the offical** `site`_ **.**

**This is an early release version of SeqFindR.** The tool is still undergoing 
rapid development. We have only tested SeqFindR on linux systems. 


Requirements
------------

You'll need to install/have installed:
    * ncbiblast >= 2.2.27
    * python >= 2.7 (Python 3 is not supported)

You can check these are installed by::
    
    $ python --version
    $ which blastn

The following python libraries will be installed automatically if you follow 
the installation instructions detailed below.

We also use the following python libraries:
    * numpy >= 1.6.1
    * scipy >= 0.10.1
    * matplotlib >= 1.1.0
    * biopython >= 1.59


Installation
------------

If you're a member of the Beatson Group you'll already have the SeqFindR script 
in your barrine $PATH. You do not need to install SeqFindR. UQ based 
researchers should email me (m.stantoncook@gmail.com) for the location 
of SeqFindR.

Option 1a (with root/admin)::
    
    $ pip install SeqFindR

Option 1b (as a standard user)::

    $ pip install SeqFindR --user


You'll need to have git installed for the following alternative install 
options. git can be really useful for scientists. See `here`_ for some 
discussion.

Option 2a (with root/admin & git)::

    $ cd ~/
    $ git clone git://github.com/mscook/SeqFindR.git
    $ cd SeqFindR
    $ sudo python setup.py install

Option 2b (standard user & git) **replacing INSTALL/HERE with appropriate**::

    $ cd ~/
    $ git clone git://github.com/mscook/SeqFindR.git
    $ cd SeqFindR
    $ echo 'export PYTHONPATH=$PYTHONPATH:~/INSTALL/HERE/lib/python2.7/site-packages' >> ~/.bashrc
    $ echo 'export PATH=$PATH:~/INSTALL/HERE/bin' >> ~/.bashrc
    $ source ~/.bashrc
    $ python setup.py install --prefix=~/INSTALL/HERE/SeqFindR/  
    

If the install went correctly::

   $ which SeqFindR
   /INSTALLED/HERE/bin/SeqFindR
   $ SeqFindR -h


**Please regularly check back to make sure you're running the most recent 
SeqFindR version.** You can upgrade like this:

If installed using option 1x::

    $ pip install --upgrade SeqFindR
    $ # or
    $ pip install --upgrade SeqFindR --user

If installed using option 2x::

    $ cd ~/SeqFindR
    $ git pull
    $ sudo python setup.py install
    $ or
    $ cd ~/SeqFindR
    $ git pull
    $ echo 'export PYTHONPATH=$PYTHONPATH:~/INSTALL/HERE/lib/python2.7/site-packages' >> ~/.bashrc
    $ echo 'export PATH=$PATH:~/INSTALL/HERE/bin' >> ~/.bashrc
    $ source ~/.bashrc
    $ python setup.py install --prefix=~/INSTALL/HERE/SeqFindR/  


Example figure produced by SeqFindR
-----------------------------------

SeqFindR CU fimbriae genes image. 110 E. *coli* strains were investigated. 
Order is according to phylogenetic analysis. Black blocks represent gene 
presence.

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/CU_fimbriae.png
    :alt: SeqFindR CU fimbriae genes image
    :align: center


SeqFindR database files
-----------------------

The SeqFindR database is in multi-fasta format. The header needs to be
formatted with *4 comma separated* elements.

The elements are:
    * identifier,
    * common name,
    * description and 
    * species

The final element, separated by **[]** contains a classification.

An example::

    >70-tem8674, bla-TEM, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    AAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATAC
    >70-shv86, bla-SHV, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    CTCAAGCGGCTGCGGGCTGGCGTGTACCGCCAGCGGCAGGGTGGCTAACAGGGAGATAATACACAGGCGA
    >70-oxa(1)256, bla-OXA-1, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    >70-tetB190, tet(B), Tetracycline Antibiotic resistance (tetracycline), Unknown sp. [Tetracycline]
    CAAAGTGGTTAGCGATATCTTCCGAAGCAATAAATTCACGTAATAACGTTGGCAAGACTGGCATGATAAG


How does SeqFindR determine positive hits
-----------------------------------------

We use the following calculation::

    hsp.identities/float(record.query_length) >= tol

Where:
    * hsp.identities is number of identities in the high-scoring pairs between
      the query (databse entry) and subject (contig/scaffold/mapping
      consensus),
    * record.query_length is the length of the database entry and,
    * tol is the cutoff threshold to accept a hit (0.95 default)

**Why not just use max identity?**
    * Eliminate effects of scaffolding characters/gaps,
    * Handle poor coverage etc. in mapping consensuses where N characters/gaps
      may be introduced

**What problems may this approach cause?** I'm still looking into it...


Tutorial
--------

Navigate to the SeqFindR/example directory (from git clone). The following files should be present:
    * A database file called *Antibiotic_markers.fa* (-d option)
    * A ordering file called *dummy.order* (-i option)
    * An assemblies directory containing *strain1.fa, strain2.fa and strain3.fa*
      (-a option)
    * A consensus directory containing *strain1.fa, strain2.fa and strain3.fa*
      (-m option)

The toy assemblies and consesuses were generated such that:
    * **strain1** was missing: 70-shv86, 70-ctx143 and 70-aac3(IV)380 with 
      mis-assembly of 70-aphA(1)1310 & 70-tem8674
    * **strain2** was missing: 70-oxa(7)295, 70-pse(4)348 70-ctx143, 
      70-aadA1588, 70-aadB1778 and 70-aacC(2)200
    * **strain2** was missing 70-shv86, 70-ctx143 and 70-aac3(IV)380 with 
      mis-assembly of 70-aphA(1)1310, 70-tem8674 and 70-aadA1588


Run 1 - Looking at only assemblies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Command::

    SeqFindR -o run1 -d Antibiotic_markers.fa -a assemblies/ -l


.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run1_small.png
    :alt: run1
    :align: center


Link to full size `run1`_.


Run 2 - Combining assembly and mapping consensus data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR -o run2 -d Antibiotic_markers.fa -a assemblies/ -m consensus/ -l


.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run2_small.png
    :alt: run2
    :align: center


Link to full size `run2`_.


Run 3 - Combining assembly and mapping consensus data with differentiation between hits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR -o run3 -d Antibiotic_markers.fa -a assemblies/ -m consensus/ -l -r


.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run3_small.png
    :alt: run3
    :align: center


Link to full size `run3`_.


The clustering dendrogram looks like this:

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/dendrogram_run3_small.png
    :alt: run3 dendrogram
    :align: center


Link to full size `dendrogram`_.


Run 4 - Combining assembly and mapping consensus data with defined ordering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR -o run4 -d Antibiotic_markers.fa -a assemblies/ -m consensus/ -l -i dummy.order -r


.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run4_small.png
    :alt: run4
    :align: center


Link to full size `run4`_.


How to generate mapping consensus data
--------------------------------------

We use `Nesoni`_. We use the database file (in multi-fasta format) as the 
reference. The workflow is something like this::

    $ nesoni make-reference myref ref-sequences.fa
    $ # for each strain
    $ nesoni analyse-sample: mysample myref pairs: reads1.fastq reads2.fastq

For each sample we then extract the consensus.fa file which we term the 
mapping consensus. This file is a multi-fasta file of the consensus base calls
relative to the database sequences.

Caveats: 
    * you will probably want to allow multi-mapping reads (giving *--monogamous
      no --random yes* to nesoni consensus), 
    * The (poor) alignment of reads at the start and the end of the database 
      genes can result in N calls. This can result in downstream false 
      negatives. We are currently working on this.


SeqFindR usage options
----------------------

Help listing::

    Usage: SeqFindR.py -o OUTPUT -d DB -a ASS [-h] [-v] [-t TOL] [-m CONS]
                       [-i INDEX] [-l] [-c COLOR] [-r]

    optional arguments:
      -h, --help                 show this help message and exit
      -v, --verbose              verbose output
      -o OUTPUT, --output OUTPUT [Required] output prefix
      -d DB, --db DB             [Required] full path database fasta file
      -a ASS, --ass ASS          [Required] full path to dir containing assemblies
      -t TOL, --tol TOL          Similarity cutoff (default = 0.95)
      -m CONS, --cons CONS       full path to dir containing consensuses (default = None)
      -i INDEX, --index INDEX    maintain order of index (no cluster) (default = None)
      -l, --label_genes          label the x axis (default = False)
      -c COLOR, --color COLOR    color index (default = None)
      -r, --reshape              Differentiate between mapping and assembly hits

    Licence: ECL by Mitchell Stanton-Cook <m.stantoncook@gmail.com>


Future
------

Current plans:
    * Make into a Web Application
    * Trim off first N characters when using mapping consensuses
    * More dynamic sizing labelling



.. _here: http://blogs.biomedcentral.com/bmcblog/2013/02/28/version-control-for-scientific-research/
.. _run1: https://raw.github.com/mscook/SeqFindR/master/example/run1.png
.. _run2: https://raw.github.com/mscook/SeqFindR/master/example/run2.png
.. _run3: https://raw.github.com/mscook/SeqFindR/master/example/run3.png
.. _dendrogram: https://raw.github.com/mscook/SeqFindR/master/example/dendrogram_run3.png
.. _run4: https://raw.github.com/mscook/SeqFindR/master/example/run4.png
.. _site: http://mscook.github.io/SeqFindR/
.. _Nesoni: http://www.vicbioinformatics.com/software.nesoni.shtml
