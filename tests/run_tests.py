#!/usr/bin/env python

import sys 
sys.path.append('../')
import doctest

doctest.testfile("blast.tests")
doctest.testfile("imaging.tests")
doctest.testfile("SeqFindR.tests")
doctest.testfile("vfdb_to_seqfindr.tests")
doctest.testfile("config.tests")
doctest.testfile("util.tests")
