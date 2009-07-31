#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# You will find the latest version of this code at the following address:
# http://hugomatic.ca/source/cncOnline
#
# You can contact me at the following email address:
# hugo@hugomatic.ca
#

import math

def circularCut( dia0, dia1, tooldia, zSurf, zsafe, cutPerTurn, zcuts, feed):
    
    print ""
    print ""
    print "(circularCut d0=%.4f d1=%.4f, zSurf=%.4f, zSafe=%.4f)" % (dia0, dia1, zSurf, zSafe)
    print "G0 Y0"
    x0 = 0.5 * (dia0 + toolDia)
    
    #currentAngle = a0
    for z in zcuts:
        print "G0 X%.4f" % (x0)
        #print "g0 Z%.4f" % (zSurf + 0.005) 
        print "g01 Z%.4f f%.4f" % (z, feed)
        xEnd = 0.5 * (dia1 + toolDia)
        turns = (x0 - xEnd) / cutPerTurn
                
        print "g92.1 (reset offsets)"
        print "g92 a0 (set A axis to 0)"
        currentAngle = 360.0 * turns
        
        rotSpeed = abs(feed / (dia1 * 0.5))
        linearFeed = abs(rotSpeed * 2 * math.pi / 360) 
        
        
        print "G01 x%.4f A%.4f f%.4f" % (xEnd, currentAngle,linearFeed)
        print "(One full revolution + 10 degrees at final X)"
        currentAngle += 370.0 
        
        rotSpeed = feed / (dia0 * 0.5)
        rotFeed = rotSpeed * 360 * 0.5 / math.pi 
        rotFeed = 2 * rotFeed
        print "G01 A%.4f f%.4f" % (currentAngle, rotFeed)
    
    print "G0 Z%.4f" % zSafe 
    #return currentAngle 
