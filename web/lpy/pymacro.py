"""~
        pymacro.py - text macros in python

Using embedded python as a macro language.
In a sense, this is a bit like php or asp - the text goes straight
through, except for @ signalled stuff, which can be processed 
in a variety of ways.  It's not the same in the sense that asp/php
have an implied structure across boundaries; 
an example would be instructive.

"""
#~@danbala_logo
__Id__ = "$Id: pymacro.py,v 1.9 2000/05/18 21:14:56 dirck Exp $"

#@reset_contents
#~@h3{Table of Contents}
#~@display_contents

#---------------------------------------------------------------------------

#@contents_item{Introduction}

"""~
macro syntax:
    
    @# double @ present for fancy formatting from lpy
    @# read them as single @ when looking at the source
    
    direct evaluation
        @@(python expression)
    
    direct execution
        @@{python code}
    
    indirect evaluation
        @@function(parameters...)
    
    implied string parameter
        @@function{a string without quotes}
    
    alternative string delimeters:
        @@function/almost any delimeter/

    to end of block/of text (depending on context)
        @@function:to end of text

    comment to end of line:
        @@#comment    

    single symbol - evaluated or executed (no () needed for 0 parm functions)
        @@symbol - looks for and doesn't eat white space after
        use @@symbol@@ if white space isn't desired
        
    assignment syntaxes:
        as a shortcut for
            @@{symbol='string'} or @@{symbol=integer}
        to white space, which is eaten, assumed to be string unless all digits
            @@symbol=value    
        can also use quotes (single or triple of either):
            @@symbol='string'
        also:
            @@symbol=(expression)
            
    needed(?): a way for a macro to eat input outside itself
    setup an implied read like the implied write?
    some other way: primarily for @@iflike macros?
    
    needed(?):
    another syntax? for what? dictionaries and list access/assignment
        @@symbol[X]
        @@symbol[X]=value
    multiple string parameters?
        @@xlink{danbala|http://www.danbala.com}

Was using re to find the brackets and parentheses, which isn't constructive
due to nesting issues.  _find_matching implemented instead.
                       
"""

#---------------------------------------------------------------------------
#@contents_item{Imports}
#~ All standard python: @stdlink('sys', 'string', 're', 'traceback', 'cStringIO')
#@#cool if that was automatic in  the code itself;
#@# requires a dictionary of stdlib modules

import sys
import string
import re
import traceback
from cStringIO import StringIO

#@contents_item{Globals}

_prefix = '@'                    # macro _prefix

# kind of a loose definition of symbol, so what
symbol_match = r"[A-Za-z_][A-Za-z0-9_\.]*"
integer_match = r"[0-9]+"

_re_white = re.compile("\s")
_re_symbol = re.compile(symbol_match)
_re_integer = re.compile(integer_match)

# be careful, macros execute in this name space

_g = globals()
_l = _g

write = sys.stdout.write

#---------------------------------------------------------------------------
#@contents_item{pymax_process - public}

def pymax_process(line):
    temp = sys.stdout
    out = StringIO()    # in case somebody prints
    sys.stdout = out
    try:
        _process(line, out)
        line = out.getvalue()
    except:
        line = pymax_excepted('pymax_process', line)
    sys.stdout = temp
    return line

#---------------------------------------------------------------------------
#@contents_item{_process: primary internal function}

