"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 28 July 2013
Website: www.guptalab.org/dnacloud
This module is the registry file used to create registry entry for .dnac
files.
#########################################################################
"""

from _winreg import *
import sys, os

if hasattr(sys, "frozen"):
        PATH = os.path.dirname(sys.executable)
else:
        PATH = os.path.dirname(os.path.abspath(__file__))

xyzKey = CreateKey(HKEY_CLASSES_ROOT, ".dnac")
SetValue(xyzKey, None, REG_SZ, "dnaFile")
CloseKey(xyzKey)

myTestKey = CreateKey(HKEY_CLASSES_ROOT, "dnaFile")
iconKey = CreateKey(myTestKey, "DefaultIcon")

shellKey = CreateKey(myTestKey, "shell")
openKey = CreateKey(shellKey, "open")
cmdKey = CreateKey(openKey, "command")
CloseKey(myTestKey)
CloseKey(myTestKey)
CloseKey(shellKey)
CloseKey(openKey)

SetValue(iconKey, None, REG_SZ, PATH + '/../icons/DNAicon.ico')
CloseKey(iconKey)
SetValue(cmdKey, None, REG_SZ, "notepad.exe %1")
CloseKey(iconKey)


