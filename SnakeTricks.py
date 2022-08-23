from rumps import App, MenuItem, Window, quit_application, alert#, debug_mode # pip install rumps
from googletrans import Translator # pip install googletrans==4.0.0-rc1
from pyperclip import copy # conda install -c conda-forge pyperclip
from os import system, popen, path
from json import load, dump

VERSION = '2022.08.23'

'''
I̶t̶ i̶s̶ n̶e̶c̶e̶s̶s̶a̶r̶y̶ t̶o̶ i̶m̶p̶l̶e̶m̶e̶n̶t̶:̶
0) C̶r̶e̶a̶t̶e̶ a̶n̶ a̶p̶p̶r̶o̶x̶i̶m̶a̶t̶e̶ i̶n̶t̶e̶r̶f̶a̶c̶e̶ o̶f̶ t̶h̶e̶ i̶n̶t̶e̶n̶d̶e̶d̶ p̶r̶o̶g̶r̶a̶m̶
1) I̶m̶p̶l̶e̶m̶e̶n̶t̶ s̶a̶v̶i̶n̶g̶ d̶a̶t̶a̶ t̶o̶ a̶ J̶S̶O̶N̶ f̶i̶l̶e̶ a̶n̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ u̶p̶d̶a̶t̶e̶ p̶r̶o̶g̶r̶a̶m̶s̶ w̶h̶e̶n̶ c̶h̶a̶n̶g̶e̶s̶ a̶r̶e̶ m̶a̶d̶e̶
2) A̶d̶d̶ b̶u̶t̶t̶o̶n̶s̶:̶ h̶i̶d̶e̶ d̶e̶s̶k̶t̶o̶p̶;̶ h̶i̶d̶e̶ t̶h̶e̶ n̶a̶m̶e̶ o̶f̶ t̶h̶e̶ p̶r̶o̶g̶r̶a̶m̶;̶ f̶i̶n̶d̶ g̶l̶o̶b̶a̶l̶ a̶n̶d̶ l̶o̶c̶a̶l̶ I̶P̶ a̶d̶d̶r̶e̶s̶s̶
3) A̶d̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ s̶e̶l̶e̶c̶t̶ a̶ l̶a̶n̶g̶u̶a̶g̶e̶ 
4) C̶r̶e̶a̶t̶e̶ a̶ f̶o̶r̶m̶ t̶o̶ c̶r̶e̶a̶t̶e̶ n̶e̶w̶ n̶o̶t̶e̶s̶
5) C̶o̶l̶l̶e̶c̶t̶ a̶p̶p̶ f̶i̶l̶e̶
6) A̶d̶d̶ t̶h̶e̶ a̶b̶i̶l̶i̶t̶y̶ t̶o̶ d̶e̶l̶e̶t̶e̶ a̶ n̶o̶t̶e̶ f̶r̶o̶m̶ t̶h̶e̶ d̶a̶t̶a̶b̶a̶s̶e̶
7) I̶m̶p̶l̶e̶m̶e̶n̶t̶ i̶c̶o̶n̶ c̶h̶a̶n̶g̶e̶ "̶d̶a̶y̶ ̶a̶n̶d̶ ̶n̶i̶g̶h̶t̶"̶
'''

def Quit(Exit): quit_application(sender=True)

def IP(IP): copy(ip) if alert( title = ( ip := popen("curl ifconfig.me").read().strip() if (list((Interface := Database()['Interface']['Menu']).keys())[list(Interface.values()).index( str(IP).split('\'', 1)[1].split('\'')[0] )] == 'Find out global IP') else popen("ipconfig getifaddr en0").read().strip() ) , message="to paste the copied IP press Ctrl+V", ok='Click to save the IP to the clipboard') == 1 else print("ERROR")

def Database(): return load( open('settings.json', 'rt') )

def Save(content): dump(content, open('settings.json', 'wt'), sort_keys=True, indent=2); system('bash rerun.sh')

def Switching(variable):
    content = Database()
    if ( naming := list((Interface := content['Interface']['Menu']).keys())[list(Interface.values()).index(str(variable).split('\'', 1)[1].split('\'')[0]) ] ) == 'Hide Desktop' : system(f"defaults write com.apple.finder CreateDesktop -bool {bool(variable.state)}; killall Finder")
    variable.state = not variable.state
    content['Switch'][ naming ] = variable.state
    Save(content)

