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

import os
import cgi

try:
    from utils import printHead, printBanner, printFooter, printSourceViewNavBar
    from lpy import *
except:
    from hugomatic.web.utils import printHead, printBanner, printFooter, printSourceViewNavBar
    from hugomatic.web.lpy import *


DEBUG = False

def mainDebug():
  
    print "<h1>Source view</h1>"
    print "<br>"

    print query
    print "<br>"
    print "<br>"
            
    print "<h1>CGI</h1>"
    form = cgi.FieldStorage()
    for key in form.keys():
        val = form[key].value
        print key,": ", val, ": ", form[key]

    str = ""
    for name in os.environ.keys():
          str += "%s = %s<br />\n" % (name, os.environ[name])
    print str    

def main2(sourceFile):
    print "<h1>" + sourceFile+"</h1>"
    print "<Pre>"
    f = open(sourceFile)
    lines  = f.readlines()
    for line in lines:
        htmlLine = html_escape(line[0:-1])
        print htmlLine
    print "</Pre>"
    

def printPyFileSrcLinks(root):
    
    def printLink(fileName, newRow):
        pre = "\n<tr><td class='xref'>"
        post = "</td>"
        
        if not newRow:
            pre = "<td  class='xref'>"
            post = "</td></tr>\n"
        
        anchor = "<a href=\"" + "sourceView.py?src=" + fileName + "\">" + fileName + "</a>"
        print pre + anchor + post
    
    def process(dirName, prefix):
        doNotPublish = ['index.py', 'sourceView.py']
        #print "PROCESSING ", dirName
        files =  os.listdir(dirName)
        newRow = False
        for f in files:         
            if f.endswith(".py"):
                if doNotPublish.__contains__(f) == False:
                    newRow = not newRow    
                    printLink(prefix + f, newRow )
            else:
                pass # print "** ", f   
    
    root = os.getcwd().replace("/hugomatic/web","")
    process(root, "")
    process(root + "/hugomatic", "hugomatic/")
    process(root + "/hugomatic/web", "hugomatic/web/")
    process(root + "/hugomatic/web/lpy", "hugomatic/web/lpy/")
    
def getSource():
    src = "index.py"
    form = cgi.FieldStorage()
    key = 'src'
    src = form[key].value
    return src

def main(sourceFile):  
    print "Content-Type: text/html"
    print
    
    oldwd = os.getcwd()
    filedir = oldwd.replace("/hugomatic/web","")
#    os.chdir(curdir)
#    cwd = os.getcwd()

    printHead('Hugomatic source explorer', ('banner','nav','footer'), path='' )
    printBanner(path='')
   
    printSourceViewNavBar(sourceFile)
    head, tail = os.path.split(sourceFile)
    print "<h1>" + tail+"</h1>"
    
    filePath = filedir + "/" + sourceFile
#    print "<h4><pre>"
#    print "sourceFile: " + sourceFile
#    print "head:  " + head
#    print "tail:  " + tail
#    print "oldwd: " + oldwd
#    print "cwd:   " + cwd
#    print "filePath: " + filePath
#    print "</pre></h4>"
    
    PyToHTML(filePath, sys.stdout)
    print
    print
    print "<hr>"
    print '<table>'
    printPyFileSrcLinks(".")
    print '</table>'
    
    printFooter()
    print "</body>"

sourceFile = getSource()
main(sourceFile)



