"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 5 November 2013
Website: www.guptalab.org/dnacloud
This module is used to freeze the application.
#########################################################################
"""

from cx_Freeze import setup, Executable
import sys

includes = ["extraModules","panels","barcodeGenerator","encode","decode","HuffmanDictionary","pytxt2pdf"]
excludes = [
    '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
    'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
    'Tkconstants', 'Tkinter'
]
include_files = ['PIL/','barcode/']
if 'win' in sys.platform and not 'darwin' in sys.platform:
	include_files = ['barcode/','PIL/',"registryFile.py"]

build_exe_options = {
                     "includes":includes, 
                     "excludes":excludes,
                     "include_files":include_files
}

base = None
if "win" in sys.platform and not 'darwin' in sys.platform:
	base = "Win32GUI"

exe = Executable(
    script="MainFrame.py",
    icon = "DNAicon.ico",
    targetName="DNACloud.exe",
    base=base
)
 
setup(
    name = "DNACloud",
    version = "1",
    description = "An software to store Data",
    options = {"build_exe": build_exe_options},
    executables = [exe]
)
