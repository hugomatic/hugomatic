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

import sys
import os
import inspect
from utils import printHead, printBanner, printFooter

#def getLink(pyPath):
#    
#    text = pyPath.replace('.py', "")
#    return "<br><h3><a href=\"" + pyPath + "\">" + text + "</a></h3>"
#doNotPublish = ['index.py', 'sourceView.py', 'httpd.py']

def main():
    print "Content-Type: text/html"
    print
    printHead('Hugomatic under construction', ('banner','footer'),path='')
    printBanner(path='')
    print  """
    <br>
    <h1>Under construction ;-(</h1>
    <br>
    <br>
    <br>If all knowledge, all culture, all art, all useful information, can be costlessly given to everyone at the same price that it is given to anyone... free access to information is essential because the alternative is unethical and unacceptable.
    """

    printFooter()
    print "        </body>"
main()