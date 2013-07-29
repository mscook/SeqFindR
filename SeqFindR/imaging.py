# Copyright 2013 Mitchell Stanton-Cook Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# http://www.osedu.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.


import random

SEED = 99

def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB
    
    :param h: hue
    :param s: saturation
    :param v: value
    """
    h_i = int(h*6)
    f   = h*6 - h_i
    p   = v * (1 - s)
    q   = v * (1 - f*s)
    t   = v * (1 - (1 - f) * s)
    if h_i == 0: 
        r, g, b = v, t, p
    elif h_i == 1: 
        r, g, b = q, v, p
    elif h_i == 2: 
        r, g, b = p, v, t
    elif h_i == 3: 
        r, g, b = p, q, v
    elif h_i == 4: 
        r, g, b = t, p, v
    elif h_i == 5: 
        r, g, b = v, p, q
    else:
        print "Problem"
    return [int(r*256), int(g*256), int(b*256)]

def generate_colors(number_required):
    """
    Generate a list of length number of distinct "good" random colors

    Based on http://martin.ankerl.com/
        2009/12/09/how-to-create-random-colors-programmatically/
    
    :param number_required: int
    :type: int
    :rtype: a list of lists in the form: [[243, 137, 121], [232, 121, 243], 
                                          [216, 121, 243]]
    """
    rgb_list = []
    golden_ratio_conjugate = 0.618033988749895
    random.seed(SEED)
    for i in range(0, int(number_required)):
        h = (random.random()+golden_ratio_conjugate) % 1
        rgb = hsv_to_rgb(h, 0.5, 0.95)
        rgb = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
        rgb_list.append(rgb)
    return rgb_list
