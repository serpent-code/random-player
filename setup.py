from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\SRS\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\SRS\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"

build_exe_options = {"packages": ["os","tkinter","keyboard"], "include_files": [
                r"C:\Users\SRS\AppData\Local\Programs\Python\Python36\DLLs\tcl86t.dll",
                 r"C:\Users\SRS\AppData\Local\Programs\Python\Python36\DLLs\tk86t.dll"]}


setup(name="SerpentLabs Random Player",
      version="1.6",
      description = "Open random files from given directories.",
      options = {"build_exe": build_exe_options},
      executables = [Executable("Random Player.pyw",base="Win32GUI",
                    icon='.//images//dice-cube-outlinenimnimalpha3.ico',
                    copyright = "SerpentLabs Inc.")])