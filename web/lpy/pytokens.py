"""
        pytokens.py - specific enhancements to tokenize

not a standalone program, specifically for import

Interesting symbols:
        Parse(infile)       returns a list of tuples of
            (TOKENNUMBER, STRING, LINE, COLUMN)
        gTokenNames[]       strings for token numbers
        gNTokens            len(gTokenNames)
        gReservedWords{}    dictionary of reserved words : token number
        gReservedWordList[] simple list of reserved words
"""
#---------------------------------------------------------------------------

# specifically uses Python/lib/ token, tokenize, and keyword
# some of what is used isn't part of the 'published interface'

import tokenize
from token import *
from tokenize import tokenize, tok_name, NL, COMMENT
from keyword import kwlist

# some improvements to the token stuff from tokenize

gTokenNames = tok_name

WHITE    = NL + 1
RESERVED = WHITE + 1
gTokenNames[WHITE]    = 'WHITE'
gTokenNames[RESERVED] = 'RESERVED'
NEXT_TOKEN = RESERVED + 1

#---------------------------------------------------------------------------

# this is a global cause it might be handy from elsewhere
# dictionary for lookup speed
# numbers represent 'RESERVED+VALUE' for tagging reserved words
# instead of explicitly breaking out the reserved words above
# self isn't reserved, but it's in here anyways(?)  
# values in the initializer are bogus

gReservedWordList = []

gReservedWords = {}

def __fixupReserved():
    "add reserved words to gTokenNames on startup - don't call twice!"
    global NEXT_TOKEN, gTokenNames, gReservedWords, gReservedWordList
    gReservedWordList = kwlist[:]   # copy
    gReservedWordList.append('self') # debatable...
    gReservedWordList.sort()
    g = globals()
    for r in gReservedWordList:
        gTokenNames[NEXT_TOKEN] = r       # add reserved word to token list
        gReservedWords[r] = NEXT_TOKEN    # words[word] = token number
        x = 'TOKEN_' + r + '=' + str(NEXT_TOKEN)
        exec x in g
        NEXT_TOKEN = NEXT_TOKEN + 1       # one more token
        
__fixupReserved()

#---------------------------------------------------------------------------

class parsefile:
    """ manage an input file
        handle missing WHITE tokens by tracking raw input
        also provide an equivalent to readlines for reading raw input
    """
    def __call__(self, infile, constructor=None):
        """ initialize with the raw input file
            new contructor for a class instead of tuples only
        """
        self.lines = infile.readlines()
        infile.close()
        self.crow  = 0
        self.ccol  = 0
        self.cline = 0
        self.fResult = []
        self.constructor = constructor
        tokenize(self.readline, self.tokenizeCB)
        return self.fResult
        
    def readline(self):
        "input style"
        if self.cline < len(self.lines):
            l = self.lines[self.cline]
            self.cline = self.cline + 1
            return l
        return ""
            
    def skip(self, toRow, toCol):   #NIU?
        "in case we need to explicitly skip something"
        self.crow = toRow - 1
        self.ccol = toCol

    def through(self, row, col):
        "return data through row, col; possible multiple linefeeds?"
        row = row - 1   # off by 1
        ll = ""
        if row < self.crow:
            return ll
        if row == self.crow and col <= self.ccol:
            return ll
        r = self.crow
        while r <= row:
            if r >= len(self.lines):
                return ll
            l = self.lines[r]
            if r == row:
                l = l[:col]
            if r == self.crow:
                l = l[self.ccol:]
            ll = ll + l
            r = r + 1
        self.crow = row
        self.ccol = col
        return ll

    def tokenizeCB(self, type, token, (srow, scol), (erow, ecol), line):
        """tokenize calls us back on this method"""
        cr = self.crow + 1
        cc = self.ccol
        white = self.through(srow, scol)
        k = self.constructor
        res = self.fResult
        
        if white:
            cr = srow   # funkiness in tokenize...
            if k:
                res.append( k(WHITE, white, cr, cc, srow, scol) )
            else:
                res.append( (WHITE, white, cr, cc, srow, scol) )
        
        t = self.through(erow, ecol)
        if type == NAME:
            w = gReservedWords.get(token)
            if w:
                type = w
        
        if k:
            res.append( k(type, token, srow, scol, erow, ecol) )
        else:
            res.append( (type, token, srow, scol, erow, ecol) )

#---------------------------------------------------------------------------

def Parse(infile, k=None):
    " return a list of tuples from the infile (type, token)"    
    p = parsefile()
    return p(infile, k)

#---------------------------------------------------------------------------

# command line invocation; testing only

if __name__ == '__main__':  
    import sys
    if len(sys.argv) > 1: 
        files = sys.argv[1:]
        for fileName in files:
            p = Parse(open(fileName, 'r'))
            for t in p:
                if 0:   # standard test input == output
                    sys.stdout.write(t[1])
                if 1:   # alternative output
                    print (gTokenNames[t[0]], t[1], t[2], t[3], t[4], t[5])
    else: 
        print __doc__
    
