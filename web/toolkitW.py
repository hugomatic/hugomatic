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
import inspect
import sys
import cgi
import types
#import re
import cgitb; cgitb.enable()
import atexit

import utils

#from utils import HtmlTree

# GOOGLE APP ENGINE PATCH!!!
googleAppEngine = False
try:
    import google.appengine
    import imp
    import hugomatic.web.gcode2svg as gcode2svg
    import hugomatic.web.gcode2json as gcode2json
    
    googleAppEngine = True
    
    def get_suffixes():
        return [('.py', 'U', 1)]
    imp.get_suffixes = get_suffixes
except:
    import gcode2svg
    import gcode2json


def print_stack_info():
    """
    Not used in the web version
    """
    pass

def gcodeCommentEscape(s):
    """
    Removes '(' and ')' to avoid illegal nested comments in gcode
    """
    niceStr = s.replace("(", "-")
    niceStr = niceStr.replace(")", "-")
    return niceStr

def print_interactive_post_footer():
    sys.stdout = sys.stdout.out # remove the line numbering decorator
    print "</pre>" #no more space preserving
    utils.printFooter()
    print "</body></html>"

# svg_document = None
    
def print_params_post_footer(stdout1 = None, xform = None):
    form = xform
    if form == None:
        form = sys.stdout.xform
    stdout = stdout1
    if stdout == None:
        sys.stdout = sys.stdout.out
    else:
        sys.stdout = stdout

    text = form.get_document()
    print text



class ParamsRedirectStdOut:
    
    def __init__(self, out, xform):    
        self.out = out
        self.xform = xform
        self.tmp = ""
        
    def _writeline(self, line):
        self.xform.add_gcode_line(line)
        ll = line.lower()
        if googleAppEngine:
            if ll.split('(')[0].find("m2") != -1 :
                print_params_post_footer(self.out, self.xform)
    
    def write1(self, s):
        lines = s.splitlines()
        if len(lines) > 1:
            for l in lines:
                self._writeline(l)
                # self._writeline('\n')
        else:
            self._writeline(s)
                    
    def write(self, s):
        self.write2(s)
        
    def write2(self,s):
        lines = s.splitlines()
        if len(lines) > 1:
            for l in lines:
                self._writeline(self.tmp +l)
                self.tmp = ''
        if s.endswith("\n"):
            self._writeline(self.tmp + s[:-1])
            self.tmp = ""
        else:    
            self.tmp += s
#        
#        if len(lines) > 1:
#            for l in lines:
#                self._writeline(l + '\n')
#        else:
#            self._writeline(s)
#                
 
