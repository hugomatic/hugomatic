"""
    htmlmax.py
    
html macros for use from pymacro by lpy app

"""
__Id__ = "$Id: htmlmax.py,v 1.8 2000/05/18 21:14:56 dirck Exp $"

#@reset_contents
#~@h3{Table of Contents}
#~@display_contents

#---------------------------------------------------------------------------

#@contents_item{Introduction}
"""~ html macros for lpy

This stuff is getting a little hectic, primarily with
the Netscape v Explorer issues becoming apparent.  
Several different HTML strategies have been tried, 
and there remains lots of cruft in here from mucking about.

The Netscape jaggy-gray-background issue is really pretty tragic.
"""

#---------------------------------------------------------------------------
#@contents_item{Imports}

import string

# circular...
              
import pymacro
#---------------------------------------------------------------------------
#@contents_item{simple macros}
#@indent
#@{def simple(X): return contents_item(X, 'simple macros')}

#@simple{pre}
#~@@pre{Preformatted} -> @pre{Preformatted}

# using single-parameter %s strings works just as well for f{s}

pre = "<pre>%s</pre>"

#@simple{h2}
#~@@h2{heading 2} -> @h2{heading 2}

h2 = '<h2>%s</h2>'

#@simple{h3}
#~@@h3{heading 3} -> @h3{heading 3}

def h3(s):
    return '<h3>%s</h3>' % s

#@simple{b}
#~@b{b is for bold}

def b(s):
    return '<b>%s</b>' % s

#~@i{i is for italic}

def i(s):
    return '<i>%s</i>' % s

#~@bi{bi is bold italic}

def bi(s):
    return '<b><i>%s</i></b>' % s

#~@tt{tt for teletype}

def tt(s):
    return '<tt>%s</tt>' % s

#@simple{xlink}
"""~
    @@xlink('Danbala Software', 'http://www.danbala.com') ->
    @xlink('Danbala Software', 'http://www.danbala.com')
"""

def xlink(s,x=None):
    if x is None:
        x = s      
    return '<a href="%s">%s</a>' % (x, s)

def nested(s):
    """ keep on expanding """
    while string.find(s, '@') >= 0:
        s = pymacro.pymax_process(s)
    return s
    
def html(s):
    """ put it back """
    return string.replace(string.replace(s, '&lt;','<'),'&amp;','&')

def image(name, w=0, h=0):
    if w and h:
        return '<img src="%s" width=%d height=%d, border=0>' % (name,w,h)
    else:
        return '<img src="%s" border=0>' % name

startlink = '<a href="%s">'
endlink = '</a>'
invert = '<div width=100% style="color:white; background:black;">'
endinvert = '</div>'

#@outdent
#---------------------------------------------------------------------------

#~ handy random symbols
"""~
Let's put a @P Paragraph in, followed by a @N line break and then a line
@L
"""
P = '<p>'
N = '<br>'
L = '<hr>'

"""~
@@indent @indent
@@bullet @bullet 
@@outdent @outdent
"""
indent = "<ul>"
outdent = "</ul>"
bullet = "<li>"

# this need to be tested - perhaps a different tag?

ff = '<div style="page-break-after:always"></div>'

#@contents_item{UL: unordered list}

"""~
@pre{
@UL{unordered list
a
b
c} 
}
@UL{unordered list
a
b
c}
"""


def UL(s):
    return '<ul>' + string.join(string.split(s, '\n'), '<li>\n') + '</ul>'

#@contents_item{OL: ordered list}

"""~
@pre{
@OL{ordered list
one
two
three}
}

@OL{ordered list
one
two
three}
"""

def OL(s):
    return '<ol>' + string.join(string.split(s, '\n'), '<li>\n') + '</ol>'

#---------------------------------------------------------------------------

#@contents_item{TABLE}

"""~

@pre{
@TABLE{
    this; is; the; way
    it's; supposed; to; work
    more; or; less; ok?}
}
->

@TABLE{
    this; is; the; way
    it's; supposed; to; work
    more; or; less; ok?}

@TABLE(
'''this, is, the, way
    it's, supposed, to, work
    more, or, less, ay?''', ',', 1)

"""

def TABLE(s, c=';', border=None):
    lines = string.split(s, '\n')
    if border:
        r = '<table border=%d>' % border
    else:
        r = '<table>'
    for line in lines:
        r = r + '\n<tr>'
        cols = string.split(line, c)
        for col in cols:
            r = r + '<td>' + col
    r = r + '</table>'
    return r

#~python module link: @@pylink{pymacro} -> @pylink{pymacro}

def pylink(module, dir=""):
    " generate a link to an external .py.html (import) "
    if dir:
        dir = dir + '/'
    return '<a href="%s%s.py.html">%s</a>' % (dir, module, module)

#~python standard library module link: @@stdlink{sys} -> @stdlink{sys}

def stdlink(*args):
    s = ''
    for module in args:
        if s:
            s = s + ', '
        s = (
'%s<a href="http://www.python.org/doc/current/lib/module-%s.html">%s</a>'
            % (s, module, module))
    return s
    
#~@i{hidden stuff:}@rem{you can't see this @{ha!}}
def rem(s):
    """ remark out some stuff so it doesn't appear """
    return ""

#~ Command Line options
#~ use attributes to make sure we complain if you mis-spell a flag

class Generic:
    pass
    
gFlags = Generic()
gFlags.printing = 0
gFlags.nosplits = 0
gFlags.noindex  = 0
gFlags.autoformat = 0
gFlags.autosplit  = 0

def SetFlag(s):
    global gFlags
    if not hasattr(gFlags, s):
        raise 'unrecognized option', s
    setattr(gFlags, s, 1)

def TestFlag(s):
    global gFlags
    return getattr(gFlags, s)

def danbala_logo():
    return TABLE(image('d88.jpg',88,88)+';'+
    TABLE('for more information,\ncontact:\n' + 
        xlink('Danbala Software', 'http://www.danbala.com')))
    
#---------------------------------------------------------------------------
#@contents_item{lpy configuration}

"""~ Here's the lpy specific bits
 this is getting a bit brutal...
 Navigator v Explorer v Layout options etc. etc.
 Maybe external style sheets would be better, though harder to distribute
    lpy-netscape.css
    lpy-explorer.css
    lpy-p-netscape.css
    lpy-p-explorer.css

The table mode layout was an interesting option;
maybe there is a simple wayt to make it a live option...
"""

STANDARDSCRIPT ='''
<script language="javascript">
var isNetscape = (navigator.appName.indexOf("Netscape") != -1);
var isExplorer = (navigator.appName.indexOf("Microsoft") != -1);
</script>
'''

def escape_quote(s):
    return string.replace(s, "'", "\\'")
    
def NetscapeOrExplorer(netscape, explorer):
    return '''
<script language="javascript">
if (isNetscape) {
    document.writeln(%s);
} else {
    document.writeln(%s);
}
</script>
''' % (escape_quote(netscape), escape_quote(explorer))
    
#~ Escaping in and out of HTML mode
# still worried about our extra blank line gas...

#

# terminology is bassackwards - leading/trailing wrap the special comment

# trailing opens a new code segment
html_trailing = '''<ul><div class="code"><pre>'''

# leading actually ends the open code segment

html_leading = '''</pre></div></ul>'''

# for split mode, alternative wrappers

split_starting = html_leading + '</td></tr></table><table><tr><td class="splitdoc">'
split_ending   = html_leading + '</td></tr></table><table><tr><td class="doc">'
split_leading  = html_leading + '</td></tr><tr><td class="splitdoc">'
split_trailing = '</td><td>'  + html_trailing


#~ html_prefix is what goes out at the top

# be careful of % signs in strings - use multiple strings instead of % format

html_start = '''<html><head><title>'''

# then title, plus:

stdprefix = '''</title>
<!-- html produced by lpy.py, http://www.danbala.com -->
<!-- this is the standard header -->
<style>
<!--
a:link { color:blue; text-decoration:none }
a:visited { color:purple; text-decoration:none }
a:active { color:red; text-decoration:none }
a:hover { color:red; text-decoration:none }
-->
</style>
<style>
<--
H3 {    /* need this for navigator */
   font: bold 14pt "Verdana", "Arial", "Helvetica" 
}
div.code { 
    background: #e0e0e0;
    font: 10pt "Courier New", "Courier", "Monaco" 
}
div.doc { 
    font: 10pt "Courier New", "Courier", "Monaco" 
}
td.doc { 
    width:600; 
    font: 9pt "Verdana", "Arial", "Helvetica" 
}
td.xref { 
    font: 9pt "Courier New", "Courier", "Monaco" 
}
table.xref { 
    font: 9pt "Courier New", "Courier", "Monaco" 
}
td.splitdoc { 
    width:50%; 
    font: 9pt "Verdana", "Arial", "Helvetica" 
 }
td.splitcode { 
    width:50%; 
    font: 9pt "Verdana", "Arial", "Helvetica" 
}
-->
</style>
</head>
<body><table><tr><td class="doc">''' + html_trailing

stdsuffix = html_leading + '</td></tr></table></body></html>'

printprefix = '''</title>
<!-- html produced by lpy.py, http://www.danbala.com -->
<!-- this is the -printing header -->
<style>
<!--
H3 {        /* need this for navigator */ 
    font: bold 10pt "Verdana", "Arial", "Helvetica" 
}
div.code { 
    font: 7pt "Courier New", "Courier", "Monaco" 
}
pre.code { 
    font: 7pt "Courier New", "Courier", "Monaco" 
}
td.doc { 
    width:600; font: 6pt "Verdana", "Arial", "Helvetica" 
}
td.xref { 
    font: 6pt "Courier New", "Courier", "Monaco" 
}
table.xref { 
    font: 6pt "Courier New", "Courier", "Monaco" 
}
td.splitdoc { 
    width:50%; font: 6pt "Verdana", "Arial", "Helvetica" 
}
td.splitcode { 
    width:50%; 
    font: 9pt "Verdana", "Arial", "Helvetica" 
}
-->
</style>
</head>
<body><table><tr><td class="doc">''' + html_trailing

def html_prefix(title):
    global gFlags
    if gFlags.printing:
        return html_start + title +printprefix
    return html_start + title + stdprefix
    
#~ html_suffix for End of file/cleanup:

def html_suffix():
    return stdsuffix

#@contents_item{side by side}

# lot's of guffing about for split mode

kSplitStart = 1
kSplitting = 2
kSplitEnd = 3

gSplitMode = 0
    
def startsplit():
    global gFlags, gSplitMode
    # do two positives make a negative? yeah, right
    if not gFlags.nosplits and not gSplitMode:
        gSplitMode = kSplitStart
    
def endsplit():
    global gSplitMode
    if gSplitMode:
        gSplitMode = kSplitEnd

def html_wrap(leading, trailing, s):
    global gSplitMode
    uselead = html_leading
    usetrail = html_trailing
    if gSplitMode:
        if gSplitMode == kSplitting:
            uselead = split_leading
            usetrail = split_trailing
        else:
            if gSplitMode == kSplitStart:
                uselead = split_starting
                usetrail = split_trailing
                gSplitMode = kSplitting
            elif gSplitMode == kSplitEnd:
                uselead = split_ending
                usetrail = html_trailing
                gSplitMode = 0
            if not leading:
                uselead = html_trailing + uselead
                leading = 1
            
    if leading:
        s = uselead + s
    if trailing:
        s = s + usetrail
    return s

#----------------------------------------------------------------

#~ Specific classes of tokens need special handling...
# those tokens come from module @imp{pytokens}
from pytokens import COMMENT, STRING, RESERVED

gPreAndPost = { 
    COMMENT   : ["<i><font color=green>","</font></i>"],
    STRING    : ["<font color=darkcyan>","</font>"],
    RESERVED  : ["<b>","</b>"]}

gWraps = { 
    COMMENT   : "<i><font color=green>%s</font></i>",
    STRING    : "<font color=darkcyan>%s</font>",
    RESERVED  : "<b>%s</b>"}

#----------------------------------------------------------------
#@contents_item{contents generator}
"""~
For manually constructing a table of contents
"""
_contents = {}

def reset_contents():
    global _contents
    _contents = {}

def reset_contents1(which="default"):
    global _contents
    _contents[which] = []
                          
def display_contents(which="default"):
    """ potential runaway recursion, be careful """
    global _contents
    content = _contents.get(which, None)
    if content:
        s = "<ul>"
        for item in content:
            s = '%s\n<li><a href="#%s">%s' % (s, item, item)
            if _contents.has_key(item):
                s = s + display_contents(item)
        s = s + "\n</ul>"
        return s
    return ""
    
def contents_item(c, which="default"):
    global _contents
    content = _contents.get(which,None)
    if content is None:
        content = []
        _contents[which] = content
    content.append(c)
    return '<a name="%s"><h3>%s</h3></a>' % (c, c)


