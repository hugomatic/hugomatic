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


def show_params_gui( title_and_desc, parameters_dict, usage, dbg_callback, picture_path, history ):
                # p_dict,          title_and_desc, usage, with_debug_line, picture_path, history, parameters_dict
    gui = ShowGui(title_and_desc, usage, dbg_callback, picture_path, history, parameters_dict)
    gui.show()   
    dbg_line = gui.debug_line
    clear = gui.clear_btn_pressed
    ok_pressed = gui.ok_btn_pressed
    vals = gui.return_vals
    return ok_pressed, clear, dbg_line, vals


from Tkinter import *

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1)
                      #font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class Command:
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.callback(*self.args, **self.kwargs)

def file_picker_callback(entry):
    str  = askopenfilename() 
    if str != ():
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
        #self.__set_values_from_dict(self.default_values)
        for param, attributes in self.parameters_dict.iteritems():
            value = attributes['default']
            s = str(value)
            if type(value) == bool:
                #print "BOOOOO", value
                if value:
                    s = '1'
                else:
                    s = '0'
            self._set_widget_value_string(param, s)
            
        

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
        index = -1
        s = what.split('[')[1].split(']')[0]
        index = int(s) -1
        ev = self.history[index]
        values = ev[1]
        self.__set_values_from_dict(values)
        
#        for ev in self.history:
#            date = ev[0]
#            if date == what:
#                values = ev[1]
#                self.__set_values_from_dict(values)


    def _ok_pressed(self):
        self.ok_btn_pressed = True
        if self.dbg_callback:
            s = self._get_widget_value_as_string('_debug_line_')
            self.debug_line = int(s)
        self.return_vals = self._get_new_values()
        self._quit_gui()
    

    
    def _get_current_value(self, k):
        old_value = self.parameters_dict[k]['value']
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
        return current_value
    
                
    def _get_new_values(self):
        
        tk_vars = self.tkvars
        new_values = {} # at least we'll get some emtpy thing
        
        for k in self.parameters_dict.keys():
            old_value = self._get_initial_value(k)
            current_value = self._get_current_value(k)
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

    def __init__(self, title_and_desc, usage, dbg_callback, picture_path, history, parameters_dict):
        HugomaticGui.__init__(self)
        self.parameters_dict = parameters_dict
        self.title_and_desc = title_and_desc
        self.usage = usage
        self.dbg_callback = dbg_callback
        self.picture_path = picture_path
        self.history = history
    
    def _get_initial_value(self, param):
        return self.parameters_dict[param]['value']
        
    def _init_gui(self):
        self.tkvars = {}
        self.tkwidgets = {}
        self.tk = Tk()

        self.default_value_color = self.tk.cget("bg")
        self.initial_value_color = "#%02x%02x%02x" % (128, 192, 200) #"blue"
        self.new_value_color = "#%02x%02x%02x" % (112, 171, 206) #"red"
        

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

    def __gui_bg_color_update(self):
        for param, widget in self.tkwidgets.iteritems(): 
            new_color = self.new_value_color
            default = None
            current = None
            initial_value = None
            if param == '_debug_line_':
                default = -1
                current = int(widget.get())
                initial_value = -5552
                new_color = "red"
            else:
                default = self.parameters_dict[param]['default']
                initial_value = self.parameters_dict[param]['value']
                try:
                    current = self._get_current_value(param)
                except:
                    continue
               
            if current == default:
                #print param, "D default: ", default, ", initial:", initial_value, ", current:",current
                widget.config(bg=self.default_value_color)
            else: 
                if current == initial_value:
                    #print param, "I default: ", default, ", initial:", initial_value, ", current:",current
                    widget.config(bg=self.initial_value_color)
                else:
                    #print param, "N default: ", default, ", initial:", initial_value, ", current:",current
                    widget.config(bg=new_color)
        
        
    def _entry_validation_callback(self, param):
        self.__gui_bg_color_update()
        return True
    
    def _var_w_callback(self, param, *args):
        self.__gui_bg_color_update()     
        
    def __create_tooltip(self, widget, param):
        
        tt_text  = "variable: " + param 
        tt_text += "\n"
        tt_text += "default: "+str(self.parameters_dict[param]['default'])
        attributes = self.parameters_dict[param]
        if attributes.has_key('group'):
            group = attributes['group']
            tt_text += "\n"
            tt_text += "group: " + str(group)
        
        createToolTip(widget, tt_text)  
    
    def _create_debug_line_widget(self, g, row, entry_col,label_col):
        v = -1
        title_str = "Debug line (-1 = not set)"
        entry = Entry(g)
        entry.insert(0,v)
        entry.grid(row=row, column=entry_col, sticky=E+W)
        debug_label = Label(g, text= title_str)
        debug_label.grid(row=row, column=label_col , sticky=W)
        dbg_str = str(self.dbg_callback)
        createToolTip(debug_label, "Invokes a script method before the program\nprints the specified line\ncall_back: %s" % (dbg_str) ) 
        self.tkvars["_debug_line_"] = entry
        self.tkwidgets["_debug_line_"] = entry
    
    def _create_check_box(self,tk_frame,param,row,col):
        v = self.parameters_dict[param]['value']
        title = self.parameters_dict[param]['title']
        var = IntVar(name=param)
        check_box = Checkbutton(tk_frame, justify= LEFT, text=title, variable = var)
        self.__create_tooltip(check_box, param)
        check_box.grid(row=row, column = col, columnspan=2, sticky=N+W)
        self.tkvars[param] =  var
        self.tkwidgets[param] = check_box
        var.trace("w", self._var_w_callback)
        var.set(v) # callback must be registered and tkvars must be set
    
    def _create_option_menu(self,g, param, row, entry_col, label_col):
        choices = self.parameters_dict[param]['choices']
        title = self.parameters_dict[param]['title']
        v = self.parameters_dict[param]['value']
        
        myLabel = Label(g, text= title)
        var = StringVar(name = param)
        # * because OptionMenu is a variable argument list
        menu = choices
        opt = OptionMenu(g, var, *menu)  
        var.trace("w", self._var_w_callback)
        var.set(v) # callback must be registered and tkvars must be set
        opt.grid( column = entry_col, columnspan=1, row=row, sticky=E+W)#N+W
        myLabel.grid  (row=row, column= label_col, columnspan = 1, sticky= W) #N+W+E
        self.__create_tooltip(myLabel, param)
        self.tkvars[param] =  var
        self.tkwidgets[param] = opt
        
    def _fill_tk_frame(self, tk_frame):
        """
        Adds all the widgets on the screen using a grid layout (necessary for scroll)
        """
        g = tk_frame
        # master = f
        keys = self.parameters_dict.keys()
        item_count = len(keys)
        
        # column numbers
        COL_IMG = 0
        COL_ENTRY = 1
        COL_LABEL = 2

        bitmap_rowspan = item_count
        if self.dbg_callback:
            bitmap_rowspan += 1
            

        # the pict reference must be store to avoid garbage collection
        self.pict = self._add_picture(tk_frame, self.picture_path, COL_IMG, bitmap_rowspan)
        
        # print "TITLE: %s" % title_and_desc
        entry_width = 15
        i = 0
        if self.dbg_callback:    
            self._create_debug_line_widget(tk_frame, i, COL_ENTRY, COL_LABEL)
            #g.rowconfigure(i, weight=0)
            
        for counter in range(item_count):
            i = counter
            if self.dbg_callback:
                i +=1
                
            k = keys[counter]
            title = self.parameters_dict[k]['title']
            v = self.parameters_dict[k]['value']
            
            #print k
            # is it a list to choose from?
            
            if self.parameters_dict[k].has_key('choices'):
                self._create_option_menu(tk_frame, k, i, COL_ENTRY, COL_LABEL,)
            else:    
                type_of_value = type(v)
                if type_of_value == bool:
                    self._create_check_box(tk_frame,k,i,COL_ENTRY)
                    
                else:
                    if self.parameters_dict[k].has_key('filePath'):
                        pass
                    else:
                        pass
                    
                    group = g
                    #group = LabelFrame(g, text="Group", padx=5, pady=5)
                    #group.pack(padx=10, pady=10)
                    
                    entry = Entry(group,validate = "all", validatecommand=Command(self._entry_validation_callback,k)) # Command(text_changed_callback, self, k) 
                    self.tkvars[k] =  entry
                    self.tkwidgets[k] = entry
                    
                    myLabel = myLabel = Label(group, text= title)
                    self.__create_tooltip(myLabel, k)
                    
                    if self.parameters_dict[k].has_key('filePath'):
                        bt = None
                        #lambda: self._file_path_pressed(k)
                        #bck = FilePickerCallback(entry)
                        bt = Button(group, text= "...", command = Command(file_picker_callback,entry))
                        
                        myLabel.grid  (row=i, column= COL_LABEL, columnspan= 1, sticky= W) #N+W+E
                        bt.grid  (row=i, column= COL_ENTRY, columnspan= 1, sticky= E)
                    else:
                        myLabel.grid  (row=i, column= COL_LABEL, columnspan= 1, sticky= W) #N+W+E
                    entry.insert(0, v)
                    entry.grid( column = COL_ENTRY, columnspan=1, row=i, sticky=E+W)#N+W  
                    g.rowconfigure(i, weight=0)  
          
        row_count = i      
        # cmd line
