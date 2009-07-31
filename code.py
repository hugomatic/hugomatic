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
import paths

def z_cut_compiler(zdepth, cut, zsurf= 0.0, first_cut = 0.0, last_cut = 0.0):
       
    if cut <=  0.0:   
       msg = "Wrong cut: '" + str(cut) + "'. Cut must be >= 0.0"
       raise UtilsError(msg) 
     
    cuts=[]
    z = zsurf
    z = z - cut
            
    while z > zdepth:
        if z < zdepth:
            z = zDepth
        cuts.append(z)
        z = z -cut
    
    if len(cuts) == 0:
        cuts.append(zdepth)
    if cuts[-1] > zdepth:
        cuts.append(zdepth)
    
    if first_cut > 0:
        zfirst = zsurf - first_cut
        if cuts[0] < zfirst:
            cuts.insert(0,zInit)
    if last_cut > 0:
        zlast = zdepth + last_cut
        if cuts[-1] < zFinish:
            cuts.insert(-1, zlast)     
    return tuple(cuts)



class HelicalHole(object):
    def __init__(self, xPos, yPos, dia,  depth, safetyHeight, depthPerCircle, tooldia):
        rad = 0.5 * (dia - tooldia)
        x1 = xPos + rad
        self.dict = {"xPos": xPos, 
                     "diameter":dia, 
                     "yPos":yPos, 
                     "x1" : x1,
                     "rad": rad,
                     "safetyHeight":safetyHeight, 
                     "depth" : depth, 
                     "depthPerCircle" : depthPerCircle, 
                     "toolDia":tooldia}
        
        self.head = """
  (helical hole milling, load tool and set feed first, then use like so:)
  (x pos = %(xPos).4f) 
  (y pos = %(yPos).4f) 
  (safety height = %(safetyHeight).4f the tool height upon approach)
  (hole depth = %(depth).4f)
  (hole dia = %(diameter).4f)
  (tool dia = %(toolDia).4f tool dia)
g0 z%(safetyHeight).4f (safety height = %(safetyHeight).4f)
(start for entry to the ccw arcs)
g0 x%(x1).4f y%(yPos).4f 

""" % self.dict
        
        self.loop = ""
        currentDepth = safetyHeight - depthPerCircle
        while currentDepth > depth :
            #print "currentDepth " + str(currentDepth) + " depth: " + str(depth)
            arc = "g3 x%(x1).4f y%(yPos).4f i-%(rad).4f j0" % self.dict
            self.loop += arc + "z%.3f\n" %(currentDepth)
            currentDepth = currentDepth -depthPerCircle 
        
        self.foot = """
        
(down to the actual depth)
g3 x%(x1).4f y%(yPos).4f i-%(rad).4f j0 z%(depth).4f
(full circle at the actual depth)
g3 x%(x1).4f y%(yPos).4f i-%(rad).4f j0
g0 x%(xPos).4f y%(yPos).4f 
g0 z%(safetyHeight).4f

""" % self.dict
        template = self.head + self.loop + self.foot
        print template

    
class HelicalHoleComp(object):

    def __init__(self, xPos, yPos, dia,  depth, zsafe, depth_per_circle, tooldia, zsurface):
        self.dict = {"xPos": xPos, 
                     "diameter":dia, 
                     "yPos":yPos, 
                     "safetyHeight":zsafe, 
                     "depth" : depth, "depthPerCircle" : depth_per_circle, 
                     "toolDia":tooldia,
                     "zsurface":zsurface}
        
        self.head = """
  (helical hole milling, load tool and set feed first, then use like so:)
  (x pos = %(xPos).4f) 
  (y pos = %(yPos).4f) 
  (safety height = %(safetyHeight).4f the tool height upon approach)
  (hole depth = %(depth).4f)
  (hole dia = %(diameter).4f)
  (tool dia = %(toolDia).4f tool dia doesn't have to be specified exactly.)
g0 z%(safetyHeight).4f (safety height = %(safetyHeight).4f)
(start above and right so we make a convex corner for entry to the ccw arcs)
g0 x[%(xPos).4f + %(toolDia).4f] y[%(yPos).4f + [%(diameter).4f / 2]] 
g41 g0 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]]
g0 z%(zsurface).4f
""" % self.dict
        
        self.loop = ""
        currentDepth = zsurface- depth_per_circle
        while currentDepth > depth :
            #print "currentDepth " + str(currentDepth) + " depth: " + str(depth)
            arc = "g3 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]] i0 j[0 - [%(diameter).4f / 2]] " % self.dict
            self.loop += arc + "z%.3f\n" %(currentDepth)
            currentDepth = currentDepth - depth_per_circle 
        
        self.foot = """
        
(down to the actual depth)
g3 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]] i0 j[0 - [%(diameter).4f / 2]] z%(depth).4f
(full circle at the actual depth)
g3 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]] i0 j[0 - [%(diameter).4f / 2]]
g0 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]] z%(safetyHeight).4f

g40 (tool compensation)

""" % self.dict
        template = self.head + self.loop + self.foot
        print template