class RedirectStdOut:
    
    isComment = False
    isToken = False
    
    def __init__(self, out, pretty = False):
        self.out = out
        self.debugLine = -1
        self.prettyPrint = pretty
        self.printLineCounter = 0
        if self.prettyPrint:
            self.prettyWrite('\n')
    
    def _prettyGcode(self,s):
        def prettyChar(c):
            if c == "(":
                self.isComment = True
                return "<font color=darkcyan>("
            if c == ")":
                self.isComment = False
                return ")</font>"
            if self.isComment:
                return c
            # not a comment
            if c in 'aAXxYyZzIiJjpPrR':
                pre = ""
                if self.isToken:
                    pre = "</b>"
                return pre + "<font color=darkblue>" + c+ "</font>"
            if  c== 'F' or c == 'f':
                return "<b>" + c + "</b>"
            if c == 'G' or c == 'g' or c == 'M' or c == 'm':
                self.isToken = True
                return "<b>" + c
            if c == ' ':
                if self.isToken:
                    return "</b> "
            return c
        
        nice = ""
        for c in s:
            nice += prettyChar(c)
        return nice
    
    def traceBack(self): 
        
        def esca(v):
            val = str(v)
            val = utils.html_escape(val)
            if type(v) == str:
                val = v.replace("\n", "\\n")
                val = "\"" + val + "\""
            return val
        
        def get_html_file_link(name, root, lineNb): 
            f = os.path.split(name)[1]
            if name.startswith(root):
                i = len(root)
                f =  name[i+1:] # +1 removes the '/' in front
            s = "%s#%d" % (f,lineNb)
            link = '<a href="hugomatic/web/sourceView.py?src=' + s + '">' + f + ', line '+ str(lineNb)+'</a>'
            return link
        
        def print_func_name(file_name, current_dir, line_nb, func_name):
            file_link = get_html_file_link(file_name, current_dir, line_nb)
            if func_name == '?':
                func_name = '<i>N/A (Module scope)</i>'
            frameString = "<h2>" + file_link + "</h2>" + "Function/method: <b>" +  func_name +  "</b>\n"
            self.out.write(frameString )
            
        def print_snippet(snippet_lines, current_line_nb):
            self.out.write("<hr><font color=black>")
            for i in range(len(snippet_lines) ):
                pre =   ""
                post =  ""
                if i == current_line_nb:
                    pre = "<font color=red><b>"
                    post = "</b></font>"
                line = pre + utils.html_escape( snippet_lines[i]) + post
                self.out.write(line)
            self.out.write("</font><hr>")

        def print_locals_dict(locals_dict):            
            self.out.write("    <b>locals:</b>\n")
            for key, val in locals_dict.items():
                printVar(key,val)
                
        def print_globals_dict(globals_dict):
            self.out.write("    <b>globals:</b>\n")
            for key, val in globals_dict.items():
                printVar(key,val)
                
            
        def print_variables (line_nb, locals_dict, globals_dict):    
            print_locals_dict(locals_dict)
            print_globals_dict(globals_dict)
        
        def add_var_to_tree(tree, key, val):
            if inspect.isclass(val):
                return
            if inspect.isroutine(val):
                return
            if inspect.ismodule(val):
                return
            if key.startswith("_"):
                return
            
            name = utils.html_escape(key)
            value = esca(val)
            tree.add_file_text(name + ":" + value)
            
                          
        def printVar(key, val):
            if inspect.isclass(val):
                return
            if inspect.isroutine(val):
                return
            if inspect.ismodule(val):
                return
            if key.startswith("_"):
                return
            
            key = utils.html_escape(key)
            val = esca(val)
            val = '<a class="val">' + val + "</a>"
            self.out.write("       " +key+ ": "+ val + "\n")

        gcode_line_number = self.printLineCounter
        currentDir = os.getcwd()        
        self.out.write("<div id=\"div%d\" class='trace' style='display:none'>" % gcode_line_number)
        stack_frame = inspect.currentframe().f_back.f_back # skip 'prettyPrint' and 'write'
        stack_frames = []
        while stack_frame.f_back != None:
            stack_frame = stack_frame.f_back
            stack_frames.append(stack_frame)
            
        stack_frames.reverse()    
        for frame in stack_frames:
            info = inspect.getframeinfo(frame,5)
            
            file_name = info[0]
            py_line_number = info[1]
            func_name = info[2] 
            snippet_lines = info[3]
            snippet_current_line_nb = 2
            globals_dict = frame.f_globals
            locals_dict =  frame.f_locals
            
            print_func_name(file_name, currentDir, py_line_number, func_name)
            print_snippet(snippet_lines, snippet_current_line_nb)
            print_variables(gcode_line_number, locals_dict, globals_dict)
        self.out.write("</div>")
        
    def prettyWrite(self, s):
        
        def getLineNbString(nb):
            s = "%0.4d" % nb
            divName = "div" + str(nb)
            nbStr = """<br><a class="nb" onclick="toggle(""" +  divName + ')">' + s + "</a>   "
            return nbStr
        
            
        if s == '\n':
            if self.isToken:
                self.out.write("</b>")
            self.printLineCounter += 1
            self.isComment = False
            self.isToken = False
            self.out.write(getLineNbString(self.printLineCounter))
            #if self.printLineCounter == self.debugLine:
            
        else:  
            niceStr = self._prettyGcode(s)
            self.out.write(niceStr)
            self.traceBack()
            ll = s.lower()
            if googleAppEngine:
                if ll.split('(')[0].find("m2") != -1 :
                    print_interactive_post_footer()


    def write(self, s):
        if self.prettyPrint == False:
            self.out.write(s)
        else:
            lines = s.splitlines()
            if len(lines) > 1:
                for l in lines:
                    self.prettyWrite(l)
                    self.prettyWrite('\n')
            else:
                self.prettyWrite(s)



    def setDebugLine(self, nb):
        self.debugLine = nb
    def flush(self):
        self.out.flush()
    def seek(self, a, b =0):
        self.out.seek(a, b)
    def readline(self):
        return None


          
