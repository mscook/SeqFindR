# Copyright 2013-2014 Mitchell Stanton-Cook Licensed under the
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
SeqFindr utility methods
"""

import os
import sys
import re
from Bio import SeqIO


def ensure_paths_for_args(args):
    """
    Ensure all arguments with paths are absolute & have simplification removed

    Just apply os.path.abspath & os.path.expanduser

    :param args: the arguments given from argparse

    :returns: an updated args
    """
    args.seqs_of_interest = os.path.abspath(
        os.path.expanduser(args.seqs_of_interest))
    args.assembly_dir = os.path.abspath(os.path.expanduser(args.assembly_dir))
    if args.output is not None:
        args.output = os.path.abspath(os.path.expanduser(args.output))
    if args.cons is not None:
        args.cons = os.path.abspath(os.path.expanduser(args.cons))
    if args.index_file is not None:
        args.index_file = os.path.abspath(os.path.expanduser(args.index_file))
    return args


def init_output_dirs(output_dir):
    """
    Create the output base (if needed) and change dir to it

    :param args: the arguments given from argparse
    """
    current_dir = os.getcwd()
    if output_dir is not None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            sys.stderr.write("Output directory exists\n")
        os.chdir(output_dir)
    try:
        os.mkdir("DBs")
    except OSError:
        sys.stderr.write("A DBs directory exists. Overwriting\n")
    return current_dir


def get_fasta_files(data_path):
    """
    Returns all files ending with .fas/.fa/fna in a directory

    :param data_path: the full path to the directory of interest

    :returns: a list of fasta files (valid extensions: .fas, .fna, .fa
    """
    in_files = []
    for files in os.listdir(data_path):
            if files.endswith(".fas") or files.endswith(".fna") \
                    or files.endswith(".fa") or files.endswith(".fasta"):
                in_files.append(os.path.join(data_path, files))
    return in_files


def order_inputs(order_index_file, dir_listing):
    """
    Given an order index file, maintain this order in the matrix plot

    **This implies no clustering.** Typically used when you already have
    a phlogenetic tree.

    :param order_index_file: full path to a ordered file (1 entry per line)
    :param dir_listing: a listing from util.get_fasta_files

    :type order_index_file: string
    :type dir_listing: list

    :rtype: list of updated glob.glob dir listing to match order specified
    """
    with open(order_index_file) as fin:
        lines = fin.readlines()
    if len(lines) != len(dir_listing):
        print len(lines), len(dir_listing)
        sys.stderr.write("In order_inputs(). Length mismatch\n")
        sys.exit(1)
    ordered = []
    for l in lines:
        cord = l.strip()
        for d in dir_listing:
            tmp = os.path.basename(d.strip())
            if tmp.find('_') == -1:
                cur = tmp.split('.')[0]
            else:
                cur = tmp.split("_")[0]
            if cur == cord:
                ordered.append(d)
                break
    if len(ordered) != len(dir_listing):
        print len(ordered)
        print len(dir_listing)
        sys.stderr.write("In order_inputs(). Not 1-1 matching. Typo?\n")
        sys.stderr.write("In ordered: "+str(ordered)+"\n")
        sys.stderr.write("In dir listing:" + str(dir_listing)+"\n")
        sys.exit(1)
    return ordered


def is_protein(fasta_file):
    """
    Checks if a FASTA file is protein or nucleotide.

    -1 if no protein detected

    TODO: Abiguity characters?
    TODO: exception if mix of protein/nucleotide?

    :param fasta_file: path to input FASTA file

    :type fasta_file: string

    :rtype: number of protein sequences in fasta_file (int)
    """
    protein_hits = -1
    with open(fasta_file, 'rU') as fin:
        for record in SeqIO.parse(fin, 'fasta'):
            if re.match('[^ATCGNatcgn]+', str(record.seq)) is not None:
                protein_hits += 1
    return protein_hits


def check_database(database_file):
    """
    Check the database conforms to the SeqFindr format

    .. note:: this is not particulalry extensive

    :args database_file: full path to a database file as a string

    :type database_file: string
    """
    at_least_one = 0
    stored_categories = []
    with open(database_file) as db_in:
        for line in db_in:
            if line.startswith('>'):
                at_least_one += 1
                # Do the check
                if len(line.split(',')) != 4 or line.split(',')[-1].count(']') != 1 or line.split(',')[-1].count('[') != 1:
                    raise Exception("Database is not formatted correctly")
                else:
                    tmp = line.split(',')[-1]
                    cur = tmp.split('[')[-1].split(']')[0].strip()
                    stored_categories.append(cur)
    if at_least_one == 0:
        raise Exception("Database contains no fasta headers")
    # Check that the categories maintain the correct order.
    cat_counts = len(set(stored_categories))
    prev = stored_categories[0]
    # There will always be 1
    detected_cats = 1
    for i in range(1, len(stored_categories)):
        if stored_categories[i] != prev:
            detected_cats +=1
        prev = stored_categories[i]
    if cat_counts != detected_cats:
        print ("Please ensure that your classifications ([ element ]) are "
               "grouped")
        sys.exit(1)
    print "SeqFindr database checks [PASSED]"

