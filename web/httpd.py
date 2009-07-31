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

"""
This is a simple http server to help you run the gcode generators from your PC
It serves files on port 8080 by default, but you can pass a port as the program argument
"""

import sys
import os
import CGIHTTPServer
import BaseHTTPServer

PORT = 8080
index = "index.py"

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ['']
    
    def is_cgi(self):
        print "path", self.path
        if self.path == "/":
            self.path =  "/" + index
            print 'redirecting to "%s"' % self.path
        if not self.path.endswith(".py"):
            return None
        return CGIHTTPServer.CGIHTTPRequestHandler.is_cgi(self)

if len(sys.argv) >= 2:
    PORT = int (sys.argv[1])
if len(sys.argv) >= 3:
    index = int (sys.argv[3])
    
directory,filename = os.path.split(__file__)
if len(directory) ==0 :
    directory = '.'
os.chdir(directory)
os.chdir("../../")
print "Current working directory: " + os.getcwd()

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port: ", PORT
httpd.serve_forever()