def header_mm(feed):
    header("mm",feed)

def header_inch(feed):
    header("Inches",feed)

def header(units, feed):
    if units not in ['Inches','mm']:
        raise Exception(units + " is not a valid unit")
    ffeed = float(feed)
    if units == 'Inches':
        print """
    
G20   (G20 set inch mode)
F%.3f  (Feed rate in inches/min)

""" %(ffeed)
    else:
        print """
    
G21   (G21 set mm mode)
F%.3f  (Feed rate in mm/min)

""" %(ffeed)           
            
def footer():
    print "M2"

# used for engraving
#def circle(x,y,dia, safety, zCut): 
#    print ""
#    print "(circle)"
#    print "g0 x%.4f y%.4f z%.4f" %(x,y+dia/2,safety)
#    print "g01 z%.4f" %(zCut)
#    print "g3 x%.4f y%.4f i0 j[0 - [%.4f / 2]]" %(x,y+dia/2,dia)
#    print "g0 z%.4f" %(safety)



def _zigzag_dy(x0, y0, x1, y1, dy):
            y = y0
            while y > y1:
                print "g01 Y%.4f (*)" % y
                print "g01 X%.4f" % x1
                y += dy
                if y < y1:
                    y = y1
                print "g01 Y%.4f" % y
                print "g01 X%.4f" % x0
                y += dy
                if y < y1:
                    y = y1    
    
class _PocketRectangle(object):
    
    def __init__(self, x0, y0, x1, y1, zsafe, zsurf,  tooldia, cuts):
        # find top left (x0, y0) and bottom right (x1, y1)
        if x1 < x0:
            self.x0 = float(x1)     
            self.x1 = float(x0)
        else:    
            self.x0 = float(x0)
            self.x1 = float(x1)
        
        if y1 > y0:
            self.y0 = float(y1)
            self.y1 = float(y0)
        else:
            self.y0 = float(y0)
            self.y1 = float(y1)
   
        self.zsafe = zsafe * 1.0
        self.zsurf = zsurf * 1.0
        self.toolRad = tooldia * 0.5
        self.z = zsurf * 1.0
        self.x0inside = self.x0 + self.toolRad
        self.y0inside = self.y0 - self.toolRad
        self.x1inside = self.x1 - self.toolRad
        self.y1inside = self.y1 + self.toolRad
        
        print ""
        print "(rectangular pocket)"
        print "(top left  [%.4f, %.4f])" % (self.x0, self.y0)
        print "(bottom right [%.4f, %.4f])" % (self.x1, self.y1)
        print "G00 Z%.4f" % self.zsafe  
        print "G00 X%.4f Y%.4f (x0 y0 with tool comp)" % (self.x0inside, self.y0inside)

        self.__approach()
        for z in cuts:
            self.z = z
            self.__mill()
        print "g00 Z%.4f" % (self.zsafe)
        
    def __approach(self):
        print "g00 Z%.4f" % self.zsurf
    
    def __mill(self):     
        zigzagWidth = self.toolRad * 1.2 #1.25
        if self.y0inside - self.y1inside > zigzagWidth: 
            x0z = self.x0inside + self.toolRad
            x1z = self.x1inside - self.toolRad
            if x0z < x1z:
                y0z = self.y0inside - self.toolRad
                y1z = self.y1inside + self.toolRad
                print "g01 X%.4f Y%.4f z%.4f" % (x0z, y0z, self.z)
                _zigzag_dy(x0z, y0z, x1z, y1z, - zigzagWidth) 
                print "g00 x%.4f y%.4f" % (x0z, y0z)
                print "g01 x%.4f y%.4f" % (self.x0inside, self.y0inside)            
            else:
                print "g01 z%.4f" % (self.z)
        else:
            print "g01 z%.4f" % (self.z)       
        print "(rectangle to complete slice)"    
        self.__rectangle(self.x0inside, self.y0inside, self.x1inside , self.y1inside)
       
    def __rectangle(self, x0, y0, x1, y1): 
        print "g01 x%.4f " % (x1)
        print "g01 y%.4f " % (y1)
        print "g01 x%.4f " % (x0)
        print "g01 y%.4f " % (y0)
            

