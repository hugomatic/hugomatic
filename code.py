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

def z_cut_compiler(z_depth, cut, z_surf= 0.0, first_cut = 0.0, last_cut = 0.0):
       
    if cut <=  0.0:   
       msg = "Wrong cut: '" + str(cut) + "'. Cut must be >= 0.0"
       raise UtilsError(msg) 
     
    cuts=[]
    z = z_surf
    z = z - cut
            
    while z > z_depth:
        if z < z_depth:
            z = z_depth
        cuts.append(z)
        z = z -cut
    
    if len(cuts) == 0:
        cuts.append(z_depth)
    if cuts[-1] > z_depth:
        cuts.append(z_depth)
    
    if first_cut > 0:
        zfirst = z_surf - first_cut
        if cuts[0] < zfirst:
            cuts.insert(0,zInit)
    if last_cut > 0:
        zlast = z_depth + last_cut
        if cuts[-1] < zFinish:
            cuts.insert(-1, zlast)     
    return tuple(cuts)



class HelicalHole(object):
                #      (x, y, diameter,  z, z_safe, z_rapid, cut )
    def __init__(self, xPos, yPos, dia,  safetyHeight, z_rapid, cuts):
        rad = dia * 0.5 # circle radius
        x1 = xPos + rad
        self.dict = {"xPos": xPos, 
                     "diameter":dia, 
                     "yPos":yPos,
                     "safetyHeight":safetyHeight, 
                     "x1" : x1,
                     "rad":rad,
                     "z_rapid":z_rapid}
        
        self.head = """
  (helical hole milling, load tool and set feed first, then use like so:)
  (x pos = %(xPos).4f) 
  (y pos = %(yPos).4f) 
  (safe  z = %(safetyHeight).4f the tool height upon approach)
  (rapid plane = %(z_rapid).4f height where movement starts)
  (hole dia = %(diameter).4f)
g0 z%(safetyHeight).4f (safety height = %(safetyHeight).4f)
(start for entry to the ccw arcs)
g0 x%(x1).4f y%(yPos).4f 
g0 Z%(z_rapid).4f
""" % self.dict
        
        self.loop = ""
        for z in cuts:
            currentDepth = z
            arc = "g3 x%(x1).4f y%(yPos).4f i[-1.0 * %(rad).4f] j0" % self.dict
            self.loop += arc + " z%.3f\n" %(currentDepth)
        self.foot = """
        
(full circle at the actual depth)
g3 x%(x1).4f y%(yPos).4f i[-1.0 * %(rad).4f] j0
 
g0 z%(safetyHeight).4f

""" % self.dict
        template = self.head + self.loop + self.foot
        print template

    
class HelicalHoleComp(object):

    def __init__(self, xPos, yPos, dia,  depth, z_safe, depth_per_circle, tool_dia, z_surface):
        self.dict = {"xPos": xPos, 
                     "diameter":dia, 
                     "yPos":yPos, 
                     "safetyHeight":z_safe, 
                     "depth" : depth, "depthPerCircle" : depth_per_circle, 
                     "tool_dia":tool_dia,
                     "z_surface":z_surface}
        
        self.head = """
  (helical hole milling, load tool and set feed first, then use like so:)
  (x pos = %(xPos).4f) 
  (y pos = %(yPos).4f) 
  (safety height = %(safetyHeight).4f the tool height upon approach)
  (hole depth = %(depth).4f)
  (hole dia = %(diameter).4f)
  (tool dia = %(tool_dia).4f tool dia doesn't have to be specified exactly.)
g0 z%(safetyHeight).4f (safety height = %(safetyHeight).4f)
(start above and right so we make a convex corner for entry to the ccw arcs)
g0 x[%(xPos).4f + %(tool_dia).4f] y[%(yPos).4f + [%(diameter).4f / 2]] 
g41 g0 x%(xPos).4f y[%(yPos).4f + [%(diameter).4f / 2]]
g0 z%(z_surface).4f
""" % self.dict
        
        self.loop = ""
        currentDepth = z_surface- depth_per_circle
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
    
    def __init__(self, x0, y0, x1, y1, z_safe, z_rapid,  tool_dia, cuts):
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
   
        self.z_safe = z_safe * 1.0
        self.z_rapid = z_rapid * 1.0
        self.toolRad = tool_dia * 0.5
        self.z = z_rapid * 1.0
        self.x0inside = self.x0 + self.toolRad
        self.y0inside = self.y0 - self.toolRad
        self.x1inside = self.x1 - self.toolRad
        self.y1inside = self.y1 + self.toolRad
        
        print ""
        print "(rectangular pocket)"
        print "(top left  [%.4f, %.4f])" % (self.x0, self.y0)
        print "(bottom right [%.4f, %.4f])" % (self.x1, self.y1)
        print "G00 Z%.4f" % self.z_safe  
        print "G00 X%.4f Y%.4f (x0 y0 with tool comp)" % (self.x0inside, self.y0inside)

        self.__approach()
        for z in cuts:
            self.z = z
            self.__mill()
        self.__retract()
        
    def __retract(self):
        print "g00 Z%.4f" % (self.z_safe)
        
    def __approach(self):
        print "g00 Z%.4f" % self.z_rapid
    
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
            
