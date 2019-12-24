"""
This module launches the tkinter GUI for the SerpentLabs Random File Player (c).
Provided as-is and free of charge.
Courtesy of Serpentlabs Inc.

"""
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import ranplayer
import file_extensions
import db
import os
import sys
import _thread
import secrets
import keyboard
import atexit


def rand_next(event=None):
    result = ranplayer.rand_next(Path.get(), scan_sub.get(), filetypes.get(),
                               repeat_files_session.get(), repeat_files_persistent.get())

    if result == 'EmptyDirError':
        messagebox.showwarning("Empty Directories",
                               "Directories don't exist or are empty.")
    elif result == 'NoSuchTypeError':
        messagebox.showwarning("No Such Filetype",
                               "No such filetype in selected directories.")
    elif result == 'EndOfFilesReached':
        messagebox.showinfo("End Of Files Reached",
                            "All files have been played once.\nPress Play again to go through the files again!")
    else:
        try:
            listbox.insert(END, ranplayer.history[-1])
            listbox.selection_clear(0, listbox.size()-2)
            listbox.selection_set(listbox.size()-1)
            listbox.yview(END) 
        except:
            pass


def play_previous():
    result = ranplayer.play_previous()

    if result == 'RecentFilesEmpty':
        messagebox.showinfo("No History",
                               "You have to play some files first so that you could go backwards!")
    else:
        try:
            listbox.selection_clear(0, listbox.size()-1) 
            listbox.selection_set(listbox.size()+ranplayer.playlist_index)
            listbox.see(listbox.size()+ranplayer.playlist_index)

        except:
            pass

def play_next():
    result = ranplayer.play_next()

    try:
        listbox.selection_clear(0, listbox.size()-1)
        listbox.selection_set(listbox.size()+ranplayer.playlist_index)
        listbox.see(listbox.size()+ranplayer.playlist_index)
    except:
        pass

def create_history_window():
    global history_window, listbox, ws, hs

    if history_window is not None:
        close_history_window()

    else:
        lv_x = root.winfo_rootx()
        lv_y = root.winfo_rooty()
        history_window = Toplevel(root)
        history_window.transient(master=root)
        history_window.title('History')
        history_window.geometry(f'{720}x{410}+{lv_x + 564}+{lv_y - 46}')
        history_window.protocol("WM_DELETE_WINDOW", close_history_window)
        make_rightmenu_openexplore(history_window)
        scrollbar = Scrollbar(history_window)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(history_window,selectmode=BROWSE, yscrollcommand=scrollbar.set)
        listbox.config(height=15,width=50)
        listbox.pack(fill=BOTH, expand=1,padx=(3,0))

        scrollbar.config(command=listbox.yview)

        for item in ranplayer.history:
            listbox.insert(END, item)

        listbox.bind("<<ListboxSelect>>", history_select)
        listbox.bind("<Double-Button-1>", history_play)
        listbox.bind("<Return>", history_play)
        listbox.bind("<Delete>", history_removeitem)
        listbox.bind_class("Listbox", "<Button-3><ButtonRelease-3>", show_rightmenu_openexplore)
        listbox.selection_set(listbox.size()+ranplayer.playlist_index)
        listbox.see(listbox.size()+ranplayer.playlist_index)

def close_history_window():
    global history_window
    history_window.withdraw()
    history_window = None

def history_select(event):
    widget = event.widget
    selection=widget.curselection()
    try:
        ranplayer.playlist_index = selection[0] - listbox.size()
    except IndexError:
        pass

