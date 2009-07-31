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


# Exception class for program errors
class UtilsError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

def gCut(points, zsafe=None, zsurf=None, feed = None):
    if zsafe != None:
        print "g0 Z%.5f" % zsafe
        print "g0 X%.5f Y%.5f" % (points[0][0], points[0][1])
    
    if zsurf != None:
        print "g0 Z%.5f" % zsurf
    
    if feed != None:
        print "F%.5f" % feed
        
    for point in points:
        print "g01 X%.5f Y%.5f Z%.5f" % point
    
    #if zSafe != None:
    #    print "g0 Z%.5f" % zSafe
    

def backAndForth(points, cuts, zsafe, zsurf):
    xyz = []
    direction = True
    revPoints = []
    for p in points:
        revPoints.append( p )
    revPoints.reverse()
        
    for z in cuts:
        if direction:  
            for p in points:
                xyz.append( (p[0], p[1], z) )
        else:
            for p in revPoints:
                xyz.append( (p[0], p[1], z) )    
                
        direction = not direction            
    t = tuple(xyz)
    gCut(t, zsafe, zsurf)
    

def repeatCuts(points, cuts, zsafe, zsurf):
    for z in cuts:  
        xyz = []
        for p in points:
            xyz.append( (p[0], p[1], z) )
        t = tuple(xyz)
        gCut(t, zSafe, zsurf)
        # don't bother going to z safe between each cut, stay at zSurf
        zsafe = zsurf
        zsurf = None
    

def staircase(closed_curve_points, cuts, zsafe=None, zsurf=None):
    zPlungePointIndex = 0
    currentPoint = 0
    
    # Remove the last point from closed_curve_points
    # that repeats the initial point of the curve
    points = tuple(closed_curve_points[0:-1])
    count  = len(points)
    
    xyz = []
    pIx = 1
    
    for z in cuts:  
        for i in range(0,count+1):
            x = points[pIx][0]
            y = points[pIx][1]
            xyz.append((x, y, z))
            pIx += 1
            if pIx == count:
                pIx = 0
    
            
    t = tuple(xyz)   
    gCut(t, zsafe, zsurf)  
    return t
    
    
     


def selectPaths(paths, selection):
    selectedPaths = []
    for p in paths:
        if p[0] in selection:
            selectedPaths.append(p)
    return tuple(selectedPaths)  


def getPathFromName(paths, name):
    paths = selectPaths(paths, [name])
    if len(paths) == 0:
        return None
    return paths[0]


def bezierInterpolate(t, p0, p1, p2, p3):
    """
    The Bezier formula. Returns the point on the curve at the position t (t varies between 0 and 1).  
    """
    x0 = p0[0]
    x1 = p1[0]
    x2 = p2[0]
    x3 = p3[0]
    y0 = p0[1]
    y1 = p1[1]
    y2 = p2[1]
    y3 = p3[1]

    t_1 = 1.0 - t
    t_1_2 = t_1 * t_1
    t_1_3 = t_1_2 * t_1
    t2 = t * t
    t3 = t2 * t
    
    x = t_1_3 * x0  + 3 * t *  t_1_2 * x1 + 3 * t2 * t_1 * x2 + t3 * x3
    y = t_1_3 * y0 + 3 * t *  t_1_2 * y1 + 3 * t2 * t_1 * y2 + t3 * y3
    p = (x,y)
    return p

        
