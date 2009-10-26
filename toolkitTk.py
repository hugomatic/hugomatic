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
from tkFileDialog   import askopenfilename 


def show_params_gui( title_and_desc, values, titles, defaults, choices, filePaths, usage, withDebugLine, picture_path, history ):
    gui = ShowGui()
    gui.show( title_and_desc, values, titles, defaults, choices, filePaths, usage, withDebugLine, picture_path, history )   
    return gui.ok_btn_pressed, gui.clear_btn_pressed, gui.debug_line, gui.return_vals


class FilePickerCallback(object):
    def __init__(self, name, tkvars):
        self.name = name
        self.tkvars = tkvars
        
    def boom(self):
        str  = askopenfilename() 
        if str != ():
            entry = self.tkvars[self.name]
            entry.delete(0, END)
            entry.insert(0, str) 


class HugomaticGui(object): 
   
    def __init__(self):        
        self.ok_btn_pressed = False
        self.clear_btn_pressed = False 
        self.debug_line = None
        self.return_vals = {}
        self.history = None

        self.old_values = None
        self._init_gui()
        
    def _clear_pressed(self):
        self.clear_btn_pressed = True
        self._disable_history_browsing()
        
    def _default_pressed(self):
        self.__set_values_from_dict(self.default_values)

    def __set_values_from_dict(self, values):
        for k in values:
            value = values[k]
            s = str(value)
            if type(value) == bool:
                #print "BOOOOO", value
                if value:
                    s = '1'
                else:
                    s = '0'
            self._set_widget_value_string(k, s)
               
    def _history_pressed(self, what):
        values = []
        for ev in self.history:
            date = ev[0]
            if date == what:
                values = ev[1]
                self.__set_values_from_dict(values)


    def _ok_pressed(self):
        self.ok_btn_pressed = True
        if self.with_debug_line:
            s = self._get_widget_value_as_string('_debug_line_')
            self.debugLine = int( s)
        self.return_vals = self._get_new_values()
        self._quit_gui()
            
    def _get_new_values(self):
        old_values = self.old_values
        tk_vars = self.tkvars
        new_values = {} # at least we'll get some emtpy thing
        
        for k in self.old_values.keys():
            old_value = old_values[k]
            old_type = type(old_value)
            user_value_string = self._get_widget_value_as_string(k)
            current_value  = None
                       
            if old_type == int:
                current_value = int(user_value_string)
            elif old_type == float:
                current_value = float(user_value_string)
            elif old_type == str:
                current_value = str(user_value_string)
            elif old_type == bool:
                new_bool = True
                if user_value_string == '0':
                    new_bool = False
                #print "BOOOOL", user_value_string, new_bool
                current_value = new_bool
                
            elif current_value == None:
                current_value = user_value_string         
            if(old_value != current_value):
                new_values[k] = current_value    
        return new_values
    

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

    
class ShowGui(HugomaticGui):

    def _init_gui(self):
        self.tkvars = {}
        self.tk = Tk()

    def _quit_gui(self):
        self.tk.quit()

    def _set_widget_value_string(self, item_name, str_value):
        var = self.tkvars[item_name]
        t = var.__class__ 
        if t == Entry:
            var.delete(0, END)
            var.insert(0, str_value)
        else:
            var.set(str_value)
    
    def _get_widget_value_as_string(self, item_name):
        #print '_get_widget_value_as_string %s:' %(item_name)
        w = self.tkvars[item_name]   
        #print " tkvar ", type(w)        
        v = w.get() 
        #print " v =",v       
        s = str(v)
        #print " s =",s
        return s    
    
    def _disable_history_browsing(self):
        self.history_var.set('')
        self.history_options.config(state=DISABLED) 
        self.button_clear.config(state=DISABLED)
    
    def __fill_tk_parameter_list(self): 
        pass
   
    def _add_picture(self, tk_frame, picture_path, column, rowspan):
        pict = None
        if picture_path:
            if os.path.exists(picture_path):
                pict  = PhotoImage(file=picture_path)
                bitmap_label = Label(tk_frame, image= pict)
                #bitmap_label = Label(g, text= "twot")
                bitmap_label.grid(row =0, column=column, rowspan = rowspan, columnspan = 1, sticky = W+E+N+S)
                tk_frame.columnconfigure( column, weight = 1 )
        return pict    

    def _fill_tk_frame(self, tk_frame, values, picture_path, with_debug_line, titles, choices, file_paths, usage, history):
        g = tk_frame
        # master = f
        keys = values.keys()
        item_count = len(keys)
        
        # column numbers
        COL_IMG = 0
        COL_ENTRY = 1
        COL_LABEL = 2

        bitmap_rowspan = item_count
        if with_debug_line:
            bitmap_rowspan += 1

        # the pict reference must be store to avoid garbage collection
        self.pict = self._add_picture(tk_frame, picture_path, COL_IMG, bitmap_rowspan)
        
        # print "TITLE: %s" % title_and_desc
        entry_width = 15
        i = 0
        if with_debug_line:    
            v = -1
            title = "Debug line (-1 = not set)"
            entry = Entry(g)
            entry.insert(0,v)
            entry.grid(row=i, column=COL_ENTRY, sticky=E+W)
            Label(g, text= title).grid(row=i, column=COL_LABEL , sticky=W)
            self.tkvars["_debug_line_"] = entry
            #g.rowconfigure(i, weight=0)
            
        for counter in range(item_count):
            i = counter
            if with_debug_line:
                i +=1
                
            k = keys[counter]
            title = titles[k]
            v = values[k]
            
            #print k
            #print " title: %s" % title
            #print " value: %s, [%s]" % (v,type(v))
            #print " default: %s" % defaults[k]
            #print " choices: %s" % choices[k]
            #print " isFilePath: %s" % filePaths[k]
          
            # is it a list to choose from?
            if choices[k]:
                myLabel = Label(g, text= title)
                var = StringVar()
                # * because OptionMenu is a variable argument list  
                opt = OptionMenu(g, var, *choices)  
                var.set(v)
                self.tkvars[k] =  var
                opt.grid( column = COL_ENTRY, columnspan=1, row=i, sticky=E+W)#N+W
                myLabel.grid  (row=i, column= COL_LABEL, columnspan = 1, sticky= W) #N+W+E
        
            else:    
                type_of_value = type(v)
                if type_of_value == bool:
                    var = IntVar()
                    var.set(v)
                    checkBox = Checkbutton(g, justify= LEFT, text=title, variable = var)
                    checkBox.grid(row=i, column = COL_ENTRY, columnspan=2, sticky=N+W)
                    self.tkvars[k] =  var
                else:
                    group = g
                    #group = LabelFrame(g, text="Group", padx=5, pady=5)
                    #group.pack(padx=10, pady=10)
                    
                    entry = Entry(group)
                    self.tkvars[k] =  entry
                    myLabel = None
                    if file_paths[k]:
                        bt = None
                        #lambda: self._file_path_pressed(k)
                        bck = FilePickerCallback(k, self.tkvars)
                        bt = Button(group, text= "...", command = bck.boom)
                        myLabel = Label(group, text= title)
                        myLabel.grid  (row=i, column= COL_LABEL, columnspan= 1, sticky= W) #N+W+E
                        bt.grid  (row=i, column= COL_ENTRY, columnspan= 1, sticky= E)
                    else:
                        myLabel = Label(group, text= title)
                        myLabel.grid  (row=i, column= COL_LABEL, columnspan= 1, sticky= W) #N+W+E
                    entry.insert(0, v)
                    entry.grid( column = COL_ENTRY, columnspan=1, row=i, sticky=E+W)#N+W
                                     
                    g.rowconfigure(i, weight=0)  
                
        # cmd line
        row_count = i + 1
        text_cmd = Text( g, width = 3, height = 4 )
        text_cmd.grid( row = row_count, column = 0, columnspan = 3, sticky = W+E+N+S)
        g.grid_rowconfigure( row_count, weight = 1 )
        text_cmd.insert( INSERT, usage )
        text_cmd.config(state=DISABLED) # (state=NORMAL)
        
        # button bar
        row_count += 1
        self.button_clear = Button( g, text = "Clear list", command = self._clear_pressed )
        self.button_clear.grid( row = row_count, column = 1, sticky = W+E+S )
        buttonDefault = Button( g, text = "Default values", command = self._default_pressed )
        buttonDefault.grid( row = row_count, column = 2, sticky = W+E+S )
        
        # history select box
        choices = []
        for ev in history:
            choices.insert(0, ev[0])
        choices = tuple(choices)
        self.history_var = StringVar()
        empty = len(choices) == 0
        if empty:
            choices = ['']
        self.history_options = OptionMenu(g, self.history_var, command = self._history_pressed, *choices)
        if not empty :
            self.history_var.set(choices[0])
        else:
            self.history_options.config(state=DISABLED)
            self.button_clear.config(state=DISABLED)
            
        self.history_options.grid( row = row_count, column = 0, sticky = W+E+S )
        row_count += 1
        buttonOk = Button( g, text = "OK", command = self._ok_pressed )
        buttonOk.grid( row = row_count, column = 1, sticky = W+E+S )
    
        g.rowconfigure( row_count, weight = 0 )
        g.columnconfigure( 0, weight = 1 )
        g.columnconfigure( 1, weight = 1 )
        g.columnconfigure( 2, weight = 1 )  
        g.grid_columnconfigure(2, weight=1)        

    def show(self, title_and_desc, values, titles, defaults, choices, filePaths, usage, withDebugLine, picture_path, history ):

        self.with_debug_line =  withDebugLine       
        self.old_values = values
        self.default_values = defaults
        self.history = history
      

        self.tk.title(title_and_desc)

        root = self.tk   
        vscrollbar = None
        hscrollbar = None
        vscrollbar = AutoScrollbar(root)
        vscrollbar.grid(row=0, column=1, sticky=N+S)
        hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E+W)

        canvas = Canvas(root, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        
        # make the canvas expandable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        #
        # create canvas contents
        frame = Frame(canvas)
        
        self._fill_tk_frame(frame, values, picture_path, withDebugLine, titles, choices, filePaths, usage, history)

        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        scrollregion=canvas.bbox("all")
        canvas.config(scrollregion = scrollregion)
        
        dim_str = "%sx%s" % (scrollregion[2]+25, scrollregion[3] + 5 )    
        self.tk.geometry(dim_str)
        
        root.mainloop()    

