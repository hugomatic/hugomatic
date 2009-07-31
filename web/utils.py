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


class HtmlTree(object):
    
    html_header_text = """
    
        <link rel="stylesheet" href="./hugomatic/web/stylesheets/jquery/jquery.treeview.css" />
        <script type="text/javascript" src="./hugomatic/web/stylesheets/jquery/jquery-1.3.1.min.js"></script>
        <script src="./hugomatic/web/stylesheets/jquery/jquery.cookie.js" type="text/javascript"></script>
        <script src="./hugomatic/web/stylesheets/jquery/jquery.treeview.js" type="text/javascript"></script>
        
        """
    def __init__(self, tree_name):
        self.name =  tree_name
        self.html = []
        self.level = 1
        self.tab_space = " "
        self.html.append(self._get_tree_script_element())

    def _get_tree_script_element(self):
        tree_script_text = """
        <script type="text/javascript">
        $(document).ready(function(){ $("#%s").treeview();  });
        </script>   
        """ % self.name
        return tree_script_text
        
    def _get_tab_space(self):
        s = '\n' + self.tab_space * self.level
        return s
        
    def open_folder(self, txt):
        s = '%s<li class="closed"><span class="folder">%s</span>' % (self._get_tab_space(), txt)
        self.html.append(s)
        s1 = "%s<ul>" % (self._get_tab_space())
        self.html.append(s1 )
        self.level += 1
    
    def close_folder(self):
        s = "%s</ul>" % (self._get_tab_space())
        self.html.append(s )
        self.level += -1
    
    def add_file_link(self, txt):
        s = '%s<li><span class="file"><a href="%s">%s</a></span></li>' % (self._get_tab_space(),txt, txt)
        self.html.append(s)
    
    def add_file_text(self, txt):
        s = '%s<li><span class="file">%s</span></li>' % (self._get_tab_space(),txt)
        self.html.append(s)
       
    def get_html(self):
        s =  '<div id="%s" class="filetree treeview-famfamfam">' % self.name
        s += "".join(self.html)
        s += '\n</div>\n'
        return s


def html_escape(text):
    text = text.replace('&', '&amp;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    text = text.replace(">", '&gt;')
    text = text.replace("<", '&lt;')
    return text

def printHead(title, styleSheets, path="hugomatic/web/", extraText=None):
    path += "stylesheets/"
    print "<html>"
    print "<head>"
    print '  <title>%s</title><link rel="shortcut icon" href="%simg/favicon.ico"/>' % (title,path)
    for css in styleSheets:
        print '  <link type="text/css" rel="stylesheet" href="%s%s.css" />' % (path,css)
    
    
    print extraText or ''
    print "</head>"
    print "<body>"
#    print "<h4>Current working dir:"  + os.getcwd() + "</h4>"
#    print "<h4>printHead path '" + path + "'</h4>"

def printBanner(path = "hugomatic/web/"):
    path += "stylesheets/"
#    cwd = os.getcwd()
#    print "<h4>Current working dir:"  + cwd + "</h4>"
#    print "<h4>printBanner path '" + path + "'</h4>"
    print """
    <div id="banner">
       <a href="http://basbrun.com/"><IMG class="bannerImg" SRC="%simg/banner.gif"/></a>
    </div>
    """ % (path)

def printPyFileSrcLinks(root):
    path = "hugomatic/web/"
    print "<h4>Current working dir:"  + os.getcwd() + "</h4>"
    print "<h4>printPyFileSrcLinks path' " + path + "'</h4>"
    def printLink(fileName):
        print "<a href=\"" + path + "sourceView.py?src=" + fileName + "\">" + fileName + "</a>"
    
    def process(dirName, prefix):
        #print "PROCESSING ", dirName
        files =  os.listdir("..")
        for f in files:
            if f.endswith(".py"):
                if doNotPublish.__contains__(f) == False:
                    printLink(prefix + f)
            else:
                pass #print "** ", f
    process(root, "")
    process(root + "/hugomatic", "hugomatic/")

def printGetNavBar(sourceFile):
    nothing, name = os.path.split(sourceFile)
    sourceRef = "hugomatic/web/sourceView.py?src=" + name
    print """
    <ul id='nav'>
        <li><a href="index.py">Home</a></li>   
        <li><a href=\"%s\">View source: <b>%s</b></a></li>
        <li><a href="../../../cncOnline.zip">Get Hugomatic</a></li>
        <li><a href="hugomatic/web/todo.py">Report a Bug</a></li>
        <li><a href="hugomatic/web/contact.py">Contact us</a></li>
    </ul>
    """ % (sourceRef, name)
    
def printContactNavBar():
    print """
        <ul id='nav'>
            <li><a href="../../index.py">Home</a></li>   
            <li><a href="../../../cncOnline.zip">Get Hugomatic</a></li>
            <li><a href="todo.py">Report a Bug</a></li>
        </ul>"""

def printIndextNavBar():
    print """
        <ul id='nav'> 
            <li><a href="../../../cncOnline.zip">Get Hugomatic</a></li>
            <li><a href="todo.py">Report a Bug</a></li>
            <li><a href="hugomatic/web/contact.py">Contact us</a></li>
        </ul>"""
                                 
def printPostNavBar(sourceFile):   
    nothing, name = os.path.split(sourceFile)
    sourceRef = "hugomatic/web/sourceView.py?src=" + name
    print """
        <ul id='nav'>
            <li><a href="index.py">Home</a></li>   
            <li><a href=\"%s\">Run <b>%s</b> again</a></li>
            <li><a href=\"%s\">View source: <b>%s</b></a></li>
            <li><a href="../../../cncOnline.zip">Get Hugomatic</a></li>
            <li><a href="hugomatic/web/todo.py">Report a Bug</a></li>
            <li><a href="hugomatic/web/contact.py">Contact us</a></li>
        </ul>
    """ % (name, name, sourceRef, name)
    print """
    <!--
    hugomatic.web.utils.printPostNavBar
    name %s
    sourceFile %s
    sourceRef %s
    -->
    """ % (name, sourceFile, sourceRef)

def printSourceViewNavBar(sourceFile):
        nothing, name = os.path.split(sourceFile)
        print """
    <ul id='nav'>
        <li><a href="../../index.py">Home</a></li>   
        <li><a href=\"/%s\">Run <b>%s</b></a></li>
        <li><a href="../../../cncOnline.zip">Get Hugomatic</a></li>
        <li><a href="todo.py">Report a Bug</a></li>
        <li><a href="contact.py">Contact us</a></li>
    </ul>
""" % (name, name)

def printFooter():
            print """
    <div id="footer">
        <p>&copy; Copyright Hugomatic. <span class="unit">All code generators are licenced under the GPL</span></p>
    </div>  
  </body>
</html>
""" 

if __name__ == "__main__":
    printPyFileSrcLinks("..")