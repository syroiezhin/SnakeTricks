from setuptools import setup

APP = ['MindNotes.py']
DATA_FILES = ['settings.json', 'rerun.sh', 'MN.png']
OPTIONS = { 
    'iconfile':'MN.png',
    'argv_emulation': True, 
    'plist': { 'LSUIElement': True }, 
    'packages': ['pyperclip', 'json', 'googletrans', 'rumps'] 
    }
setup( app=APP, data_files=DATA_FILES, options={'py2app': OPTIONS}, setup_requires=['py2app'] )
