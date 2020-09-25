import PySimpleGUI as sg
import string
LC= string.ascii_lowercase
UC= string.ascii_uppercase
Nom= string.digits
Sym= "._!@#$%&*"
XSym= "<>,;'\"()[]}{=+-:~^"
sg.theme('LightGrey')
Vlayout=[
        [sg.Text('Enter Your Password:'),sg.InputText('',background_color='LightGrey',text_color='Black',size=(30,3))],
        [sg.Button('Check',bind_return_key=True),] #sg.Text(key='Check')
        ]
window= sg.Window('Password Validator',Vlayout)
while True:
    VE,VV=window.read()
    Password=VV[0]
    Valid=0
    
    Dic = {}
    for char in Password:
        if char in Dic and Dic[char]==1:
            #if char.lower() in LC:
            Dic[char]+=1
        else:
            Dic[char] = 1

    Valid += sum(list(Dic.values()))**2
    
    NLC=10
    NUC=15
    NN =15
    NS =20
    NXS=25
    for char in Password:
        if char in LC:
            Valid+=NLC
            NLC=0
        if char in UC:
            Valid+=NUC
            NUC=0
        if char in Nom:
            Valid+=NN
            NN=0
        if char in Sym:
            Valid+=NS
            NS=0
        if char in XSym:
            Valid+=NXS
            NXS=0
    BC= 'Green' if Valid>=60 else 'Red'
    
    new=[[sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar',bar_color=(BC,'LightGrey')),
        sg.T('0',key='nom',size=(7,1))],
        [sg.T('Checking...',key='Check',size=(35,1))]]
    windowV = sg.Window('Validation', new,)
    progress_bar = windowV['progressbar']
    for i in range(Valid+1):
        eventV, valuesV = windowV.read(timeout=10)
        progress_bar.UpdateBar(i + 1)
        windowV['nom'].Update(f'  {i}/100') #f'{i}/100'
    
    #windowV['progressbar'].UpdateBar(bar_color=(BC,'LightGrey'))

    if Valid>=150:
        VP='The Most Strong Password'
    elif 150>Valid>=125:
        VP='Realy Strong'
    elif 125>Valid>=100:
        VP='Very Strong'
    elif 100>Valid>=80:
        VP='Strong'
    elif 80>Valid>=60:
        VP='Normal'
    elif 60>=Valid>=40:
        VP='Weak'
    elif 40>Valid:
        VP='Very Weak'
    windowV['Check'].update(f'{Password} is {VP}')