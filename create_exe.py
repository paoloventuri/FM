import os, shutil

shutil.copy2('FM', 'dist/FM')
os.system("start setup.py py2exe")