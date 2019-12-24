"""
This module does the directory walking on given directories,
making a list of all filenames (with paths) matching input criteria
and then randomly selects from said list and opens the file.

There is a caching mechanism implemented so that the list of files regenarates
only upon changing the inputs (paths/types/scanning subdirectory or not).
Therefore all file openings with a given setting happen instantly
after the first file has been opened.

"""
import db
import os
import re
import secrets
from file_extensions import hardcoded_extensions as ext


dirlist_cache = None
scan_sub_cache = True
dontrepeat_session_cache = True
dontrepeat_persistent_cache = False
filetypes_cache = None
types = None
filelist = []
playlist = []
already_played = db.already_played
history = db.history
playlist_index = 0
path_list = db.lspathlist


def rand_next(working_dirs, scan_sub, filetypes, dontrepeat_session, dontrepeat_persistent):
    global dirlist_cache, filetypes_cache, scan_sub_cache
    global dontrepeat_session_cache, dontrepeat_persistent_cache
    global filelist, playlist, playlist, types
    global already_played, history, playlist_index

    dirlist = re.split("""[*?<>"']""", working_dirs.strip())
    dirlist = list(filter(None, dirlist))

    if dirlist != dirlist_cache or scan_sub is not scan_sub_cache:
        filelist = []

        if scan_sub:
            for dir in dirlist:
                filelist.extend(f"{root}\\{filename}" for root, _ ,files in os.walk(dir) for filename in files)
        else:
            for dir in dirlist:
                filelist.extend(entry.path for entry in os.scandir(dir) if entry.is_file())

        if not filelist: return 'EmptyDirError'
        else: 
            if dirlist != dirlist_cache:
                path_keeper(working_dirs.strip())

    if (filetypes != filetypes_cache
        or dontrepeat_session is not dontrepeat_session_cache
        or dirlist != dirlist_cache or scan_sub is not scan_sub_cache):

        if   filetypes == 'All':       types = ''
        elif filetypes == 'Images':    types = ext['Images']
        elif filetypes == 'Audios':    types = ext['Audios']
        elif filetypes == 'Videos':    types = ext['Videos']
        elif filetypes == 'Documents': types = ext['Documents']
        elif filetypes == 'Archives':  types = ext['Archives']
        else:
            filetypes = filetypes.strip().lower()
            if filetypes in {'all', '*', ''}:
                types = ''
            else:
                types = re.split("""[ ;,*?<>"']""", filetypes)
                types = list(filter(None, types))
                temptypes = []
                for t in types:
                    if t in {'images','image','img','imgs'}:
                        temptypes.extend(ext['Images'])
                    if t in {'audios','audio','aud','auds'}:
                        temptypes.extend(ext['Audios'])
                    if t in {'videos','video','vid','vids'}:
                        temptypes.extend(ext['Videos'])
                    if t in {'documents','document','doc','docs'}:
                        temptypes.extend(ext['Documents'])
                    if t in {'archives','archive','arc','arcs'}:
                        temptypes.extend(ext['Archives'])
                types.extend(temptypes)
                types = tuple(types)


        playlist = [x for x in filelist if x[-6:].lower().endswith(types)]
        if not playlist: return 'NoSuchTypeError'

        filetypes_cache = filetypes
        dirlist_cache = dirlist
        scan_sub_cache = scan_sub
        dontrepeat_session_cache = dontrepeat_session
        dontrepeat_persistent_cache = dontrepeat_persistent

        if dontrepeat_persistent and dontrepeat_session:
            playlist = [x for x in playlist if x not in already_played]

        if not dontrepeat_session:
            already_played = set()

    if playlist:
        randindex = secrets.randbelow(len(playlist))

        if dontrepeat_session:
            file = playlist.pop(randindex)
            already_played.add(file)
        else:
            file = playlist[randindex]

        history.append(file)
        playlist_index = 0
        os.startfile(file)

    else:
        playlist = [x for x in filelist if x[-6:].lower().endswith(types)]
        already_played = set()
        return 'EndOfFilesReached'

def path_keeper(path):
    global path_list

    if path not in path_list:
        if len(path_list) < 5 :
            path_list.insert(0, path)
        else:
            path_list.pop()
            path_list.insert(0, path)



def play_previous():
    global playlist_index, history

    if len(history) == 0:
        return 'RecentFilesEmpty'

    if playlist_index == 0:
        playlist_index = -1

    try:
        file = history[playlist_index-1]
    except IndexError:
        playlist_index = 0
        file = history[playlist_index-1]
    playlist_index -= 1
    os.startfile(file)


def play_next():
    global playlist_index, history

    if len(history) == 0:
        return 'RecentFilesEmpty'

    if playlist_index == 0:
        pass
    elif playlist_index == -1:
        pass
    else:
        playlist_index += 1      
        file = history[playlist_index]
        os.startfile(file)

