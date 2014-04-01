SeqFindR
========

.. image:: https://travis-ci.org/mscook/SeqFindR.png?branch=master
        :target: https://travis-ci.org/mscook/SeqFindR

|

.. image:: https://landscape.io/github/mscook/SeqFindR/master/landscape.png
   :target: https://landscape.io/github/mscook/SeqFindR/master
   :alt: Code Health


SeqFindR - easily create informative genomic feature plots.

Work in progress:
    * `SeqFindR documentation`_
    * `SeqFindR official site`_

**SeqFindR is nearing a stable API.** 

**We have only tested SeqFindR on linux systems.** There has been some 
success with `MacOSX`_. 

Best use "git log" for a changelog as the `changelog`_ for most recent 
changes/fixes/enhancements may not be up to date.


Cite this Github repository if you use SeqFindR to generate figures 
for publications:: 

    STANTON-COOK M, NF ALIKHAN, FORDE BM, BEN ZAKOUR NL & BEATSON SA^. 
    SeqFindR - easily create informative genomic feature plots.
    https://github.com/mscook/SeqFindR.


Quick install (Ubuntu)
----------------------

Simple install for Ubuntu/Debian systems::

    $ sudo apt-get install python-numpy python-scipy python-matplotlib python-biopython ncbi-blast+ python-dev python-pip libatlas-dev liblapack-dev gfortran libfreetype6-dev libfreetype6 libpng-dev git && cd ~/ && git clone https://github.com/mscook/SeqFindR.git && pip install -e SeqFindR/


Requirements
------------

You'll need to install/have installed:
    * ncbiblast >= 2.2.27
    * python >= 2.7 (**Python 3 is not supported**)
    * `pip`_
    * git (depending on your install route) 

You can check these are installed by::
    
    $ python --version
    $ which blastn
    $ which pip
    $ which git


The following python libraries should be installed automatically if you follow 
the installation instructions detailed below.

We use the following python `libraries`_:
    * numpy >= 1.6.1
    * scipy >= 0.10.1
    * matplotlib >= 1.1.0
    * biopython >= 1.59
    * ghalton>=0.6

These libraries will also have dependencies (i.e. atlas, lapack, fortran 
compilers, freetype and png).

The state of Python packaging (distribution of code) is that bad, you could 
miss many nights sleep. I'm looking at you SciPy. **For the smoothest possible 
install we recommend installing the requirements using your distributions 
package manager.** That is via apt-get, yum or similar.

For Ubuntu (fresh server install) you can get requirements using::

    $ sudo apt-get install python-numpy python-scipy python-matplotlib
    python-biopython ncbi-blast+ python-dev python-pip libatlas-dev
    liblapack-dev gfortran libfreetype6-dev libfreetype6 libpng-dev git


Installation (possibly painful)
-------------------------------

If you are a member of the Beatson Group you'll already have SeqFindR in your 
$PATH on barrine. You do not need to install SeqFindR. UQ based researchers 
should email me (m.stantoncook@gmail.com) for the location of SeqFindR.

Option 1a (with root/admin)::
    
    $ pip install SeqFindR

Option 1b (as a standard user)::

    $ pip install SeqFindR --user

This assumes you have pip installed (see `pip`_). The SciPy, NumPy and 
matplotlib installations will break if you are missing libraries such as 
atlas, lapack, fortran compilers, freetype and png).


**You'll need to have git installed** for the following alternative install 
options. git can be really useful for scientists. See `here`_ for some 
discussion. Installing this way will provide you with the most recent version 
of SeqFindR.

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
    $
    $ # or
    $
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
formatted with *4 comma separated* elements. We concede that inventing 
another file format is annoying, but, future versions of SeqFindR will 
exploit this information.

The elements headers are:
    * identifier,
    * common name **(this is taken as the gene label in the plot)**,
    * description and 
    * species

The final element, separated by **[]** contains a classification. This
information is used by SeqFindR to draw different coloured blocks.

An example::

    >70-tem8674, bla-TEM, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    AAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATAC
    >70-shv86, bla-SHV, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    CTCAAGCGGCTGCGGGCTGGCGTGTACCGCCAGCGGCAGGGTGGCTAACAGGGAGATAATACACAGGCGA
    >70-oxa(1)256, bla-OXA-1, Beta-lactams Antibiotic resistance (ampicillin), Unknown sp. [Beta-lactams]
    >70-tetB190, tet(B), Tetracycline Antibiotic resistance (tetracycline), Unknown sp. [Tetracycline]
    CAAAGTGGTTAGCGATATCTTCCGAAGCAATAAATTCACGTAATAACGTTGGCAAGACTGGCATGATAAG