class Parameters(object): 
    postHead = """

<script type="text/javascript">
<!--

function toggle(id)
{
   if (id.style.display == 'none')
   {
      id.style.display = ''
   }
   else
   {
      id.style.display = 'none'
   }
}

-->
</script>

"""

    getHead = """

<SCRIPT type="text/javascript">
function OnButtonPreview()
{

    document.GcodeForm.generation.value = "interactive"
    document.GcodeForm.submit();             // Submit the page

    return true;
}

function OnButtonCanvas()
{
    document.GcodeForm.generation.value = "canvas"
    document.GcodeForm.submit();             // Submit the page

    return true;
}

function OnButtonSvg()
{
    document.GcodeForm.generation.value = "svg"
    document.GcodeForm.submit();             // Submit the page

    return true;
}

function OnButtonDownload()
{
    document.GcodeForm.generation.value = "download"
    document.GcodeForm.submit();             // Submit the page

    return true;
}

</SCRIPT>

"""

    def __init__(self, name, desc, picture_file = "", debug_callback = None, debug_line = -1):
        self.title = name
        self.desc = desc
        self.params = list()
        self.picture_file = None
        if len(picture_file) > 0:
            self.picture_file = "images/" + picture_file
        frame = inspect.currentframe().f_back
        frameInfo = inspect.getframeinfo( frame )
        self.fileName = frameInfo[0]
         
    def _printPost2(self):
        print 'Content-Type: text/plain'
        print
        print
        print "<h1>DEBUG POST</h1>"
        form = cgi.FieldStorage()
        for key in form.keys():
            val = form[key].value
            print key,": ", val, ": ", form[key]
    
    def getRelativePath(self, name):
        fn = 'files/' + name
        return fn

    def _uploadFile(self, fileItem):
        fn = os.path.basename(fileItem.filename)
        content = fileItem.file.read()
        path = self.getRelativePath(fn)
        open(path, 'wb').write(content)   
        return fn
    
    def _interactive_post(self, name, output_file, form):
        print "Content-Type: text/html"
        print
        html_header = self.postHead
        # add the tree control javascript stuff
        #html_header += HtmlTree.html_header_text
        utils.printHead('Hugomatic gcode', ('banner','nav','interactive','footer'),  extraText=html_header)
        utils.printBanner()
        utils.printPostNavBar(self.fileName)
        print "<h1>" + output_file + "</h1><Pre>"
        #print '<h2>Source code: <a href="sourceView.py?src=' + name + '">' + name+'</a></h2>'
        old_out = sys.stdout
        sys.stdout = RedirectStdOut(old_out, True)
        # add hook to end program with a copyright notice
        if googleAppEngine == False:
            atexit.register(print_interactive_post_footer)


    def _svg_post(self, name, output_file, form, values_dict):
        #print 'Content-Type: text/plain'
        print  "Content-Type: image/svg+xml"
        print
        
        
        old_out = sys.stdout
        sys.stdout = ParamsRedirectStdOut(old_out, gcode2svg.Gcode2Svg(output_file, values_dict)  )
        # add hook to end program with an svg text
        if googleAppEngine == False: 
            atexit.register(print_params_post_footer)
    
    def _canvas_post(self, name, output_file, form, values_dict):
        print  "Content-Type: text/html"
        print
        
        old_out = sys.stdout
        sys.stdout = ParamsRedirectStdOut(old_out, gcode2json.Gcode2json(output_file, values_dict) )
        if googleAppEngine == False: 
            atexit.register(print_params_post_footer)
   
    def _download_post(self, name, output_file, form):
        print 'Content-Type: text/plain'
        print "Content-Disposition: attachment; filename=\"" + output_file + "\""
        print
        
        print "( " + self.title + " )"
        print "( " + self.desc + " )"
        print
    

    def  _inject_form_values_into_global_vars(self, form, callingFrame):
        
        import inspect
        import sys, traceback

        for p in self.params:
            
            name = p['name'] 
            desc = p['desc']
            value = p['obj']
             
            newVal = None
            if type(value) == bool:
                if form.__contains__(name):
                    newVal = True
                else:
                    newVal = False
            else:
                if form.__contains__(name):
                    newVal = None
                    if type(value) == float:
                        newVal = float(form[name].value)
                    elif type(value) == int:
                            newVal = int(form[name].value)   
                    if form[name].filename:
                            newVal = self._uploadFile(form[name])            
                    if newVal == None:
                        # if the value has not changed, set newVal to the old one
                        newVal = form[name].value
            # assign the new value    
            callingFrame.f_globals[name] = newVal
            
            
        
    
    def _printPost(self):
        name = os.path.basename(self.fileName)
        output_file = name.replace(".py",".ngc")
        form = cgi.FieldStorage()       
        callingFrame = inspect.currentframe().f_back.f_back
        self._inject_form_values_into_global_vars(form, callingFrame)
        new_values = {}
        for p in self.params:
            name = p['name']
            new_values[name] = callingFrame.f_globals[name]
            
        if form['generation'].value == 'interactive':
            self._interactive_post(name, output_file, form)
        if form['generation'].value == 'download':
            self._download_post(name, output_file, form)
        if form['generation'].value == 'svg':
            self._svg_post(name, output_file, form, new_values)
        if form['generation'].value == 'canvas':
            self._canvas_post(name, output_file, form, new_values)
        #print "POST IT"           
            
        
    def _printForm(self):
        """
        Generates a web page that contains a FORM with inputs for
        every parameter published via addArgument in the self.params list
        """
        
        def openGroup(group):
            print "<fieldset><legend>" + group + "</legend>"
            
        def closeGroup(group):
            print "</fieldset>"
            
        def printInputField(name, desc, value, choices, isFilePath):
            
            def printSelect(name, value, choices, desc):
                print "<select name=\"%s\">" % name
                for option in choices:
                    s = '>'
                    if option == value:
                        s = ' selected>'
                    print '   <option value ="' + option + '"' + s + option + "</option>"
                print "</select> " + desc + " ( " + value + " )<br>" 
               
            
            size = 10
            t = type(value)
            if t == bool:
                if value == True:
                    #text on the right
                    print """<input type="checkbox" name=\""""+ name+ "\"value=\"", value, "\"CHECKED/>", desc, "(", value,")<br>"
                else:
                    print """<input type="checkbox" name=\""""+ name+ "\"value=\"", value, "\"/>", desc, "(", value,")<br>"

                #text on the left
                #print "<br>"+ desc +"""<input type="checkbox" name=\""""+ name+ "\"value=\"", value, "\">", "(", value,")"

            else:
                if isFilePath:
                    print "<input type=\"file\" name=\""+name+  "\" size=\"", size * 2 , "\" value=\"", value ,"\"/>", desc, "(", value,")<br>"
                else:
                    
                    if choices:
                        printSelect(name, value, choices, desc)
                    else:
                        print "<input type=\"text\" name=\""+name+  "\" size=\"", 10, "\" value=\"", value ,"\"/>", desc, "(", value,")<br>"        
        
        
        print "Content-Type: text/html"
        print
        utils.printHead('Hugomatic gcode generator', ('banner','getform','nav','footer'),  extraText=self.getHead)
        utils.printBanner()
        utils.printGetNavBar(self.fileName)
        
        print "<h1>", self.title, "</h1>"
        if self.picture_file != None:
            print """ 
<div id="form-content">

<div id="form-image">
 <IMG SRC=\"""" + self.picture_file + """"\">
</div>"""        
        print """
        <div id="form-elements">
          <form name="GcodeForm" enctype="multipart/form-data" method="post">"""
        
        legend = self.desc
        print "<strong>" + legend + "</strong>"
        print "<fieldset>" # <legend>" + legend + "</legend>"
        
        currentGroup = None
        for p in self.params:
            name = p['name'] 
            desc = p['desc']
            value = p['obj']
            filePath = p['filePath']
            choices = p['choices']
            group = p['group']
            if group != currentGroup:
                if currentGroup != None:
                    closeGroup(currentGroup)
                currentGroup = group
                if currentGroup != None:
                    openGroup(group)
                if group == None:
                    print "<br>" # reopening the top group.. add a spacer
            printInputField(name, desc, value, choices, filePath)
        if currentGroup != None:
                    closeGroup(currentGroup)
        print """
        
    <input type="hidden" name="generation" value="none" />        
<br><INPUT type="button" value="Web view" name=button1 onclick="return OnButtonPreview();">
    <INPUT type="button" value="Generate & download" name=button2 onclick="return OnButtonDownload();">
    <INPUT type="button" value="SVG (BETA)" name=button3 onclick="return OnButtonSvg();">
    <INPUT type="button" value="UI (BETA)" name=button3 onclick="return OnButtonCanvas();">
    <input value="RESET" type="reset"> 
    
             </fieldset>
          </form>
        </div>
       </div>
        """
        print """
        <p><i>A computer in every workshop!</i></p>
        """
        utils.printFooter()
    

    def addArgument(self, object, title, choices=None, filePath=False, short = None, help=None, group=None):    
        def getArgNameFromCallStack(call):
            sp = call.split('(')
            s = sp[1] 
            sp2 = s.split(",")
            s = sp2[0]
            argument =  s.split(')')[0]
            argument = argument.strip()
            return argument
        
        info = inspect.getframeinfo( inspect.currentframe().f_back )
        call = str(info[3])
        name = getArgNameFromCallStack(call)
        params ={'name':name, 
                 'desc':title, 
                 'obj':object, 
                 'short':short, 
                 'group': group,
                 'filePath' : filePath,
                 'choices':choices}
        self.params.append( params )
    
    def loadParams(self):
        method = os.environ['REQUEST_METHOD']
        if method == 'GET':
            self._printForm()
            sys.exit()
            return False
    
        if method == 'POST':
            self._printPost()
            return True



    
        
