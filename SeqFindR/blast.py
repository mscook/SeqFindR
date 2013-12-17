# Copyright 2013 Mitchell Stanton-Cook Licensed under the
#     Educational Community License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may
#     obtain a copy of the License at
#
#      http://www.osedu.org/licenses/ECL-2.0
#
#     Unless required by applicable law or agreed to in writing,
#     software distributed under the License is distributed on an "AS IS"
#     BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#     or implied. See the License for the specific language governing
#     permissions and limitations under the License.

"""
SeqFindR BLAST methods
"""

import subprocess
import shutil
import os
import sys

from Bio.Blast              import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbitblastnCommandline
from Bio.Blast.Applications import NcbitblastxCommandline

import SeqFindR.util

def make_BLAST_database(fasta_file):
    """
    Given a fasta_file, generate a nucleotide BLAST database

    Database will end up in DB/ of working directory or OUTPUT/DB if an
    output directory is given in the arguments

    :param fasta_file: full path to a fasta file
    :type fasta_file: string

    :rtype: the strain id **(must be delimited by '_')**
    """
    proc = subprocess.Popen([ "makeblastdb", "-in" , fasta_file, "-dbtype",
                                'nucl' ], stdout=subprocess.PIPE)
    sys.stderr.write(proc.stdout.read())
    for file_ext in ['.nhr', '.nin', '.nsq']:
        path = fasta_file + file_ext
        shutil.move(path, os.path.join('DBs', os.path.basename(path)))
    sys.stderr.write(("Getting %s and assocaiated database files to the DBs "
                        "location\n") % (fasta_file))
    shutil.copy2(fasta_file, os.path.join('DBs', os.path.basename(fasta_file)))
    return os.path.basename(fasta_file).split('_')[0]


def run_BLAST(query, database, args):
    """
    Given a mfa of query sequences of interest & a database, search for them.

    Important to note:
        * Turns dust filter off,
        * Only a single target sequence (top hit),
        * Output in XML format as blast.xml.

    # TODO: Add  evalue filtering ?
    # TODO: add task='blastn' to use blastn scoring ?

    .. warning:: default is megablast

    .. warning:: tblastx funcationality has not been checked

    :param query: the fullpath to the vf.mfa
    :param database: the full path of the databse to search for the vf in
    :param args: the arguments parsed to argparse

    :type query: string
    :type database: string
    :type args: argparse args (dictionary)

    :returns: the path of the blast.xml file
    """
    protein = False
    # File type not specified, determine using util.is_protein()
    if args.reftype == None:
        if SeqFindR.util.is_protein(query) != -1:
            protein = True
            sys.stderr.write('%s is protein' % (query))
    elif args.reftype == 'prot':
        protein = True
        sys.stderr.write('%s is protein\n' % (query))
    run_command = ''
    if protein:
        sys.stderr.write('Using tblastn\n')
        run_command = NcbitblastnCommandline(query=query, seg='no',
                    db=database, outfmt=5, num_threads=args.BLAST_THREADS,
                    max_target_seqs=1, out='blast.xml')
    else:
        if args.tblastx:
            sys.stderr.write('Using tblastx\n')
            run_command = NcbitblastxCommandline(query=query, seg='no',
                        db=database, outfmt=5, num_threads=args.BLAST_THREADS,
                        max_target_seqs=1, out='blast.xml')
        else:
            sys.stderr.write('Using blastn\n')
            if args.short == False:
                run_command = NcbiblastnCommandline(query=query, dust='no',
                            db=database, outfmt=5, 
                            num_threads=args.BLAST_THREADS,
                            max_target_seqs=1, out='blast.xml')
            else:
                sys.stderr.write('Optimising for short query sequences\n')
                run_command = NcbiblastnCommandline(query=query, dust='no',
                            db=database, outfmt=5, word_size=7,
                            num_threads=args.BLAST_THREADS, evalue=1000,
                            max_target_seqs=1, out='blast.xml')

    sys.stderr.write(str(run_command)+"\n")
    run_command()
    return os.path.join(os.getcwd(), 'blast.xml')


def parse_BLAST(blast_results, tol):
    """
    Using NCBIXML parse the BLAST results, storing & returning good hits

    Here good hits are:
        * hsp.identities/float(record.query_length) >= tol

    :param blast_results: full path to a blast run output file (in XML format)
    :param tol: the cutoff threshold (see above for explaination)

    :type blast_results: string
    :type tol: float

    :rtype: list of satifying hit names
    """
    if os.path.isfile(os.path.expanduser(blast_results)):
        hits = []
        for record in NCBIXML.parse(open(blast_results)):
            for align in record.alignments:
                for hsp in align.hsps:
                    hit_name = record.query.split(',')[1].strip()
                    if hsp.identities/float(record.query_length) >= tol:
                        hits.append(hit_name.strip())
    else:
        sys.stderr.write("BLAST results do not exist. Exiting.\n")
        sys.exit(1)
    return hits