def pocket_rectangle(x0, y0, x1, y1, z_safe, z_rapid,  tool_dia, cuts):
    _PocketRectangle( x0, y0, x1, y1, z_safe, z_rapid,  tool_dia, cuts)
    
def cylinder(x, y, outsidedia, tool_dia, z_safe, z_rapid, cuts):
    pie_segment(0., 360., x, y, 0., outsidedia, tool_dia, z_safe, z_rapid, cuts)

def pie_segment(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, inside_dia, outside_dia, tool_dia, safe_z, rapid_z, cuts):
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
        print "G1 z%.4f" % (z_rapid)
        print "G1 z%.4f" % (cutZ)
        print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
    
    rad = inside_dia * 0.5
    if rad <= tool_dia * 0.75:
        rad = tool_dia * 0.75
    
    rads = [rad]
    while rad < outside_dia * 0.5:
        rad += tool_dia * 0.75
        rads.append(rad)
    if rads[-1] > outside_dia * 0.5:
        rads[-1] = outside_dia * 0.5
    
    for cutZ in cuts:
        for rad in rads:
            (startX, startY, endX, endY, i, j, cmd) = arc(x, y, degAngleFromHorizonStart, degAngleFromHorizonEnd, rad, cutZ)
            print "G0 X%.4f y%.4f" % (startX, startY)
            print "G1 z%.4f" % (cutZ)
            print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
            print "G0z%.4f" % (safe_z)


def pie_segment_tool_comp(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, insideDia, outsideDia, tool_dia, safeZ, cuts):
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
    
    startRadius = (insideDia  + tool_dia) * 0.5
    endRadius = (outsideDia - tool_dia) * 0.5
    rad =  startRadius
    if rad <= tool_dia * 0.75:
        rad = tool_dia * 0.75
    
    rads = [rad]
    while rad < endRadius:
        rad += tool_dia * 0.75
        rads.append(rad)
    if rads[-1] > endRadius:
        rads[-1] = endRadius
    
    for cutZ in cuts:
        for rad in rads:
            sinus = (tool_dia * 0.5) / rad
            offsetAngle = math.degrees(math.asin(sinus))
            print "(offset angle is %.4f)" % offsetAngle
            startAngle = degAngleFromHorizonStart - offsetAngle
            endAngle = degAngleFromHorizonEnd + offsetAngle
            (startX, startY, endX, endY, i, j, cmd) = arc(x, y, startAngle, endAngle, rad, cutZ)
            print "G0 X%.4f y%.4f" % (startX, startY)
            print "G1 z%.4f" % (cutZ)
            print "G2 x%.4f y%.4f i%.4f j%.4f" % (endX, endY, i, j)
            print "G0z%.4f" % (safeZ)

                            
#def stock(stockX0, stockY0,  stockDx, stockDy, stockZ0, stockZ1):
def stock(x0, y0,  dx, dy, z0, z1):
    
    def blankRect(x0, y0, x1, y1, z):
        print "g0 z%.4f" %(z)
        print "G0 x%.4f y%.4f" % (x0, y0)
        print "G0 x%.4f y%.4f" % (x0, y1)
        print "G0 x%.4f y%.4f" % (x1, y1)
        print "G0 x%.4f y%.4f" % (x1, y0)
        print "G0 x%.4f y%.4f" %(x0, y0)
  
    dz = z1-z0
    print "(blank)"
    print "(hugomatic['stock_x0']= %.4f)" % (x0)
    print "(hugomatic['stock_y0']= %.4f)" % (y0)
    print "(hugomatic['stock_h'] = %.4f)" % (dy)
    print "(hugomatic['stock_w'] = %.4f)" % (dx)
    print "(hugomatic['stock_dz'] = %.4f)" % (dz)

    print "M00 (don't move until the operator presses the S key)"
    x1 = x0 + dx
    y1 = y0 + dy
    blankRect(x0, y0,  x1, y1, z0)
    blankRect(x0, y0,  x1, y1, z1)   
    
    
     

