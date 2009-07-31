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

inches = 'Inches'
mm = 'mm'
units = (inches, mm)

def m_to_feet(m):
    feet = m * 3.2808399
    return feet
    
def feet_to_m(feet):
    meters = feet / 3.2808399
    return meters

def inches_to_mm(inches):
    """1 inch = 25.4 millimeters"""               
    mm = inches * 25.4
    return mm

def mm_to_inches(mm):
    """1 inch = 25.4 millimeters"""               
    inches = mm / 25.4
    return inches

def inches_to_units(unit, inches):
    if unit.lower() == inches.lower():
        return inches
    return inches_to_mm(inches)

def mm_to_units(unit, mm):
    if unit.lower() == mm.lower():
        return mm
    return mm_to_inches(mm)

def sphere_volume(radius):
    """volume of a sphere:
    4/3 pi * r^3
    """
    volume = (4./3.) * math.pi * radius * radius * radius
    return volume

def circle_to_circle_distance(x1,y1, d1, x2, y2, d2):
    """
    given 2 circles (center coordinates and diameters), returns
    the shortest distance between them.
    If the number is negative, there is interference.
    
    This is usefull to see if for example a screw head is too close to 
    another hole.  
    """
    if d1 < 0.:
        raise Exception, "negative diameter specified for d1" 
    if d21 < 0.:
        raise Exception, "negative diameter specified for d2" 
    # closest point between 2 circles lies on the line between its center
    dx = x2-x1
    dy = y2-y1
    center_distance = math.sqrt(dx*dx + dy*dy)
    radius1 = d1 * 0.5
    radius2 = d2 * 0.5
    distance = center_distance - radius1 - radius2
    return distance