def pocketRectangle(x0, y0, x1, y1, zsafe, zsurf,  tooldia, cuts):
    _PocketRectangle( x0, y0, x1, y1, zsafe, zsurf,  tooldia, cuts)
    


    

#def cylinder(x, y, insideDia, outsideDia, toolDia, safeZ, cuts):
#     
#    def slice(z):
#        
#        def circle(x, y, z, rad, first):
#            x0 = x + rad
#            print "G1 x%.4f y%.4f" % (x0, y)
#            if first == True:
#                print "G1 z%.4f" % z
#            print "G3 x%.4f y%.4f i%.4f j0" % (x0, y, -rad)    
#        
#        print
#        print "(Cylinder)"
#        print "(", "x: ", x, " y: ", y, ")"
#        print "(", "inside dia : ", insideDia, " outside dia: ", outsideDia, ")"
#        print "(", "depth: ", cuts[-1], " safeZ: ", safeZ, ")"
#        print "(", "toolDia: ", toolDia, ")"
#        
#        radMin = 0.5 * (insideDia + toolDia)
#        radMax = 0.5 * (outsideDia - toolDia)
#        
#        toolPathWidth = 0.5 * toolDia      
#        
#        rads = []
#        rad = radMin
#        while rad < radMax:
#            rads.append(rad)
#            rad += toolPathWidth
#        if len(rads) == 0: # happens if radMin == radmax
#            rads.append(radMax)
#        if rads[-1] < radMax:
#            rads.append(radMax)
#            
#        print "G0 x%.4f y%.4f" % (x+rads[0], y)
#        first = True
#        for r in rads:
#            circle(x,y, z, r, first)
#            first = False
#        
#       
#    print "G0 z%.4f" % safeZ  
#    for z in cuts:    
#        slice(z)    
#    print "G0 x%.4f y%.4f" % (x, y)
#    print "G0 z%.4f" % safeZ   
        
def cylinder(x, y, outsidedia, tooldia, zsafe, cuts):
    pie_segment(0., 360., x, y, 0., outsidedia, tooldia, zsafe, cuts)

def pie_segment(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, insideDia, outsideDia, tooldia, safeZ, cuts):
    import math
    def arc(x,y, degAngleFromHorizonStart, degAngleFromHorizonEnd, radius, cutZ):
        startRad = math.radians(degAngleFromHorizonStart)        
        startCos = math.cos(startRad)
        startSin = math.sin(startRad)
        startX = x + radius * startCos 
        startY = y + radius * startSin
        endRad = math.radians(degAngleFromHorizonEnd)        
        endCos = math.cos(endRad)        
        endSin = math.sin(endRad)
        endX = x + radius * endCos 
        endY = y + radius * endSin
        i = x - startX
        j = y - startY
        
         
        print "(arc clockwise from %.4f to %.4f deg)" % (degAngleFromHorizonStart, degAngleFromHorizonEnd)
        print "(  radius %.4f, center [%.4f, %.4f]  )" % (radius, x,y)
        print "(  angles [%.4f, %.4f])" % (degAngleFromHorizonStart, degAngleFromHorizonEnd)
        
        return (startX, startY, endX, endY, i, j, "g2")
        
        print "G0 X%.4f y%.4f" % (startX, startY)
        print "G1 z%.4f" % (cutZ)
        print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
    
    rad = insideDia * 0.5
    if rad <= tooldia * 0.75:
        rad = tooldia * 0.75
    
    rads = [rad]
    while rad < outsideDia * 0.5:
        rad += tooldia * 0.75
        rads.append(rad)
    if rads[-1] > outsideDia * 0.5:
        rads[-1] = outsideDia * 0.5
    
    for cutZ in cuts:
        for rad in rads:
            (startX, startY, endX, endY, i, j, cmd) = arc(x, y, degAngleFromHorizonStart, degAngleFromHorizonEnd, rad, cutZ)
            print "G0 X%.4f y%.4f" % (startX, startY)
            print "G1 z%.4f" % (cutZ)
            print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
            print "G0z%.4f" % (safeZ)