#        row_count += 1
#        text_cmd = Text( g, width = 3, height = 4 )
#        text_cmd.grid( row = row_count, column = 0, columnspan = 3, sticky = W+E+N+S)
#        g.grid_rowconfigure( row_count, weight = 1 )
#        text_cmd.insert( INSERT, usage )
#        text_cmd.config(state=DISABLED) # (state=NORMAL)
        
        # button bar
        row_count += 1
        self.button_clear = Button( g, text = "Clear list", command = self._clear_pressed )
        
        self.button_clear.grid( row = row_count, column = 1, sticky = W+E+S )
        buttonDefault = Button( g, text = "Default values", command = self._default_pressed )
        buttonDefault.grid( row = row_count, column = 2, sticky = W+E+S )
        
        # history select box
        choices = []
        counter = 0
        for ev in self.history:
            counter += 1
            s = "[%s] %s" % (counter, str(ev[0]) )  
            choices.insert(0, s)
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

    def show(self ):
        
        #title_and_desc = self.title_and_desc 
        #values, titles, defaults, choices, filePaths, 
        #usage, withDebugLine, picture_path, 
        
        window_title = self.title_and_desc # + " [%s]" % len(self.history)
        self.tk.title(window_title)

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
        
        self._fill_tk_frame(frame)

        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        scrollregion=canvas.bbox("all")
        canvas.config(scrollregion = scrollregion)
        
        dim_str = "%sx%s" % (scrollregion[2]+25, scrollregion[3] + 5 )    
        self.tk.geometry(dim_str)
        
        #frame.bind("<Return>", self._ok_pressed)

        root.mainloop()    

