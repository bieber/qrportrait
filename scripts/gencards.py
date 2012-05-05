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
import sys
import math
import random
import time

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch

####
## User Parameters
###

# Turns card grid on or off
PRINTGRID = True

# Font sizes for the card text
URLSIZE = 14
SERIALSIZE = 26

# The width, height, and safe area of each card
CARDWIDTH = 3.625 * inch
CARDHEIGHT = 2.125 * inch
CARDSAFEWIDTH = 3.25 * inch
CARDSAFEHEIGHT = 1.75 * inch

# Offsets from bottom left corner of card to bottom left corner of element
URLOFFSET = (0.1 * inch, 1.5 * inch)
SERIALOFFSET = (0.1 * inch, 1.0 * inch)

QROFFSET = (1.5 * inch, 0.10 * inch)

# Size of the QR codes on each page
QRSIZE = 1.2 * inch

# Size of the page
PAGESIZE = landscape(letter)

# URL to print on each card
URL = "www.testsite.com/phototest"

# Set of characters from which to generate serial numbers
SERIALCHARS = "123456789QRXTV"

# Length of each serial number
SERIALLEN = 5

####
## Generated Parameters
###

CARDSWIDE = int(PAGESIZE[0] / CARDWIDTH)
CARDSHIGH = int(PAGESIZE[1] / CARDHEIGHT)
MARGINX = (PAGESIZE[0] - CARDSWIDE * CARDWIDTH) / 2
MARGINY = (PAGESIZE[1] - CARDSHIGH * CARDHEIGHT) / 2
PERPAGE = CARDSWIDE * CARDSHIGH

# Gives the (x, y, width, height) of a card at (x, y)
def card(x, y):
    return (MARGINX + x * (PAGESIZE[0] - MARGINX * 2) / CARDSWIDE 
            + (CARDWIDTH - CARDSAFEWIDTH) / 2,
            MARGINY + y * (PAGESIZE[1] - MARGINY * 2) / CARDSHIGH
            + (CARDHEIGHT - CARDSAFEHEIGHT) / 2,
            CARDSAFEWIDTH,
            CARDSAFEHEIGHT)

#####
## Execution begins here
####

if(len(sys.argv) != 3):
    print "Usage: gencards.py <number of cards> <output file>"
    sys.exit(1)

numcards = int(sys.argv[1])
numpages = int(math.ceil(float(numcards) / PERPAGE))
serials = [""]

random.seed(time.clock())

pdf = Canvas(sys.argv[2], pagesize = PAGESIZE)

for page in range(0, numpages):
    if PRINTGRID:
        # Drawing vertical lines
        for i in range(0, CARDSWIDE + 1):
            pdf.line(MARGINX + i * (PAGESIZE[0] - MARGINX * 2) / CARDSWIDE,
                     MARGINY,
                     MARGINX + i * (PAGESIZE[0] - MARGINX * 2) / CARDSWIDE,
                     PAGESIZE[1] - MARGINY)
            
        # Drawing horizontal lines
        for i in range(0, CARDSHIGH + 1):
            pdf.line(MARGINX,
                     MARGINY + i * (PAGESIZE[1] - MARGINY * 2) / CARDSHIGH,
                     PAGESIZE[0] - MARGINX,
                     MARGINY + i * (PAGESIZE[1] - MARGINY * 2) / CARDSHIGH)
            
    # Generating a serial for each card
    for x in range(0, CARDSWIDE):
        for y in range(0, CARDSHIGH):
            
            # Generating the serial
            serial = ""
            while(serials.count(serial) != 0):
                serial = ""
                for i in range(0, SERIALLEN):
                    serial += SERIALCHARS[random.randint(0, 
                                                         len(SERIALCHARS) - 1)]
            serials.append(serial);

            # Writing text
            coords = card(x, y)

            pdf.setFont("Helvetica", URLSIZE)
            px = coords[0] + URLOFFSET[0]
            py = coords[1] + URLOFFSET[1]
            pdf.drawString(px, py, URL)

            pdf.setFont("Helvetica", SERIALSIZE)
            px = coords[0] + SERIALOFFSET[0]
            py = coords[1] + SERIALOFFSET[1]
            pdf.drawString(px, py, serial)

            # Generating and writing the QR code
            os.system("qrencode -o .tempqr.png -s 30 -m 0 -l H " + serial)
            
            px = coords[0] + QROFFSET[0];
            py = coords[1] + QROFFSET[1]
            pdf.drawInlineImage(".tempqr.png", px, py,
                                width=QRSIZE, height=QRSIZE)

            os.remove(".tempqr.png")

    # Closing the page
    pdf.showPage()

pdf.save()
                 
