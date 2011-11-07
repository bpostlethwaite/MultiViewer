#!/usr/bin/python2
# Command Window - For displaying text view apps as well as
# Other useful desktop widgets.
4#
#######################################################


from Tkinter import *
from Modules.viewer import FileViewer
from Modules.widgets import LowerButtons, RadioViewBar
from Modules.widgets import AddRemove
from Modules.MultiViewer import MVB
import os, os.path, subprocess


class MultiViewerMain(Frame,MVB):
    def __init__(self,parent=None,showviewers=3,height=600,width=2000):
        Frame.__init__(self,parent,bg=MVB.bg,width=width,height=height)
        self.showviewers = showviewers      #Set num of viewers shown
        self.buildframes()                  #Build structural Frames
        self.panels = []
        self.pack(fill=BOTH,expand=YES)
        self.pack_propagate(False)
        self._initviewers()
        

        
        self.addbuttons()                       # Pack Buttons
        
        self.packviewer(self.showviewers)

    def _initviewers(self):
        """ Initializes Viewers for max viewers allowed by app, set in MultiViewerBase"""
        for i in range(MVB.maxviewers):
                 # Initialize starting viewers, kept in memory, and packed and unpacked as needed
            MVB.viewers.append(FileViewer(self,bg=MVB.bg,fg=MVB.fg,
                                          deepfg=MVB.deepfg,highfg=MVB.highfg,
                                          titlecolor=MVB.titlecolor,
                                          width = 30,file2view=None))

    def buildframes(self):
        """Build major structural Frames"""
        self.rside = Frame(self,bg=MVB.bg)
        self.rside.pack(side=RIGHT,fill=Y,expand=NO)
        #self.rside.pack_propagate(False)
        self.bside = Frame(self,bg=MVB.bg)
        self.bside.pack(side=BOTTOM,fill=X,expand=NO)
  
    def addbuttons(self):
        """Add Buttons to specifed location"""
        self.panels.append(LowerButtons(self.bside))
        self.panels[-1].pack(side=LEFT,fill=BOTH,expand=NO)
        self.panels.append(AddRemove(self.bside))
        self.panels[-1].pack(side=RIGHT,fill=BOTH,expand=NO)
        self.panels.append(RadioViewBar(self.rside))
        self.panels[-1].pack(side=RIGHT,fill=Y,expand=NO)
            

if __name__ == '__main__':

    if 'bpostlet' or 'ben' == os.environ['USER']:
        process = subprocess.Popen('xrandr | grep "*"', shell=True, stdout=subprocess.PIPE)
        screens = process.communicate()[0]
        try:
            PIXwidth = int(max(field.split('x')[0] for field in screens.split() if 'x' in field))
        except Exception as err:
            print err
            PIXwidth = 1900

    root = Tk(className="MultiViewer")
    root.title("MultiViewer")
    M = MultiViewerMain(parent = root, showviewers=3, width=PIXwidth)
    M.mainloop()



    # TO DO, Simply filetest routines and warning labels, + add button on warning labels
    

