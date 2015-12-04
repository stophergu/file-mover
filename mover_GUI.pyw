from tkinter import *
import pickle, os
from file_mover import find_files, parse, move

ALL = N+S+W+E

class Application(Frame):
    '''
    A simple GUI interface to facilitate the transfer of files,
    last source path and target path are pickled and used to autofill their
    respective fields
    '''
    def __init__(self, master=None):
        '''Create a 'master' frame of 1 row x 1 column'''
        Frame.__init__(self, master, bg = 'snow3',
                       highlightthickness =4,
                       highlightbackground = 'grey')
     
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.bind('<Return>', self.run)
        self.grid(sticky = W+E+S+N)
        self.createWidgets()
        
    def createWidgets(self):
        '''Create and add widgets to 'master' frame'''
        for r in range(20):
            self.rowconfigure(r, weight = 1)
        for  c in range(3):
            self.columnconfigure(c, weight = 1)

        #Centralized Color definitions
        bg = 'snow3'
        fg = 'grey'
        line = 'white'

        #Extension
        self.extension = Frame(self, bg = bg)
        self.extension_entry = Entry(self.extension)
        self.extension_entry.pack()
        self.extension_entry.focus()
        self.extension_label = Label(self.extension,
                                      text = "Extensions\n",
                                      bg = bg,
                                      fg = fg)
        
        self.extension_label.pack(side = LEFT)
        self.extension.grid(row = 1, column = 0, sticky = W)

        #Source Path
        self.path = Frame(self, bg = bg)
        self.path_entry = Entry(self.path,width = 35)
        self.path_entry.pack()
        self.path_label = Label(self.path,
                                text = 'From Path or Drive\n',
                                bg = bg,
                                fg = fg)
        self.path_label.pack(side = LEFT)
        self.path.grid(row = 5, column = 0, sticky = W)
        
        #check for previously pickled source path
        if os.path.isfile('last_source.pkl'):
            fill = pickle.load(open('last_source.pkl', 'rb'))
            self.path_entry.insert(0, fill)
        #Transfer to path
        self.target = Frame(self, bg = bg)
        self.target_entry = Entry(self.target,width = 35)
        self.target_entry.pack()
        self.target_label = Label(self.target, 
                                  text = 'path/to/store/file\n',
                                  bg = bg,
                                  fg = fg)
        self.target_label.pack(side = LEFT)
        self.target.grid(row = 6, column = 0, sticky = W)
        #Check for target path
        if os.path.isfile('last_target.pkl'):
            fill = pickle.load(open('last_target.pkl', 'rb'))
            self.target_entry.insert(0, fill)
        #min date
        self.mindate = Frame(self, bg = bg)
        self.mindate_entry = Entry(self.mindate)
        self.mindate_entry.pack()
        self.mindate_label = Label(self.mindate,
                                   text = 'From mm/dd/yyyy\n',
                                   bg = bg, 
                                   fg = fg)
        self.mindate_label.pack(side = LEFT)
        self.mindate.grid(row = 7, column = 0, sticky = W)
        #max date
        self.maxdate = Frame(self, bg = bg)
        self.maxdate_entry = Entry(self.maxdate)
        self.maxdate_entry.pack()
        self.maxdate_label = Label(self.maxdate,
                                   text = 'To mm/dd/yyyy\n',
                                   bg = bg, 
                                   fg = fg)
        self.maxdate_label.pack(side = LEFT)
        self.maxdate.grid(row = 7, column = 0, sticky = E)
        #visual line break
        self.line = Frame(self, bg = bg)
        self.line_label = Label(self.line, bg = bg,
                                fg = line,
                                text = '_________'*7).pack()
        self.line.grid(row = 10, columnspan = 2, column = 0,sticky = ALL)

        #created/modified checkbox
        self.check = Frame(self, bg = bg)
        self.check.grid(row = 9, column = 0, sticky = W)
        self.created_var = BooleanVar()
        self.modified_var = BooleanVar()
        self.created_var.set(True)
        self.created = Checkbutton(self.check, 
                              bg = bg,
                              fg = fg, 
                              text = 'created',
                              variable = self.created_var,
                              onvalue = True,
                              offvalue = False).pack(side = LEFT)
        self.modified = Checkbutton(self.check,
                                    bg = bg,
                                    fg = fg,
                                    text = 'Modified',
                                    variable = self.modified_var,
                                    onvalue = True,
                                    offvalue = False).pack(side = LEFT)

        #copy or cut/paste radiobuttons
        self.move = Frame(self, bg = bg)
        self.move.grid(row = 12, column = 0, sticky = W)

        self.but_var = IntVar()
        self.but_var.set(1)
        self.copy = Radiobutton(self.move,
                                    text = 'Copy Only',
                                    variable = self.but_var,
                                    value = 1,
                                    bg = bg,
                                    fg = fg)
        
        self.copy.pack(side = TOP)
        self.cut = Radiobutton(self.move,
                                   text = 'Cut/Paste',
                                   variable = self.but_var,
                                   value = 0,
                                   bg = bg,
                                   fg = fg)
        self.cut.pack(side = TOP)
        #final read out
        self.readout = Frame(self)
        self.read_label = Label(self.readout,
                                bg = bg,
                                fg = fg,
                                text = '')
        
        self.readout.grid(row = 19, column = 0)
        self.read_label.pack()
        #Submit button
        self.submit = Frame(self, bg = 'dark grey')
        self.submit.grid(row = 20, column = 0, columnspan = 2, sticky = E)
        self.sbutton = Button(self.submit,
                              bg = bg,
                              fg = fg,
                              text = 'Submit',
                              command = self.run)
        self.sbutton.pack(side = RIGHT)
    
    def run(self, event = None):
   
        #retrieve entry field info
        extensions, path, target, mindate, maxdate,\
        created, modified, transfer  = self.get_entry()
        #generate list of files to be moved
        files = find_files(path, extensions)
        #pickle last source/last target paths
        pickle.dump(path, open('last_source.pkl', 'wb'))
        pickle.dump(target, open('last_target.pkl', 'wb'))
        parsed = []

        #if maxdate field is empty, search only date entered as mindate
        if maxdate == '':
            maxdate = mindate
        if created:
            for fn in parse(files, mindate, maxdate, created = True):
                if fn not in parsed:    
                    parsed.append(fn)
        if modified:
            for fn in parse(files, mindate, maxdate, modified = True):
                if fn not in parsed:
                    parsed.append(fn)
        if transfer == 1:
            move(parsed, target, copy = True)
            self.read_label.configure(text = 'Copied %d files' % (len(parsed)))
        if transfer == 0:
            move(parsed, target, cut = True)
            self.read_label.configure(text = 'Cut/Paste %d files'%(len(parsed)))
     

    def get_entry(self):
        values = []
        #self.sbutton.config(relief = SUNKEN)
        self.entries = [self.extension_entry,
                        self.path_entry,
                        self.target_entry,
                        self.mindate_entry,
                        self.maxdate_entry,
                        self.created_var,
                        self.modified_var,
                        self.but_var]
            
        for entry in self.entries:
            values.append(entry.get())
        return tuple(values)


root = Tk()
root.title("Nifty File Mover 3.1")
app = Application(master=root)
app.mainloop()