def _process(line, out):
    #~ so macro code can 'write' without worrying about to where
    
    global write    
    write = out.write
    
    #~ repeatedly
    while 1:

        #~ look for prefix
        pos = string.find(line, _prefix)
        
        #~ not found, done
        if pos < 0:
            write(line)
            break
        
        #~ get the next char    
        p = pos + 1
        c = line[p]
        
        #~ watch for double 'escaped' prefix
        if c == _prefix:
            write(line[:p])
            line = line[p+1:]
            continue
        #~ ignore free standing prefix
        elif c == ' ':
            write(line[:p])
            line = line[p:]
            continue
        
        #~ chop off the front, write it out
        write(line[:pos])
        line = line[p:]
        
        #~ look at the next character - special cases
        if c == '{':    # exec anything
            ep = _find_matching(line, 0, '{', '}')   # not necessary?
            v = pymax_exec(line[1:ep-1])
        elif c == '(':  # eval anything
            ep = _find_matching(line, 0, '(', ')')   # necessary!
            v = pymax_eval(line[:ep])
        elif c == '#':  # comment to end of line
            ep = _must_find(line, '\n', 0)
            v = ''
        
        #~ @b{symbol case}
        else:           # symbol + something?
            m = _re_symbol.match(line)
            #~ not a symbol?
            if not m:
                #if line[0] == '\n':
                line=line[1:]   # ignore one (\n?) character after the @??
                continue    # or complain?
            
            #~ handle symbol
            p = m.end()
            s = line[:p]
            c = line[p]
            
            #~ followed by...
            if c == '{':        # single string
                ep = _find_matching(line, p, '{', '}')
                v = _do(s, line[p+1:ep-1])
            elif c == '(':      # parameter list
                ep = _find_matching(line, p, '(', ')')   # necessary!
                v = pymax_eval(line[:ep])
            elif c == ':':      # to EOF
                ep = 0
                v = _do(s, line[p+1:])
                line = ''
            elif c == '=':      # assignment
                ep, v = _assign(s, line, p+1)
            elif c == '@':      # standalone, abutted
                ep = p+1
                v = pymax_eval(s)
                if callable(v):
                    v = v()
            elif c in string.whitespace:    # standalone
                ep = p
                v = pymax_eval(s)
                if callable(v):
                    v = v()
            else:               # single string, arbitrary delimeter
                ep = _must_find(line, c, p+1)
                v = _do(s, line[p+1:ep-1])
        
        #~ write the result, and strip out the eaten stuff, continue
        
        if v is None:
            v = ''
        write(str(v))
        line = line[ep:]  # ep points after the last et char
#---------------------------------------------------------------------------
#@contents_item{_assign: handle assignment}

def _assign(s, line, p):
    if line[p] == '"':
        if line[p+1] == '"':
            ep = _must_find(line, '"""', p+3) + 2
        else:
            ep = _must_find(line, '"', p+1)
        v = pymax_exec(line[:ep])        #assuming s @ line[0]
            
    elif line[p] == "'":
        if line[p+1] == "'":
            ep = _must_find(line, "'''", p+3) + 2
        else:
            ep = _must_find(line, "'", p+1)
        v = pymax_exec(line[:ep])        #assuming s @ line[0]
    
    elif line[p] == '(':
        ep = _find_matching(line, p, '(', ')')   # not necessary?
        v = pymax_exec(line[:ep])        #assuming s @ line[0]
    
    else:
        m = _re_white.search(line, p)
        if not m:
            ep = len(line)
        else:
            ep = m.end()
        if _re_integer.match(line[p:ep]):
            v = pymax_exec(line[:ep])        #assuming s @ line[0]
        else:   # assume it's a string
            v = pymax_exec( s + '=' + '"""' + line[p:ep] + '"""' )
    
    return ep, v

#---------------------------------------------------------------------------

#@contents_item{Utility functions}

def pymax_excepted(f, l):
    """ error wrapping """
    t = sys.exc_info()
    s = string.join(traceback.format_exception(t[0], t[1], t[2])) + "\nFor: " + l
    # report to stderr as well
    sys.stderr.write(s)
    return s

def pymax_eval(line):
    """ eval with error wrapping """
    try:
        return eval(line,_g,_l)
    except: 
        return pymax_excepted('pymax_eval', line)

def pymax_exec(line):
    """ exec with error wrapping """
    try:
        exec line in _g, _l
        return ''
    except:
        return pymax_excepted('pymax_exec', line)

def _must_find(s, e, p=0):
    """ puke if not found """
    ep = string.find(s, e, p)
    if ep < 0:
        raise "NoMatching", e
    return ep+1
    
def _find_matching(s, p, b, e):
    """ handle nesting () and {} """
    nb = 1
    ne = 0
    p = p + 1
    while ne < nb:
        ep = string.find(s, e, p)
        if ep < 0:
            raise "NoMatching", e
        nb = nb + string.count(s, b, p, ep)
        ne = ne + 1
        p  = ep + 1
    return ep+1 # next char

def _do(v, p):
    """ one symbol with one string parameter """
    try:
        v = pymax_eval(v)
        if callable(v):
            return v(p)
        else:   # auto format % string
            return v % p
    except:
        return pymax_excepted('_do', p)

#---------------------------------------------------------------------------

#@contents_item{macros}

# maybe 'using' or something for import X?

def load(s):
    s = 'from %s import *' % s
    pymax_exec(s)
    return ''

#---------------------------------------------------------------------------
#@contents_item{main - for testing}
    
if __name__ == '__main__':  
    import fileinput
    import string
    lines = []
    for line in fileinput.input():
        lines.append(line)     
    print pymax_process(string.join(lines, ''))