def pie_segment_tool_comp(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, insideDia, outsideDia, tooldia, safeZ, cuts):
    import math
    def arc(x,y, degAngleFromHorizonStart, degAngleFromHorizonEnd, radius, cutZ):
        startRad = math.radians(degAngleFromHorizonStart)        
        startCos = math.cos(startRad)
        startSin = math.sin(startRad)
        startX = x + radius * startCos 
        startY = y + radius * startSin
        endRad = math.radians(degAngleFromHorizonEnd)        
        endCos = math.cos(endRad)        
        endSin = math.sin(endRad)
        endX = x + radius * endCos 
        endY = y + radius * endSin
        i = x - startX
        j = y - startY
        
         
        print "(arc clockwise from %.4f to %.4f deg)" % (degAngleFromHorizonStart, degAngleFromHorizonEnd)
        print "(  radius %.4f, center [%.4f, %.4f]  )" % (radius, x,y)
        print "(  angles [%.4f, %.4f])" % (degAngleFromHorizonStart, degAngleFromHorizonEnd)
        
        return (startX, startY, endX, endY, i, j, "g2")
        
        print "G0 X%.4f y%.4f" % (startX, startY)
        print "G1 z%.4f" % (cutZ)
        print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
    
    startRadius = (insideDia  + tooldia) * 0.5
    endRadius = (outsideDia - tooldia) * 0.5
    rad =  startRadius
    if rad <= tooldia * 0.75:
        rad = tooldia * 0.75
    
    rads = [rad]
    while rad < endRadius:
        rad += tooldia * 0.75
        rads.append(rad)
    if rads[-1] > endRadius:
        rads[-1] = endRadius
    
    for cutZ in cuts:
        for rad in rads:
            sinus = (tooldia * 0.5) / rad
            offsetAngle = math.degrees(math.asin(sinus))
            print "(offset angle is %.4f)" % offsetAngle
            startAngle = degAngleFromHorizonStart - offsetAngle
            endAngle = degAngleFromHorizonEnd + offsetAngle
            (startX, startY, endX, endY, i, j, cmd) = arc(x, y, startAngle, endAngle, rad, cutZ)
            print "G0 X%.4f y%.4f" % (startX, startY)
            print "G1 z%.4f" % (cutZ)
            print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
            print "G0z%.4f" % (safeZ)

                            
def stock(stockX0, stockY0,  stockDx, stockDy, stockZ0, stockZ1):
    def blankRect(x0, y0, x1, y1, z):
        print "g0 z%.4f" %(z)
        print "G0 x%.4f y%.4f" % (x0, y0)
        print "G0 x%.4f y%.4f" % (x0, y1)
        print "G0 x%.4f y%.4f" % (x1, y1)
        print "G0 x%.4f y%.4f" % (x1, y0)
        print "G0 x%.4f y%.4f" %(x0, y0)
        #print "G0 x%.4f y%.4f " % (x0, y1 * 0.5)
        #print "G0 x%.4f" %(x1)    

    print "(blank )"
    print "M00 (don't move until the operator presses the S key)"
    stockX1 = stockX0 + stockDx
    stockY1 = stockY0 + stockDy
    blankRect(stockX0, stockY0,  stockX1, stockY1, stockZ0)
    blankRect(stockX0, stockY0,  stockX1, stockY1, stockZ1)    

