from setuptools import setup # python setup.py py2app

setup(
    app=['SnakeTricks.py'],
    name="SnakeTricks",
    data_files=['settings.json', 'rerun.sh', 'icon.png'],
    setup_requires=['py2app'],
    options={'py2app': { 
        'iconfile':'NEU3RON.png',
        'argv_emulation': True, 
        'plist': { 'LSUIElement': True }, 
        'packages': ['pyperclip', 'json', 'googletrans', 'rumps'],
        'includes': ['pyperclip', 'json', 'googletrans', 'rumps']
        }
    },

    version='2022.08.23',
    description='menubar asst.',
    long_description="creates buttons for visiting sites in incognito mode and allows you to call up some useful functions on click thanks to the command line",

    author='@NEU3RON',
    license="Syroiezhin",
    author_email='v.syroiezhin@gmail.com',
    url="https://github.com/syroiezhin",
)
