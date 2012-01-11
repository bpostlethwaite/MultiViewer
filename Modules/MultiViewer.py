# ArchFrame -> Main Control Frame with Class variables to be
#               shared by component Frames
#
#######################################################
#!/usr/bin/ python2

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from viewer import FileViewer
from widgets import LowerButtons, RadioViewBar, AddRemove
import os, os.path, pickle, subprocess

bg = 'black'

class MaxViewersPacked(Exception):
    """For now just raises a max reached error, extend this later"""
   

class MinViewersUnpacked(Exception):
    """For now just raises a min reached error, extend this later"""


class MVB(Frame,object):                                      # MVB = MultiViewerBase Class
    def __init__(self,parent=None,showviewers=3,height=800,width=2000):
        Frame.__init__(self,parent,bg=bg,width=width,height=height)
        self.viewers = []
        self.panels = {}                                         # keep track of button panels and radiobuttons etc
        self.packindex = 0                                       # Keeps track of which viewer has been packed
        self.maxviewers = 5
        self.bg = 'black'
        self.fg = 'green'
        self.deepfg = "#0704E4"
        self.highfg = '#233DFD'
        self.titlecolor ='#272EF5' #'#1116B8' #beige
        self.fontBig =  ("Arial",14,"bold")
        self.savedir = os.path.join(os.path.expanduser("~"),".ViewerBin")
    # Make Save Directory if it does not exists
        if not os.path.isdir(self.savedir):
            os.mkdir(self.savedir)

        self.showviewers = showviewers      #Set num of viewers shown
        self.buildframes()                  #Build structural Frames
        self.pack(fill=BOTH,expand=YES)
        self.pack_propagate(False)
        self._initviewers()


        self.LowerButtonDict = {'Edit in Emacs': self.editviews,
                                'Save View': self.saveview,
                                'Load View': self.loadview,
                                'Delete View': self.deleteview}
        
        self.ARButtonDict = {'+': lambda: self.packviewer(1),
                             '-': lambda: self.unpackviewer(1)}
        self.addbuttons()                       # Pack Buttons
        self.packviewer(self.showviewers)
        self.radiokeybind()
        self.focus_set()

######## Assign Event handlers to specific keypresses ##################
# Bind a number plus mod1 key for each radiobutton number. Remember the 
# Radio buttons actually start at zero, so we need to subtract 1 before
# setting the radiobutton IntVar
#######################################################################
    def radiokeybind(self):
        [self.bind("<Alt-KeyPress-{}>".format(i+1), self.radiokey)
         for i in range( int(self.panels["RadioViewBar"].index) )]
                     
    def radiokey(self,event):    
        self.focus_force()
        rad = int(event.keysym) - 1
        #self.panels["RadioViewBar"].v.set(rad)
        self.panels["RadioViewBar"].rads[rad].invoke()

#########################################################################    
# Initialize, build framework, add buttons.
#########################################################################
    def _initviewers(self):
        """ Initializes Viewers for max viewers allowed by app, set in MultiViewerBase"""
        for i in range(self.maxviewers):
            # Initialize starting viewers, kept in memory, and packed and unpacked as needed
            self.viewers.append(FileViewer(self,bg=self.bg,fg=self.fg,
                                           deepfg=self.deepfg,highfg=self.highfg,
                                           titlecolor=self.titlecolor,
                                           width = 30,file2view=None))

    def buildframes(self):
        """Build major structural Frames"""
        self.rside = Frame(self,bg=self.bg)
        self.rside.pack(side=RIGHT,fill=Y,expand=NO)
        #self.rside.pack_propagate(False)
        self.bside = Frame(self,bg=self.bg)
        self.bside.pack(side=BOTTOM,fill=X,expand=NO)
  
    
    def shout(self):
        print "Holy Jesus this is MultiViewer!"


    def addbuttons(self):
        """Add Buttons to specifed location"""
        self.panels["LowerButtons"] = (LowerButtons(self.LowerButtonDict,self.bside))
        self.panels["LowerButtons"].pack(side=LEFT,fill=BOTH,expand=NO)
        self.panels["AddRemove"] = (AddRemove(self.ARButtonDict,self.bside))
        self.panels["AddRemove"].pack(side=RIGHT,fill=BOTH,expand=NO)
        self.panels["RadioViewBar"] = RadioViewBar(self.savedir,self.loadview,self.rside)
        self.panels["RadioViewBar"].pack(side=RIGHT,fill=Y,expand=NO)
