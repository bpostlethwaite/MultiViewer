# MultiViewerWidgets -> Widgets to go along with the MultiViewer
#
# Still to create   => Save and Load list widget
#                   => strvar() command display
#                   => Error based logging system for command display
#######################################################
#!/usr/bin/env python

from Tkinter import *
from MultiViewer import MVB
import os


class ViewerButton(Button):
    """ Standardized button options across viewer application"""
    def __init__(self,parent=None,**options):
        Button.__init__(self,parent,**options)
        self.config(activebackground=MVB.fg,highlightthickness=0,
                    bg=MVB.bg,fg=MVB.fg,relief=RAISED,bd=0)


class ViewerButtonBar(Frame,MVB):
    """ Standardized button frame"""
    def __init__(self,parent=None):
        Frame.__init__(self,parent,bg=MVB.bg)

    def addbuttons(self,**options):
        for key,value in self.ButtonDic.iteritems():
            button = ViewerButton(self,text=key,command=value)
            button.pack(side=LEFT,anchor=CENTER)
            button.config(**options)


class LowerButtons(ViewerButtonBar):
    def __init__(self,parent=None):
        super(LowerButtons, self).__init__(parent)
        self.ButtonDic = {'Edit in Emacs': self.editviews,
                          'Save View': self.saveview,
                          'Load View': self.loadview}
        self.addbuttons(padx=10,pady=4)


class RadioViewBar(Frame,MVB):
    def __init__(self,parent=None):
        Frame.__init__(self,parent,bg=MVB.bg)
        viewlist = os.listdir(MVB.savdir)
        v = IntVar()
        v = 99
        for index,view in enumerate(sorted(viewlist)):
            radio = Radiobutton(self,text=view,variable=v,value=index,
                                underline=0,
                                command=lambda view=view:self.loadview(view))
            radio.pack(anchor=W)
            radio.config(activebackground=MVB.bg,selectcolor=MVB.bg,
                         fg=MVB.fg,bg=MVB.bg,activeforeground=MVB.fg,
                         bd=0,highlightthickness=0)


class AddRemove(ViewerButtonBar):
    def __init__(self,parent=None):
        super(AddRemove, self).__init__(parent)
        self.ButtonDic = {'+': lambda: self.packviewer(1),
                          '-': lambda: self.unpackviewer(1)}
        self.addbuttons(padx=20,pady=0,font=MVB.fontBig)



            
    
if __name__ == '__main__':
    os.chdir("..")
    #ViewerButtonBar().pack(expand=YES,fill=BOTH)
    RadioViewBar().pack(expand=YES,fill=BOTH)
    mainloop()