class ToolChanger(object):
    def __init__(self, x0, y0, z_tool_change, zsafe):
        self.current_tool = None   
        self.x0 = x0
        self.y0 = y0
        self.zsafe = zsafe
        self.tool_changeZ = z_tool_change
        self.diameter = None
        
    def change_tool(self, diameter, toolName, tool_type='end mill'):
        
        if self.current_tool != toolName:
            print
            print "(Tool change from %s to %s)" % (self.current_tool, toolName)
            if diameter != self.diameter or tool_type != self.tool_type:
                self.diameter = diameter
                self.tool_type = tool_type
                print "g0 z%.4f" % self.zsafe 
                print "g0 x%.4f y%.4f" % (self.x0, self.y0)
                print "g0 z%.4f" % self.tool_changeZ 
                print
                print "(display a message for the operator)"
                print '(MSG,Load tool "%s" of type "%s" and diameter: %.4f then press S to continue)' % (toolName,  self.tool_type, self.diameter)
                print "M00 (don't move until the operator presses the S key)"


def circle_heli(x, y, diameter,  z, zsafe, zsurf, cut ):
    tooldia = diameter / 10.
    diameter += tooldia * 0.5
    HelicalHoleComp(x, y, diameter,  z, zsafe, cut, tooldia, zsurf)


def circle_heli_tool_outside(x, y, diameter,  z, zsafe, zsurf, tooldia, cut ):
    diameter += tooldia
    HelicalHoleComp(x, y, diameter,  z, zsafe, cut, tooldia, zsurf)

def circle_heli_tool_inside(x, y, diameter,  z, zsafe, zsurf, tooldia, cut ): 
    HelicalHoleComp(x, y, diameter,  z, zsafe, cut, tooldia, zsurf)



def rectangle(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts):
    offset = 0.
    _rectangle_offset(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts, offset)

def rectangle_tool_inside(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts): 
    offset = tooldia * 0.5
    _rectangle_offset(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts, offset)

def rectangle_tool_outside(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts): 
    offset = -tooldia * 0.5
    _rectangle_offset(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts, offset)
    
def _rectangle_offset(x0, y0, x1, y1, zsafe, zsurf, tooldia, cuts, offset):
    # order the points
    xleft = x0
    xright = x1
    if x1 < x0:
        xleft = x1
        xright = x0
    ybottom = y0
    ytop = y1
    if y1 < y0:
        ytop = y0
        ybottom = y1
    
    bottom_left = (xleft + offset, ybottom + offset)
    top_right   = (xright - offset, ytop - offset)
    top_left    = (bottom_left[0], top_right[1])
    bottom_right= (top_right[0], bottom_left[1])
    
    dx = top_right[0] - top_left[0]
    dy = top_right[1] - bottom_right[1]
    print
    print "(rectangle with offset %.4f)" % offset
    print "(dx %.5f)" % dx
    print "(dy %.5f)" % dy
    closed_curve_points = [bottom_left, top_left, top_right, bottom_right, bottom_left]
    paths.staircase(closed_curve_points, cuts, zsafe, zsurf)
    #hugomatic.code.pocketRectangle(x0, y0, x1, y1, zsafe, zsurf,  tooldia, cuts)
    

   
