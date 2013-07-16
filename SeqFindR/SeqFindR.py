#!/usr/bin/env python

"""
VirFindR. Presence/absence of virulence factors in draft genomes 

"""

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
#
### CHANGE LOG ###
# 2013-07-16 Nabil-Fareed Alikhan <n.alikhan@uq.edu.au>
#  * Added Ability to use amino acid sequences as Virluence factors
#  * Added helper method to automatically detect type of sequence file 
#       (nucl or pro)
#  * Added commandline override option for above auto-detection ( -R )
#  * Replaced a number of system calls and pathnames with cross platform 
#    friendly alternatives
#  * Added support for fasta file extensions .fna, .fas, .fa; rather than just 
#    .fas (For query sequences)



import sys, os, traceback, argparse
import time
import ast

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from   matplotlib.ticker import MultipleLocator, FormatStrFormatter

import numpy as np
from   scipy.cluster.hierarchy import linkage, dendrogram
from   scipy.spatial.distance  import pdist

from Bio.Blast import NCBIXML

# MODIFIED BY NABIL 2013.07.16
# If BioPython is already required, I'll just use the SeqRecord parser for 
# isPro method. And BLAST commandline wrapper too for run_BLAST. and std regex 
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbitblastnCommandline
import re, shutil, subprocess 

__author__ = "Mitchell Stanton-Cook & Nabil Alikhan"
__licence__ = "ECL"
__version__ = "2.0"
__email__ = "m.stantoncook@gmail.com"
epi = "Licence: "+ __licence__ +  " by " + __author__ + " <" + __email__ + ">"
USAGE = "VirFindR -h"

class SeqFindRConfig():
    """
A SeqFindR configuration class - subtle manipulation to plots
"""

    def __init__(self):
        self.config = self.read_config()

    def __getitem__(self, key):
        try:
            return self.config[key]
        except KeyError:
            print "Trying to get config option that does not exist."
            return None

    def __setitem__(self, key, item):
        self.config[key] = item

    def read_config(self):
        """
Read a SeqFindR configuration file

Currently only supports category colors in RGB format

category_colors = [(0,0,0),(255,255,255),....,(r,g,b)]
"""
        cfg = {}
        try:
            with open(os.path.expanduser('~/')+'.SeqFindR.cfg') as fin:
                print "Using a SeqFindR config file"
                colors = []
                for line in fin:
                    if line.startswith('category_colors'):
                        option, list = line.split('=')
                        list = list.strip().strip(' ')
                        list = ast.literal_eval(list)
                        for e in list:
                            fixed = (e[0]/255.0, e[1]/255.0, e[2]/255.0)
                            colors.append(fixed)
                        cfg[option] = colors
                        break
        except IOError:
            print "Using defaults"
        return cfg

    def dump_items(self):
        """
Prints all set configuration options to STDOUT
"""
        config = ''
        for key, value in self.config.items():
            print str(key)+" = "+str(value)+"\n"


def prepare_db(db_path):
    """
    Given a VF db, extract all possible hits and hit classes

    A Vf db is a mfa file in the format:

    >ident, gene id, annotation, organism [class]

    :param db_path: the fullpath to a VF db (mfa file)

    :type db_path: string

    :rtype: list of all vfs and corresponding classes
    """
    with open(db_path) as fin:
        lines = fin.readlines()
    vfs_list, vfs_class = [], []
    # Get the IDS and the classes
    for l in lines:
        if l.startswith('>'):
            vfs_list.append(l.split(',')[1].strip())
            vfs_class.append(l.split('[')[-1].split(']')[0].strip())
    # Check for duplicates
    unique = list(set(vfs_list))
    print "Investigating "+str(len(unique))+" features"
    for e in unique:
        if vfs_list.count(e) != 1:
            print "Duplicates found for: ",e
            print "Fix duplicates"
            sys.exit(1)
    return vfs_list, vfs_class


