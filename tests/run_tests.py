#!/usr/bin/env python

import sys, os, doctest 

sys.path.insert(0, "../")

doctest.testfile("blast.tests")
doctest.testfile("imaging.tests")
doctest.testfile("SeqFindR.tests")
doctest.testfile("vfdb_to_seqfindr.tests")
doctest.testfile("config.tests")
doctest.testfile("util.tests")
