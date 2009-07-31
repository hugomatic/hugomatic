#!/usr/bin/python


"""~
    lpy.py - convert python source to formatted html

usage:
    lpy [-options(s)] filename(s)

writes:
    filename.html (beware!)

options:
    -autoformat = for processing python source with no formatting cues
    -autosplit  = inserts split directives automatically
    -nosplits   = disables split directives
    -noindex    = disable automatic index
    -printing   = uses smaller fonts

"""
"""~
@xlink('download lpy.zip', 'http://www.danbala.com/python/lpy/lpy.zip')

@danbala_logo
"""
__Id__ = "$Id: lpy.py,v 1.5 2000/05/18 21:14:56 dirck Exp $"

#---------------------------------------------------------------------------

#@reset_contents
#~@h3{Table of Contents}
#~@display_contents

#@contents_item{Introduction}
"""~

@b{lpy.py} is a tool for @b{code publishing} inspired by Knuth's
@xlink('Literate Programming', 'http://www.literateprogramming.com/')
concepts.  It's purpose is to make code presentable for reading.

Practically speaking, it's yet-another-Python-to-HTML too, with additions.

Other than regular Python colorizing, we're looking for some special stuff in 
comments and docstrings.  A comment or string starting with ~ is pulled
out and passed through a macro engine.  The macro engine looks for the @ sign
as a macro marker, using several syntaxes:

    @@symbol - can be a variable replacement or function call (no arguments)
    @@symbol{string} - call a function (or % a string) with one literal string
    @@symbol(args) - call a function with args
    @@{any Python code} - execute any Python
    @@(any Python expression) - evaluate any Python and display result

The Python functions invoked can return a result string or print (to sys.stdout).
 See @pylink{pymacro} for more information about the macro engine.

The macro set has some simplified html macros, like @@i{to italicize} 
@i{to italicize}, for example.  HTML is simple widely known, but it is 
@b{verbose}, and put lots of noise in the input stream.  
The macros are intended to make the source tidier.  See @pylink{htmlmax} for
information about the macro set.

We're also looking for comments or strings starting with @, which maps
to early instead of late execution.  The ~ stuff is processed on the way 
out (late), and the @ on the way in (early), so the @ directives occuring 
later in the source can affect the behavior of the ~ directives occurring 
earlier in the source.  The contents macros use this mechanism.

One other little thing - any comment starting with #- is replaced with <hr>.

@rem{------------------------------------------------------------------------
Here is the original discussion from a cpp2html program I've been playing with 
off and on for years...
@indent
I've become interested in the 'Literate Programming' Metaphor
that Knuth and some other academiacs are using.
The fundamental principle of literate programming is this:
"Programs should be written to be read by humans, not computers."

This is an important point, and it produces some interesting programs.
Some literate programming tools are WEB, CWEB, NUWEB, NOWEB, Funnel WEB, etc.
They are based on mixing the source and a macro-like facility with TeX and/or
LaTeX style document formatting commands.

While it seems pretty neat, there are a few fundamental problems for me:
@indent
TeX or LaTeX are unfamiliar (can be remedied)

There are no WEB like tools in my development environment (can be remedied)

The difference between the source I see, and the source the
compiler sees, causes problems:
    IDE's are cool, quick turnaround is cool, etc.  An intermediate step kills this.
    Trying to debug intermediate/generated code isn't cool.  It can be very tedious.

The source I work on, not just print or browse, ought to be
readable as well, without lots of cryptic stuff in it.
@outdent
@outdent
------------------------------------------------------------------------}
Traditional LP involves writing a mixture of formatting and code, 
and then extracting the program and document from the source using 
separate programs ('tangle' and 'weave').

The term inverted literate programming describes producing the document from
the actual program source code instead of from a separate source file.
That's what this tool does.  The concept of having to preprocess
a Python script file in order to execute does seem perverse.

There are other useful approaches to LP - eventually there could be
a wysiwyg / hyperlinked / outlining / structured / browser 
coding-and-documenting environment that really @i{understands} the program, 
in order to help the programmer or reader make sense out of it.

This tool is a lot less ambitious, it's simply to help me
write better code.  Writing readable programs is more fun
(and more difficult and time-consuming).

@rem{--------------------------------------------------------------------
@h3{To Do etc.}
Still having some problems with blank lines in the output,
both with and without line numbers.

Some auto/push/pop stuff for htmlishness would be cool

Still putting out spurious line numbers on lines with only white space
End of file has a couple of extra line numbers.

Macro arguments on the command line - for example -printing could
set up different fonts when printing.

A shortcut for #x involving in place macro substitution without leaving 
<pre> mode might be cool for sticking links and stuff in inline comments.
The DOC mode stuff is neat but tends to be vertically gassy (even if/when
the too many blank lines thing is sorted)

A single syntax for doing both early and late execution might be interesting?

Comprehensive indexing of the file would also be useful;
function, class, and method Table of contents (with extracted doc strings!)
at the top of the output, with a full cross reference at the bottom;
Handling import via hyperlinks would be cool.
However, the dynamic nature of Python can make it difficult to know which
symbol actually lives where...

Style sheets are in use to produce easily formatted results.
Javascript maybe useful for making the output live in terms of show/hide
outlining type of stuff.  More on the to do list...

One major advantage of traditional LP is the macro facility, with
long descriptive names for macros, and crucially, @b{open} macros
that allow accumulating stuff into the macro in various places, without
having to define everything at once.  This can make the presentation
more coherent.  Maybe we could work out a way to invert this, too.

Hmm... need a comment comment to hide stuff in the output
    @i{...hidden stuff...}
@rem{
Some of the original babble-style notes from this program:
 presentable python including formatting-independent stuff, i.e.,
 it should be possible to produce html/rtf/tex etc. from the same .py file
 what are the pieces?
 we'd probably like a TOC up top with sections and subsections
 with top level def's listed in each
 followed by the actual processed stuff
 followed by a function & class cross reference and full index of symbols
 any use of a symbol could link to its index entry?
 all line numbers are possible targets..
 we'd like links out form import statements where possible
 links forward from the toc...
 hard and soft formatting... < and & off and on...
 we can link to stuff flipped in the pymacro module to check modes...
 or install our own stuff in it?  how?
apparently free standing strings are valid Python comments,
 which eliminate the fun #~ #~ stuff over and over... 
  not sure what it does to the python object code.

The HTML stack stuff from dbmodel might be useful;
 automatically pop the stack at the end of the special stuff...
  we need pre/post...
Gotta go back and sort that...
------------------------------------------------------------------}
}
"""
#-
"""~
Order of presentation is important, and Python is pretty flexible,
because stuff doesn't have to be defined until executed.

Imports should come first - using @tt{from module import *}, 
our symbols can get stomped on.
"""