def order_inputs(order_index_file, dir_listing):
    """
    Given an order index file, maintain this order in the matrix plot

    THIS IMPLIES NO CLUSTERING!

    Typically used when you already have a phlogenetic tree

    :param order_index_file: full path to a ordered file (1 entry per line)
    :param dir_listing: a glob.glob dir listing as a list

    :type order_index_file: string
    :type dir_listing: list

    :rtype: list of updated glob.glob dir listing to match order specified
    """
    with open(order_index_file) as fin:
        lines = fin.readlines()
    if len(lines) != len(dir_listing):
        print "In order_inputs(). Length mismatch"
        sys.exit(1)
    ordered = []
    for l in lines:
        cord = l.strip()
        for d in dir_listing:
            tmp   = d.strip().split('/')[-1]
            if tmp.find('_') == -1:
                cur = tmp.split('.')[0]
            else:
                cur = tmp.split("_")[0]
            if cur == cord:
                ordered.append(d)
                break
    if len(ordered) != len(dir_listing):
        print "In order_inputs(). Not 1-1 matching. Typo?"
        print ordered
        print dir_listing
        sys.exit(1)
    return ordered


def make_BLASTDB(fasta_file):
    """
    Given a fasta_file, generate a nucleotide BLAST database

    Database will end up in DB/ of working directory

    :param fasta_file: full path to a fasta file
    
    :type fasta_file: string

    :rtype: the strain id (must be delimited by '_')
    """
    # MODIFIED BY NABIL 2013.07.168
    # Uses subprocess to launch makeblastdb, easier for error handling 
    proc = subprocess.Popen([ "makeblastdb", "-in" , fasta_file, "-dbtype", \
            'nucl' ], stdout=subprocess.PIPE)
    print(  proc.stdout.read())
    # Nabil: Using python shutil for cp & mv csystem calls: 
    # safer and cross platform.
    print fasta_file
    for f in ['.nhr','.nin','.nsq']:
        path = fasta_file + f
        shutil.move(path, os.path.join('DBs',os.path.basename(path) ) )
    shutil.copy2(fasta_file, os.path.join('DBs',os.path.basename(fasta_file)))
    # Get the strain ID
    # Nabil: Uses basename, rather than string splitting on '/' for filename.
    # Less chance of conflict from weird filenames. 
    return os.path.basename(fasta_file).split('_')[0]
    # END OF MODIFICATIONS

# MODIFIED BY NABIL 2013.07.168
# Now Requires file type of query (nucl or prot) and runs appropriate BLAST
# Assumes database is nucleotide
def run_BLAST(query, database):
    """
    Given a mfa of query virulence factors and a database, search for them
    
    Turns dust filter off. Only run on a single thread. Only a single target
    sequence. Output in XML format as blast.xml

    :param query: the fullpath to the vf.mfa
    :param database: the full path of the databse to search for the vf in

    :type query: string
    :type database: string
    """
    global args
    # TODO: Ideally I shouldn't pull down the option from global args but
    # This avoids altering parent method.
    # SeqPro: Is sequence protein. Prot = True, nucl = False
    SeqPro = False
    # File type not specified, determine using isPro()
    if args.reftype == None:
        print query 
        if isPro(query) > 0: SeqPro = True
    elif args.reftype == 'prot':
        SeqPro = True
    cline = ''
    if SeqPro:
        cline = NcbitblastnCommandline(query=query, seg='no', \
                db=database, outfmt=5, num_threads=1, \
                max_target_seqs=1, out='blast.xml')
    else:
        # TODO: Add  evalue filtering 
        # TODO: Set to use Megablast (as default), 
        # add task='blastn' to use blastn scoring
        cline = NcbiblastnCommandline(query=query, dust='no', \
                db=database, outfmt=5, num_threads=1, \
                max_target_seqs=1, out='blast.xml')
    print str(cline)
    cline()
    # TODO: This possibly should return location of BLAST results rather than
    # dumping to a static location...
    #END OF CHANGES - Nabil

# MODIFIED BY NABIL 2013.07.168
# HELPER METHOD TO CHECK NUCLEOTIDE OR PROTEIN SEQUENCE
def isPro( fastaFile ):
    """
    Checks if a FASTA file is protein or nucleotide.  returns number of protein
    sequences detected. 
    
    :param fastaFile: path to input FASTA file

    :type fastaFile: string

    :rtype: number of protein sequences in fastafile (int)
    """
    handle = open(fastaFile, 'rU')
    proHit = 0 
    for record in SeqIO.parse(handle, 'fasta'):
    # TODO: This probably should include ambiguity characters for nucleotide.
        if re.match('[^ATCGNatcgn]+', str(record.seq)) != None:
            proHit += 1
    handle.close() 
    return proHit 