def Add(Add):
    try:
        content = Database()
        while True:
            if (name_site := Window(title='Сreate Note (1/3)', default_text='Google' if content['Switch']['Hide Hints'] == 0 else "", message='Set note title', ok='Next', cancel='Cancel', dimensions=(200, 20)).run()).clicked == 1:
                if (url_site := Window(title='Сreate Note (2/3)', default_text='https://www.google.com' if content['Switch']['Hide Hints'] == 0 else "", message='Paste the copied link to the source', ok='Next', cancel='Cancel', dimensions=(200, 20)).run()).clicked == 1:
                    if alert(title='Сreate Note (3/3)', message='Click \'Keep\' to save to database', ok='Keep', cancel='Cancel') == 1: 
                        content['Notesbox']['Naming'].append(name_site.text)
                        content['Notesbox']['URL'].append(url_site.text)
                    else: break
                else: break
            else: break
    finally: Save(content)

def Delete(Remove):
    idx = 0
    databook = {}
    content = Database()
    if (list_site := Window(title='Deleting Notes', default_text=str("\n".join(content['Notesbox']['Naming'])), message='please, remove unnecessary notes from the list', ok='Next', cancel='Cancel', dimensions=(200, 20*len(content['Notesbox']['Naming']))).run()).clicked == 1:
        for control,adress in zip(content['Notesbox']['Naming'],content['Notesbox']['URL']):
            try:
                if control == (list_site.text).replace('\n', ' ').split()[idx]: 
                    databook[control] = adress
                    idx += 1
            except: pass
        content['Notesbox']['Naming'] = list(databook.keys())
        content['Notesbox']['URL'] = list(databook.values())
        Save(content)

def Notes(Note): 
    content = Database()
    id = content['Notesbox']['Naming'].index(str(Note).split('\'', 1)[1].split('\'')[0])
    onoff = " " if content['Switch']['Incognito Mode'] == 0 else " -incognito "
    system(f"open -a Google\ Chrome --new --args{onoff}{ content['Notesbox']['URL'][ id ]}")

def Language(Accents):
    content = Database()
    content['Interface']['Language'] = str(Accents).split('\'', 1)[1].split('\'')[0]
    for value in list(content['Interface']['Menu'].keys()) : content['Interface']['Menu'][value] = Translator().translate( value, src='en', dest = content['Accents'][content['Interface']['Language']] ).text
    Save(content)

def IconSelection(Icon): 
    content = Database()
    pwd = popen('pwd').read().strip()
    
    while True:
        if (new_pwd := Window(title='Сhange program icon', default_text=f"{pwd}/{content['Icon']}" if content['Switch']['Hide Hints'] == 0 else "", message='enter the full address of the new icon', ok='Keep', cancel='Cancel', dimensions=(400, 20)).run()).clicked==1:
            if path.isfile(new_pwd.text):
                system(f'cp {new_pwd.text} {pwd}/new_icon.png')
                content['Icon'] = 'new_icon.png'
                break
            else:
                content['Icon'] = 'icon.png'
                alert(title = 'ERROR', message = 'the specified file was not found at the specified address')
        else: break
    Save(content)

def menu():
    # debug_mode(True)
    M = {}
    Note = []
    Accents = []
    content = Database()
    Menu = content['Interface']['Menu']

    for button,denomination,func in zip(['m','i','d','h','n','g','l','c','e','q','s'],["Incognito Mode","Hide Icon","Hide Desktop","Hide Hints","Hide Name","Find out global IP","Find out local IP","Create Note","Edit Notes","Turn off","Icon Selection"],[Switching,Switching,Switching,Switching,Switching,IP,IP,Add,Delete,Quit,IconSelection]): M[button] = MenuItem( Menu[denomination], key=button, callback=func )
    for key in content['Accents'].keys(): Accents.append( MenuItem( key, callback = Language ) )
    for id,value in enumerate(content['Notesbox']['Naming']): Note.append( MenuItem(value, key=str(id) if id<10 else None, callback = Notes) )
    for switch,json in zip( [M['m'],M['i'],M['d'],M['h'],M['n']] , ['Incognito Mode','Hide Icon','Hide Desktop','Hide Hints', 'Hide Name'] ) : switch.state = content['Switch'][json]
    return [ [ Menu["Settings"], [ [ Menu["Menu Language"], Accents ], None, M['c'], M['m'], M['e'], None, M['d'], M['h'], M['s'], M['i'], M['n'], None, M['g'], M['l'], None, Menu["Version"]+" "+VERSION, None, M['q'] ] ], None, [ Menu['Notes'], Note ] ]

if __name__ == "__main__": App('𝕾𝕿', icon = (Database()["Icon"] if path.isfile(Database()['Icon']) else 'icon.png') if Database()['Switch']['Hide Icon'] == 0 else None, title = '\ud835\udd7e\ud835\udd93\ud835\udd86\ud835\udd90\ud835\udd8a\ud835\udd7f\ud835\udd97\ud835\udd8e\ud835\udd88\ud835\udd90\ud835\udd98' if Database()['Switch']['Hide Name'] == 0 else None, menu = menu(), quit_button=None).run()