class ToolChanger(object):
    def __init__(self, x0, y0, z_tool_change, z_safe):
        self.current_tool = None   
        self.x0 = x0
        self.y0 = y0
        self.z_safe = z_safe
        self.tool_changeZ = z_tool_change
        self.diameter = None
        
    def change_tool(self, diameter, toolName, tool_type='end mill'):
        
        if self.current_tool != toolName:
            print
            print "(Tool change from %s to %s)" % (self.current_tool, toolName)
            if diameter != self.diameter or tool_type != self.tool_type:
                self.diameter = diameter
                self.tool_type = tool_type
                print "g0 z%.4f" % self.z_safe 
                print "g0 x%.4f y%.4f" % (self.x0, self.y0)
                print "g0 z%.4f" % self.tool_changeZ 
                print
                print "(display a message for the operator)"
                print '(MSG,Load tool "%s" of type "%s" and diameter: %.4f then press S to continue)' % (toolName,  self.tool_type, self.diameter)
                print "M00 (don't move until the operator presses the S key)"
                print "(hugomatic['tool_dia'] = %.4f)" % self.diameter 


def circle_heli(x, y, diameter, z_safe, z_rapid, cuts ):
    HelicalHole(x, y, diameter, z_safe, z_rapid, cuts )


def circle_heli_tool_outside(x, y, diameter, z_safe, z_rapid, tool_dia, cuts ):
    diameter += tool_dia
    circle_heli(x, y, diameter, z_safe, z_rapid, cuts )

def circle_heli_tool_inside(x, y, diameter, z_safe, z_rapid, tool_dia, cuts ): 
    diameter = diameter - tool_dia
    circle_heli(x, y, diameter, z_safe, z_rapid, cuts )



def rectangle(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts):
    offset = 0.
    _rectangle_offset(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts, offset)

def rectangle_tool_inside(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts): 
    offset = tool_dia * 0.5
    _rectangle_offset(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts, offset)

def rectangle_tool_outside(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts): 
    offset = -tool_dia * 0.5
    _rectangle_offset(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts, offset)
    
def _rectangle_offset(x0, y0, x1, y1, z_safe, z_rapid, tool_dia, cuts, offset):
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
    paths.staircase(closed_curve_points, cuts, z_safe, z_rapid)
    #hugomatic.code.pocketRectangle(x0, y0, x1, y1, z_safe, z_surf,  tool_dia, cuts)
    

   
class _RoundRectOffset(object):
    
    def __init__(self, x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts, offset):
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
            
        self.z_safe = z_safe
        self.z_surf = z_surf
        self.toolRad = tool_dia * 0.5
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
        print "G00 Z%.4f" % self.z_safe  
        print "G00 X%.4f Y%.4f (A)" % self.A 
       
        # get in position
        self.__approach()
        
        for z in cuts:
            self.__mill(z)
            
        print "g00 Z%.4f" % (self.z_safe)
        
    def __approach(self):
        print "g00 Z%.4f" % self.z_surf
    
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
        
def round_rectangle(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts):   
    """
    Rectangle with round corners. the tool path is on the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts, 0.)

def round_rectangle_tool_inside(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts):
    """
    Rectangle with round corners. the tool is inside of the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts, -0.5 * tool_dia)

def round_rectangle_tool_outside(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts):
    """
    Rectangle with round corners. the tool is outside of the dimension provided
    """
    _RoundRectOffset(x0, y0, x1, y1, radius, z_safe, z_surf,  tool_dia, cuts, 0.5 * tool_dia)
    
def peck_drill(x, y, z_safe, z_rapid, peck, z ):
    print "g0 Z%.4f (move tool out of the way)" % z_safe
    print "g0 x%.4f y%.4f" % (x,y)
    print "G4 p0.1 (0.1 sec Pause)"
    print "G83 x%.4f y%.4f z%.4f r%.4f q%.4f" %(x,y, z, z_rapid, peck)
    print "g0 Z%.4f (move tool out of the way)" % z_safe
    print "G4 p0.1 (0.1 sec Pause)"

def line(x0, y0, x1, y1, z_safe, z_rapid, cuts):
        points = [(x0, y0),(x1, y1)]
        paths.backAndForth(points, cuts, z_safe, z_rapid)
        print "g0 Z%.4f (move tool out of the way)" % z_safe
        
#def screwCap1032(xPos, yPos, z_safe, cut, tool_dia):
#    dia = 0.31 + 0.07     
#    zDepth = -0.22 
#    print ""
#    print "\n(%.4f %.4f)" % (xPos, yPos)
#    helicalHole(xPos, yPos, dia,  zDepth, z_safe, cut, tool_dia)
#

       
