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
vfdb_to_seqfindr
================

Convert VFDB formatted files (or like) to SeqFindR formatted database files


VFDB: Virulence Factors Database
www.mgc.ac.cn/VFs/
a reference database for bacterial virulence factors.


This is based on a sample file (TOTAL_Strep_VFs.fas) provided by 
Nouri Ben Zakour.

Examples::

    # Default (will set VFDB classification identifiers as the classification)
    $ vfdb_to_seqfindr -i TOTAL_Strep_VFs.fas -o TOTAL_Strep_VFs.sqf
    
    # Sets any classification to blank ([ ])
    $ vfdb_to_seqfindr -i TOTAL_Strep_VFs.fas -o TOTAL_Strep_VFs.sqf -b

    # Reads a user defined classification. 1 per in same order as input 
    # sequences
    $ python convert_vfdb_to_SeqFindR.py -i TOTAL_Strep_VFs.fas 
      -o TOTAL_Strep_VFs.sqf -c blah.dat 


About option --class_file
-------------------------

Suppose you want to annotate a VF class with user defined values. Simply 
develop a file containing the scheme (1-1 matching). If you had 6 input 
sequences and the first 3 are Fe transporters and the next two are Toxins
and the final sequence is Misc your class file would look like this:

Fe transporter
Fe transporter
Fe transporter
Toxins
Toxins
Misc
"""

__author__ = "Mitchell Stanton-Cook"
__licence__ = "ECL"
__version__ = "0.2"
__email__ = "m.stantoncook@gmail.com"
epi = "Licence: "+ __licence__ +  " by " + __author__ + " <" + __email__ + ">"
USAGE = "vfdb_to_seqfindr -h"


import sys, os, traceback, argparse, time, fileinput, shutil
from   Bio import SeqIO

def main():
    global args
    count = 0
    if args.class_file != None:
        with open(os.path.expanduser(args.class_file)) as class_in:
            class_lines = class_in.readlines()
            args.blank_class = False
    with open(os.path.expanduser(args.outfile), "w") as fout:
        with open(os.path.expanduser(args.infile)) as fin:
            classi = '[ ]'
            for line in fin:
                if line.startswith('>'):
                    elements    = line.split(' ')
                    identifier  = elements[0].strip()
                    common_name = elements[1].strip()
                    # For the annotation
                    tmp   = line.split('-')[1:]
                    rjoin = '-'.join(tmp)
                    ann   = rjoin.split('[')[0].replace(',', ';').strip()
                    spec  = line.split('[')[1].split(']')[0].strip()
                    # For the classification
                    tmp = elements[-1]
                    if args.class_file != None:
                        classi = '[ %s ]' % (class_lines[count].strip())
                        count = count+1
                    else:
                        count = count+1
                        if args.blank_class == False:
                            if tmp.find('(') != -1:
                                classi = tmp.strip().replace(
                                                '(', '[').replace(')', ']')
                    fout.write('%s, %s, %s, %s %s\n' % (identifier, 
                                                common_name, ann, spec, classi))
                else:
                    fout.write(line.strip().upper()+'\n')
    print 'Wrote %s records' % count
    if not args.blank_class:
        order_by_class()

def order_by_class():
    """
    Ensure that all particualr classes are in the same block
    """
    global args
    
    d = {}
    with open(args.outfile, "rU") as fin:
        for record in SeqIO.parse(fin, "fasta") :
            cur_class = record.description.split('[')[-1].split(']')[0].strip()
            if not d.has_key(cur_class):
                d[cur_class] = []
                cur = d[cur_class]
                cur.append(record)
                d[cur_class] = cur
            else:
                cur = d[cur_class]
                cur.append(record)
                d[cur_class] = cur
        BASE, EXT = os.path.splitext(args.outfile)
        sub_files = []
        for key in d.keys():
            # Write each of the subfiles
            sub_files.append(BASE+"_"+key+EXT)
            with open(sub_files[-1], 'w') as fout:
                cur = d[key]
                for e in cur:
                    fout.write('>'+e.description+'\n')
                    fout.write(str(e.seq)+'\n')
            handle.close()
        # Write the concatenated
        with open(BASE+".tmp", 'w') as fout:
            for line in fileinput.input(sub_files):
                fout.write(line)
    shutil.mv(BASE+".tmp", args.outfile)

if __name__ == '__main__':
    try:
        start_time = time.time()
        desc = __doc__.split('\n\n')[1].strip()
        parser = argparse.ArgumentParser(description=desc,epilog=epi)
        parser.add_argument('-i', '--infile', action='store', 
                            help='[Required] fullpath to the in fasta file')
        parser.add_argument('-o','--outfile',action='store',
                            help='[Required] fullpath to the out fasta file')
        parser.add_argument('-c', '--class_file', action='store', default=None,
                            help='[Optional] full path to a file containing '
                                  'factor classifications')
        parser.add_argument('-b', '--blank_class', action='store_true', 
                                  default=False, help='[Optional] set '
                                  'classification blank even if such exist')
        args = parser.parse_args()
        msg = "Missing required arguments.\nPlease run: vfdb_to_seqfindr -h"
        if args.infile == None:
            print msg
            sys.exit(1)
        if args.outfile == None:
            print msg
            sys.exit(1)

        print "Executing @ " + time.asctime()
        main()
        print "Ended @ " + time.asctime()
        print 'total time in minutes:',
        print (time.time() - start_time) / 60.0
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