class _RoundRectOffset(object):
    
    def __init__(self, x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts, offset):
        # find bottom left (x0, y0) and top right (x1, y1)
        if x1 < x0:
            self.x0 = float(x1)     
            self.x1 = float(x0)
        else:    
            self.x0 = float(x0)
            self.x1 = float(x1)
        
        if y1 < y0:
            self.y0 = float(y1)
            self.y1 = float(y0)
        else:
            self.y0 = float(y0)
            self.y1 = float(y1)
        
        self.offset = offset 
            
        self.zsafe = zsafe
        self.zsurf = zsurf
        self.toolRad = tooldia * 0.5
        self.x0toolpath = self.x0 - offset
        self.y0toolpath = self.y0 - offset
        self.x1toolpath = self.x1 + offset
        self.y1toolpath = self.y1 + offset
        self.radius = radius
        self.radius_toolpath = self.radius + offset
           
        #ij = self.toolRad + self.radius
        ij = self.radius_toolpath
        #self.A = (self.x0toolpath + self.radius , self.y0toolpath - self.toolRad)
        self.A = (self.x0toolpath + self.radius_toolpath , self.y0toolpath)
        #self.B = (self.x0toolpath - self.toolRad , self.y0toolpath + self.radius, 0., ij)
        self.B = (self.x0toolpath , self.y0toolpath + self.radius_toolpath, 0., ij)
        self.C = (self.B[0] ,self.y1toolpath - self.radius_toolpath)
        #self.D = (self.A[0] , self.y1toolpath + self.toolRad, ij, 0.)
        self.D = (self.A[0] , self.y1toolpath, ij, 0.)
        self.E = (self.x1toolpath - self.radius_toolpath,  self.D[1])
        
        #self.F = (self.x1toolpath + self.toolRad, self.C[1], 0., -ij)
        self.F = (self.x1toolpath, self.C[1], 0., -ij)
        self.G = (self.F[0], self.B[1])
        
        self.H = (self.E[0], self.A[1], -ij, 0.)
        
        
        print ""
        print "(RoundRectOffset... round rectangle with tool offset)"
        print "(bottom left  [%.4f, %.4f])" % (self.x0, self.y0)
        print "(top right [%.4f, %.4f])" % (self.x1, self.y1)
        print "(offset %.4f)" % offset
        print "G00 Z%.4f" % self.zsafe  
        print "G00 X%.4f Y%.4f (A)" % self.A 
       
        # get in position
        self.__approach()
        
        for z in cuts:
            self.__mill(z)
            
        print "g00 Z%.4f" % (self.zsafe)
        
    def __approach(self):
        print "g00 Z%.4f" % self.zsurf
    
    def __mill(self, z): 
        print ("(new slice)")
        print ("g01 z%.4f" % z)
        print "(bottom left corner)"
        print ("g02 x%.4f y%.4f i%.4f j%.4f (B/H)" % self.B)
        print ("g01 x%.4f y%.4f (C/H)" % self.C)
        print "(top left corner)"
        print ("g02 x%.4f y%.4f i%.4f j%.4f (D/H)" % self.D)
        print ("g01 x%.4f y%.4f (E/H)" % self.E)
        print "(top right corner)"
        print ("g02 x%.4f y%.4f i%.4f j%.4f (F/H)" % self.F)
        print ("g01 x%.4f y%.4f" % self.G)
        print "(bottom right corner)"
        print ("g02 x%.4f y%.4f i%.4f j%.4f (H/H)" % self.H)
        print ("g01 x%.4f y%.4f (A/H)" % self.A)
        
def round_rectangle(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts):   
    """
    Rectangle with round corners. the tool path is on the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts, 0.)

def round_rectangle_tool_inside(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts):
    """
    Rectangle with round corners. the tool is inside of the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts, -0.5 * tooldia)

