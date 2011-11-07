# File Viewer: A text based file viewing class
# 
#  Going to seperate out the text bits, and attach ala composition
#  This way we can also attach a text viewer, for editing, and have
#  the text and the canvas communicate via the FileViewer.
#
#  Using composition on this one, not inheritance.
#######################################################
#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import os.path, os, shutil, md5

class FileViewer(Frame,object):
    def __init__(self, parent=None, bg=None,titlecolor=None,
                 fg=None,deepfg=None,highfg=None,width=50,height=30,file2view=None):
        super(FileViewer, self).__init__(parent)
        #Frame.__init__(self, parent)
        # Set Attributes
        self.width = width
        self.height = height
        self.dtitle = "{:^{width}}".format(self.__class__,width=self.width)      
        self.dtxt = '\n{:^{width}}{}{}{}'.format("Double Click to Load File"," "*20,
                                                 "\n"*40,"",width=self.width)
        self.titlecolor = titlecolor
        self.fg = fg
        self.bg = bg
        self.deepfg = deepfg
        self.highfg = highfg
        self.Tag = 'TextTag'                                # Set Tags to manipulate text in viewer
        self.titleVAR = StringVar()
        self.editVAR = StringVar()
        self.editVARII = StringVar()
        
        # Initialize Components
        self.init_text()
        self.init_scrollbar()
        self.scroll_text_link()
        self.init_widgets()
        self.toggleNoSave()                               # Enters state=Disabled and sets text in mode change button
        
        # Packing
        self.sybar.pack(side=RIGHT, fill=Y)                 # pack first=clip last
        self.sxbar.pack(side=BOTTOM, fill=X)                     # pack first=clip last
        self.titleLabel.pack(side=TOP,fill=X)
        self.bframe.pack(side=BOTTOM,fill=X,expand=NO)
        self.editmode.pack(side=LEFT, fill=BOTH)
        self.editmodeII.pack(side=LEFT,fill=BOTH)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)         # canv clipped first

        # Set event Handlers
        self.text.bind('<Double-1>',self.onDoubleClick)
        self.text.bind('<Button-2>', self.onRightClick)                      # set event handler 2

        # Set View File and initiate display
        self.viewfile = file2view           
