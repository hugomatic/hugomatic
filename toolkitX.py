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


import sys    # system library
import getopt # command line argument parser
import cPickle as pickle
import inspect
import os # path split
import operator
import datetime
import re





# Exception class for program arguments errors
class ParamsError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class RedirectStdOut:       
        
        def __init__(self, stdout):
            self.stdout = stdout
            self.debugLine = -1
            self.printLineCounter = 0
            self.callback = None
            
        def setDebugLine(self, debugLine, callback):
            self.debugLine = debugLine
            self.callback = callback
            
        def write(self,s):
            lines = str(s).splitlines()
            if len(lines) > 1:
                for l in lines:
                    self.write(l)
                    self.write('\n')
            else:        
                k = str(s)    
                if k == '\n':
                    self.printLineCounter += 1
                    #nb = '(' + str(self.printLineCounter) + ' * )' 
                    nb = ""
                    self.stdout.write( nb +'\n')
                else:
                    l = len(k)
                    if l != 0:
                        lineStr = ""
                        #lineStr         += '(' + str(self.printLineCounter + 1) + ')' + " "
                        self.stdout.write(lineStr + s)
                if self.printLineCounter == self.debugLine:
                    if self.callback:
                        cb = self.callback
                        cb()
                        self.debugLine = -1
                    else:
                        self.stdout.write ("(----- debugStop! line: %d ----- ERROR: no callback defined!)" % self.printLineCounter )

class Parameters:
    
    def __init__(self, name, desc, picture_file = "", debug_callback = None, debug_line = -1):
        self.history = [] # A list of previous loaded values entered by the user 
        self.name = name
        self.desc = desc
        self.argumentsDict = Odict()
        self.shortDict = dict()
        self.printLineCounter = 0
         # image for the dialog, or leave empty
        self.pictureFile = picture_file
        
        frame = inspect.currentframe().f_back
        self.globalValues = frame.f_globals
        
        frameInfo = inspect.getframeinfo( frame )
        self.fileName = frameInfo[0]
                
        # debug line and call back stuff
        self.debug_callback = debug_callback
        self.old_stdout = None
        if self.debug_callback:
            self.old_stdout = sys.stdout
            sys.stdout = RedirectStdOut(self.old_stdout)
            sys.stdout.setDebugLine(debug_line, self.debug_callback)
            
    def setDebugLine(self, debugLine, callBack = None):
        if callBack:
            self.debug_callback = callBack
            cb = self.debugCallbac
        if self.debug_callback:        
            sys.stdout.setDebugLine(debugLine, self.debug_callback)
      
    def getRelativePath(self, name):
        fn = name
        return fn   
                
    def setValue(self, name, newValue):
        
        t = type(self.globalValues[name])
        if t == int:
            self.globalValues[name] = int(newValue)
        else: 
            if t == bool:
                self.globalValues[name] = bool(newValue)
            else:
                if t == float:
                    self.globalValues[name] = float(newValue)
                else:
                    self.globalValues[name] = newValue
              
    def getTileAndDesc(self):
        s = self.name + ": " + self.desc
        return s
    
    def addAttribute(self, argName, attName, attValue):
        self.argumentsDict[argName][attName] = attValue
    
    def getValue(self,name):
        return self.globalValues[name]
        
    def getDefault(self, name):
        return self.getAttributeValue(name, 'default')
    
    def getAttributeValue(self, argName, attName):
        if self.argumentsDict.__contains__(argName):
            if self.argumentsDict[argName].__contains__(attName):
                return self.argumentsDict[argName][attName]
        return None
    
    def getCmdLine(self):

        s = self.fileName + " "
        for k in self.argumentsDict.keys():
            value = self.globalValues[k]
            v = str(value)
