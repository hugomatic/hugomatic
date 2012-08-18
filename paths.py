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
        gCut(t, zsafe, zsurf)
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
            cmdName = cmd[0]
            if cmdName == 'C':
                p0 = currentPoint
                p1 = cmd[1][-3]
                p2 = cmd[1][-2]
                p3 = cmd[1][-1]
                currentPoint = p3
                cubicBezier(points, p0, p1, p2, p3, resolution)
                
            elif cmdName == 'c':
                p0 = currentPoint
                rp1 = cmd[1][-3]
                rp2 = cmd[1][-2]
                rp3 = cmd[1][-1]
                
                x =0
                y =0
                if len(points) > 0:
                    x,y = points[-1]
                
                p1 = (rp1[0]+x, rp1[1]+y)
                p2 = (rp2[0]+x, rp2[1]+y)
                p3 = (rp3[0]+x, rp3[1]+y)
                    
                currentPoint = p3
                cubicBezier(points, p0, p1, p2, p3, resolution)
                    
            elif cmdName in ('L','M'):
                currentPoint = cmd[1][-1]
                points.append(currentPoint)
                
            elif cmdName in ('l','m'):
                delta = cmd[1][-1]
                x =0
                y =0
                if len(points) > 0:
                    x,y = points[-1]
                currentPoint = (x+delta[0], y+delta[1])
                points.append(currentPoint)    
                
            elif cmdName == 'V':
                distance = cmd[1][0]
                x = currentPoint[0]
                y = distance
                currentPoint = (x,y)
                points.append(currentPoint)
                            
            elif cmdName == 'v':
                distance = cmd[1][0]
                x = currentPoint[0]
                y = currentPoint[1] + distance
                currentPoint = (x,y)
                points.append(currentPoint)
                
            elif cmdName  == 'H':
                distance = cmd[1][0]
                x = distance
                y = currentPoint[1] 
                currentPoint = (x,y)
                points.append(currentPoint)     
                               
            elif cmdName  == 'h':
                distance = cmd[1][0]
                x = currentPoint[0] + distance
                y = currentPoint[1] 
                currentPoint = (x,y)
                points.append(currentPoint)

            elif cmdName in ('Z','z'):
                print "(unexpected Z command )"
                
                
            elif cmdName in ('S','s', 'Q', 'q', 'T','t', 'A', 'a'):
                print "(UNSUPPORTED SVG PATH COMMAND:", cmdName, ")"
                
            else:
                print "(UNKNOWN SVG PATH COMMAND:", cmdName, ")"         
        return  points
            
    #points = []
    cmds = path[1]
    
    
    isClosed = False
    lastCmd = path[1][-1][0]
    if len(path[1]) == 0: # no points in path
        isClosed = False
       
    elif lastCmd in ('Z','z'):
        isClosed = True

    points = []
    currentPoint = None
    
    # split path into strokes
    strokes = []
    stroke = []
    for cmd in cmds:
        # move to command... we add 
        # a new stroke instance to the list
        if cmd[0] in ('M','m'):
            stroke = []
            strokes.append(stroke)
                
        if cmd[0] not in ('Z','z'):
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
        data = getPathsFromPathNode(node)
        paths.append(data)
   
    allPaths =  tuple(paths)
    if selection == None:
        return allPaths
    
    return selectPaths(allPaths, selection)

def getPathsFromPathNode(node):
        name = node.getAttribute('id')
        dataStr = node.getAttribute('d')
        style = node.getAttribute('style')
        #print "name: ", name, "\n dataStr: ", dataStr, "\n style: ", style
        data = parseCmds(dataStr)
        return name, data, style
            

 
def parseCmds_with_repeats(data_str):
    
    cmds = []
    
    """
    the current_cmd format is: [c,[n0,n1...n]] where c is the command letter and [n0...n] is a list of numbers
    """
    def append_cmd(current_cmd):
        if current_cmd == None:
            return
        nbs = current_cmd[1]
        command = current_cmd[0]
        if command.lower() == 'c':
            i =0
            while i < len(nbs):
                cmds.append( (command, ((nbs[i], nbs[i+1]),(nbs[i+2],nbs[i+3]),(nbs[i+4],nbs[i+5]))) )
                i+=6
        if command.lower() == 'm':
            cmds.append( (command, ((nbs[0],nbs[1]), ), )  )   

        if command.lower()  == 'l':
            cmds.append( (command, ((nbs[0],nbs[1]), ), )  )   

        if command.lower()  == 'v':
            cmds.append( (command, (nbs[0],), )  )  

        if command.lower()  == 'h':
            cmds.append( (command, (nbs[0],), )  ) 
            
        if command.lower()  == 'z':
            cmds.append( (command,) )    
         
        
    toks = data_str.split()
    
    current_cmd = None
    for i,t in enumerate(toks):
        if t.lower() in ['z','c','m','l','v','h']:
            append_cmd(current_cmd)
            current_cmd = [t,[]]
        else:
            number_str = t.split(',')
            
            for s in number_str:
                n = s.strip()
                if len(n) >0:
                    nb = float(n)
                    current_cmd[1].append(nb)
    append_cmd(current_cmd)    
    return tuple(cmds)

def parseCmds(data_str):
    #cmds = parseCmds_with_repeats(data_str)
    cmds = parseCmds_with_repeats(data_str)
    return cmds