def getStrokesFromPath(path, xOff, yOff, scaleX, scaleY, resolution):
    
    def cubicBezier(points, p0, p1, p2, p3, res):
        """
        Interpolates between 4 control points. Returns a tuple of points. The length of 
        the tuple depends on the resolution (bigger the res, the less points you get)
        """
    
        def getStepCount(p0, p1, p2, p3, res):
            """
            Given a resolution (max line length), computes how many lines segments in the curve 
            """
            
            def getDistance(p0, p1):
                x2 = (p1[0] - p0[0]) * (p1[0] - p0[0])
                y2 = (p1[1] - p0[1]) * (p1[1] - p0[1])
                d = math.sqrt(x2 + y2)
                return d
            
            d = getDistance(p0, p1) + getDistance(p1, p2) + getDistance(p2, p3)
            step = res / d
            return step
        
        
        def interPolate(t, p0, p1, p2, p3):
            p = bezierInterpolate(t, p0, p1, p2, p3)
            return p
            
        
        # compute many line segments for this spline 
        step = getStepCount(p0, p1, p2, p3, res)
        
        t = 0.0
        p = interPolate(t, p0, p1, p2, p3)
        # first point
        points.append(p)
        
   
        # add one point for each step       
        t += step     
        while t < 1.0:
            p = interPolate(t, p0, p1, p2, p3)
            points.append(p)
            t += step 
            
        t = 1.0 
        p = interPolate(t, p0, p1, p2, p3)
        # end point
        points.append(p)
       
    def commandsToPoints(cmds):     
        points = []
        for cmd in cmds:
            if cmd[0] == 'C':
                p0 = currentPoint
                p1 = cmd[1][-3]
                p2 = cmd[1][-2]
                p3 = cmd[1][-1]
                currentPoint = p3
                cubicBezier(points, p0, p1, p2, p3, resolution)
            else:
                currentPoint = cmd[1][-1]
                points.append(currentPoint)
        return tuple(points)
            
    points = []
    cmds = path[1]
    isClosed = False
    
    if path[1][-1] == 'Z':
        isClosed = True
        # remove z command
        cmds = path[1][0:-1]

    points = []
    currentPoint = None
    
    print
    print "(path)" 
    # split path into strokes
    strokes = []
    stroke = []
    for cmd in cmds:
        if cmd[0] == 'M':
            stroke = []
            strokes.append(stroke)    
        stroke.append(cmd)
    
    strokePoints = []
    for stroke in strokes:
        points = commandsToPoints(stroke)
        if isClosed:
            points.pop()
        strokePoints.append(tuple(points))
    
    scaledStrokes = [] 
    for points in strokePoints:
        scaled = []  
        for p in points:
            x = p[0] * scaleX + xOff
            y = p[1] * scaleY + yOff
            scaled.append( (x, y) )
        scaledStrokes.append(tuple(scaled))
    return tuple(scaledStrokes), isClosed
    
def readPathsFromSvgFile(fileName, selection = None):
    """
    Opens the SVG files, grabs (only) the 'paths' elements and returns sets of points
    """
    import xml.dom.minidom
    f = open(fileName,'r')
    svgStr = f.read()
    f.close()
    dom = xml.dom.minidom.parseString(svgStr)
    pathNodes = dom.getElementsByTagName("path")
    paths = []
    for node in pathNodes:
        name = node.getAttribute('id')
        dataStr = node.getAttribute('d')
        style = node.getAttribute('style')
        #print "name: ", name, "\n data: ", data, "\n style: ", style
        data = parseCmds(dataStr)
        paths.append( (name, data, style) )
   
    allPaths =  tuple(paths)
    if selection == None:
        return allPaths
    
    return selectPaths(allPaths, selection)
            
def parseCmds(dataStr):

 def parsePoint(p):
    toks = p.split(',')
    x = float(toks[0])
    y = float(toks[1])
    return (x, y)

 toks = dataStr.split()
 cnt = 0
 it = iter(toks)
 t = tuple(it)
 cnt = len(t)
 idx=0
 cmds = []
 while idx < cnt:
    cmd = t[idx]
        
    if cmd == 'Z':
        cmds.append( (cmd,) )        

    if cmd in ('M','L'):
        p = t[idx+1]
        if not ',' in p:
            idx+=1
            p = p + "," + t[idx+1] 
        
        cmds.append( (cmd, (parsePoint(p),)) )
        idx +=1
    
    if cmd == 'C':
        idx = idx+1
        p1 = t[idx]
        if not "," in p1:
            idx+=1
            p1 = p1 + "," + t[idx] 
        idx+=1
        p2 = t[idx]
        if not ',' in p2:
            idx+=1
            p2 = p2 + "," + t[idx]
        idx+=1
        p3 = t[idx]
        if not ',' in p3:
            idx+=1
            p3 = p3 + "," + t[idx] 
        
        cmds.append( (cmd, (parsePoint(p1), parsePoint(p2), parsePoint(p3)) ) )
    idx +=1
 return tuple(cmds)