def history_play(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    ranplayer.playlist_index = selection[0] - listbox.size()
    os.startfile(value)

def history_explorefolder(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    folder = value.split('\\')[:-1]
    folder = '\\'.join(folder)
    os.startfile(folder)

def history_removeitem(event):
    widget = event.widget
    selection=widget.curselection()
    ranplayer.history.pop(selection[0])
    listbox.delete(selection[0])

def listen_for_hotkey():
    listen_text.set("Listening...")
    listenbutton.update()
    root.focus()

    keyboard.unhook_all()
    root.unbind("<Return>")
    root.unbind("<Escape>")

    globalhotkey_entry.config(state=DISABLED)

    k=keyboard.read_shortcut()

    if k == 'enter' or k == 'esc' or k == 'plus' or k == 'decimal' or len(k) == 1:
        k = 'Invalid sequence'

    globalhotkey.set(k)
    globalhotkey_entry.config(state=NORMAL)

    listen_text.set("Listen")
    keyboard.hook(globalhotkey_randnext)
    root.after(200, root_key_bind)

def listen_for_hotkey_th():
    _thread.start_new_thread(listen_for_hotkey,())

def root_key_bind():
    root.bind("<Return>", rand_next)
    root.bind("<Escape>", quit_all)


def globalhotkey_randnext(e):
    if keyboard.is_pressed(str(globalhotkey.get()).strip().lower()):
        rand_next()


def on_exit():
    db.on_exit(Path.get(), ranplayer.path_list, scan_sub.get(),
               filetypes.get(), repeat_files_session.get(), repeat_files_persistent.get(),
               clear_history.get(), globalhotkey.get())

def repeat_pers_set():
    if not repeat_files_session.get():
        repeat_pers.config(state=DISABLED)
    else:
        repeat_pers.config(state=NORMAL)


def repeat_pers_init():
    if not lsrepeat_session:
        repeat_pers.config(state=DISABLED)
    else:
        repeat_pers.config(state=NORMAL)


def make_rightmenu_cutcopypaste(w):
    global the_menu
    the_menu = Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")


def show_rightmenu_cutcopypaste(e):
    w = e.widget
    the_menu.entryconfigure("Cut",command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

def make_rightmenu_openexplore(w):
    global the_menu2
    the_menu2 = Menu(w, tearoff=0)
    the_menu2.add_command(label="Open")
    the_menu2.add_command(label="Open containing folder")
    the_menu2.add_command(label="Remove this item from history")


def show_rightmenu_openexplore(e):
    w = e.widget
    index = w.nearest(e.y)
    item = w.get(index)
    listbox.selection_clear(0, listbox.size()-1)
    listbox.selection_set(index)

    the_menu2.entryconfigure("Open",
        command=lambda: w.event_generate(history_play(e)))
    the_menu2.entryconfigure("Open containing folder",
        command=lambda: w.event_generate(history_explorefolder(e)))
    the_menu2.entryconfigure("Remove this item from history",
        command=lambda: w.event_generate(history_removeitem(e)))
    the_menu2.tk.call("tk_popup", the_menu2, e.x_root, e.y_root)

def direntry_callback(event):
    direntry.selection_range(0, END)

def update_dirs():
    direntry['values'] = ranplayer.path_list

def open_readme():
    os.startfile('README.txt')

def quit_all(event=None):
    sys.exit()

def about_display():
    messagebox.showinfo("About", """SerpentLabs Random File Player Version 1.6

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

This program is released under GNUGPLv3.
Copyright (C) 2017 SerpentLabs Inc.""")


def eightballpress():
    possiblelist = ("It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Maybe",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful.")

    eightballanswer = secrets.choice(possiblelist)
    eightballtext.config(text=eightballanswer)

################################################################################################
################################################################################################
################################################################################################
################################################################################################

lastpath = db.lastpath
lscansub = db.lscansub
lasttypes = db.lasttypes
lsrepeat_session = db.lsrepeat_session
lsrepeat_persistent = db.lsrepeat_persistent
lsglobalhotkey = db.lsglobalhotkey
lsclear_history = db.lsclear_history
typechoices = [k for k in file_extensions.hardcoded_extensions]

history_window = None

root = Tk()

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

root.geometry(f'{560}x{390}+{ws//36}+{hs//15}')

root.minsize(490,380)

root.iconbitmap(default='.//images//dice-cube-outlinenimnimalpha3.ico')
root.title("Random Player")

root_key_bind()

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=9)
root.columnconfigure(2, weight=0)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.rowconfigure(9, weight=1)

menu = Menu(root)
root.config(menu=menu)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Readme", command=open_readme)
helpmenu.add_command(label="About", command=about_display)
helpmenu.add_command(label="Exit", command=quit_all)

make_rightmenu_cutcopypaste(root)

(Label(root, text="SerpentLabs Random File Player", font="Calibri 15 bold")
 .grid(row=1, columnspan=4, pady=(9, 9), sticky=(E, W, N, S)))

Label(root, text="Directories:").grid(row=2, column=0, pady=(8, 2), padx=(10, 0), sticky='e')
Path = StringVar()  # defines the widget state as string
direntry = ttk.Combobox(root, textvariable=Path, postcommand=update_dirs)
direntry.bind("<FocusIn>", direntry_callback)
direntry.bind_class("TCombobox", "<Button-3><ButtonRelease-3>", show_rightmenu_cutcopypaste)
direntry.grid(row=2, column=1, columnspan=2, pady=(8, 2), sticky=(E, W))
Path.set(lastpath)

Label(root, text="Filetypes:").grid(row=3, column=0, pady=(8, 2), padx=(10, 0), sticky='e')
filetypes = StringVar()
(ttk.Combobox(root, width=41, textvariable=filetypes, values=typechoices)
 .grid(row=3, column=1, columnspan=2, pady=(8, 2), padx=(0, 130), sticky='w'))
filetypes.set(lasttypes)

scan_sub = BooleanVar()
(Checkbutton(root, text="Scan subdirectories for files", variable=scan_sub)
 .grid(row=4, column=1, padx=(0, 0), pady=(10, 2), sticky='w'))
scan_sub.set(lscansub)

repeat_files_session = BooleanVar()
(Checkbutton(root, text="Open unique files for this session",
             variable=repeat_files_session,
             command=repeat_pers_set)
 .grid(row=5, column=1, padx=(0, 0), pady=(10, 0), sticky='w'))
repeat_files_session.set(lsrepeat_session)

repeat_files_persistent = BooleanVar()
repeat_pers = Checkbutton(root, text="Also between sessions",
                          variable=repeat_files_persistent)
repeat_pers.grid(row=6, column=1, padx=(0, 0), pady=(1, 10), sticky='w')
repeat_files_persistent.set(lsrepeat_persistent)

repeat_pers_init()

clear_history = BooleanVar()
clear_hist = Checkbutton(root, text="Clear history window on exit",
                          variable=clear_history)
clear_hist.grid(row=7, column=1, padx=(0, 0), pady=(1, 10), sticky='w')
clear_history.set(lsclear_history)

Label(root, text="Global Hotkey:").grid(row=8, column=0, pady=(8, 14), padx=(10, 0), sticky='e')
globalhotkey = StringVar()
globalhotkey_entry = Entry(root, width=37, textvariable=globalhotkey)
globalhotkey_entry.grid(row=8, column=1, pady=(8, 14), padx=(0, 0), sticky='w')
globalhotkey.set(lsglobalhotkey)

listen_text = StringVar()
listenbutton = Button(root, textvariable=listen_text, command=listen_for_hotkey_th)
listen_text.set("Listen")
listenbutton.grid(row=8, column=1, columnspan=2, pady=(0, 6), padx=(230, 0), sticky='w')

eightballpic = PhotoImage(file=".//images//8-Ball-Pool-PNG-Photossmaller.png")
eightballbutton = Button(root, image=eightballpic, height=38, width=38, command=eightballpress)
eightballbutton.grid(row=9, column=0, pady=(0, 0), padx=(10, 0))

eightballtext = Label(root, text="Consult the magic 8 ball for important decisions.", font="Constantia 11")
eightballtext.grid(row=9, column=1, columnspan=2, pady=(0, 0), padx=(0, 60))

(Label(root, text="""How did reason come into the world?
    As is fitting, in an irrational manner, by accident.
    One will have to guess at it as at a riddle.
    -Friedrich Nietzsche""""", font="Calibri 9")
 .grid(row=10, column=0, pady=2, padx=(0, 50), columnspan=2))

historypic = PhotoImage(file=".//images//history.png")
historybutton = Button(root, image=historypic,command=create_history_window,height=50, width=45)
historybutton.grid(row=10, column=1, pady=(0, 16), padx=(0, 7), sticky=(S, E))

prevpic = PhotoImage(file=".//images//prev.png")
prevbutton = Button(root, image=prevpic, command=play_previous,height=50, width=33)
prevbutton.grid(row=10, column=2, pady=(0, 16), padx=(0, 103), sticky=(S, W))


playpic = PhotoImage(file=".//images//play.png")
playbutton = Button(root, image=playpic, command=rand_next, height=50, width=90)
playbutton.grid(row=10, column=2, pady=(0, 16), padx=(0, 3), sticky=(S, E))

nextpic = PhotoImage(file=".//images//next.png")
nextbutton = Button(root, image=nextpic, command=play_next,height=50, width=33)
nextbutton.grid(row=10, column=3, pady=(0, 16), padx=(0, 10), sticky=(S, E))

keyboard.hook(globalhotkey_randnext)

atexit.register(on_exit)

root.mainloop()
