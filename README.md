
MultiViewer
===========

>A file viewing program allowing for saved displayed views
>of files. Basic editing, emacs linkage and viewer increase
>decrease permitted.

Summary
-------

Need to write summary

### Future Implementation

* See if calling `invoke()` simplies the radiobutton-after-save refresh.
* 'Exit edit without save' does not restore original file when pressed.
* Change position of viewers.
* Change name of some classes.

### Change Log
#### December 21, 2011
* added README.md

#### Unknown Date, 2011
* Totally Changed the namespace structure of the program.
  - Hollowed out MultiViewerMain and put all functionality including
  frame functionality in the MVB class.
  - Now the methods of the FileViewer are passed in as arguements
  to initialize the various buttons, so the buttons aquire the 
  appropriate namespaces of MVB and can share data and
  call each others methods. 
* This finally allowed the implementation of the refreshing of the 
  Radiobuttons after saving a new view. Though now that I know
  about calling `invoke()` on the radiobutton in question, this
  may simpify the script somewhat.

#### January 5th, 2012
* Added alt-num keyboard shortcuts to the radiobuttons. 
