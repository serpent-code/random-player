import marshal
import ranplayer
import os


try:
    db = open('.\\data\\last_state.data', 'rb')
    lastpath = marshal.load(db)
    lspathlist = marshal.load(db)
    lscansub = marshal.load(db)
    lasttypes = marshal.load(db)
    lsrepeat_session = marshal.load(db)
    lsrepeat_persistent = marshal.load(db)
    lsclear_history = marshal.load(db)
    lsglobalhotkey = marshal.load(db) 
    already_played = marshal.load(db)
    history = marshal.load(db)
    db.close()

except FileNotFoundError:
    try:
        os.mkdir('.\\data')
    except FileExistsError:
        pass
    finally:
        db = open('.\\data\\last_state.data', 'wb')
        db.close()
        lastpath = 'Enter directories here! Multiple directories separated by * or ?'
        lspathlist = []
        lscansub = True
        lasttypes = 'All'
        lsrepeat_session = False
        lsrepeat_persistent = False
        lsclear_history = False
        lsglobalhotkey = 'ctrl+shift+space'
        already_played = set()
        history = []


def on_exit(path, pathlist, scan_sub, filetypes, repeat_files_session,
            repeat_files_persistent, clear_history, globalhotkey):
    db = open('.\\data\\last_state.data', 'wb')

    marshal.dump(path, db)
    marshal.dump(pathlist, db)
    marshal.dump(scan_sub, db)
    marshal.dump(filetypes, db)
    marshal.dump(repeat_files_session, db)
    marshal.dump(repeat_files_persistent, db)
    marshal.dump(clear_history, db)
    marshal.dump(globalhotkey, db)


    if repeat_files_persistent and repeat_files_session:
        marshal.dump(ranplayer.already_played, db)
    else:
        marshal.dump(set(), db)


    if clear_history:
        marshal.dump([], db)
    else:
        marshal.dump(ranplayer.history, db)

    db.close()