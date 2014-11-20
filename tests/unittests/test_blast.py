from context import blast
from context import pytest
import os
import glob


def test_make_BLAST_database(tmpdir):
    """
    Test the make_BLAST_database() function

    Function signature::

    make_BLAST_database(fasta_file)
    """
    fasta = os.path.abspath("../../example/Antibiotic_markers.fa")
    tmpdir = str(tmpdir)
    os.chdir(str(tmpdir))
    os.mkdir("DBs")
    blast.make_BLAST_database(fasta)
    infs = glob.glob(os.path.join(tmpdir, "DBs")+"/*")
    tidied = []
    for f in infs:
        tidied.append(f.split('/')[-1])
    assert len(infs) == 4
    assert "Antibiotic_markers.fa.nhr" in tidied
    assert "Antibiotic_markers.fa.nin" in tidied
    assert "Antibiotic_markers.fa.nsq" in tidied
    assert "Antibiotic_markers.fa" in tidied


def test_run_BLAST():
    """
    Test the run_BLAST() function

    Function signature::

        run_BLAST(query, database, args)
    """
    pass


def test_parse_BLAST():
    """
    Test the parse_BLAST() function

    Function signature::

        parse_BLAST(blast_results, tol, careful)
    """
    pass