# END OF CHANGES - Nabil 

def parse_BLAST(blast_results, tol):
    """
    Using NCBIXML parse the BLAST results, storing good hits.

    Here good hits are:
        * hsp.identities/float(record.query_length) >= tol

    :param blast_results: full path to a blast run output file (in XML format)
    :param tol: the cutoff threshold (see above for explaination)

    :type blast_results: string
    :type tol: string

    :rtype: list of satifying hit names
    """
    vf_hits = []
    for record in NCBIXML.parse(open(blast_results)) :
        for align in record.alignments :
            for hsp in align.hsps :
                virFactorName = record.query.split(',')[1].strip()
                if hsp.identities/float(record.query_length) >= tol:
                    vf_hits.append(virFactorName.strip())
    return vf_hits


def build_matrix_row(all_vfs, accepted_hits , score=None):
    """
    Populate row given all possible hits, accepted hits and an optional score 
    
    :param all_vfs: a list of all virulence factor ids
    :param accepted_hits: a list of a hits that passed the cutoof
    :param score: the value to fill the matrix with (default = None which 
                  implies 0.5)

    :type all_vfs: list
    :type accepted_hits: list
    :type score: float

    :rtype: a list of floats 
    """
    if score == None:
        score = 0.0
    row = []
    for factor in all_vfs:
        if factor in accepted_hits:
            row.append(score)
        else:
            row.append(0.5)
    return row

def match_matrix_rows(ass_mat, cons_mat):
    """
    Reorder a second matrix based on the first row element of the 1st matrix
    
    :param ass_mat: a 2D list of scores 
    :param cons_mat: a 2D list scores

    :type ass_mat: list
    :type cons_mat: list
    
    :rtype: 2 matricies (2D lists)   
    """
    reordered_ass, reordered_cons = [], []
    for i in range(0, len(ass_mat)):
        for j in range(0, len(cons_mat)):
            if ass_mat[i][0] == cons_mat[j][0]:
                reordered_ass.append(ass_mat[i][1:])
                reordered_cons.append(cons_mat[j][1:])
                break
    return reordered_ass, reordered_cons

def strip_id_from_matrix(mat):
    """
    Remove the ID (1st row element) form a matrix

    :param mat: a 2D list

    :rtype: a 2D list with the 1st row elelemnt (ID) removed
    """
    new_mat = []
    for i in range(0, len(mat)):
        new_mat.append(mat[i][1:])
    return new_mat


def cluster_matrix(matrix, y_labels):
    """
    From a matrix, generate a distance matrix & perform hierarchical clustering
 
    :param matrix: a numpy matrix of scores
    :param y_labels: the virulence factor ids for all row elements
    """
    print "Clustering the matrix"
    # Clear any matplotlib formatting
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Hide x labels/ticks
    ax.set_yticklabels([])
    ax.set_yticks([])
    plt.xticks(fontsize=6)
    Y = pdist(matrix)
    Z = linkage(Y)
    dend = dendrogram(Z,labels=y_labels)
    plt.savefig("dendrogram.png", dpi=600)
    #Reshape
    ordered_index   = dend['leaves']
    updated_ylabels = dend['ivl']
    tmp = []
    for i in range(0, len(ordered_index)):
        tmp.append(list(matrix[ordered_index[i],:]))
    matrix = np.array(tmp)
    return matrix, updated_ylabels


