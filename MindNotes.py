from pyperclip import copy
from json import load, dump
from os import system, popen
from rumps import debug_mode
from rumps import App, MenuItem
from googletrans import Translator
from rumps import quit_application, alert

VERSION = '2022.08.19'

'''
It is necessary to implement:
0) C̶r̶e̶a̶t̶e̶ a̶n̶ a̶p̶p̶r̶o̶x̶i̶m̶a̶t̶e̶ i̶n̶t̶e̶r̶f̶a̶c̶e̶ o̶f̶ t̶h̶e̶ i̶n̶t̶e̶n̶d̶e̶d̶ p̶r̶o̶g̶r̶a̶m̶
1) I̶m̶p̶l̶e̶m̶e̶n̶t̶ s̶a̶v̶i̶n̶g̶ d̶a̶t̶a̶ t̶o̶ a̶ J̶S̶O̶N̶ f̶i̶l̶e̶ a̶n̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ u̶p̶d̶a̶t̶e̶ p̶r̶o̶g̶r̶a̶m̶s̶ w̶h̶e̶n̶ c̶h̶a̶n̶g̶e̶s̶ a̶r̶e̶ m̶a̶d̶e̶
2) Add buttons: hide desktop; hide the name of the program; find global and local IP address
3) Add the ability to select a language
4) Create a form to create new notes
5) Add the ability to delete a note from the database
6) Implement icon change "day and night"
7) Сollect app file
'''

def Update(): system('bash rerun.sh')

def Save(denomination, variable):
    with open('settings.json', 'rt') as r: content = load(r)
    content[denomination] = variable.state
    with open('settings.json', 'wt') as w: dump(content, w, sort_keys=True, indent=2)

def Header(Title):
    Title.state = not Title.state
    Save( [name for name, value in locals().items() if value is Title][0] , Title )
    Update()

def Mode(Incognito): 
    Incognito.state = not Incognito.state
    Save( [name for name, value in locals().items() if value is Incognito][0] , Incognito )
    Update()

def Add(Add):   alert(title='Сreate Note', message='...', ok='Keep', cancel='Cancel')

def Quit(Exit): quit_application(sender=True)

def menu():
    Note = []
    Accents = []
    debug_mode(True)
    with open('settings.json', 'rt') as r: content = load(r)
    Сreate = MenuItem("Create", key="c", callback = Add)
    Invisible = MenuItem("Incognito", key="i", callback = Mode)
    Invisible.state = content['Incognito']
    Title = MenuItem("Hide Header", key="h", callback = Header)
    Title.state = content['Title']
    Exit = MenuItem("Quit", key="q", callback = Quit)

    return [ Сreate, None, [ "Settings", [ Invisible, [ "Language", Accents ], None, Title, None, " "+VERSION, None, Exit ] ], None, [ "Notes", Note ] ]

if __name__ == "__main__": App('MindNotes', icon = 'MN.png', title = 'MindNotes' if load(open('settings.json', 'rt'))['Title'] == 0 else None, menu = menu(), quit_button=None).run()