def round_rectangle_tool_outside(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts):
    """
    Rectangle with round corners. the tool is outside of the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, zsafe, zsurf,  tooldia, cuts, 0.5 * tooldia)
    
      
#def slotCut(wheelThicknessX, slotWidthY, tooldia, depth, cut):
#    slot = "\n"
#    slot += "(tool dia: %.4f)" % (tooldia)
#    
#    endZ = -depth
#    z = -cut
#    finished = False
#    while finished == False:
#        slot += _slotCutXy(wheelThicknessX, slotWidthY, tooldia, z)
#        if z <= endZ:
#            finished = True             
#        z -= cut
#        if z < endZ:
#            z = endZ
#
#    print slot
#    
#def _slotCutXy(wheelThicknessX, slotWidthY, tooldia, z):
#    
#    slot = ""
#    startX = 0
#    endY = (slotWidthY - tooldia) * 0.5
#    startY = -endY
#    slot += "(start Y %.4f end y %.4f)\n" %(startY, endY)
#    dy = tooldia * 0.75
#    slot +=  "(max dy %.4f)\n" %(dy)
#    slot +=  "g0 x0 y%.4f (move to start position)\n" %(startY)
#    slot +=  "g01 z%.4f (plunge)\n" % (z)
#    y = startY
#    forward = True # true when going towards +X
#    finished = False
#    while finished == False:
#        slot += "g01 y%.4f\n" % (y)
#        x = 0
#        if forward:
#            x = wheelThicknessX
#        slot += "g01 x%.4f\n" % (x)
#        forward = not forward
#
#        if y >= endY:
#            finished = True             
#        y += dy
#        if y > endY:
#            y = endY
#        
#    slot += "g0 x0\n" 
#    slot += "g0 y0\n"
#     
#    return slot

# used for engraving
#def rectangle(x, y, dx, dy, safety, zCut): 
#    print ""
#    print "(rectangle)"
#    print "g0 z%.4f" % (safety)
#    print "g0 x%.4f y%.4f" %(x,y)
#    print "g01 z%.4f" %(zCut)
#    print "g01 x%.4f " % (x + dx)
#    print "g01 y%.4f " % (y + dy)
#    print "g01 x%.4f " % (x)
#    print "g01 y%.4f " % (y)
#    print "g0 z%.4f" %(safety)

#class HorixontalSlotWithRoundCorners(object):
#    def __init__(self, safetyHeight, radius, xLength, depth, cut):
#        self.dict = {"safetyHeight": safetyHeight, 
#                 "depth":depth, 
#                 "radius" : radius, 
#                 "xLength" : xLength,
#                
# "cut":cut
#                 
#                 }
#        self.head = """
#  (round rectangle)
#  (safety height = %(safetyHeight).4f the tool height upon approach)
#  (hole depth = %(depth).4f)
#  (cut depth = %(cut).4f)
#  (radius = %(radius).4f)
#  (box length = %(xLength).4f)
#G00 X0 Y[0-%(radius).4f] Z%(safetyHeight).4f    (bottom left)
#""" % self.dict
#        self.loop = ""
#        
#        currentDepth = safetyHeight - cut
#        while currentDepth > depth :
#            
#            self.loop += "G01 Z%.4f  (plunge)" % currentDepth
#            self.loop += """    
#G01 X[0-%(radius).4f/2] Y[0-%(radius).4f] (-)
#G02 X[0-%(radius).4f] Y[0-%(radius).4f/2] I0 J[%(radius).4f/2]  (\)
#G01 Y[%(radius).4f/2] (|)
#G02 X[0-%(radius).4f/2] Y[%(radius).4f] I[%(radius).4f/2] J0 (/)
#G01 X[%(radius).4f/2 + 2* %(xLength).4f] (-)
#G02 X[%(radius).4f+ 2* %(xLength).4f] Y[%(radius).4f/2] I[0] J[0-%(radius).4f/2](\)
#G01 Y[0-%(radius).4f/2] (|)
#G02 X[%(radius).4f/2 + 2* %(xLength).4f] Y[0-%(radius).4f] I[0-%(radius).4f/2] J0
#G01 X0 
#G01 Z0 (surface)
#"""  % self.dict
#            currentDepth = currentDepth -cut
#        self.foot = ""
#        template = self.head + self.loop + self.foot
#        print template
#        
#
#    def __str__(self):
#        # return "(Hello %(name).4f! d = %(depth).4f n=%(name).4f)" % self.dict
#        template = self.head + self.loop + self.foot
#        return template 

#def drill_hole(x, y, dia, z, zsafe, zsurf):
#    print
#    print "(drill hole [%4.f, %.4f, %.4f] diameter = )" % (x,y,z)
#    print "g0 Z%.4f" % zsafe
#    print "g0 x%.4f y%.4f" % (x,y)
#    print "g0 z%.4f" % zsurf
#   

#def screwCap1032(xPos, yPos, zsafe, cut, tooldia):
#    dia = 0.31 + 0.07     
#    zDepth = -0.22 
#    print ""
#    print "\n(%.4f %.4f)" % (xPos, yPos)
#    helicalHole(xPos, yPos, dia,  zDepth, zsafe, cut, tooldia)
#

       