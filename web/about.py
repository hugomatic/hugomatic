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

try:
    # google app engine
    from hugomatic.web.utils  import  printHead, printBanner, printFooter, printAboutNavBar

except:
    from utils import  printHead, printBanner, printFooter, printAboutNavBar


print "Content-Type: text/html"
print

printHead('About Hugomatic',('nav','banner','footer'), path="")
printBanner( path='')

printAboutNavBar()
       

print "<h1>About Hugomatic</h1>"
print '<div id="about">' 

print """

<h2>What we do</h2>

Hi, my name is Hugo Boyer and I founded a micro company called Hugomatic so I could share my fascination for robotics, electronics, computers and machines with my friends. 
We build Open Source platform to generate Open Physical Objects. We supply free projects for hobby CNC milling and lathes. 
We want to empower people to make professional objects simply, and want to remove the complexity of hobby robotics. 
<h3>Free designs</h3>
The designs are free, so anyone can build the objects with their own equipment. Or you can get someone to build it for you. We can help you get the parts you need.
<h3>Generated objects</h3>
Because the objects are created from a generator program, rather than drawings for example, they can be customized and personalized. So the same object can be made with different tools, different dimensions, different material etc. 
Instead of making a million identical objects with one machine, we want to see a million people create their unique object.
Instead of fancy hard to learn 3D CAD/CAM programs that can do almost anything but leaves you starting from scratch each time, we want to build programs that build a single objects well. 
<h3>Open Source</h3>
Because the designs are open, anyone can improve them, and build new designs on top of existing ones. People can work in teams, improving the design over time, using the collaborative tools that have enabled the Open Source movement.
Designs need to evolve over time, bugs must be continually identified and fixed. Experiments and one offs must be encouraged. Building physical objects with the tools used to build complex software is a powerful idea.
 
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

The Hugomatic python library is the engine behind CNC Online. It is both web based, so you can use it without installing any software, 
and a stand alone application, so you can use it on your own machine when you are offline.</p>
<p>Made with the pragmatic tinkerer in mind: it has a simple api to create generators, 
it allows you to debug your program online (with a stack trace for every line of G-code), and a debugger friendly mechanism.</p>
<p>It is also easy to learn, with examples you can browse online</p>
"""

print """ 

<h2>Intellectual Property</h2>

You won't find much here. We simply have fresh ideas, and we want to hear yours.

<p>
<p>
<i>
If nature has made any one thing less susceptible than all others of exclusive property, it is the action of the thinking power called an idea, which an individual may exclusively possess as long as he keeps it to himself; but the moment it is divulged, it forces itself into the possession of every one, and the receiver cannot dispossess himself of it. Its peculiar character, too, is that no one possesses the less, because every other possesses the whole of it. He who receives an idea from me, receives instruction himself without lessening mine; as he who lights his taper at mine, receives light without darkening me.
<p>
Thomas Jefferson, 1813
</i>
<p>
<p>

"""

print '<br>Hugomatic is a Montreal based company'


print '</div>'

printFooter()

print "</body>"
