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

printHead('Contact Hugomatic',('nav','banner','footer'), path="")
printBanner( path='')

printContactNavBar()
       

print "<h1>About Hugomatic</h1>"
print '<div id="about">' 

print """

<h2>What we do</h2>

"""

print """

<h2>Who we are</h2>

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

"""

print """ 

<h2>Intellectual Property</h2>

"""

print '<br>Hugomatic is a Montreal based company'


print '</div>'

printFooter()

print "</body>"