def plot_matrix(matrix, strain_labels, vfs_classes, gene_labels, 
                show_gene_labels, color_index, config_object, grid,
		aspect='auto'):
    """
    Plot the VF hit matrix

    :param matrix: the numpy matrix of scores
    :param strain_labels: the strain (y labels)
    :param vfs_classes: the VFS class (in mfa header [class])
    :param gene_labels: the gene labels
    :param show_gene_labels: wheter top plot the gene labels
    :param color_index: for a single class, choose a specific color
    """
    if config_object['category_colors'] != None:
            colors = config_object['category_colors']
    else:
        colors = [(0/255.0,0/255.0,0/255.0),
                (255/255.0,102/255.0,0/255.0),
                (170/255.0,255/255.0,0/255.0),
                (255/255.0,0/255.0,170/255.0),
                (0/255.0,102/255.0,255/255.0),
                (156/255.0,0/255.0,62/255.0),
                (203/255.0,168/255.0,255/255.0),
                (156/255.0,131/255.0,103/255.0),
                (255/255.0,170/255.0,0/255.0),
                (0/255.0,255/255.0,204/255.0),
                (0/255.0,0/255.0,255/255.0),
                (0/255.0,156/255.0,41/255.0),
                (238/255.0,255/255.0,168/255.0),
                (168/255.0,215/255.0,255/255.0),
                (103/255.0,156/255.0,131/255.0),
                (255/255.0,0/255.0,0/255.0),
                (0/255.0,238/255.0,255/255.0),
                (238/255.0,0/255.0,255/255.0),
                (156/255.0,145/255.0,0/255.0),
                (255/255.0,191/255.0,168/255.0),
                (255/255.0,168/255.0,180/255.0),
                (156/255.0,103/255.0,138/255.0)] 
    if color_index != None:
        colors = [colors[int(color_index)]]
    # Build the regions to be shaded differently
    regions, prev = [], 0
    for i in xrange(0, len(vfs_classes)-1):
        if vfs_classes[i] != vfs_classes[i+1]:
            regions.append([prev+0.5, i+0.5])
            prev = i
    regions.append([prev+0.5, len(vfs_classes)-0.5])
    regions[0][0] = regions[0][0]-1.0
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # aspect auto to widen
    ax.matshow(matrix, cmap=cm.gray, aspect=aspect)
    # Make sure every strain
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%s'))
    ax.set_yticklabels(strain_labels)
    if len(gene_labels) < 999:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%s'))
        ax.xaxis.grid(False) 
    if show_gene_labels:
        ax.set_xticklabels([''] +gene_labels)#, rotation=90)
    for i in xrange(0, len(regions)):
        plt.axvspan(regions[i][0], regions[i][1], facecolor=colors[i],         \
                        alpha=0.1)
    if show_gene_labels:
        ax.tick_params(axis='both', which='both', labelsize=6, direction='out',\
                       labelleft='on', labelright='off', \
                       labelbottom='off', labeltop='on', \
                       left='on', right='off', bottom='off', top='on')
    else:
        ax.tick_params(axis='both', which='both', labelsize=6, direction='out',\
                       labelleft='on', labelright='off', \
                       labelbottom='off', labeltop='off', \
                       left='on', right='off', bottom='off', top='off')
    plt.xticks(rotation=90)
    if grid: ax.grid(True)
    fig.set_size_inches(10.0,12.0, dpi=600)
    plt.savefig("results.png", bbox_inches='tight',dpi=600)

def do_run(vf_db, data_path, match_score, order, cutoff, vfs_list):
    """
    Perform a VirFindR run
    """
    matrix, y_label = [], []
    # Nabil:  amended with listdir rather than glob, to allow for more complex
    # matching
    in_files = []
    for files in os.listdir(data_path):
        # TODO: There HAS to be a neater way of checking different extensions.
            if files.endswith(".fas") or files.endswith(".fna") \
                    or files.endswith(".fa"):
                in_files.append(os.path.join(data_path, files))
    # Reorder if requested 
    if order != None:
        in_files = order_inputs(order, in_files)
    for genome_file in in_files:
        id = make_BLASTDB(genome_file)
        y_label.append(id)
        db_loc = genome_file.split('/')[-1]
        run_BLAST(vf_db, "DBs/"+db_loc)
        accepted_hits = parse_BLAST("blast.xml", float(cutoff))
        row = build_matrix_row(vfs_list, accepted_hits, match_score)
        row.insert(0,id)
        matrix.append(row)
    return matrix, y_label


