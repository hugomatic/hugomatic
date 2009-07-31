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

import hugomatic.code
import sys



def gear_metrics(p, N):
    
    addendum = 1.0 / p
    dedendum = 1.200 / p + 0.002
    ht = 2.20 / p + 0.002 
    D = float(N) / p 
    index = 360.0 / N
    blankD = D + 2 * addendum
    
    print "(P: ", p, ")"
    print "(teeths:", N, ")"
    print "(addendum: ", addendum, ")"
    print "(dedendum: ", dedendum, ")"
    print "(Whole depth: ", ht, ")"
    print "(Diameter: ", D, ")"
    print "(Outside diameter: ", blankD, ")"
    print "(Indexing angle, degrees:", index, ")"
    print
    return ht, blankD
    

def cut_gear(p, nbOfTeeths, xLength, cut, feed, ySafe):
    ht, d =  gear_metrics(p,nbOfTeeths)
    print
    print "(Gear cutting)"
    print "(gear P: ",p,")"
    index = 360.0 / nbOfTeeths
    print "(teeth: ",nbOfTeeths,", index degrees: ", index, ")"
    print "(Outside Diameter: ",d,")"
    print "(max cut: ",cut,")"
    print "(feed: ",feed,")"
    print "(x span: ",xLength,")"
    print "(y safe",ySafe,")"
    depth = -ht
    print "(Depth:",depth,")"
    print
 
    print "G0 Y0 X0 A0"
    
    cuts = hugomatic.code.z_cut_compiler(depth, cut)
    
    
    turns = 0
    for k in cuts:
        for i in range(0, nbOfTeeths):
            angle = i * index + 360.0 * turns
            print
            print "(tooth: ",i, " depth: ", k,")"
            print "G0 A%.4f" % angle
            print "G0 Y%.4f" % ySafe
            print "G0 X%.4f" % xLength
            print "G01 Y%.4f" % k
            print "G01 X0"
            print "G0 Y%.4f" % ySafe
        turns += 1
 

class GlobalParams (hugomatic.toolkit.Parameters):
    
    def getValues(self):
        return globals()    
    
    def getFileName(self):
        import inspect
        return inspect.getfile(GlobalParams)
  

class StdOut (hugomatic.toolkit.RedirectStdOut):
    def debugStop(self):
        a = 42



if __name__ == "__main__":
    import hugomatic.toolkit
    
    old_stdout = sys.stdout
    sys.stdout = StdOut(sys.stdout, 3784)
    
    params = GlobalParams('Gearing', 'Cut gears')
    
    N = 24
    P = 24
    xLen = 1.0
    params.addArgument('P', 'Diametral pich')
    params.addArgument('N', 'Number of teeth')
    params.addArgument('xLen', 'Length of cut along X')
    
    cut = 0.025
    feed = 20.0
    ySafe = 0.1
    params.addArgument('feed', 'Feed rate in inch/min')
    params.addArgument('cut',  'cut per pass in inch' )
    params.addArgument('ySafe', 'Safety height above blank in inch')
    
    
    params.loadParams()
    
    hugomatic.code.header_inch(feed)
    cut_gear(P,N, xLen, cut, feed, ySafe)
    hugomatic.code.footer()