#########################################################################################
# Pack and Unpack Viewers
#########################################################################################
    def packviewer(self,num2pack):
        """Pack N viewers - up to maxviewers, then raise MaxViewersPacked Error"""      
        for i in range(num2pack):
            if self.packindex <= self.maxviewers:
                self.viewers[self.packindex].pack(side=LEFT,expand=1,fill=BOTH)
                self.packindex+=1
            else:
                raise MaxViewersPacked
                break
        
    def unpackviewer(self,num2unpack):
        """For now it just unpacks all... """
        for i in range(self.packindex, self.packindex - num2unpack, -1):
            if self.packindex > 1:
                self.viewers[self.packindex-1].pack_forget()
                self.packindex-=1
            else:
                raise MinViewersUnpacked
                break
#########################################################################################
# Save, Load, Delete and edit Views
#########################################################################################         
    def saveview(self):
        """Create own widget eventually which asks for file name, and
        ensures that there the max num of saved views is not breached"""
        try:
            viewname = asksaveasfilename(initialdir=self.savedir)
        except IOError as err:
            viewname = None
        if viewname:
            viewfiles = [(self.viewers[i].viewfile) for i in range(self.packindex)]
            pickle.dump(viewfiles,open(viewname,"wb"))          # Pickle List
        # UPDATE RADIOVIEW BARS
        self.refresh()


    def loadview(self,viewname=None):
        """Eventually create own widget that shows the list of saved views
        and allows user to select from list, perhaps a list of buttons"""
        
        if not viewname:
            # If there is not viewname given to function, we presume we are dealing with a fresh load button
            # Thus we ask user for file to load, go to initial savebin directory first
            try:
                viewname = askopenfilename(initialdir=self.savedir)
            except IOError as err:
                viewname = None
                
        else:
            # Most cases this will be called by radio button and the like, thus will have a viewname
            # Passed into the function, in this case we set viewname as full path name.
            viewname = os.path.join(self.savedir,viewname)
        
        if viewname:
            viewfiles = pickle.load(open(viewname))             # Load up viewfile list
            self.unpackviewer(self.packindex -1)                    # Unpack all views
            for viewer,viewfile in zip(self.viewers,viewfiles):  #Zip loaded viewfile together with a viewer
                viewer.viewfile = viewfile                      # Set the new viewfile (runs property set)
            self.packviewer(len(viewfiles)-1)                     # Repack views = to number of views in viewfile (-1 since we have 1 loaded all ready)

    def deleteview(self):
        # Find what RadioButton index we are on
        # Reload the viewlist and correlate the index with the view
        # Delete the corrisponding viewname and refresh the radiobuttons.

        deleteindex = self.panels["RadioViewBar"].v.get() #Get index of current radiobutton
        viewlist = os.listdir(self.savedir)    #Get list of saved views
        for index,view in enumerate(sorted(viewlist)): # Enumerate alphabetically, just like radiobutton outlay
            if index == deleteindex:   #Match the two indices
                viewname = os.path.join(self.savedir,view)    # Get full path
                print "we will delete view: ", viewname   # Not yet implemented
                print "But feature not yet implemented until safeguards are in place"
        self.refreshradiobuttons()   # Refresh the radiobutton bar.

    def editviews(self):
        viewfiles = [(self.viewers[i].viewfile) for i in range(self.packindex) 
                     if self.viewers[i].viewfile is not None]
        if viewfiles:
            subprocess.Popen('emacs -geometry 140x60 {}'.format(' '.join(viewfiles)), shell=True)
###################################################################################################        
# Refresh the application after modification.
###################################################################################################
    def refresh(self):
        self.panels["RadioViewBar"].pack_forget() # Unpack
        self.panels["RadioViewBar"] = RadioViewBar(self.savedir,self.loadview,self.rside) # Reload
        self.panels["RadioViewBar"].pack(side=RIGHT,fill=Y,expand=NO) # Repack
        self.radiokeybind()
            
        
            
    
