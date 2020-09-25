import random, time
import PySimpleGUI as sg
import string
LC= string.ascii_lowercase
UC= string.ascii_uppercase
Nom= string.digits
Sym= "._!@#$%&*"
XSym= "<>,;'\"()[]}{=+-:~^"
FN=''
sg.theme('LightGrey')
LAYOUT_BUTTON_BG='Green'
def PAllF(lngth):
    return "".join(random.sample(FN,lngth))
def Main():
    layout=[
            [sg.Text('Include:',font=(1,13))],
            [sg.Checkbox('Lower Case', default=True), sg.Checkbox('Upper Case'), sg.Checkbox('Number'), sg.Checkbox('Symbol')],
            [sg.Text('Password Length:\t\t      '), sg.Spin([i for i in range(1,21)], initial_value=8, size=(25,5))],
            [sg.Button('Generate Password',button_color=('White',LAYOUT_BUTTON_BG),size=('44','2'),font=(10,14,))], #,pad=((0,0),(0,10))
            [sg.Text('')],
            [sg.Text('Your Password:',font=(1,13)),sg.Input('nothing',key='PASSW',size=(50,3),font=(1,13,'bold'),background_color='White',text_color=LAYOUT_BUTTON_BG)]]
    window = sg.Window('Password Generator', layout,size=(375,210),keep_on_top=True,resizable=True)#element_justifaction='Center'
    while True:             # Event Loop
        event, values = window.read()
        if values[0] == False and values[1] == False and values[2] == False and values[3] == False :#and values[4] == False
            sg.PopupTimed('Error\nPlease Choose at least one option.',auto_close_duration=5,no_titlebar=True,keep_on_top=True)
        elif values[4]==0:
            sg.PopupTimed('Error\nPlease Type Length of Password.',keep_on_top=True)
        else:
            global FN
            FN=''
            if values[0]:
                FN+=LC
            if values[1]:
                FN+=UC
            if values[2]:
                FN+=Nom
            if values[3]:
                FN+=Sym
            PassLen= values[4]
            if type(PassLen)!=int or int(PassLen) < 1:
                sg.Popup('Password Length Can Not Be Lower Than 1.',keep_on_top=True)
            elif int(PassLen) > 20:
                sg.Popup('Password Length Can Not Be Higher Than 20.',keep_on_top=True)
            x=PAllF(PassLen)
            window['PASSW'].Update(x)    
Main()