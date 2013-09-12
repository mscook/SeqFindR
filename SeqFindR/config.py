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
SeqFindR configuration class
"""

import os
import sys

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
                sys.stderr.write("Using a SeqFindR config file\n")
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
            sys.stderr.write("No SeqFindR config file. Using defaults\n")
        return cfg

    def dump_items(self):
        """
        Prints all set configuration options to STDOUT
        """
        config = ''