#            if v.count(' ') > 0:
#                v = '"' + v + '"'
            s += "--" + k + " " + v + " "
        return s    
    
    def usage(self):
        usage = "Script: " + self.fileName + "\n\n"
        usage += self.getTileAndDesc() + "\n\n"
        nothing, name = os.path.split(self.fileName)
        usage += "Usage: python " + name +" [OPTION]...\n"
        usage += "   OPTIONS\n" # + self.name + " [OPTIONS] \n" + self.desc + "\n"
        for k,v in self.argumentsDict.iteritems():     
             usage += "   "
             if v.__contains__('short'):
                  usage += "-"+v['short'] + ", "
             usage += "--" + k
             if type(v['default']) != bool:
                usage += ' = "' + str(v['default']) + '"'
             usage += ": " + v['title']
            
             if v.__contains__('help'):
                helpStr = str(v['help'])
                usage += " (" + helpStr + ")"
             usage += "\n"
        usage += "   OTHER OPTIONS\n"
        usage += "   --help: displays this message\n"
        usage += "   --no-gui: When no other options are specified, hides the gui and stays in cmd line mode\n"

        return usage
    
    def shortFormArgString(self):
        short = ""
        #values = self.getValues()
        for k,v in self.argumentsDict.iteritems():
            if v.has_key('short'):
                short += v['short']
            v = self.getValue(k) #values[k]
            if type(v) != bool:
                short += ':'
        return short
    
    def longFormArgList(self):
        args = list()
        for k,v in self.argumentsDict.iteritems():
            s = ""
            s += str(k)
            v = self.getValue(k)
            if type(v) != bool:
                s += '='
            args.insert(0,s)    
        return args    

    def loadParams(self):
        def printCmd(cmd):
            cmds = cmd.split("--")
            print "(" + cmds[0] + ")"
            i = 1
            while i < len(cmds):
                s = cmds[i]
                niceStr = s.replace("(", "-")
                niceStr = niceStr.replace(")", "-")
                niceStr = niceStr.replace("\n","\\n")
                print "(--"+ niceStr +")"
                i = i+1
                
        resp = False
        args = sys.argv[1:]
        l = len(args)
        if l > 0 :
            resp = self.__parseArgs(args)
        else: 
            resp = self.__showDialog()
        if resp:
            printCmd(self.getCmdLine())    
        return resp
            
    def __showDialog(self):
        from toolkitTk import ParameterGui
        self.__autoLoad()    
        values = Odict()
        titles = dict()
        defaults = dict()
        choicesDict = dict()
        filePathDict = dict()
        for k in self.argumentsDict.keys():
            title = self.getAttributeValue(k, 'title')
            titles[k] = title
            value = self.globalValues[k]
            values[k] = value
            default = self.getAttributeValue(k, 'default')
            defaults[k] = default
            choices = self.getAttributeValue(k, 'choices')
            choicesDict[k] = choices
            isPath = self.getAttributeValue(k, 'filePath') == True
            filePathDict[k] = isPath
        
        path = inspect.getfile(Parameters)
        tail,head =  os.path.split(path)
        rootDir, pyDir = os.path.split(tail)
        imageDir = os.path.join(rootDir, "images")
        picturePath = None
        if len(self.pictureFile) > 0:
            picturePath = os.path.join(imageDir, self.pictureFile)
        withDebugLine = self.debug_callback != None
        dialog = ParameterGui(self.getTileAndDesc(), values, titles, defaults, choicesDict, filePathDict, self.usage(), withDebugLine, picturePath, self.history)
        dialog.mainloop()
        if dialog.okButtonHasBeenPressed:
            if dialog.clearButtonHasBeenPressed:
                self.__deleteAutosaveFile()
            if self.debug_callback:
               debugLine = dialog.getDebugLine() 
               self.setDebugLine(debugLine)
            vals = dialog.getChangedValues()
            changes = len(vals) > 0
            if changes == True:
                   for k in vals:
                       v = vals[k]
                       self.setValue(k,v)
                   self.__autoSave()
            return True
        else:
            print "(Cancelled by the user)"
            return False
    
    def __getInifile(self):
        fileName = self.fileName
        tail,head =  os.path.split(fileName)
        if len(tail) == 0:
            tail = "."
        ext = ".ini"
        fileName = tail + '/' + head.replace('.py', ext)
        return fileName
    
    def __deleteAutosaveFile(self):
        fileName = self.__getInifile()
        os.remove(fileName)
        
    def __autoSave(self):
        fileName = self.__getInifile()
        self.__save(fileName)

    def __autoLoad(self):
        fileName = self.__getInifile()
        self.__load(fileName)        
    
    def __save(self, fileName):
        output = open(fileName, 'wb')
        savedValues = dict()        
        for key in self.argumentsDict.keys():
            v = self.globalValues[key]
            savedValues[key] = v
        t = datetime.datetime.now()
        self.history.append((t,savedValues))
        pickle.dump(self.history, output)
        output.close()
        
    def __load(self, fileName):
        try:
            pkl_file = open(fileName, 'rb')
        except:
            print  "( ERROR: can't open \"" + fileName +"\")"
            return
    
        self.history = pickle.load(pkl_file)
        pkl_file.close()
        
        t, values = self.history[-1]
        for name in values.keys():
            try:
                self.setValue(name, values[name])
            except KeyError, e:
                print  "( ERROR: " + str(e) +")"
            except ParamsError, e:
                print  "( ERROR: " + str(e) +")"
    
    def __parseArgs(self, args): # sys.argv[1:]
        try:
            short = self.shortFormArgString()
            long = self.longFormArgList()
            long.append('no-gui')
            long.append('help')
            opts, args = getopt.getopt(args, short, long)
        except getopt.GetoptError, e:
            print "ERROR: " + str(e)
            # print help information and exit:
            print self.usage()
            sys.exit(2)  
         
        for o, a in opts:
            
            if o in ("-h", "--help"):
                print self.usage()
                sys.exit()
                
            if o in ('--no-gui'):
                continue
            
            argument = ""
            # check for '--'
            if o[1] == '-':
                argument = o[2:]
            else:
                short = o[1:]
                argument = self.shortDict[short]
            
            if len(a) == 0:
                a = True
                
            print "(cmd line argument '" + argument + "' value = '"+ str(a) + "')"
            self.setValue(argument, a)
            

        return True
            
    def addArgument(self, object, title, choices=None, filePath=False, short = None, help=None, group=None):
        frame = inspect.currentframe().f_back
        frameInfo = inspect.getframeinfo( frame )
        call = str(frameInfo[3])
        sp = call.split('(')
        s = sp[1] 
        sp2 = s.split(",")
        s = sp2[0]
        name =  s.split(')')[0]
        name = name.strip()   

        if self.argumentsDict.__contains__(name):
            s = 'The parameter "' + name + '" already exists'
            raise ParamsError(s)
        if self.globalValues.__contains__(name):
            default = self.globalValues[name] #self.getValues()[name]
            self.__addArg(name, default, choices, filePath, short, title, help, group)
        else:
            s = 'The global variable "' + name + '" does not exist'
            raise ParamsError(s)
                
    def __addArg(self, name, default, choices, filePath, short, title, helpString, group):
        if self.argumentsDict.__contains__(name):
            s = 'The argument "' + name + '" is already in use'
            raise ParamsError(s)
        
        if short != None:
            if self.shortDict.__contains__(short):
                raise ParamsError('The short argument "' + short +'" for ' + name + ' is already in use')
            # check short name uniqueness
            self.shortDict[short] = name
        
        # add argument to list with empty attributes
        attributes = dict()

        self.argumentsDict[name] = attributes
        self.addAttribute(name, 'name', name)
        self.addAttribute(name, 'title', title)
        self.addAttribute(name, 'default',default)
        
        if choices != None:
            self.addAttribute(name, 'choices', choices)
        if filePath:
            self.addAttribute(name, 'filePath', True)       
        if group != None:
            self.addAttribute(name, 'group', group)
        if short != None:
            self.addAttribute(name, 'short', short)
        if helpString != None:
            self.addAttribute(name, 'help', helpString)
        

from UserDict import DictMixin

#
# Ordered dictionary. items are iterated in the 
# same order they were added
#
class Odict(DictMixin):
    
    def __init__(self):
        self._keys = []
        self._data = {}
        
        
    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value
        
        
    def __getitem__(self, key):
        return self._data[key]
    
    
    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)
        
        
    def keys(self):
        return list(self._keys)
    
    
    def copy(self):
        copyDict = Odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict


