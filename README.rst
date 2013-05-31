SeqFindR
========

SeqFindR - easily create informative genomic feature plots

**This is an early release version of SeqFindR.** The tool is still undergoing 
rapid development. We have only tested SeqFindR on linux systems.


Requirements
------------

ncbiblast >= 2.2.27
python >= 2.7 (not Python 3 supported)
numpy >= 1.6.1
scipy >= 0.10.1
matplotlib >= 1.1.0


Installation
------------

You'll need to have git installed. As a scientist git can be really useful. See
`here`_ for some discussion.


Option 1 (with root/admin)::

    cd ~/
    git clone git@github.com:mscook/SeqFindR.git
    cd SeqFindR
    sudo python setup.py install

Option 2 (standard user)::

    TODO


.. notes:: Please regularly check back or git pull/python setup.py to make sure
           you're running the most recent SeqFindR version.


Example figure produced by SeqFindR
-----------------------------------

.. image:: https://raw.github.com/mscook/SeqFindR/master/example/CU_fimbriae.png
    :alt: SeqFindR CU fimbriae genes image
    :align: center




SeqFindR usage
--------------

Help listing::

    Usage: SeqFindR.py [-h] [-v] [-o OUTPUT] [-d VFDB] [-a ASS] [-t TOL] [-m CONS]
                       [-i INDEX] [-l] [-c COLOR] [-r]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         verbose output
      -o OUTPUT, --output OUTPUT
                            output prefix (default = "")
      -d VFDB, --vfdb VFDB  full path to database fasta file
      -a ASS, --ass ASS     full path to dir containing assemblies
      -t TOL, --tol TOL     cutoff (default = 0.95)
      -m CONS, --cons CONS  full path to dir containing consensuses (default =
                            None)
      -i INDEX, --index INDEX
                            maintain order of index (no cluster) (default = None)
      -l, --label_genes     label the x axis (default = False)
      -c COLOR, --color COLOR
                            color index (default = None)
      -r, --reshape         Differentiate between mapping and assemblies

    Licence: ECL by Mitchell Stanton-Cook <m.stantoncook@gmail.com>



.. _here: http://blogs.biomedcentral.com/bmcblog/2013/02/28/version-control-for-scientific-research/

