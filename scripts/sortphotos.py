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

import sys
import os.path
import subprocess
import shutil

####
## Constants
###

RAWFILES = [".dng", ".raw", ".nef", ".raf", ".orf", ".srf", ".sr2", ".arw",
            ".k25", ".kdc", ".dcr", ".mos", ".pnx", ".crw", ".cr2", ".mrw",
            ".pef", ".mef"]

####
## Helper functions
###

# Reads a directory and returns a list of (filename, .ufraw file) pairs
# For JPG files, the second element of the pair is None
def scandir(root, ufraw = None):
    files = []
    dirs = []
    
    # First scan for files
    for f in sorted(os.listdir(root)):
        path = os.path.join(root, f)
        
        if os.path.isdir(path):
            # Queueing up directories to scan after every file is checked
            dirs.append(path)
        elif os.path.splitext(path)[1].lower() == '.ufraw':
            ufraw = path
        else:
            files.append((path, ufraw))

    # Then recurse on directories
    for path in dirs:
        files.extend(scandir(path, ufraw))

    return files

####
## Execution begins here
###

if(len(sys.argv) != 3):
    print("Usage: sortphotos.py <input directory> <output directory>")
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print("Error: Input path must be a directory")
    sys.exit(1)

if not os.path.isdir(sys.argv[2]):
    if os.path.exists(sys.argv[2]):
        print("Error: Output path must be a directory")
        sys.exit(1)
    else:
        os.mkdir(sys.argv[2])
        
serial = "missing_serial"
serials = {"missing_serial": 0}
imgcount = 0
files = scandir(sys.argv[1])
for (path, ufraw) in files:
    
    # Carrying out RAW conversion if necessary
    if RAWFILES.count(os.path.splitext(path)[1].lower()) != 0:
        command = "ufraw-batch "
        command += "--silent "
        command += "--overwrite "
        command += "--out-path=./ "
        command += "--output=.temp.jpg "
        if ufraw:
            command += "--conf=" + ufraw + " "
        command += path
        os.system(command)
        os.remove(".temp.ufraw")
        
    # Otherwise just copy over the JPEG file
    else:
        shutil.copyfile(path, ".temp.jpg")

    # First resize to something ZBar can handle
    os.system("convert .temp.jpg -resize 500x500^ .temp_small.jpg")

    # Now scan the JPEG file for QR codes
    try:
        zbarout = subprocess.check_output(["zbarimg", "-q", ".temp_small.jpg"])

        # check_output throws an exception if no bar code is found, so at this
        # point we can assume we've found something

        print zbarout

    except subprocess.CalledProcessError:
        pass
    
    # Cleaning up
    os.remove(".temp.jpg")
    os.remove(".temp_small.jpg")

    imgcount += 1
    print "Finished image %d of %d" % (imgcount, len(files))