**Note:** if you do not have all information you can simplify the expected 
database header to::

     >, bla-TEM, , [classification]
    

The script **vfdb_to_seqfindr** is now included in SeqFindR to convert VFDB 
formatted files (or like) to SeqFindR formatted database files.

VFDB: Virulence Factors Database (www.mgc.ac.cn/VFs/) is a reference database 
for bacterial virulence factors.

At this stage we have tested this script on limited internal datasets.
Success/mileage will depend on the consistency of the VFDB formatting.


Example usage of **vfdb_to_seqfindr**::

    # Default (will set VFDB classification identifiers as the classification)
    $ vfdb_to_seqfindr -i TOTAL_Strep_VFs.fas -o TOTAL_Strep_VFs.sqf
    
    # Sets any classification to blank ([ ])
    $ vfdb_to_seqfindr -i TOTAL_Strep_VFs.fas -o TOTAL_Strep_VFs.sqf -b

    # Reads a user defined classification. 1 per in same order as input 
    # sequences
    $ python convert_vfdb_to_SeqFindR.py -i TOTAL_Strep_VFs.fas -o TOTAL_Strep_VFs.sqf -c user.class


The -c (--class_file) option is very useful. Suppose you want to annotate your 
sequences of interest with user defined classification values. Simply develop a 
file containing the scheme as pass using the -c option (3rd example above). 
A sample file for the situation where you had 7 input sequences with the first 
3 Fe transporters, the next two  Toxins, the next a Misc and the final 
sequence is a Toxin would look like this::

    Fe transporter
    Fe transporter
    Fe transporter
    Toxin
    Toxin
    Misc
    Toxin


How does SeqFindR determine positive hits
-----------------------------------------

We use the following calculation::

    hsp.identities/float(record.query_length) >= tol

Where:
    * hsp.identities is number of identities in the high-scoring pairs between
      the query (database entry) and subject (contig/scaffold/mapping
      consensus),
    * record.query_length is the length of the database entry and,
    * tol is the cutoff threshold to accept a hit (0.95 default)

For a database entry of 200 bp you can have up to 10 mismatches/gaps without 
being penalised.

**Why not just use max identity?**
    * Eliminate effects of scaffolding characters/gaps,
    * Handle poor coverage etc. in mapping consensuses where N characters/gaps
      may be introduced

**What problems may this approach cause?** I'm still looking into it...


Fine grain configuration
------------------------

SeqFindR can read a configuration file. At the moment you can only redefine 
the category colors (suppose you want to use a set of fixed colors instead of 
the default randomly generated). The configuration file is expected to expand 
in the future.

To define category colors::

    touch ~/.SeqFindR.cfg
    vi ~/.SeqFindR.cfg
    # Add something like
    category_colors = [(100,60,201), (255,0,99)]

Category colors can be any RGB triplet. You could use a tool similar to this
one: http://www.colorschemer.com/online.html

For example the first row of colors in RGB is: 
(51,102,255), (102,51,255), (204,51,255), (255,51,204)


Short PCR primers
-----------------

In some cases you may want to screen using PCR primers. Please use the --short 
option. Here we adjust BLASTn parameters wordsize = 7 & Expect Value = 1000


Tutorial
--------

We provide a `script`_ to run all the examples. **Note:** We have changed the 
color generation code. As a consequence the background colors will be 
different when running this yourself. The results will not change.

Navigate to the SeqFindR/example directory (from git clone). The following files should be present:
    * A database file called *Antibiotic_markers.fa* 
    * A ordering file called *dummy.order* (-i option)
    * An assemblies directory containing *strain1.fa, strain2.fa and strain3.fa*
    * A consensus directory containing *strain1.fa, strain2.fa and strain3.fa*
      (-m option)

The toy assemblies and consensuses were generated such that:
    * **strain1** was missing: 70-shv86, 70-ctx143 and 70-aac3(IV)380 with 
      mis-assembly of 70-aphA(1)1310 & 70-tem8674
    * **strain2** was missing: 70-oxa(7)295, 70-pse(4)348 70-ctx143, 
      70-aadA1588, 70-aadB1778 and 70-aacC(2)200
    * **strain2** was missing 70-shv86, 70-ctx143 and 70-aac3(IV)380 with 
      mis-assembly of 70-aphA(1)1310, 70-tem8674 and 70-aadA1588


