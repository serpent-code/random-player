# random-player

This small GUI program for Windows randomly selects files from one 
or multiple directories and passes it to the OS to be opened.
The OS in turn passes the file to the program already associated 
with the file extension and opens it.

It only works on windows because os.startfile(file) only works on windows and I haven't yet looked for a replacement 
to make it work under Linux.

It can optionally select and open random files from all subdirectories 
in given directory trees.

By default it opens any files present in the Path field with
any extensions when "All" is passed in Filetypes field.
But arbitrary number of case-insensitive file extensions may be passed
in Filetypes field, separated by commas, semicolons or spaces (among other delimiters).

Delimiters supported in the Path field are *?<>"'
Delimiters supported in the Filetypes field are ;,*?<>"' and spaces.

When the option "Open unique files for this session" is enabled,
it will open unique files each time but loses it's memory of files already
opened when program exits. To make the list of files already opened
persistent between sessions enable the "Also between sessions" option.

"History" refers to recently opened files. The history window can be opened by the clock icon
on the bottom. The Next and Previous buttons also go through files in this list and open
files in the order that each one suggests. History will be cleared on program exit if 
"Clear history window on exit" option is enabled. Otherwise it's persistent between sessions.

Global hotkey feature is provided for your convenience to initiate opening of the next file
regardless of what window currently is in focus.

The program also remembers all of its configuration when closed and restores settings
upon being launched again.

Example usage:

Path : "D:\Softcore" , "C:\dir1*C:\dir2"
Filetypes : "All" , "Images", "mp4" , "flv AVI Mpeg", "txt*pdf; epub"

Whole Filetype categories (and their short forms) and arbitrary extensions
can also be mixed.
The following are also valid Filetypes inputs:
"img videos", "vid imgs pdf", "aud img doc" 


The program is written and distributed with Python 3.6.3.
It leverages faster directory walking with os.scandir() introduced in Python 3.5
as well as the secrets module in Python 3.6.

A frozen build including pythong 3.6.3 is available for windows 64 bit.

For license information please see the license file.

Project was active circa 2017.