def main():
    configObject = SeqFindRConfig()
    default_no_hit = 0.5
    global args
    try:
        os.mkdir("DBs")
    except:
        print "A DBs directory exists. Overwriting"
    vfs_list, vfs_class = prepare_db(args.db)
    results_a, ylab = do_run(args.db, args.ass, -0.15, args.index,           \
                                args.tol, vfs_list)
    if args.cons != None:
        # Trim off db and sequences 
        #TODO: Exception handling if do_run fails or produces no results. 
        # Should be caught here before throwing ugly exceptions downstream.
        results_m, _ = do_run(args.db, args.cons, -0.85, args.index,         \
                                args.tol, vfs_list)
        if len(results_m) == len(results_a):
            results_a, results_m = match_matrix_rows(results_a, results_m)
            default_no_hit = 1.0
            matrix = np.array(results_a) + np.array(results_m)
        else:
            print "Assemblies and mapping consensuses don't match"
            sys.exit(1)
    else:
        args.reshape = False
        results_a = strip_id_from_matrix(results_a)
        matrix = np.array(results_a)
    # cluster if not ordered
    if args.index == None:
        matrix, ylab = cluster_matrix(matrix, ylab)
    np.savetxt("matrix.csv", matrix, delimiter=",")
    # Add the buffer
    newrow = [default_no_hit] * matrix.shape[1]
    matrix = np.vstack([newrow, matrix])
    matrix = np.vstack([newrow, matrix])
    #Handle new option to only show presence
    if args.reshape == True:
        for x in np.nditer(matrix, op_flags=['readwrite']):
            if x < 0.99:
                x[...] = -1.0
    ylab = ['', '']+ ylab
    plot_matrix(matrix, ylab, vfs_class, vfs_list, args.label_genes, args.color, configObject, args.grid) 
    # Handle labels here
    #print vfs_class
    os.system("rm blast.xml")
    os.system("rm DBs/*")


if __name__ == '__main__':
    try:
        start_time = time.time()
        desc = __doc__.split('\n\n')[1].strip()
        parser = argparse.ArgumentParser(description=desc,epilog=epi)
        # ADDED BY  NABIL 13.07.16
        # Reference database type override & support for protein sequences
        parser.add_argument('-R', '--reftype', action='store', help='Reference\
                Sequence type', dest='reftype', choices=('nucl','prot'),\
                default=None)
        # END OF CHANGES 
        parser.add_argument('-v', '--verbose', action='store_true',            \
                                default=False, help='verbose output')
        # Nabil: Not used, removed Required flag so it can be ignored.
        parser.add_argument('-o','--output',action='store',                    \
                                help='output prefix')
        # TODO: Nabil; Required options should be positional arguments not 
        # optional flags
        parser.add_argument('-d', '--db', action='store',                    \
                                help='[Required] full path database fasta file')
        parser.add_argument('-a', '--ass', action='store',                     \
                                help='[Required] full path to dir containing '+\
                                     'assemblies')
        parser.add_argument('-t', '--tol', action='store', default=0.95,       \
                                help='Similarity cutoff (default = 0.95)')
        parser.add_argument('-m', '--cons', action='store', default=None,      \
                                help=('full path to dir containing consensuses'\
                                    +' (default = None)'))
        parser.add_argument('-i', '--index', action='store', default=None,     \
                                help=('maintain order of index (no cluster)'   \
                                    +' (default = None)'))
        parser.add_argument('-l', '--label_genes', action='store_true',        \
                                    default=False, help=('label the x axis' 
                                    +' (default = False)'))
        parser.add_argument('-c', '--color', action='store', default=None,     \
                                help='color index (default = None)')
        parser.add_argument('-r', '--reshape', action='store_false',           \
                                default=True, help='Differentiate '
                                        'between mapping and assembly hits')
        parser.add_argument('-g', '--grid', action='store_false',              \
                                default=True, help='Plot has a grid (default ' 
                                       '= True')

        args = parser.parse_args()
        msg = "Missing required arguments.\nPlease run: SeqFindR -h"
        if args.db == None:
            print msg
            sys.exit(1)
        if args.ass == None:
            print msg
            sys.exit(1)
        if args.output == None:
            print msg
            sys.exit(1)

        if args.verbose: print "Executing @ " + time.asctime()
        main()
        if args.verbose: print "Ended @ " + time.asctime()
        if args.verbose: print 'total time in minutes:',
        if args.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

