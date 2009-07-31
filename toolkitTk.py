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

from Tkinter import *
import tkSimpleDialog

class ParameterGui( Frame ):
   
   def okPressed(self):
    self.okButtonHasBeenPressed = True    
    
    if self.showDebugLine:
        v = self.tkVars.pop('_debug_line_') #remove debugline
        self.debugLine = int(v.get())
    Frame.quit(self)
             
   def getChangedValues(self):
           """ Get the values changed by the user
           """
           return self.__getCurrentValues(True)
    
   def getCurrentValues(self):           
           """ Get the new values for all parameters
           """
           return self.__getCurrentValues(False)
    
   def __getCurrentValues(self, changedValuesOnly):    
       #noChange = True
       
       newValues = dict()
       for k,v in self.tkVars.iteritems():
           
           oldValue = self.oldValues[k]
           oldtype = type(oldValue)
           userValueStr = v.get()
           userValue  = None
                      
           if oldtype == int:
               userValue = int(userValueStr)
           elif oldtype == float:
               userValue = float(userValueStr)
           elif oldtype == str:
               userValue = str(userValueStr)
           elif oldtype == bool:
               userValue = bool(userValueStr)
           elif userValue == None:
                userValue = userValueStr
                
           #print k, ":", userValueStr, " (def:", oldValue,")"
           if changedValuesOnly == False:
               newValues[k] = userValue
           else:
                if(oldValue != userValue):
                   #noChange = False
                   #print k, " Changed!!!"
                   newValues[k] = userValue
                   
       return newValues
   
   def __init__( self, title, valuesDict, descriptions, defaultsDict, choicesDict, filePathDict, cmdLine, withDebugLine, pictureFile, history ):
        Frame.__init__( self )
        self.title = title
        self.history = history
        self.okButtonHasBeenPressed = False
        self.clearButtonHasBeenPressed = False
        # nice bitmap
        self.pict = None
        if pictureFile:
            if os.path.exists(pictureFile):
                self.pict  = PhotoImage(file=pictureFile)
            
        #self.parameters = args    
        self.oldValues = valuesDict
        self.defaultValues = defaultsDict
        self.showDebugLine = withDebugLine
        self.debugLine = -1
        self.layoutWidgets(descriptions, choicesDict, filePathDict, cmdLine)
        
        
   
   def getDebugLine(self):
       return self.debugLine
   
   def __beenModified(self):
       newVals = self.getNewValues()
       noChange = len(newVals) == 0
       if noChange == False:
           cmdLine = self.parameters.getCmdLine() + "\n\n\n" + self.parameters.usage()
           #print cmdLine
           self.textCmd.config(state=NORMAL)
           self.textCmd.insert( INSERT, cmdLine )
           self.textCmd.config(state=DISABLED) # (state=NORMAL)
       
            
   def layoutWidgets(self, titles, choicesDict, filePathDict, cmdLine): 
    
    def addWidget(v, title, choices, filePath, rowCount, master):
        myTkVar = None
        if choices:
            myLabel = Label(master, text= title)
            var = StringVar()
            # * because OptionMenu is a variable argument list  
            opt = OptionMenu(master, var, *choices)  
            var.set(v)
            myTkVar = var
            opt.grid( column = col, columnspan=1, row=rowCount, sticky=E+W)#N+W
            myLabel.grid  (row=rowCount, column= col + 1, columnspan= 3-col-1, sticky= W) #N+W+E

        else:    
            t = type(v)
            if t == bool:
                checkBoxValue = IntVar()
                checkBoxValue.set(v)
                checkBox = Checkbutton(master, justify= LEFT, text=title, variable = checkBoxValue)
                checkBox.grid(row=rowCount, column = col, columnspan=2, sticky=N+W)
                myTkVar = checkBoxValue
            else:
                entry = Entry(master)
                myLabel = None
                myButton = None
                if filePath:
                    myButton = Button(master, text= "...", command = lambda: self._filePathPressed(entry))
                    myLabel = Label(master, text= title)
                    myLabel.grid  (row=rowCount, column= col + 1, columnspan= 3-col-1, sticky= W) #N+W+E
                    myButton.grid  (row=rowCount, column= col + 1, columnspan= 3-col-1, sticky= E)
                else:
                    myLabel = Label(master, text= title)
                    myLabel.grid  (row=rowCount, column= col + 1, columnspan= 3-col-1, sticky= W) #N+W+E
                
                
                entry.insert(0, v)
                myTkVar = entry            
                entry.grid( column = col, columnspan=1, row=rowCount, sticky=E+W)#N+W
                
                
                
        self.rowconfigure(rowCount, weight=0)  
        return myTkVar
       
       
    self.master.title( self.title )
    # widget list
    self.tkVars = dict()
    self.master.rowconfigure( 0, weight = 1 )
    self.master.columnconfigure( 0, weight = 1 )
    self.grid( sticky = W+E+N+S)
    
    rowCount = -1   
    
    col = 0
    if self.pict != None:
       bitmapRowSpan = len(self.oldValues)
       if self.showDebugLine:
           bitmapRowSpan += 1 # allow room for the debug line field
           
       self.bitmapLabel = Label(self, image= self.pict)
       self.bitmapLabel.grid(row =0, rowspan = bitmapRowSpan, columnspan = 1, sticky = W+E+N+S)
       col = 1 # move all parameters 1 column to the right
    
    #    keep the list of groups
    #    groups = dict()
    #    groups["top"] = self
    #    group = groups["top"]
    group = self
    
    if self.showDebugLine:
        v = -1
        title = "Debug line (-1 = not set)"
        rowCount += 1 
        choices = None
        myTkVar = addWidget(v, title, choices, False, rowCount, group)
        self.tkVars["_debug_line_"] = myTkVar
   
    for k in self.oldValues:
        rowCount += 1 
        v = self.oldValues[k]
        # get the value for the current argument
        # v = values[k]      
        title = titles[k]
        #groupName = self.parameters.getAttributeValue(k, 'group')       
        choices = choicesDict[k] #self.parameters.getAttributeValue(k, 'choices')
        if v == None:
            v = 0.0
        filePath = filePathDict[k]
        myTkVar = addWidget(v, title, choices, filePath,rowCount, group)
        self.tkVars[k] = myTkVar
 
    # cmd line
    rowCount += 1
    self.textCmd = Text( self, width = 3, height = 2 )
    self.textCmd.grid( row = rowCount, column = 0, columnspan = 3, sticky = W+E+N+S)
    self.rowconfigure( rowCount, weight = 1 )
    self.textCmd.insert( INSERT, cmdLine )
    self.textCmd.config(state=DISABLED) # (state=NORMAL)
    
    # button bar
    rowCount += 1
    self.buttonClear = Button( self, text = "Clear list", command = self._clearPressed )
    self.buttonClear.grid( row = rowCount, column = 1, sticky = W+E+S )
    self.buttonDefault = Button( self, text = "Default values", command = self._defaultPressed )
    self.buttonDefault.grid( row = rowCount, column = 2, sticky = W+E+S )
    #self.buttonDefault.config(state=DISABLED)  
    
    choices = []
    for ev in self.history:
        choices.insert(0, ev[0])
    choices = tuple(choices)
    self.historyVar = StringVar()
    empty = len(choices) == 0
    if empty:
        choices = ['']
    self.historyOptions = OptionMenu(self, self.historyVar, command = self._historyPressed, *choices)
    if not empty :
        self.historyVar.set(choices[0])
    else:
        self.historyOptions.config(state=DISABLED)
        self.buttonClear.config(state=DISABLED)
        
    self.historyOptions.grid( row = rowCount, column = 0, sticky = W+E+S )

    rowCount += 1

    self.buttonOk = Button( self, text = "Generate CODE", command = self.okPressed )
    self.buttonOk.grid( row = rowCount, column = 1, sticky = W+E+S )

    self.rowconfigure( rowCount, weight = 0 )
    self.columnconfigure( 0, weight = 1 )
    self.columnconfigure( 1, weight = 1 )
    self.columnconfigure( 2, weight = 1 )

   def _clearPressed(self):
    self.historyVar.set('')
    self.historyOptions.config(state=DISABLED) 
    self.buttonClear.config(state=DISABLED)
    self.clearButtonHasBeenPressed = True

   def _defaultPressed(self):
    self.__setValuesFromDict(self.defaultValues)

   def _historyPressed(self, selection):
       values = []
       for ev in self.history:
           date = ev[0]
           if date == selection:
               values = ev[1]
               self.__setValuesFromDict(values)

   def __setValuesFromDict(self, values):
       for k in values:
           value = values[k]
           s = str(value)
           var = self.tkVars[k]
           t =  var.__class__ 
           if t == Entry:
               var.delete(0, END)
               var.insert(0, value)
           else:
               var.set(value)
       
   def _filePathPressed(self, entry):
       from tkFileDialog   import askopenfilename 
       str  = askopenfilename() 
       if str != ():
           entry.delete(0, END)
           entry.insert(0, str)