#@contents_item{Imports}

"""~The traditionally useful 
@xlink('Python standard library', 
       'http://www.python.org/doc/current/lib/lib.html') 
items, @stdlink{sys} and @stdlink{string} stuff:"""

import sys      # we're using sys.argv
import string   # and some string manipulations

"""~ @pylink{pytokens} is based on tokenize from the standard library,
but it adds a few useful items..."""

from pytokens import *
#Parse, WHITE, NEWLINE, NL, INDENT, DEDENT, OP, COMMENT, STRING, RESERVED

#~ @pylink{pymacro} is the module responsible for our 'macro language facility'

import pymacro

"""~@pylink{htmlmax} is the module that contains the actual html macros we're 
using, so let's get @pylink{pymacro} to load it for us...
"""
pymacro.load('htmlmax')

"""~ @pylink{htmlmax} is used to separate the actual html formatting specs from
this module, to make it easier to customize.
Sneaky -> the stuff got loaded into @pylink{pymacro} by the line above.
It could have been loaded separately to keep the pymacro name space clean,
but it's handier in there, anyway.
"""

from pymacro import html_prefix, html_suffix, html_wrap, gWraps

#---------------------------------------------------------------------------

#~@rem{startsplit}

#@contents_item{main}

"""~Now we can define our main program.  It processes
command line arguments, -macros and filenames, feeding macros to
@pylink{pymacro} and passing filenames to PyToHTML.

Invoked without arguments, print the __doc__ string as the usage message.
"""

