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
from hugomatic.web.utils import HtmlTree
from hugomatic.web.utils import printHead, printBanner, printFooter, printIndextNavBar

def getLink(pyPath):  
    text = pyPath.replace('.py', "")
    return "<h3><a href=\"" + pyPath + "\">" + text + "</a></h3>"

def get_name_from_xml_node(node):
    if node.nodeType == node.ELEMENT_NODE:
            s = node.nodeName
            a = node.getAttribute('name')
            if len(a) > 0:
                s = a
            return s
    elif node.nodeType == node.TEXT_NODE:
        return node.nodeValue
        
def add_tree_nodes_from_xml(html_tree, dom):  
        
    def do_xml_node(html_tree, node):
        txt = get_name_from_xml_node(node)
        folder_node = node.hasChildNodes()
        
        if txt.strip():
            type = "Script"
            if folder_node:
                html_tree.open_folder(txt)     
            else:
                html_tree.add_file_link(txt)
            
            children = node.childNodes
            for child in children:
                do_xml_node(html_tree, child)
                
            if folder_node:
                html_tree.close_folder()
                
    #html = []
    for node in dom.documentElement.childNodes:
        do_xml_node(html_tree, node)
 



def printIndex(dom):
    
    print "Content-Type: text/html"
    print
    
    printHead('Welcome to Hugomatic', ('banner','index','nav','footer'), extraText=HtmlTree.html_header_text)
    printBanner()
    printIndextNavBar()
    #printContactNavBar()
    
    print  "<h1>Hugomatic CNC</h1><h2>online GCODE generators</h2>"
    print "<br>"
    print '<div id="main">'
 
    ##print '<div id="browser" class="filetree treeview-famfamfam">'
    tree = HtmlTree("browser")
    add_tree_nodes_from_xml(tree, dom)
    html_tree = tree.get_html()
    print html_tree
    ##print '</div>'
    
        
    print """
    
  <div id="image">
   <IMG SRC="images/index.jpg">
  </div>
"""
   
    print '</div>' # main

    printFooter()
    print "</body>"
