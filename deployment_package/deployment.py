import sys; import os
from pathlib import Path
import configparser
import subprocess

def install(package):
    print('Installing:', fp)
    print('Install Exit Code:',
        subprocess.check_call(
            [sys.executable, "-m", "pip", 
             "install", package])
    )
    
lib_fp = Path('libraries')
ls = lib_fp.glob("*")
for fp in ls:
    if not fp.is_dir():
        print(fp, 'not a directory, skipped.')
        continue
        
    install(package=fp)
    
from mod.core import *