def main(argv):
    "for command line invocation - gimme sys.argv[1:]"
    if not len(argv): 
        print __doc__   # usage info
        return
    
    for arg in argv:
        if arg[0] == '-':   # command line - convert to @
            s = pymacro.pymax_process('@SetFlag{'+arg[1:]+'}')
            if s:           # report any output
                print s
        else:
            PyToHTML(arg, arg+".html")

#~ PyToHTML is the function that actually does the 'work'...

def PyToHTML(inputfilename, output):
    """Convert a Python file to an HTML file"""
    
    #~Open Files

    input  = open(inputfilename, 'r')
    #output = open(outputfilename, 'w')
    
    #~Make sure Token class is ready, then Parse into Tokens @N
    #~Parse calls us back and returns a list of our results
    
    Token_ClassInit()
    tokens = Parse(input, Token)
    
    #~Write out the html prefix, with title @N
    #~Write out all the Tokens as html @N
    #~Write out the html suffix    
    #~Write out the cross reference
        
    output.write(html_prefix(inputfilename))
    if Token.autosplit:
        output.write(pymacro.pymax_process('@startsplit'))
    for t in tokens:
        output.write(t.asHTML())    
    output.write(html_suffix())
    if Token.autosplit:
        output.write(pymacro.pymax_process('@endsplit'))
    if not pymacro.TestFlag('noindex'):
        output.write(Token.xref.asHTML())
    
"""~ What did we use there that we haven't defined yet?
    Parse comes from pytokens,
        html_prefix, html_suffix comes from htmlmax (via pymacro)...
    
    class Token and helper function Token_ClassInit
"""

#---------------------------------------------------------------------------
"""~
@rem{ end braces don't nest in pymacro, do they?
So, whats a good theory here?
We have lots of nice little tokens in a list
we'd like to locate some specific definitions
(global, import, function, class, and method)
as well as locating the doc strings and the special pass through stuff
it would be helpful to know some specific stuff for each token
indent level, paren level, block level, first on line, 'inside' item...
hmm...  normal parsers like to construct trees of stuff...

what is our purpose?
    table of contents with doc strings
    def X([parms]):
        ["docstring"]
    class X[(x)]:
        ["docstring"]
        def X():
            ["docstring"]
 docstring is first string after : of definition
 replacing special stuff
 index at the bottom
}
"""

#@contents_item{Token class}
#@{def token_item(X): return contents_item(X, 'Token class')}
#@token_item{Token_ClassInit}

def Token_ClassInit():
    """~ Create/re-initialize Token's class variables """
    
    Token.previous = 0      # for tracking our linked list
    Token.indentlevel = 0   # for tracking syntax levels
    Token.parenlevel = 0
    Token.bracketlevel = 0    
    Token.bracelevel = 0    
    Token.afternewline = 1  # if we came right after a newline
    Token.firstonline = 1   # need to know if we are the first real item

    # options:                            
    Token.autoformat = pymacro.TestFlag('autoformat')
    Token.autosplit = pymacro.TestFlag('autosplit')
    Token.xref = XRef()     # symbol cross reference

"""~ Token is @b{the} class...
Token is responsible for:
@UL{
Tracking each code element,
determining if it is 'special' and needs to be passed to the pymacro engine
syntax coloring of STRING, COMMENT, and RESERVED words,
Line numbers, and other HTML formatting}
"""

class Token:
    """ Token items are spewed out by the pytokens module """
    
