#!/usr/bin/python2
# Command Window - For displaying text view apps as well as
# Other useful desktop widgets.
4#
#######################################################


from Tkinter import *
from Modules.MultiViewer import MVB
import os, os.path, subprocess

            

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
    M = MVB(parent = root, showviewers=3, width=PIXwidth)
    M.mainloop()



    # TO DO, Simply filetest routines and warning labels, + add button on warning labels
    

