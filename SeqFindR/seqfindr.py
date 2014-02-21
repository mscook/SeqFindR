#!/usr/bin/env python

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
A tool to easily create informative genomic feature plots
"""

import sys, os, traceback, argparse
import time
import ast
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from   matplotlib.ticker import MultipleLocator, FormatStrFormatter

import numpy as np
from   scipy.cluster.hierarchy import linkage, dendrogram
from   scipy.spatial.distance  import pdist

from Bio import SeqIO

from SeqFindR import imaging
from SeqFindR import config
from SeqFindR import util
from SeqFindR import blast

__title__        = 'SeqFindR'
__version__      = '0.26'
__description__  = "A tool to easily create informative genomic feature plots" 
__author__       = 'Mitchell Stanton-Cook, Nabil Alikhan & Hamza Khan'
__license__      = 'ECL 2.0'
__author_email__ = "m.stantoncook@gmail.com"
__url__         = 'http://github.com/mscook/SeqFindR'

epi = "Licence: %s by %s <%s>" % (__license__, 
                                  __author__,
                                  __author_email__)
__doc__ = " %s v%s - %s (%s)" % ( __title__, 
                                  __version__, 
                                  __description__, 
                                  __url__)


def prepare_queries(args):
    """
    Given a set of sequences of interest, extract all query & query classes

    A sequence of interest file is a mfa file in the format:

    >ident, gene id, annotation, organism [class]

    query = gene id
    query_class = class

    Location of sequence of interest file is defined by args.seqs_of_interest

    :param args: the argparse args containing args.seqs_of_interest 
                 (fullpath) to a sequence of interest DB (mfa file)

    :type args: argparse args

    :rtype: 2 lists, 1) of all queries and, 2) corresponding query classes
    """
    query_list, query_classes = [], []

    with open(args.seqs_of_interest, "rU") as fin:
        records = SeqIO.parse(fin, "fasta")
        for rec in records:
            cur = rec.description
            query_list.append(cur.split(',')[1].strip())
            query_classes.append(cur.split('[')[-1].split(']')[0].strip())
    unique = list(set(query_list))
    sys.stderr.write("Investigating %i features\n" % (len(unique)))
    for e in unique:
        if query_list.count(e) != 1:
            sys.stderr.write("Duplicates found for: %s\n" % (e))
            sys.stderr.write("Fix duplicates\n")
            sys.exit(1)
    return query_list, query_classes


def strip_bases(args):
    """
    Strip the 1st and last 'N' bases from mapping consensuses

    Uses: 
        * args.cons
        * args.seqs_of_interest
        * arg.strip

    To avoid the effects of lead in and lead out coverage resulting in 
    uncalled bases
    
    :param args: the argparse args containing args.strip value

    :type args: argparse args

    :rtype: the updated args to reflect the args.cons & 
            args.seqs_of_interest location
    """
    # Get in the fasta files in the consensus directory
    fasta_in = util.get_fasta_files(args.cons)
    # Build a stripped directory
    new_cons_dir = os.path.join(args.cons, 'stripped')
    try:
        os.mkdir(new_cons_dir)
    except OSError:
        sys.stderr.write("A stripped directory exists. Overwriting\n")
    # Update the args.cons to the stripped directory
    args.cons = new_cons_dir
    args.strip = int(args.strip)
    # Strip the start and end
    for fa in fasta_in:
        tmp = os.path.basename(fa)
        out = os.path.join(args.cons, tmp)
        with open(fa, "rU") as fin, open(out, 'w') as fout:
            records = SeqIO.parse(fin, "fasta")
            for rec in records:
                rec.seq = rec.seq[args.strip:-args.strip]
                SeqIO.write(rec, fout, "fasta")
    # Trim the db as well
    tmp = args.seqs_of_interest.split('.')
    stripped_db = '.'.join(tmp[:-1])+'_trimmed.'+tmp[-1]
    with open(args.seqs_of_interest, "rU") as fin, open(stripped_db, 'w') as fout:
        records = SeqIO.parse(fin, "fasta")
        for rec in records:
            rec.seq = rec.seq[args.strip:-args.strip]
            SeqIO.write(rec, fout, "fasta")
    #Update the args.seqs_of_interest
    args.seqs_of_interest = stripped_db
    return args



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


def cluster_matrix(matrix, y_labels, dpi):
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
    plt.savefig("dendrogram.png", dpi=dpi)
    #Reshape
    ordered_index   = dend['leaves']
    updated_ylabels = dend['ivl']
    tmp = []
    for i in range(0, len(ordered_index)):
        tmp.append(list(matrix[ordered_index[i],:]))
    matrix = np.array(tmp)
    return matrix, updated_ylabels


def read_existing_matrix_data(args):
    """
    With Provided existing data, this method reads & passes to plot_matrix

    We have performed basic functional testing

    :param args: an argparse set of arguments containing atleast the location
                 of the data directory

    :returns: tuple - of lists containing required data in the order (matrix, 
              classes, strain_labels, xlabels, index_file_l)
    """
    configObject = config.SeqFindRConfig()
    matrix = []  
    classes = []  
    strain_labels = []   
    xlabels = []
    index_file_l = []
    # Fix if shorthand ~/
    data_dir = os.path.expanduser(args.data_dir)
    index_file = args.index_file
    if index_file != None:
        index_file = os.path.expanduser(index_file)
    # Open all stored files
    with open(os.path.join(data_dir, 'matrix.csv'), 'rb')  as m,               \
         open(os.path.join(data_dir, 'classes.txt'), 'rb') as rrm, \
         open(os.path.join(data_dir, 'strain_labels.txt'), 'rb') as sl,       \
         open(os.path.join(data_dir, 'xlabels.txt'), 'rb') as vfs:
        # Handle index file. By default we end up with index according to 
        # the strain labels order
        if index_file == None:
            index = sl
        else:
            index = open(index_file, 'rb')
        for row in rrm:
            classes.append(row.strip('\n'))
        for row in sl:
            strain_labels.append(row.strip('\n'))
        if index_file == None:
            index.seek(0)
        for row in index:
            index_file_l.append(row.strip('\n'))
        for row in vfs:
            xlabels.append(row.strip('\n'))           
        reader = csv.reader(m)
        for row in reader:
            matrix.append(row)
    # Convert matrix to numpy matrix
    matrix = np.array(matrix)
    matrix = matrix.astype(np.float)
    plot_matrix(matrix, strain_labels, classes, xlabels,  \
            args.label_genes, args.color, configObject, args.grid, args.seed, \
            args.DPI, args.size, args.svg, None)
             

def plot_matrix(matrix, strain_labels, vfs_classes, gene_labels,  
        show_gene_labels, color_index, config_object, grid, seed, 
        dpi, size, svg, compress, aspect='auto'):
    """
    Plot the VF hit matrix

    TODO: update doc for this

    :param matrix: the numpy matrix of scores
    :param strain_labels: the strain (y labels)
    :param vfs_classes: the VFS class (in mfa header [class])
    :param gene_labels: the gene labels
    :param show_gene_labels: wheter top plot the gene labels
    :param color_index: for a single class, choose a specific color
    """
    # Saving data for regeneration
    if compress != None:
        try:
            os.makedirs('data')
        except OSError:
            sys.stderr.write("A data directory exists. Exiting\n")
            sys.exit(-1)
        classes = open(os.path.join('data', "classes.txt"), 'wb')
        for item in vfs_classes:
            classes.write(item+'\n')
        classes.close()
        xlab = open(os.path.join('data', "xlabels.txt"), 'wb')
        for item in gene_labels:
            xlab.write(item+'\n')
        xlab.close()
        ylab = open(os.path.join('data', "strain_labels.txt"), 'wb')
        for item in strain_labels:
            if(item != ''):
                ylab.write(item+'\n')
        ylab.close()

    if config_object['category_colors'] != None:
        colors = config_object['category_colors']
    else:
        colors = imaging.generate_colors(len(set(vfs_classes)), seed)
    if color_index != None:
        print color_index
        print colors
        colors = [colors[(color_index)]]
        print colors
        print "\n"
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
    x, y = size.split('x')
    x, y = float(x), float(y)
    fig.set_size_inches(x, y, dpi=dpi)
    if svg: 
        plt.savefig("results.svg", bbox_inches='tight',dpi=dpi)
    else:
        plt.savefig("results.png", bbox_inches='tight',dpi=dpi)


def do_run(args, data_path, match_score, vfs_list):
    """
    Perform a SeqFindR run
    """
    matrix, y_label = [], []
    in_files = util.get_fasta_files(data_path)
    # Reorder if requested 
    if args.index_file != None:
        in_files = util.order_inputs(args.index_file, in_files)
    for subject in in_files:
        strain_id = blast.make_BLAST_database(subject)
        y_label.append(strain_id)
        database      = os.path.basename(subject)
        blast_xml     = blast.run_BLAST(args.seqs_of_interest, os.path.join(os.getcwd(), "DBs/"+database), args)
        accepted_hits = blast.parse_BLAST(blast_xml, float(args.tol))
        row = build_matrix_row(vfs_list, accepted_hits, match_score)
        row.insert(0,strain_id)
        matrix.append(row)
    return matrix, y_label



def core(args):
    """
    The 'core' SeqFindR method

    TODO: Exception handling if do_run fails or produces no results

    :param args: the arguments given from argparse
    """
    DEFAULT_NO_HIT, ASS_WT, CONS_WT = 0.5, -0.15, -0.85
    args = util.ensure_paths_for_args(args)   
    configObject = config.SeqFindRConfig()
    util.init_output_dirs(args.output)
    query_list, query_classes = prepare_queries(args)
    results_a, ylab = do_run(args, args.assembly_dir, ASS_WT, query_list)
    if args.cons != None:
        args = strip_bases(args)
        #TODO: Exception handling if do_run fails or produces no results. 
        # Should be caught here before throwing ugly exceptions downstream.
        results_m, _ = do_run(args, args.cons, CONS_WT, query_list)
        if len(results_m) == len(results_a):
            results_a, results_m = match_matrix_rows(results_a, results_m)
            DEFAULT_NO_HIT = 1.0
            matrix = np.array(results_a) + np.array(results_m)
        else:
            print "Assemblies and mapping consensuses don't match"
            sys.exit(1)
    else:
        args.reshape = False
        results_a = strip_id_from_matrix(results_a)
        matrix = np.array(results_a)
    # cluster if not ordered
    if args.index_file == None:
        matrix, ylab = cluster_matrix(matrix, ylab, args.DPI)
    np.savetxt("matrix.csv", matrix, delimiter=",")
    # Add the buffer
    newrow = [DEFAULT_NO_HIT] * matrix.shape[1]
    matrix = np.vstack([newrow, matrix])
    matrix = np.vstack([newrow, matrix])
    #Handle new option to only show presence
    if args.reshape == True:
        for x in np.nditer(matrix, op_flags=['readwrite']):
            if x < 0.99:
                x[...] = -1.0
    ylab = ['', '']+ ylab
    plot_matrix(matrix, ylab, query_classes, query_list, args.label_genes, args.color, configObject, args.grid, args.seed, args.DPI, args.size, args.svg, args.compress) 
    # Handle labels here
    os.system("rm blast.xml")
    os.system("rm DBs/*")


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
        parser.add_argument('-v', '--verbose', action='store_true', 
                                default=False, help='verbose output')
        subparsers = parser.add_subparsers(help="Available commands:")
        gen = subparsers.add_parser('generate', help=('Generate SeqFindR '
                                                            'figure'))
        regen = subparsers.add_parser('regenerate', help=('Regenerate SeqFindR '
                                                            'figure'))
        d3js = subparsers.add_parser('d3js', help=('Generate D3.js '
                                                        'SeqFindR figure'))
        algorithm = gen.add_argument_group('Optional algorithm options', 
                                    ('Options relating to the SeqFindR '
                                        'algorithm'))
        io = gen.add_argument_group('Optional input/output options', 
                                    ('Options relating to input and output'))

        fig = gen.add_argument_group('Figure options', ('Options relating ' 
                                    'to the output figure'))
        blast_opt = gen.add_argument_group('BLAST options', ('Options relating ' 
                                    'to BLAST'))
        blast_opt.add_argument('-R', '--reftype', action='store', 
                                help=('Reference Sequence type. If not given ' 
                                    'will try to detect it'), dest='reftype', 
                                choices=('nucl','prot'), default=None)
        blast_opt.add_argument('-X', '--tblastx', action='store_true', 
                                default=False, help=('Run tBLASTx rather than ' 
                                                     'BLASTn'))
        blast_opt.add_argument('--evalue', action='store', type=str,
                                default='10', help=('BLAST evale (Expect)'))
        blast_opt.add_argument('--short', action='store_true',
                                default=False, help=('Have short queries i.e. '
                                                    'PCR Primers'))
        io.add_argument('-o','--output',action='store', 
                                default=None, help=('Output the results to ' 
                                    'this location'))
        io.add_argument('-p','--output_prefix',action='store', 
                                default=None, help=('Give all result files ' 
                                    'this prefix'))
        # Required options now positional arguments
        gen.add_argument('seqs_of_interest', action='store', 
                                help=('Full path to FASTA file containing a ' 
                                    'set of sequences of interest'))
        gen.add_argument('assembly_dir', action='store', 
                                help=('Full path to directory containing a' 
                                      'set of assemblies in FASTA format'))
        regen.add_argument('data_dir', action='store', 
                                help=('Full path to directory containing the' 
                                      'data directory from a previous run'))
        regen.add_argument('--index_file', action='store', default=None, 
                                help=('Maintain the y axis strain order ' 
                                        'according to order given in this ' 
                                        'file. Otherwise clustering by row ' 
                                        'similarity. [default = do ' 
                                        'clustering]. See manual for more ' 
                                        'info'))
        algorithm.add_argument('-t', '--tol', action='store', type=float, 
                                    default=0.95, help=('Similarity cutoff ' 
                                        '[default = 0.95]'))
        algorithm.add_argument('-m', '--cons', action='store', default=None, 
                                help=('Full path to directory containing ' 
                                      'mapping consensuses [default = None]' 
                                      '. See manual for more info'))
        fig.add_argument('-l', '--label_genes', action='store_true', 
                                    default=False, help=('Label the x axis ' 
                                    +'with the query identifier [default = '
                                    'False]'))
        fig.add_argument('-c', '--compress', action='store_true', 
                                    default=False, help=('Remove columns ' 
                                    +'where no hits are present [default = '
                                    'False]'))
        algorithm.add_argument('-r', '--reshape', action='store_false', 
                                default=True, help=('Differentiate ' 
                                        'between mapping and assembly hits in ' 
                                        'the figure [default = no ' 
                                        'differentiation]'))
        fig.add_argument('-g', '--grid', action='store_false', default=True, 
                                help='Figure has grid lines ' 
                                    '[default = True]')
        algorithm.add_argument('--index_file', action='store', default=None, 
                                help=('Maintain the y axis strain order ' 
                                        'according to order given in this ' 
                                        'file. Otherwise clustering by row ' 
                                        'similarity. [default = do ' 
                                        'clustering]. See manual for more ' 
                                        'info'))
        fig.add_argument('--color', action='store', default=None, type=int,
                                help=('The color index [default = None]. ' 
                                        'See manual for more info'))
        fig.add_argument('--DPI', action='store', type=int, default=300,  
                                help='DPI of figure [default = 300]')
        fig.add_argument('--seed', action='store', type=int, default=99,  
                                help='Color generation seed')
        fig.add_argument('--svg', action='store_true', default=False, help=('Draws figure in svg'))
        fig.add_argument('--size', action='store', type=str, default='10x12', 
                                help='Size of figure [default = 10x12 '
                                    '(inches)]')
        regen.add_argument('-l', '--label_genes', action='store_true', 
                                    default=False, help=('Label the x axis ' 
                                    +'with the query identifier [default = '
                                    'False]'))
        regen.add_argument('-g', '--grid', action='store_false', default=True, 
                                help='Figure has grid lines ' 
                                    '[default = True]')
        regen.add_argument('--color', action='store', default=None, type=int,
                                help=('The color index [default = None]. ' 
                                        'See manual for more info'))
        regen.add_argument('--DPI', action='store', type=int, default=300,  
                                help='DPI of figure [default = 300]')
        regen.add_argument('--seed', action='store', type=int, default=99,  
                                help='Color generation seed')
        regen.add_argument('--svg', action='store_true', default=False, help=('Draws figure in svg'))
        regen.add_argument('--size', action='store', type=str, default='10x12', 
                                help='Size of figure [default = 10x12 '
                                    '(inches)]')
        algorithm.add_argument('-s', '--strip', action='store', 
                                default=10, help=('Strip the 1st and last N ' 
                                        'bases of mapping consensuses & ' 
                                        'database [default = 10]'))
        blast_opt.add_argument('--BLAST_THREADS', action='store', type=int, 
                                default=1, help=('Use this number of threads '
                                        'in BLAST run [default = 1]'))
        gen.set_defaults(func=core)
        regen.set_defaults(func=read_existing_matrix_data)
        d3js.set_defaults(func=core)
        args = parser.parse_args()
        if args.verbose: 
            print "Executing @ " + time.asctime()
        args.func(args)
        if args.verbose:
            print "Ended @ " + time.asctime()
            print 'Exec time minutes %f:' % ((time.time() - start_time) / 60.0)
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