#@token_item{Token.__init__}
#~@startsplit
    """~ The constructor does most of the work.

It is abnormally large, and should be broken into sub functions...
but it's quicker inline.

We track all of the info from tokenize,
as well as maintaining a doubly linked list of the tokens for looking around.
We're also tracking indentlevel, parenlevel, and bracketlevel
which is important for understanding the structure of the Python code.
We're only looking for 'special' strings if they are first on the line, 
which we don't know unless we know parenlevel etc. 
"""
    def __init__(self, type, token, srow, scol, erow, ecol):
        
        #~ Pick up our token info

        self.type = type
        self.token= token
        self.line = srow
        # scol, erow, ecol, not in use
            
        #~ Stitch up our linked list

        self.next     = None
        self.previous = Token.previous
        if Token.previous:
            Token.previous.next = self
        Token.previous = self

        #~ Remember our level info        
        self.indentlevel  = Token.indentlevel
        self.parenlevel   = Token.parenlevel
        self.bracketlevel = Token.bracketlevel
        self.bracelevel   = Token.bracelevel

        #~ Do all of the level tracking maintenance
        if type == INDENT:
            Token.indentlevel = Token.indentlevel + 1
        elif type == DEDENT:
            Token.indentlevel = Token.indentlevel - 1
        elif type == OP:
            if token == '(':
                Token.parenlevel = Token.parenlevel + 1
            elif token == ')':
                Token.parenlevel = Token.parenlevel - 1
            elif token == '[':
                Token.bracketlevel = Token.bracketlevel + 1
            elif token == ']':
                Token.bracketlevel = Token.bracketlevel - 1
            elif token == '{':
                Token.bracelevel = Token.bracelevel + 1
            elif token == '}':
                Token.bracelevel = Token.bracelevel - 1

        #~ Figure out if we're white space, for future reference

        self.isWhite = type in (WHITE, INDENT, DEDENT, NEWLINE, NL)

        #~ Worried about newline:
        #~ isNewLine means we're a single literal new line character,
        #~ but isAfterNewLine means previous item could have also been comment, etc.

        self.isAfterNewLine = Token.afternewline
        self.isNewLine = type == NL or type == NEWLINE
        
        #~ Set up afternewline for the Next token
        Token.afternewline = token and token[-1] == '\n'

        #~ Looking for first string on line as possible special comment

        self.isFirstString = 0
        if type == STRING and Token.firstonline:
            if not (self.parenlevel or self.bracketlevel or self.bracelevel):
                self.isFirstString = 1

        #~ For automatic formatting without explicit ~, add it in,
        #~ and preserve existing formatting by adding @@N (<br>) directives
        if Token.autoformat:
            if Token.firstonline:
                if self.isFirstString and len(token) > 2:
                    if token[0] == token[1]:
                        if token[3] <> '~':
                            token = token[0:3] + '~' + token[3:]
                    elif token[1] <> '~':
                        token = token[0] + '~' + token[1:]
                    token = string.replace(token, "\n", "@N\n")
                elif type == COMMENT:
                    if token[1] <> '~' and token[1] <> '-':
                        token = '#~'+token[1:]
                    token = string.replace(token, "\n", "@N\n")
        
        #~ Set up firstline for the Next token
        if Token.afternewline or type == DEDENT or type == INDENT:
            Token.firstonline = 1
        elif type <> WHITE:
            Token.firstonline = 0
            
        #~ Special defaults
        
        self.isSpecial = 0
        self.preprocessed = 0

        #~ Quick hack for division lines - beware of #- with other stuff

        if type == COMMENT:
            if len(token) > 1 and token[1] == '-':
                self.isSpecial = "<hr>"
                self.preprocessed = 1
                self.token = ""

        #~Look for specially marked boxes of your favorite serial
        # this isn't quite as brutal as it looks

        if type == COMMENT and len(token) > 2:
            if token[1] == '~': 
                self.isSpecial = token[2:]
            elif token[1] == '@':  # early v late execution
                self.isSpecial = pymacro.pymax_process(token[1:])
                self.preprocessed = 1
                self.token = ""
        elif self.isFirstString and len(token) > 2:
            if token[1] == '~':
                self.isSpecial = token[2:-1]
            elif token[0] == token[1] and token[3] == '~':
                self.isSpecial = token[4:-3]                
            elif (token == 
'~this is a test'):    # this is a test to make sure we don't grab this
                pass

        """~
Worrying about the extra blank lines.

If we look backward and ignore any white space
(including INDENT/DEDENT/NEWLINE/NL etc.)
and the first thing we find is also 'special',
then tell him to forget trailing wrapping,
and tell me to forget leading wrapping.
"""

        if self.isSpecial:
            # drop leading space, just because
            if self.isSpecial[0] == ' ':    
                self.isSpecial = self.isSpecial[1:]
            
            self.leading = 1
            self.trailing = 1
            previous = self.previous
            while previous:
                if previous.isWhite:
                    previous.type = WHITE
                    previous.token = '' # clear 
                    previous = previous.previous
                else:
                    if previous.isSpecial:
                        previous.trailing = 0
                        self.leading = 0
                    break

        """~
Also look forward to get rid of extra white space/new lines following special.
Handled by looking back from newline instead.

"""

        if self.isNewLine:  # look back for last special
            previous = self.previous 
            while previous:
                if previous.isWhite:
                    previous = previous.previous
                else:
                    if previous.isSpecial:
                        self.token = ''
                        # walk back forward looking for white
                        previous = previous.next
                        while not previous is self:
                            if previous.type == WHITE:
                                previous.token = ''
                            previous = previous.next
                    break

        #~ Maintain symbol cross reference for the summary Index

        if type == NAME:
            Token.xref(token, srow)

        #~ Trim the extra lines and white space at the end of the program

        if type == ENDMARKER:
            previous = self.previous 
            while previous:
                if previous.isWhite:
                    previous.type = WHITE
                    previous.token = ''
                    previous = previous.previous
                else:
                    break