Running all the examples at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Something like this::

    $ # Assuming you git cloned, python setup.py install
    $ cd SeqFindR/example
    $ ./run_examples.sh
    $ # See directories run1/ run2/ run3/ run4/


Run 1 - Looking at only assemblies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR Antibiotic_markers.fa assemblies/ -o run1 -l 

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run1_small.png
    :alt: run1
    :align: center


Link to full size `run1`_.


Run 2 - Combining assembly and mapping consensus data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR Antibiotic_markers.fa assemblies/ -m consensus/ -o run2 -l

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run2_small.png
    :alt: run2
    :align: center


Link to full size `run2`_.


Run 3 - Combining assembly and mapping consensus data with differentiation between hits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command::

    SeqFindR Antibiotic_markers.fa assemblies/ -m consensus/ -o run3 -l -r

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

    SeqFindR Antibiotic_markers.fa assemblies/ -m consensus/ -o run4 -l -r --index_file dummy.order

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/run4_small.png
    :alt: run4
    :align: center


Link to full size `run4`_.


How to generate mapping consensus data
--------------------------------------

**We strongly recommend that you use mapping consensus data.** It minimises 
the effects of missassembly and collapsed repeats.

We use `Nesoni`_. We use the database file (in multi-fasta format) as the 
reference for mapping. Nesoni has no issues with multifasta files as 
references (BWA will treat them as separate chromosomes). 
The workflow is something like this::

    $ nesoni make-reference myref ref-sequences.fa
    $ # for each strain
    $ #     nesoni analyse-sample: mysample myref pairs: reads1.fastq reads2.fastq
    $ #     extract the consensus.fa file


For those of you using a cluster running PBSPro see:
https://github.com/mscook/SeqFindR_nesoni
This is a script that generates a job array, submits and cleans up the
mapping results ready for input to SeqFindR.

The output from the described workflow and SeqFindR_nesoni is a consensus.fa 
file which we term the mapping consensus. This file is a multi-fasta file of 
the consensus base calls relative to the database sequences.

Caveats: 
    * you will probably want to allow multi-mapping reads (giving *--monogamous
      no --random yes* to nesoni consensus) (this is default for
      SeqFindR_nesoni), 
    * The (poor) alignment of reads at the start and the end of the database 
      genes can result in N base calls. This can result in downstream false 
      negatives.

**SeqFindR now provides a solution to minimise the effects of poor mapping at 
the start and end of the given sequences.** 

The SeqFindR option is -s or --STRIP::

    -s STRIP, --strip STRIP Strip the 1st and last N bases of mapping consensuses & database [default = 10]

By default this strips the 1st and last 10 bases from the mapping consensuses. 
We have had good results with this value. Feel free to experiment with 
different values (say, -s 0, -s 5, -s 10, -s 15). Please see `image-compare`_ 
a script we developed to compare the effects of different values of -s on the 
resultant figures. 


SeqFindR usage options
----------------------

See the help `listing`_. You can get this yourself with::

    $ SeqFindR -h


Future
------

Please see the `TODO`_ for future SeqFindR project directions.

.. _pip: http://www.pip-installer.org/en/latest/
.. _libraries: https://github.com/mscook/SeqFindR/blob/master/requirements.txt
.. _MacOSX: https://github.com/mscook/SeqFindR/issues/11
.. _script: https://github.com/mscook/SeqFindR/blob/master/example/run_examples.sh
.. _image-compare: https://github.com/mscook/image-compare
.. _listing: https://github.com/mscook/SeqFindR/blob/master/HELP.rst
.. _here: http://blogs.biomedcentral.com/bmcblog/2013/02/28/version-control-for-scientific-research/
.. _changelog: https://github.com/mscook/SeqFindR/blob/master/CHANGES.rst
.. _TODO:  https://github.com/mscook/SeqFindR/blob/master/TODO.rst
.. _run1: https://raw.github.com/mscook/SeqFindR/master/example/run1.png
.. _run2: https://raw.github.com/mscook/SeqFindR/master/example/run2.png
.. _run3: https://raw.github.com/mscook/SeqFindR/master/example/run3.png
.. _dendrogram: https://raw.github.com/mscook/SeqFindR/master/example/dendrogram_run3.png
.. _run4: https://raw.github.com/mscook/SeqFindR/master/example/run4.png
.. _site: http://mscook.github.io/SeqFindR/
.. _Nesoni: http://www.vicbioinformatics.com/software.nesoni.shtml
.. _SeqFindR documentation: http://seqfindr.rtfd.org
.. _SeqFindR official site: http://mscook.github.io/SeqFindR/

