# ArchFrame -> Main Control Frame with Class variables to be
#               shared by component Frames
#
#######################################################
#!/usr/bin/ python2

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from viewer import FileViewer
import os, os.path, pickle, subprocess


class MaxViewersPacked(Exception):
    """For now just raises a max reached error, extend this later"""
   

class MinViewersUnpacked(Exception):
    """For now just raises a min reached error, extend this later"""




class MVB(object):                                      # MVB = MultiViewerBase Class
    viewers = []
    panels = []                                         # keep track of button panels and radiobuttons etc


    packindex = 0                                       # Keeps track of which viewer has been packed
    maxviewers = 5
    bg = 'black'
    fg = 'green'
    deepfg = "#0704E4"
    highfg = '#233DFD'
    titlecolor ='#272EF5' #'#1116B8' #beige
    fontBig =  ("Arial",14,"bold")
    savdir = os.path.join(os.path.expanduser("~"),".ViewerBin")
    # Make Save Directory if it does not exists
    if not os.path.isdir(savdir):
        os.mkdir(savdir)


    def packviewer(self,num2pack):
        """Pack N viewers - up to maxviewers, then raise MaxViewersPacked Error"""
        
        for i in range(num2pack):
            if MVB.packindex <= MVB.maxviewers:
                MVB.viewers[MVB.packindex].pack(side=LEFT,expand=1,fill=BOTH)
                MVB.packindex+=1
            else:
                raise MaxViewersPacked
                break
        
    def unpackviewer(self,num2unpack):
        """For now it just unpacks all... """
        for i in range(MVB.packindex, MVB.packindex - num2unpack, -1):
            if MVB.packindex > 1:
                MVB.viewers[MVB.packindex-1].pack_forget()
                MVB.packindex-=1
            else:
                raise MinViewersUnpacked
                break


            
    def saveview(self):
        """Create own widget eventually which asks for file name, and
        ensures that there the max num of saved views is not breached"""
        try:
            viewname = asksaveasfilename(initialdir=MVB.savdir)
        except IOError as err:
            viewname = None
        if viewname:
            viewfiles = [(MVB.viewers[i].viewfile) for i in range(MVB.packindex)]
            pickle.dump(viewfiles,open(viewname,"wb"))          # Pickle List
            
    def loadview(self,viewname=None):
        """Eventually create own widget that shows the list of saved views
        and allows user to select from list, perhaps a list of buttons"""
        
        if not viewname:
            # If there is not viewname given to function, we presume we are dealing with a fresh load button
            # Thus we ask user for file to load, go to initial savebin directory first
            try:
                viewname = askopenfilename(initialdir=MVB.savdir)
            except IOError as err:
                viewname = None
                
        else:
            # Most cases this will be called by radio button and the like, thus will have a viewname
            # Passed into the function, in this case we set viewname as full path name.
            viewname = os.path.join(MVB.savdir,viewname)
        
        if viewname:
            viewfiles = pickle.load(open(viewname))             # Load up viewfile list
            self.unpackviewer(MVB.packindex -1)                    # Unpack all views
            for viewer,viewfile in zip(MVB.viewers,viewfiles):  #Zip loaded viewfile together with a viewer
                viewer.viewfile = viewfile                      # Set the new viewfile (runs property set)
            self.packviewer(len(viewfiles)-1)                     # Repack views = to number of views in viewfile (-1 since we have 1 loaded all ready)
            
    def editviews(self):
        viewfiles = [(MVB.viewers[i].viewfile) for i in range(MVB.packindex) if MVB.viewers[i].viewfile is not None]
        if viewfiles:
            subprocess.Popen('emacs -geometry 140x60 {}'.format(' '.join(viewfiles)), shell=True)
        
        
            
        
            
    