#~@endsplit

#@token_item{Token.asHTML}
    """~ Render as HTML
    
Some oddities remain with special:
 1) Leading spaces are always present for indented strings
 2) Whether or not to autohtml and/or escapes4html isn't obvious when/if.
    escape is appropriate on original text but not on macro output;
    autohtml is appropriate on original text without expansions...
"""

    def asHTML(self):
        """ render this Token asHTML """

        s = self.isSpecial # well, isn't that special?
        if s:
            if not self.preprocessed:
                s = autohtml(pymacro.pymax_process(escapes4html(s)))
            if 0:   # doesn't work as well as hoped - dedents come too late
                t = self.indentlevel + 1
                if self.indentlevel:
                    s = '<ul>' * t + s + '</ul>' * t
            return html_wrap(self.leading, self.trailing, s)
            
        s = ""
        # put out the line numbers
        if (self.token or self.type==DEDENT) and self.isAfterNewLine:
            s = ('<a name="%d">%4d</a>    ' % (self.line, self.line))

        type = self.type
        token = self.token
        if type > RESERVED:
            type = RESERVED
        wrap = gWraps.get(type,None)

        # check for strings with embedded newlines
        if type == STRING and string.count(token, '\n') > 1:
            t = escapes4html(string.join(
                               string.split(token, '\n'), '\n        '))
            if wrap:
                t = wrap % t
            s = s + t + '\n'
        else:
            t = escapes4html(token)
            if wrap:
                t = wrap % t
            s = s + t
        return s

#---------------------------------------------------------------------------

#@contents_item{XRef class}

"""~ The XRef class does simple symbol tracking.  
It remembers every name/line combination submitted (tossing duplicates) 
in order to render an HTML-formatted Index listing.
The indexes are too gassy by line number.  Some close-enough
value could be used for congregating lines.
Section numbers might be a better plan.
"""

