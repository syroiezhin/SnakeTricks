from pyperclip import copy # conda install -c conda-forge pyperclip
from json import load, dump
from os import system, popen
from rumps import debug_mode # pip install rumps
from googletrans import Translator # conda install -c conda-forge googletrans
from rumps import App, MenuItem, Window
from rumps import quit_application, alert

VERSION = '2022.08.20c'

'''
It is necessary to implement:
0) C̶r̶e̶a̶t̶e̶ a̶n̶ a̶p̶p̶r̶o̶x̶i̶m̶a̶t̶e̶ i̶n̶t̶e̶r̶f̶a̶c̶e̶ o̶f̶ t̶h̶e̶ i̶n̶t̶e̶n̶d̶e̶d̶ p̶r̶o̶g̶r̶a̶m̶
1) I̶m̶p̶l̶e̶m̶e̶n̶t̶ s̶a̶v̶i̶n̶g̶ d̶a̶t̶a̶ t̶o̶ a̶ J̶S̶O̶N̶ f̶i̶l̶e̶ a̶n̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ u̶p̶d̶a̶t̶e̶ p̶r̶o̶g̶r̶a̶m̶s̶ w̶h̶e̶n̶ c̶h̶a̶n̶g̶e̶s̶ a̶r̶e̶ m̶a̶d̶e̶
2) A̶d̶d̶ b̶u̶t̶t̶o̶n̶s̶:̶ h̶i̶d̶e̶ d̶e̶s̶k̶t̶o̶p̶;̶ h̶i̶d̶e̶ t̶h̶e̶ n̶a̶m̶e̶ o̶f̶ t̶h̶e̶ p̶r̶o̶g̶r̶a̶m̶;̶ f̶i̶n̶d̶ g̶l̶o̶b̶a̶l̶ a̶n̶d̶ l̶o̶c̶a̶l̶ I̶P̶ a̶d̶d̶r̶e̶s̶s̶
3) A̶d̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ s̶e̶l̶e̶c̶t̶ a̶ l̶a̶n̶g̶u̶a̶g̶e̶
4) C̶r̶e̶a̶t̶e̶ a̶ f̶o̶r̶m̶ t̶o̶ c̶r̶e̶a̶t̶e̶ n̶e̶w̶ n̶o̶t̶e̶s̶
5) Add the ability to delete a note from the database
6) Implement icon change "day and night"
7) Сollect app file
'''

def Update(): system('bash rerun.sh')

def Save(denomination, variable):
    with open('settings.json', 'rt') as r: content = load(r)
    content[denomination] = variable.state
    with open('settings.json', 'wt') as w: dump(content, w, sort_keys=True, indent=2)

def Desktop(HideDesktop):
    system(f"defaults write com.apple.finder CreateDesktop -bool {bool(HideDesktop.state)}; killall Finder")
    HideDesktop.state = not HideDesktop.state
    Save( [name for name, value in locals().items() if value is HideDesktop][0] , HideDesktop )

def Header(Title):
    Title.state = not Title.state
    Save( [name for name, value in locals().items() if value is Title][0] , Title )
    Update()

def Mode(Incognito): 
    Incognito.state = not Incognito.state
    Save( [name for name, value in locals().items() if value is Incognito][0] , Incognito )
    Update()

def Add(Add):
    name_site = Window(title='Сreate Note (1/3)', default_text='Google', message='Set note title', ok='Next', cancel='Cancel', dimensions=(200, 25)).run()
    if name_site.clicked == 1:
        url_site = Window(title='Сreate Note (2/3)', default_text='https://www.google.com', message='Paste the copied link to the source', ok='Next', cancel='Cancel', dimensions=(200, 25)).run()
        if url_site.clicked == 1:
            if alert(title='Сreate Note (3/3)', message='Click \'Keep\' to save to database', ok='Keep', cancel='Cancel') == 1: 
                with open('settings.json', 'rt') as r: content = load(r)
                content['Notes']['WebSite'].append(name_site.text)
                content['Notes']['URL'].append(url_site.text)
                with open('settings.json', 'wt') as w: dump(content, w, sort_keys=True, indent=2)
                Update()

def Global(IP): copy(ip) if alert(title=(ip := popen("curl ifconfig.me").read().strip()),       message="to paste the copied Global IP press Ctrl+V", ok='Click to save the IP to the clipboard') == 1 else print("ERROR")
def Local(IP):  copy(ip) if alert(title=(ip := popen("ipconfig getifaddr en0").read().strip()), message="to paste the copied Local IP press Ctrl+V",  ok='Click to save the IP to the clipboard') == 1 else print("ERROR")
def Quit(Exit): quit_application(sender=True)

def menu():
    Note = []
    Accents = []
    debug_mode(True)
    with open('settings.json', 'rt') as r: content = load(r)
    interface = content['Choose']['Menu']
    Сreate = MenuItem(interface[0], key="c", callback = Add)
    Invisible = MenuItem(interface[2], key="i", callback = Mode)
    Invisible.state = content['Incognito']
    HideDesktop = MenuItem(interface[4], key="d", callback = Desktop)
    HideDesktop.state = content['HideDesktop']
    Title = MenuItem(interface[5], key="h", callback = Header)
    Title.state = content['Title']
    GlobalIP = MenuItem(interface[6], key="g", callback = Global)
    LocalIP = MenuItem(interface[7], key="l", callback = Local)
    Exit = MenuItem(interface[8].capitalize(), key="q", callback = Quit)

    for key in content['Accents'].keys():
        def Language(Accents): 
            data = ["Сreate Note", "Settings", "Incognito Mode", "Menu Language", "Hide Desktop", "Hide Header", "Find out Global IP", "Find out Local IP", "Quit", "Version", "Notes"]
            content['Choose']['Language'] = str(Accents).split('\'', 1)[1].split('\'')[0]
            choose = content['Accents'][content['Choose']['Language']]
            translated = Translator().translate(data, src='en', dest=choose)
            content['Choose']['Menu'] = [translated[id].text for id in range(len(translated))]
            with open('settings.json', 'wt') as w: dump(content, w, sort_keys=True, indent=2)
            Update()
        Accents.append( MenuItem( key, callback = Language ) )

    for id,value in enumerate(content['Notes']['WebSite']):
        def Notes(Note):
            id = content['Notes']['WebSite'].index(str(Note).split('\'', 1)[1].split('\'')[0])
            system(f"open -a Google\ Chrome --new --args {content['Notes']['URL'][id]}") if content['Incognito'] == 0 else system(f"open -a Google\ Chrome --new --args -incognito {content['Notes']['URL'][id]}")
        Note.append( MenuItem(value, key=str(id+1) if id<9 else None, callback = Notes) )

    return [ Сreate, None, [ interface[1].capitalize(), [ Invisible, [ interface[3], Accents ], None, HideDesktop, Title, None, GlobalIP, LocalIP, None, interface[9].capitalize()+" "+VERSION, None, Exit ] ], None, [ interface[10].capitalize(), Note ] ]

if __name__ == "__main__": App('MindNotes', icon = 'MN.png', title = 'MindNotes' if load(open('settings.json', 'rt'))['Title'] == 0 else None, menu = menu(), quit_button=None).run()