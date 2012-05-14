#!/usr/bin/env python

# Copyright (c) 2012 Robert Bieber
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
import os.path
import sys

####
## Helper functions
###

def scandir(root):
    files = []
    dirs = []
    
    # Scan for files
    for f in sorted(os.listdir(root)):
        path = os.path.join(root, f)
        thumbpath = os.path.join(root, 'thumb' + f)
        
        if os.path.isdir(path):
            # Queueing up directories to scan after every file is checked
            dirs.append(path)
        elif os.path.splitext(path)[1].lower() == '.jpg' and f[0:5] != 'thumb':
            files.append((path, thumbpath))

    # Then recurse on directories
    for path in dirs:
        files.extend(scandir(path))

    return files

####
## Execution begins here
###

if(len(sys.argv) != 4):
    print "Usage: genthumbs.py <directory> <width> <height>"
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print("Error: Input path must be a directory")

imgcount = 0
width = int(sys.argv[2])
height = int(sys.argv[3])
files = scandir(sys.argv[1])
for f in files:
    command = ("convert " + f[0] + " -auto-orient -thumbnail " 
               + str(width) + "x" + str(height) + " " + f[1])
    os.system(command)
    imgcount += 1
    print "Finished %d out of %d" % (imgcount, len(files))