class XRef:
    """ XRef maintains a cross reference of symbols by line number """
    
    def __init__(self):
        """~ build the empty symbol table """
        self.symbols = {}
                
    def __call__(self, token, line):
        """~ add a symbol reference """
        symbols = self.symbols
        if symbols.has_key(token):
            if not symbols[token].count(line): # already on this line
                symbols[token].append(line)
        else:
            symbols[token] = [line]
        
    def asHTML(self):
        """~ render the table as html """
        refs = self.symbols
        # two columns, each containing a table of two columns
        r = '<hr><ul><table><tr><td valign=top><table>'
        nk = refs.keys()
        nk.sort()
        bp = (len(nk) + 2) / 3
        i = 0
        for n in nk:
            if i and i % bp == 0:
                r = r + '</table></td><td valign=top><table>'
            i = i + 1
            r = '%s<tr><td valign=top class="xref">%s</td><td valign=top class="xref">' % (r, n)
            s = ''
            for l in refs[n]:
                s = '%s <a href="#%d">%d</a> ' % (s, l, l)
            r = r + s + '</td></tr>\n'
        r = r + '</table></td></tr></table></ul>'
        return r

#---------------------------------------------------------------------------
#@contents_item{autohtml}
"""~@b{autohtml} tries to do some best guess formatting of the html.
We'd like to have 'pretty good' formatting without too many directives.
Two \n in a row is a paragraph
\n followed by white space is a line break with leading &nbsp chars.
Anything else useful I can think of?

"""

def autohtml(s):
    s = string.join(string.split(s, '\n\n'), '\n<p>\n')
    
    while 1:
        i = string.find(s, '\n ')
        if i >= 0:
            # beware of pseudo-blank lines and all space lines
            c = 1
            x = i + c + 1
            l = len(s)
            while x < l and s[x] == ' ':
                c = c + 1
                x = x + 1
            if i > 0 and s[i-1] == '>': # watch for <p><br>
                s = s[0:i+1] + c * "&nbsp;" + s[i+c+1:]
            else:
                s = s[0:i] + "<br>\n" +  c * "&nbsp;" + s[i+c+1:]
        else:
            break
         
    #s = string.join(string.split(s, '\n '), '\n<br>&nbsp;')
    return s

#@contents_item{escapes4html}

def escapes4html(s):
    return string.replace(string.replace(s,'&','&amp;'),'<','&lt;')

'''~@rem{
#---------------------------------------------------------------------------
"""~ This is a simple 'functor' construction class.  Build an object that
does simple string substitution.  We need it for handling < and & in the 
literal code space"""
class Replacer:
    """A Replacer object knows how to escapes4html one set of strings for another"""    
    
    def __init__(self, listOfPairs):
        self.replaceList = listOfPairs
    
    def __call__(self, s):
        for r in self.replaceList:
            s = string.replace(s, r[0], r[1])
        return(s)

"""~ and here we use it to make @b{escapes4html} - 
 a subsitution functor for cleaning literals for html"""

escapes4html = Replacer([('&', '&amp;'), ('<', '&lt;')])
#---------------------------------------------------------------------------
#~ these little bits are under construction

"""~ hmm; maybe i need to push a stack of class/def etc.
    something in order to correctly handle indent/dedent;
    got to think in terms of purpose first...
"""

def classes(tset):
    "how useful is this?"
    cset = []
    for t in tset:
        if t.token == 'class':
            cset.append(t)

def defs(tset):
    "how useful is this?"
    dset = []
    for t in tset:
        if t.token == 'def':
            dset.append(t)            
}
'''
#---------------------------------------------------------------------------
#@contents_item{Kick Off}
#~ Pass command line arguments to main

#if __name__ == '__main__':  
#    main(sys.argv[1:])

#~@rem{endsplit}
#@contents_item{Index}

