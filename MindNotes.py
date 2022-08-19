from json import load, dump
from rumps import debug_mode
from rumps import App, MenuItem
from rumps import quit_application, alert

VERSION = '2022.08.19'

'''
It is necessary to implement:
0) C̶r̶e̶a̶t̶e̶ a̶n̶ a̶p̶p̶r̶o̶x̶i̶m̶a̶t̶e̶ i̶n̶t̶e̶r̶f̶a̶c̶e̶ o̶f̶ t̶h̶e̶ i̶n̶t̶e̶n̶d̶e̶d̶ p̶r̶o̶g̶r̶a̶m̶
1) Implement saving data to a JSON file and the ability to update programs when changes are made
2) Add buttons: hide desktop; hide the name of the program; find global and local IP address
3) Add the ability to select a language
4) Create a form to create new notes
5) Add the ability to delete a note from the database
6) Implement icon change "day and night"
'''

def Mode(Incognito): Incognito.state = not Incognito.state

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
    Exit = MenuItem("Exit", key="q", callback = Quit)

    return [ Сreate, None, [ "Settings", [ Invisible, [ "Language", Accents ], None, " "+VERSION, None, Exit ] ], None, [ "Notes", Note ] ]

if __name__ == "__main__": App('Mind', icon = 'MN.png', title = 'MindNotes' if load(open('settings.json', 'rt'))['Title'] == 0 else None, menu = menu(), quit_button=None).run()