#self.DisplayContent()
   ############# VIEWFILE PROPERTY ###################     
    def _get_viewfile(self):
        return self._viewfile
                 
    def _set_viewfile(self,file2view):                      # Check files validity and run Display content
        """ Check for files existence"""                    # whenever file is changed
        if file2view == None:
            self._viewfile = file2view      # Set Viewfile to non- but then initialize defaults
            self.setDefaults()
        else:
            try:
                open(file2view)               # If viewfile
                self._viewfile = file2view    # Set viewfile, get text and display contents
                self.gettext()
            except (IOError, TypeError) as err:
                self._viewfile = None
                self.txt = err
        
        self.DisplayContent()
    viewfile = property(_get_viewfile,_set_viewfile)    
  ##############################################      
    def init_text(self):
        """ INitialize Text object onto Viewer Object"""
        self.text = Text(self,highlightthickness=0,relief=SUNKEN,bd=0,
                         bg=self.bg,fg=self.fg,height=self.height,width=self.width)
        self.setDefaults()
        self.text.config(wrap="none")
        self.text.config(insertbackground=self.fg)
        

    def init_scrollbar(self):
        """ Initialize scrollbars, add to viewer object"""
        self.sybar = Scrollbar(self,activebackground=self.fg,
                               bg=self.bg,troughcolor=self.bg,
                               relief=RIDGE)

        self.sxbar = Scrollbar(self,orient='horizontal',activebackground=self.fg,
                               bg=self.bg,troughcolor=self.bg)

    def init_widgets(self):
        """Build Title Button, Button and Frames"""
        self.bframe = Frame(self,bg=self.bg)
        self.titleLabel = Label(self,textvariable=self.titleVAR,
                                highlightthickness=0,bg=self.bg,fg=self.titlecolor)
        self.editmode = Button(self.bframe, textvariable=self.editVAR,
                               highlightthickness=0,bg=self.bg,fg=self.fg,
                               relief=SUNKEN,bd=0,activebackground=self.fg,
                               width=20,
                               command = self.toggleEditmode)
        self.editmodeII = Button(self.bframe, textvariable=self.editVARII,
                               highlightthickness=0,bg=self.bg,fg=self.fg,
                               relief=SUNKEN,bd=0,activebackground=self.fg,
                               width=20,
                               command = self.toggleNoSave)
    def scroll_text_link(self):
        """ Set Links between Scroll bars and Text Object"""
        self.sybar.config(command=self.text.yview)               # xlink sbar and canv
        self.text.config(yscrollcommand=self.sybar.set)          # move one moves other
        self.sxbar.config(command=self.text.xview)               # xlink sbar and canv      
        self.text.config(xscrollcommand=self.sxbar.set)          # move one moves other
                                                         
    def gettext(self):
        """Get text from file"""
        title,ext = os.path.splitext(os.path.basename(self.viewfile)) # Get title out of file name
        self.txt = open(self.viewfile).read()                           #Get txt
        self.titleVAR.set(title)                                    # Set title in title label bar

    def setDefaults(self):
        """Set title and default text"""
        self.titleVAR.set(self.dtitle)
        self.txt = self.dtxt
    
    def DisplayContent(self):
        """ Displays Content of file in canvas"""
        self.text.config(state=NORMAL)
        self.text.delete('1.0',END)
        self.text.insert('1.0',self.txt) #insert text
        self.text.config(state=DISABLED)

    def onDoubleClick(self, event):                       
        """ Choose File to Diplay"""
        self.viewfile = askopenfilename(initialdir=os.path.expanduser("~"))

    def onRightClick(self, event):
        """ Open file, if loaded, in emacs for editing -
        if system = linux and emacs is available."""
        pass

    def toggleEditmode(self):
        """ Toggle EditMode on and off"""
        if 'disabled' in self.text.config()['state'][4]:
            self.text.config(state=NORMAL)
            mod = "Save & back to Viewmode"
            modII = "Exit Edit without Save"
        else:
            self.saveViewfile()
            self.text.config(state=DISABLED)
            mod = "Enter Edit Mode"
            modII = ""
        self.editVAR.set(mod)
        self.editVARII.set(modII)

    def toggleNoSave(self):
        """ Toggle EditMode on and off"""
        if 'disabled' in self.text.config()['state'][4]:
            self.text.config(state=NORMAL)
            mod = "Save & back to Viewmode"
            modII = "Exit Edit without Save"
        else:
            self.text.config(state=DISABLED)
            mod = "Enter Edit Mode"
            modII = ""
        self.editVAR.set(mod)
        self.editVARII.set(modII)
        
    def saveViewfile(self):
        """Get Text from textviewer and save to file, also create a backup"""
        alltext = self.scrapetext()
        if self.viewfile:
            try:
                shutil.copy(self.viewfile,self.viewfile+'~')
                open(self.viewfile,'w').write(alltext)
                print "Wrote to file ", self.viewfile
            except TypeError as err:
                print err
        else:
            try:
                vf = asksaveasfilename(initialdir=os.path.expanduser("~"));
                print "writing", self.txt, vf
                V = open(vf,'w')
                V.write(self.txt)
                self.viewfile = vf
            except IOError as err:
                pass

    def scrapetext(self):
        return self.text.get('1.0',END+'-1c')


if __name__ == '__main__':
    root=Tk()
    FileViewer().pack(expand=YES, fill=BOTH)
    mainloop()


# import md5
#    def getsignature(contents):
#        return md5.md5(contents).digest()
#
#   text.insert(END, contents) # original contents
#   signature = getsignature(contents)
#
#
#
#   contents = text.get(1.0, END)
#   if signature != getsignature(contents):
#       print "contents have changed!"
