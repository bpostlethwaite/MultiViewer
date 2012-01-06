# MultiViewerWidgets -> Widgets to go along with the MultiViewer
#
# Still to create   => Save and Load list widget
#                   => strvar() command display
#                   => Error based logging system for command display
#######################################################
#!/usr/bin/env python

from Tkinter import *
#from MultiViewer import bg
import os

bg = 'black'
fg = 'green'
fontBig =  ("Arial",14,"bold")


class ViewerButton(Button,object):
    """ Standardized button options across viewer application"""
    def __init__(self,parent=None,**options):
        Button.__init__(self,parent,**options)
        self.config(activebackground=fg,highlightthickness=0,
                    bg=bg,fg=fg,relief=RAISED,bd=0)


class ViewerButtonBar(Frame,object):
    """ Standardized button frame"""
    def __init__(self,buttonDict,parent=None):
        Frame.__init__(self,parent,bg=bg)

    def addbuttons(self,**options):
        for text,command in self.buttonDict.iteritems():
            button = ViewerButton(self,text=text,command=command)
            button.pack(side=LEFT,anchor=CENTER)
            button.config(**options)


class LowerButtons(ViewerButtonBar):
    def __init__(self,buttonDict,parent=None):
        super(LowerButtons, self).__init__(buttonDict,parent)
        self.buttonDict = buttonDict
        self.addbuttons(padx=10,pady=4)


class RadioViewBar(Frame,object):
    def __init__(self,savedir,loadview,parent=None):
        Frame.__init__(self,parent,bg=bg)
        viewlist = os.listdir(savedir)
        self.rads = []
        self.v = IntVar()
                
        # We do text = ... index + 1, so that the number of the radiobutton starts at 1 not zero.
        for index,view in enumerate(sorted(viewlist)):
            radio = Radiobutton(self,text=str(index + 1) + ".) " + view,variable=self.v,value=(index+1),
                                underline=0,
                                command=lambda view=view:loadview(view))
            radio.pack(anchor=W)
            radio.config(activebackground=bg,selectcolor=bg,
                         fg=fg,bg=bg,activeforeground=fg,
                         bd=0,highlightthickness=0)
            self.rads.append(radio)
        
        self.index = index + 1


class AddRemove(ViewerButtonBar):
    def __init__(self,buttonDict,parent=None):
        super(AddRemove, self).__init__(buttonDict,parent)
        self.buttonDict = buttonDict
        self.addbuttons(padx=20,pady=0,font=fontBig)



            
    
if __name__ == '__main__':
    os.chdir("..")
    #ViewerButtonBar().pack(expand=YES,fill=BOTH)
    RadioViewBar().pack(expand=YES,fill=BOTH)
    mainloop()
