#!/usr/bin/python

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


from utils import  printHead, printBanner, printFooter, printContactNavBar


print "Content-Type: text/html"
print

printHead('About Hugomatic',('nav','about','banner','footer'), path="")
printBanner( path='')

printContactNavBar()
       

print "<h1>About Hugomatic</h1>"
print '<div id="about">' 

print """

<h2>What we do</h2>
We build Open Source platform to generate Open Physical Objects. We supply free projects for hobby CNC milling and lathes. 
We want to empower people to make professional objects simply, and want to remove the complexity of hobby robotics. 
<h3>Free designs</h3>
The designs are free, so anyone can build the objects on their own equipment.
<h3>Generated objects</h3>
Because the objects are created from a generator program, rather than drawings for example, they can be customized and personalized. So the same object can be made with different tools, different material etc. 
Instead of the traditional one program to make a million identical objects, we want to enable one million people to create a unique object.
That's why instead of fancy hard to learn 3D CAD/CAM programs that can do almost anything but leaves you starting from scratch each time, we want to see a program evolve for each object. 
<h3>Open Source</h3>
Because the designs are open, anyone can improve the generators, and build new designs on top of existing ones. People can work in teams, improving the design over time, using the collaborative tools that have enabled the Open Source movement.
Designs need to evolve over time, bugs must be identified and fixed. Experiments and one offs must be encouraged. Building objects with the tools used to build complex software is a powerful idea.
 
"""

print """

<h2>Who we are</h2>

Hugomatic is a small company founded by Hugo Boyer. He wants to share his fascination for robotics, electronics, computers and machines.
"""

print """  
<h2>CNC Online</h2>
<p>
The CNC online project is set of Open Source web and desktop tools written in Python. It allows you to generate useful CNC snippets of code from easy to fill form.
</p>
<p>
CNC Online offers a variety of useful generators: circular and rectangular pockets milling, bolt circles drilling, etc.
On top of the basic operations, it includes higher level operations such as SVG file path tracing.
</p>

"""

print """

<h2>The Hugomatic library</h2>

The Hugomatic python library is the engine behind CNC Online. It is both web based, so you can use it without installing any software.</p>
and a local application, so you can use it on your own machine when you are offline.</p>
<p>Made for the tinkerer, not the programming expert: it has a simple api to create generators, 
it allows you to debug your program online (with a stack trace for every line of G-code), and a debugger friendly mechanism.</p>
<p>It is also easy to learn, with examples you can browse online</p>
"""

print """ 

<h2>Intellectual Property</h2>

Not much here.

"""


print '</div>'

printFooter()

print "</body>"
