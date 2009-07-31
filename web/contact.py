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


from hugomatic.web.utils import  printHead, printBanner, printFooter, printContactNavBar


print "Content-Type: text/html"
print

printHead('Contact Hugomatic',('nav','banner','footer'), path="")
printBanner( path='')

printContactNavBar()
       

print "<h1>Contact us</h1>"
print '<div id="contact">' 

print '<img src="stylesheets/img/phone.jpg">'

print '<br>Hugomatic Enterprises'
print '<br>email: hugo@hugomatic.ca'
print '<br><br><br>'

print '</div>'

printFooter()

print "</body>"