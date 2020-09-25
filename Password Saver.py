#import pkg_resources.py2_warn    #pkg_resources.py2_warn
import os, sys, webbrowser, hashlib, subprocess
from rx7 import (files,wait,read,write,system)
import pyperclip
import PySimpleGUI as sg


# TODO:
#   Change Main Password

# TOCHANGE LINE:
#   user="rx.projectsmail@gmail.com",
#   GetPassword()



sg.theme('LightGrey')
sg.set_global_icon('.\\Files\\ICON.ico')

#< Save Backup in C: >#
def Backup_CPD(DB, popup=False):
    if popup:
        import platform
        if platform.system() != 'Windows':
            sg.popup('For Now Only Windows is Supported For Backup')
            return

    try:     os.mkdir('C:\\ProgramData')
    except:  pass
    try:     os.mkdir('C:\\ProgramData\\WindowsPS\\')
    except:  pass
    try:     files.remove('C:\\ProgramData\\WindowsPS\\PL')
    except:  pass

    files.copy(DB,'C:\\ProgramData\\WindowsPS\\') 
 
#< Send Backup Email >#
def Send_INFO(email,name,pas,msg='Backup'):
    import yagmail
    from datetime import datetime

    #####
    # WRITE YOUR OWN GMAIL INFO
    #####
    user=""
    password=""
    if not user or not password:
        raise NotImplementedError('WRITE YOUR OWN GMAIL INFO IN "Send_INFO" FUNCTION')

    yag_smtp_connection = yagmail.SMTP(
        user="",
        password="",
        host='smtp.gmail.com')
    subject = '"Passafe" Password Saver Signup'
    contents =  [f'Hello {name}. Thanks For Using "Passafe".\n']
    if msg=='Signup':
        contents[0] += f"Your Main Password is: {pas}"  #,'./PL' #,str(datetime.today())
        yag_smtp_connection.send(email, subject, contents) #\n\n{2}
    elif msg=='Backup':
        files.copy('PL','Passwords')
        contents[0] += f'Backup File is Here For You {name}.\nDate: {str(datetime.today())}'
        contents[0] += '\n\nThis File is not Usable Anywhere Except "PASSAFE PASSWORD SAVER".'
        yag_smtp_connection.send(email, subject, contents, [files.abspath("PL")])
        files.remove('Passwords')

#< Check Internet Connection (Parent:Send_INFO) >#
def internet(website="http://x.com"):
    '''
    Check if there is internet connection (Use in Send_INFO)
    I used x.com because it's faster than any other site to load
    (It's source is only a 'x'!)
    '''
    import urllib
    try:
        urllib.request.urlopen(website)
        return True
    except:
        return False

#< Progressbar (Parent:Signup) >#
def ProgressBar(nom,msg):
    '''
    This function creates Fake Progressbars
    Just You know, make it more beautiful
    (Removing Calls of this function does not change any thing)
    '''
    XL = [[sg.Text(msg)],
            [sg.ProgressBar(nom, orientation='h', size=(20, 20), key='progressbar',bar_color=('Green','LightGrey'))],
            [sg.Cancel()]]
    XLW = sg.Window('Passafe', XL)
    FK = XLW['progressbar']
    for i in range(nom):
        event, values = XLW.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        FK.UpdateBar(i + 1)
    XLW.close()

#< Signup >#
def Signup():
    if not internet():
        sg.Popup("Signup Requires Internet Connection.")
        exit()
        quit()
    Slayout=[[sg.T('Please Fill the Form Below.',font=(10,11))],
             [sg.Text('NAME:',size=(16,1)),             sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey')],
             [sg.Text('EMAIL:'   ,size=(16,1)),         sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey')],
             [sg.Text('MAIN PASSWORD:'   ,size=(16,1)), sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey',)],
             [sg.OK('SAVE'), sg.Button('Cancel')]
             ]
    Swindow= sg.Window('Signup',Slayout)
     

    while True:
        CNAME,CPASSWORD,CEMAIL = False,False,False
        SE,SV= Swindow.read() 
        if SE=='SAVE':
            if SV[0]=='':
                sg.popup('Please Type Your Name.')
            else:
                CNAME=True
            from re import search
            ECon= search(r'[^@]+@[^@]+\.[^@]+', SV[1]) 
            if ECon==None:
                sg.popup('Invalid Email Address.')
            else:
                CEMAIL=True
            pass
            if len(SV[2])<4:
                sg.popup("Length of 'MAIN PASSWORD' Should be at least 4")
            else:
                CPASSWORD=True
            pass
            if CNAME and CEMAIL and CPASSWORD:
                break
        else:
            sys.exit()

    Send_INFO(SV[1],SV[0],SV[2],'Signup')
    Enc_INFO=[]
    Enc_INFO.append([Decrypt(char,'4') for char in SV[0]])
    Enc_INFO.append([Decrypt(char,'4') for char in SV[1]])
    hashed = hashlib.sha3_256(bytes(SV[2],encoding='utf-8')).hexdigest()
    Enc_INFO.append([char for char in hashed])

    write('PL',f"InfoE={str(Enc_INFO)}\nPL=[]")
    ProgressBar(50,'Creating Account')
    ProgressBar(50,'Creating Database')
    Swindow.close()

#< Decrypt & Encrypt  Data >#
def XOR(word, key):
    for i in range(len(word)): 
        word = (word[:i] + chr(ord(word[i]) ^ ord(key)) + word[i + 1:])
    return word
def Decrypt(word,key):
    return XOR(word,key)
def Encrypt(word,key):
    return XOR(word,key)

#< Import DB >#
def Load_DB():
    while True:
        if files.exists('PL'):
            files.rename('PL','PL.py')
            from PL import PL,InfoE
            files.rename('PL.py','PL')
            PLE=PL
            PLD=[]
            for PASSWORD in PLE:
                NEW=[]
                for SECTION in PASSWORD:
                    X=[]
                    for CHAR in SECTION:
                        X.append(Decrypt(CHAR,'7'))
                    NEW.append(''.join(X))
                PLD.append(NEW)
            
            InfoD=[]
            for info in InfoE[:2]:
                NEW = ''.join([Decrypt(char,'4') for char in info])
                InfoD.append(NEW)
            InfoD.append(''.join(InfoE[2]))
            #break
            return PLE,PLD,InfoD,InfoE

        else:
            #p('Error 404.1')
            if files.exists('PL.py'):
                files.rename('PL.py','PL')
            else:
                #p('Error 404.2')
                if files.exists('C:\\ProgramData\\WindowsPS\\PL'):
                    files.copy('C:\\ProgramData\\WindowsPS\\PL','PL')
                else:
                    SysName = system.accname()
                    if files.exists(f'C:\\Users\\{SysName}\\Downloads\\Passwords'):
                        files.copy(f'C:\\Users\\{SysName}\\Downloads\\Passwords','PL')
                        sg.Popup('Passwords Restored Completely')
                    else:
                        layout=[
                            [sg.T('It seems there is no database.',font=(12,12))],
                            [sg.Button('Signup',font=(12,12)),
                            sg.Button('I Already Have Account',font=(12,12))
                            ]
                            ]
                        window= sg.Window('No Database',layout)
                        NDbE,NDbV= window.read()
                        window.close()
                        if NDbE == 'Signup':
                            Signup()
                            Backup_CPD('PL')
                        elif NDbE == 'I Already Have Account':
                            NDlayout=[[sg.T("We're Sorry but It Seems There is No Database!",font=('Times',15))],
                                    [sg.T("If You Already have account,\nMaybe Your Database Is Deleted.",font=(1,12))],
                                    [sg.T("If You have 'EMAIL BACKUP', Just Download it\nand Save it in Downloads Folder.",font=(1,12))],
                                    [sg.T("Then We Can Restore Your Passwords.",font=(1,12))],
                                    [sg.T("If You Don't have Email Backup We're Sorry To Say\nThat You've Lost All of Your Passwords.",font=(1,12))],
                                    [sg.Button('  EXIT  ')]]

                            NdbL= sg.Window('Help for Lost Passwords',NDlayout)
                            NdbL.read()
                            NdbL.close()
                        elif NDbE in (None,'None'):
                            exit()
PLE,PLD,InfoD,InfoE = Load_DB() 
#] PLD:PasswordListDecrypted | PLE:PasswordListEncrypted
#] InfoD:InfoDecrypted | InfoE:InfoEncrypted

#< Get Password >#
def GetPassword():
    layout=[[sg.T('Enter Your Main Password: '),
             sg.Input('',size=(25,1),text_color='Black',background_color='LightGrey',key='inp',)],
            [sg.Button('Login',bind_return_key=True,button_color=('White','Green'),size=(6,1),)]]
    wind= sg.Window('Identity Confirmation',layout)#,resizable=True)    {  password_Char='*' }
    while True:
        e,v= wind.read(timeout=100) #
        if len(InfoD[2])>=6:
            if v and hashlib.sha3_256(bytes(v['inp'],encoding='utf-8')).hexdigest()==InfoD[2]:
                #wind['inp'].update(text_color=('Green'))
                wind.close()
                break
        pass
        if e=='Login':
            if hashlib.sha3_256(bytes(v['inp'],encoding='utf-8')).hexdigest()==InfoD[2]:
                wind.close()
                break
            else:
                sg.PopupTimed('Wrong Password.',auto_close_duration=7)
        else:
            if not e=='__TIMEOUT__':
                exit()
GetPassword()

#< Passwords SaveAs Window >#
def SaveAs():
    from tkinter import filedialog,Tk
    #root = Tk()
    filename =  filedialog.asksaveasfilename(initialdir = "/desktop",title = "Export Passwords",defaultextension='.xls',initialfile='Passwords',
                                             filetypes = (('Excel','.xls'),('json','.json'),("CSV","*.csv"),("all files","*.*")))
    print(filename)
    ext= filename[-3:].lower()
    if ext=='xls':
        from openpyxl import Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"]='NAME'
        sheet['B1']='USERNAME'
        sheet['C1']='PASSWORD'
        sheet['D1']='CATEGORY'
        for PASSWORD in PLD:
            ind= str(PLD.index(PASSWORD)+3)
            #print(f'A{ind}')
            sheet[f'A{ind}']= PASSWORD[0]
            sheet[f'B{ind}']= PASSWORD[1]
            sheet[f'C{ind}']= PASSWORD[2]
            sheet[f'D{ind}']= PASSWORD[3]
        workbook.save(filename=filename)
        sg.PopupTimed('Excel File Created Successfully.',auto_close_duration=7)
    if ext=='csv':
        import csv
        with open(filename, mode='w') as csv_file:
            fieldnames = ['NAME/URL', 'USERNAME', 'PASSWORD', 'CATEGORY']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(PLD)-1):
                writer.writerow({'NAME/URL': PLD[i][0], 'USERNAME': PLD[i][1], 'PASSWORD':PLD[i][2] ,'CATEGORY':PLD[i][3]})
            sg.PopupTimed('CSV File Created Successfully.',auto_close_duration=7)
    if ext=='son':
        import json
        data=dict()
        for item in PLD:
            data[item[0]]= [item[1],item[2],item[3]]
        with open(filename, "w") as write_file:
            json.dump(data, write_file,indent=4,)
        sg.PopupTimed('JSON File Created Successfully.',auto_close_duration=7)

#< Get Theme >#
def Get_Theme():
    #,force_toplevel=True / ,focus=True
    try:
        rdtm= read('.\\Files\\Theme')
        if rdtm.lower()=='black' or rdtm.lower()=='dark':
            sg.theme('Black')
            THEME='BLACK'
            LAYOUT_BUTTON_BG= 'DarkGreen'
            DARK_RADIO=True
            LIGHT_RADIO=False
        else:
            raise ValueError
    except:
        sg.theme('LightGrey')
        LAYOUT_BUTTON_BG= 'Green'
        write('.\\Files\\Theme','default')
        THEME='LIGHT'
        LIGHT_RADIO= True
        DARK_RADIO=False
    
    return THEME,LIGHT_RADIO,DARK_RADIO,LAYOUT_BUTTON_BG
THEME,LIGHT_RADIO,DARK_RADIO,LAYOUT_BUTTON_BG = Get_Theme()


#############################
import pyautogui
MONITOR_X,MONITOR_Y=pyautogui.size()  #] Size of Screen for some windows
'''
sg.SystemTray.notify('Passafe', 
                     f"Hi {InfoD[1]}", display_duration_in_ms=1,
                     location=(MONITOR_X/2-210,MONITOR_Y/2-75))
'''

#< Right Click Menu (R:Right, C:Click, (N:Name,U:Username,P:Password)) >#
R_CN=[['R_CI'],['Open in New Tab','!Change::NAME'    ]]
R_CU=[['R_CI'],['Copy::USERNAME' ,'!Change::USERNAME']]
R_CP=[['R_CI'],['Copy::PASSWORD' ,'!Change::PASSWORD']]
MenuRI= [['R_CPP'],['Delete','Cut','Copy','Paste','---','Select All']]

NoPasswordLayout = [[sg.T('No Passwords Found in Database.\nChoose "Add Password" Button.',font=('',11))]]

#< Text Select Right Click Menu >#
#! NOTE: It's based on pyautogui hotkeys
def RCE(e):
    if e=='Delete':
        wait(0.1)
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('delete')
    if e=='Cut':
        wait(0.25)
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','x')
    if e=='Copy':
        wait(0.25)
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        pyautogui.click()
    if e=='Paste':
        wait(0.25)
        #pyautogui.typewrite(pyperclip.paste())
        pyautogui.hotkey('ctrl','v')
    if e=='Select All':
        wait(0.25)
        pyautogui.hotkey('ctrl','a') 

#< MAIN APP ELEMENTS >#
#] Columns
Main_Col1=[[sg.Button('Show Passwords'  ,font=('Times',12) ,size=(13,3))],  #,sg.Text(' '*int(MONITOR_X/4*3/18),key='spc')
           [sg.Button('Show By Category',font=('Times',12) ,size=(13,3))],  #button_color=('White','Green')
           [sg.Button('Change Password' ,font=('Times',12) ,size=(13,3))]
           ]
Main_Col2=[[sg.Button('Add Password'    ,font=('Times',12) ,size=(13,3))],
           [sg.Button('Show By Date'    ,font=('Times',12) ,size=(13,3))],
           [sg.Button('Remove Password' ,font=('Times',12) ,size=(13,3))]
           ]
Main_Col3=[[]]
#Main_Col4=[[sg.Text('',size=(1,11))],[sg.Button('Change Theme',)]]
Main_Col4= [[sg.Text(size=(1,9))],
            [sg.Radio('Light  ','THEME',default=LIGHT_RADIO,key='LIGHT_RADIO'), 
             #sg.T(f'  Welcome {InfoD[0]}',font=(12,12),size=(len(InfoD[0])+9,9))
             sg.Radio('Dark','THEME',default=DARK_RADIO,key='DARK_RADIO')],
            [sg.Button('Change Theme',)]]
#] Menubar
Main_Menu = [['&File', ["&Your INFO" , 'S&ave as', 'Email &Backup', '---', 
                        '!Repair Files', '!Remove extra files', '---', 'E&xit']],
             ['!Pro' , ['Go &Pro', 'Enter License &Key::Key']],
             ['&Apps', ['Password &Validator','Password &Generator', '&CLI Version','!&Costomize']],
             ['&Help', ['&RX7','&Donate','&Contact Us','&About','&Help']]
             ]
#] Layout
Main_Layout=[[sg.Col(Main_Col1),sg.Col(Main_Col2),
              sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),
              sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),
              #sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),sg.Col(Main_Col3),
              sg.Col(Main_Col4)],[sg.Menu(Main_Menu)],]
#] Make Window
Main_Window= sg.Window('Passafe',Main_Layout,size=(int(MONITOR_X/2.5),int(MONITOR_Y/3)),resizable=True)

'''
import keyboard
keyboard.add_hotkey('ctrl + shift + s', SaveAs,)  
keyboard.rem
'''


#< MAIN APP >#
while True:

    THEME,LIGHT_RADIO,DARK_RADIO,LAYOUT_BUTTON_BG = Get_Theme()

    Main_Event,Main_Values= Main_Window.read(timeout=2000)
    #print(Main_Event)

  #########################################
  #                BUTTONS                #   webbrowser.open_new_tab('http://rx7.ir/')
  #########################################
    if Main_Event=='Show Passwords':
        if not len(PLD):
            sg.popup('No Passwords Found in Database.\nChoose "Add Password" Button.',
                     title='No Password',any_key_closes=True)
            continue

        PaLi=sorted(PLD,key=lambda x: x[0].lower())
        #BUTTON_COLOR= ('White','Green')
        if len(PaLi)%2==0:
            row1=PaLi[:int(len(PaLi)/2)]
            row2=PaLi[int(len(PaLi)/2):]
        else:
            row1=PaLi[:int(len(PaLi)/2+1)]
            row2=PaLi[int(len(PaLi)/2+1):]
        layout=[]
        if len(row1)==len(row2):
            for i in range(len(row1)):
                layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}',),
                        sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row2[i][1]}  :  {row2[i][2]}')]]
        else:
            for i in range(len(row1)-1):
                layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}'),
                        sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row2[i][1]}  :  {row2[i][2]}')]]                
            layout+= [[sg.Button(f"{row1[-1][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[-1][1]}  :  {row1[-1][2]}')]]

        layout += [[sg.Exit(size=(5,1))]]
        window = sg.Window('Passwords', layout,keep_on_top=True,resizable=True)#element_justifaction='Center'
        
        def ShowPass():
            event, values = window.read()
            if event in [item[0] for item in PaLi]:
                for PASSWORD in PaLi:
                    if PASSWORD[0]==event:
                        col1=[[sg.T('NAME or URL:'    ,right_click_menu=R_CN)],
                              [sg.T('USERNAME:',right_click_menu=R_CU)],
                              [sg.T('PASSWORD:',right_click_menu=R_CP)],
                              [sg.T('CATEGORY:',)]] #,right_click_menu=[['R_CI'],['Copy::CATEGORY','!Change::CATEGORY']]
                        col2=[[sg.T(PASSWORD[0],right_click_menu=R_CN)],
                              [sg.T(PASSWORD[1],right_click_menu=R_CU)],
                              [sg.T(PASSWORD[2],right_click_menu=R_CP)],
                              [sg.T(PASSWORD[3])]] #,right_click_menu=[['R_CI'],['Copy::CATEGORY','!Change::CATEGORY']]
                        layout2=[[sg.Col(col1,pad=((0,30),(0,0))),sg.Col(col2)]]
                        layout2 += [[sg.OK(size=(4,1),pad=((8,0),(0,0)),bind_return_key=True)]]
        
                        window2 = sg.Window('Password Generator', layout2, keep_on_top=True,)
                        x=True
                        while x==True:
                            event, values = window2.read()
                            #if event[:4] == 'Copy':
                            #    pass
                            if event in ('OK',None,'None'):
                                window2.Close()
                                x=False                             
                            else:
                                if event=='Open in New Tab':
                                    webbrowser.open_new_tab(PASSWORD[0])
                                if event=='Copy::USERNAME':
                                    pyperclip.copy(PASSWORD[1])
                                if event=='Copy::PASSWORD':
                                    pyperclip.copy(PASSWORD[2])
                        #print(event)
                        ShowPass()
            if event not in [item[0] for item in PaLi]:
                window.close()
        ShowPass()

    elif Main_Event=='Add Password':  # ST if no passwords in database: STOP WORKING ERROR
        def Add_Pass(InfoE,PLE):
            layout=[
                    [sg.Text('NAME or URL:',size=(11,1)), sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey',right_click_menu=MenuRI)],
                    [sg.Text('USERNAME:'   ,size=(11,1)), sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey',right_click_menu=MenuRI)],
                    [sg.Text('PASSWORD:'   ,size=(11,1)), sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey',right_click_menu=MenuRI)],
                    [sg.Text('CATEGORY:'   ,size=(11,1)), sg.InputText(size=(35,2),text_color='Black',background_color='LightGrey',right_click_menu=MenuRI)],
                    [sg.OK('SAVE',bind_return_key=True), sg.Button('Cancel')]
                    ]

            window = sg.Window('Add Password', layout)
            while True:
                event, values = window.read()
                
                if event=='SAVE':
                    if values[0] and values[1] and values[2]:
                        if values[3]=='':
                            values[3]='Uncategorized'
                        window.close()
                        N_N=values[0]
                        nom=1
                        if len(PLD):
                            XXX = True
                            while XXX:
                                for PASSWORD in PLD:
                                    if N_N == PASSWORD[0]:
                                        nom+=1
                                        N_N= f"{N_N} ({nom})"
                                        sg.PopupTimed(f"This Name Already Exists. We Changed it to {N_N}",auto_close_duration=5)
                                    else:
                                        XXX=False
                        print('OK')
                        N_U=values[1]
                        N_P=values[2]
                        N_C=values[3]
                        #Dec
                        PLD.append([N_N,N_U,N_P,N_C])
                        #Enc
                        N_N=[Encrypt(char,'7') for char in N_N]
                        N_U=[Encrypt(char,'7') for char in N_U]
                        N_P=[Encrypt(char,'7') for char in N_P]
                        N_C=[Encrypt(char,'7') for char in N_C]
                        N_L=[N_N,N_U,N_P,N_C]
                        PLE.append(N_L)
                        print('OK')
                        write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                        sg.popup('Password Has Been Successfully Added to Database.')
                        Backup_CPD('PL')
                        break                     
                    else:
                        sg.popup('Please Fill All "NAME", "USERNAME" & "PASSWORD" Sections.')
                        window.close()
                        Add_Pass(InfoE,PLE)
                if event in ('Delete','Cut','Copy','Paste','Select All'): 
                    RCE(event)
                if event in ('Cancel',None,'None'):
                    window.Close()
                    break
 
        Add_Pass(InfoE,PLE)
        
    elif Main_Event=='Remove Password':  # Delete
        def Remove_Pass():

            if not len(PLD):
                sg.popup('No Passwords Found in Database to Remove.')
                return

            PaLi=sorted(PLD,key=lambda x: x[0].lower())

            if len(PaLi)%2==0:
                row1=PaLi[:int(len(PaLi)/2)]
                row2=PaLi[int(len(PaLi)/2):]
            else:
                row1=PaLi[:int(len(PaLi)/2+1)]
                row2=PaLi[int(len(PaLi)/2+1):]
            
            layout=[]
            if len(row1)==len(row2):
                for i in range(len(row1)):
                    layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,),sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2)]]
            else:
                for i in range(len(row1)-1):
                    layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,),sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2)]]                
                layout+= [   [sg.Button(f"{row1[-1][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,)]]
            
            layout += [[sg.Exit(size=(5,1))]]
            window = sg.Window('Remove Password', layout,keep_on_top=True,resizable=True)#element_justifaction='Center'
            event, values = window.read()
            #print(event)
            if event in [item[0] for item in PaLi]:
                for PASSWORD in PaLi:
                    if PASSWORD[0]==event:
                        layout2 = [[sg.Text("NAME:"+' '*(26)+PASSWORD[0]+"\nUSERNAME:"+' '*(17)+PASSWORD[1]+"\nPASSWORD:"+' '*(16)+PASSWORD[2]+"\nCATEGORY:"+' '*(17)+PASSWORD[3])]]
                        layout2 += [[sg.Text('Are Sure To Delete {}? '.format(PASSWORD[0])),sg.No(bind_return_key=True,size=(4,1)),sg.Yes(size=(4,1))]]
                        window2 = sg.Window('Confirm to Delete', layout2, keep_on_top=True,)
                        event2, values2 = window2.read()
                        window2.close()                        
                        #print(event2)
                        if event2 == 'Yes':
                            ind= PLD.index(PASSWORD)
                            #print(ind)
                            PaLi.remove(PASSWORD)
                            PLD.remove(PLD[ind])
                            PLE.remove(PLE[ind])
                            write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                            sg.PopupTimed('Password Has Been Successfully Removed From Database.',keep_on_top=True,auto_close_duration=7)
                            Backup_CPD('PL')
                        window.close()
                        Remove_Pass()
            if not event in [item[0] for item in PLD]:
                window.close()

        Remove_Pass()

    elif Main_Event=='Show By Category': #Show By Category
        def ShowPassByCat():

            if not len(PLD):
                sg.popup('No Passwords Found in Database.\nChoose "Add Password" Button.',
                         title='No Password',any_key_closes=True)
                return

            PaLi=sorted(PLD,key=lambda x: x[3].lower())
            sizey= len(PaLi*30)

            #BUTTON_COLOR= ('White','Green')
            '''
               col1= [[sg.Text(PASSWORD[0],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Open in new tab:: {PASSWORD[0]}',f'Copy:: {PASSWORD[0]}',f'!Change:: {PASSWORD[0]}']])] for PASSWORD in PaLi ]
               col2= [[sg.VerticalSeparator(),sg.Text(PASSWORD[1],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[1]}',f'!Change:: {PASSWORD[1]}']])] for PASSWORD in PaLi ]
               col3= [[sg.VerticalSeparator(),sg.Text(PASSWORD[2],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[2]}',f'!Change:: {PASSWORD[2]}']])] for PASSWORD in PaLi ]
               col4= [[sg.VerticalSeparator(),sg.Text(PASSWORD[3],size=(16,1),font=(13,13))] for PASSWORD in PaLi ] #,right_click_menu=[['test'],[f'Copy:: {PASSWORD[3]}',f'!Change:: {PASSWORD[3]}']]
             
             layout=[ [sg.Text(" NAME or URL",font=(1,13,'bold'),size=(21,1)),sg.Text(" USERNAME",font=(1,13,'bold'),size=(21,1)),
                     sg.Text(" PASSWORD",font=(1,13,'bold'),size=(21,1)),sg.Text(" CATEGORY",font=(1,13,'bold'),size=(16,1))],
                     [sg.Column(col1,scrollable=True,vertical_scroll_only=True),sg.Column(col2),sg.Column(col3),sg.Column(col4)]]
            '''
            layout=[]
            for PASSWORD in PaLi:
                layout+=[[sg.VerticalSeparator(), 
                sg.Text(PASSWORD[0],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Open in new tab:: {PASSWORD[0]}',f'Copy:: {PASSWORD[0]}',f'!Change:: {PASSWORD[0]}']]),sg.VerticalSeparator(), 
                sg.Text(PASSWORD[1],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[1]}',f'!Change:: {PASSWORD[1]}']]),sg.VerticalSeparator(), 
                sg.Text(PASSWORD[2],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[2]}',f'!Change:: {PASSWORD[2]}']]),sg.VerticalSeparator(), 
                sg.Text(PASSWORD[3],size=(16,1),font=(13,13))
                ]]
            
            sa=False
            if sizey>MONITOR_Y-100:
                sizey=MONITOR_Y-200
                sa=True
            layout= [[sg.Text(" NAME or URL",font=(1,13,'bold'),size=(21,1)),sg.Text(" USERNAME",font=(1,13,'bold'),size=(21,1)),
                      sg.Text(" PASSWORD",font=(1,13,'bold'),size=(21,1)),sg.Text(" CATEGORY",font=(1,13,'bold'),size=(16,1))],
                    [sg.Col(layout,scrollable=sa,vertical_scroll_only=sa,size=(850,sizey))]]

            layout += [[sg.Exit(size=(5,1),pad=((12,0),(0,0)))]]

            window = sg.Window('Password By Category', layout,keep_on_top=True,resizable=True)#,size=(850,sizey+70),element_justifaction='Center'
            
            while True:
                e,v= window.read() #event, values = 
                if e in (None,'None','Exit'):
                    window.close()
                    break
                else:
                    #print(e)
                    if e[:4]=='Copy':
                        pyperclip.copy(e[7:])
                    if e[:4]=='Open':
                        webbrowser.open_new_tab(e[18:])
                        #sg.PopupTimed('Sorry, An Error Accured')
        ShowPassByCat()

    elif Main_Event=='Show By Date': #Show by date
        def ShowPassByDate():
            
            if not len(PLD):
                sg.popup('No Passwords Found in Database.\nChoose "Add Password" Button.',
                         title='No Password',any_key_closes=True)
                return

            PaLi=PLD
            #BUTTON_COLOR= ('White','Green')
            col1= [ [                       sg.Text(PASSWORD[0],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Open in new tab:: {PASSWORD[0]}',f'Copy:: {PASSWORD[0]}',f'!Change:: {PASSWORD[0]}']])] for PASSWORD in PaLi ]
            col2= [ [sg.VerticalSeparator(),sg.Text(PASSWORD[1],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[1]}',f'!Change:: {PASSWORD[1]}']])] for PASSWORD in PaLi ]
            col3= [ [sg.VerticalSeparator(),sg.Text(PASSWORD[2],size=(21,1),font=(13,13),right_click_menu=[['test'],[f'Copy:: {PASSWORD[2]}',f'!Change:: {PASSWORD[2]}']])] for PASSWORD in PaLi ]
            col4= [ [sg.VerticalSeparator(),sg.Text(PASSWORD[3],size=(16,1),font=(13,13))] for PASSWORD in PaLi ] #,right_click_menu=[['test'],[f'Copy:: {PASSWORD[3]}',f'!Change:: {PASSWORD[3]}']]

            layout=[ [sg.Text(" NAME or URL",font=(1,13,'bold'),size=(21,1)),sg.Text(" USERNAME",font=(1,13,'bold'),size=(21,1)),
                    sg.Text(" PASSWORD",font=(1,13,'bold'),size=(21,1)),sg.Text(" CATEGORY",font=(1,13,'bold'),size=(16,1))],
                    [sg.Column(col1),sg.Column(col2),sg.Column(col3),sg.Column(col4)]]

            layout += [[sg.Exit(size=(5,1),pad=((12,0),(0,0)))]]
            window = sg.Window('Password By Date', layout,keep_on_top=True,resizable=True)#element_justifaction='Center'
            
            while True:
                e,v= window.read() #event, values = 
                if e in (None,'None','Exit'):
                    window.close()
                    break
                else:
                    #print(e)
                    if e[:4]=='Copy':
                        pyperclip.copy(e[7:])
                    if e[:4]=='Open':
                        webbrowser.open_new_tab(e[18:])
                        #sg.PopupTimed('Sorry, An Error Accured')
        ShowPassByDate()

    elif Main_Event=='Change Password': #Change Password
        
        def ShowPassName():

            if not len(PLD):
                sg.popup('No Passwords Found in Database to Change it\'s attributes.')
                return
            
            PaLi=sorted(PLD,key=lambda x: x[0].lower())
            #BUTTON_COLOR= ('White','Green')

            if len(PaLi)%2==0:
                row1=PaLi[:int(len(PaLi)/2)]
                row2=PaLi[int(len(PaLi)/2):]
            else:
                row1=PaLi[:int(len(PaLi)/2+1)]
                row2=PaLi[int(len(PaLi)/2+1):]
            
            layout=[]
            if len(row1)==len(row2):
                for i in range(len(row1)):
                    layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}'),
                               sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}')]]
            else:
                for i in range(len(row1)-1):
                    layout+= [[sg.Button(f"{row1[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}'),
                               sg.Button(f"{row2[i][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[i][1]}  :  {row1[i][2]}')]]                
                layout+= [[sg.Button(f"{row1[-1][0]}",button_color=('White',LAYOUT_BUTTON_BG),size=('25','2'),border_width=2,tooltip=f'{row1[-1][1]}  :  {row1[-1][2]}')]]

            layout += [[sg.Exit(size=(5,1))]]

            window = sg.Window('Change Password', layout,keep_on_top=True,grab_anywhere=True,resizable=True)#element_justifaction='Center'
            event, values = window.read()

            if event in [item[0] for item in PaLi]:
                for PASSWORD in PaLi:
                    if PASSWORD[0]==event:
                        layout2=[
                                [sg.Text("NAME:"    ,size=(11,1))    ,sg.Input(default_text=PASSWORD[0],background_color='Grey90',text_color='Black',right_click_menu=MenuRI,size=(35,2))],
                                [sg.Text("USERNAME:",size=(11,1)),sg.Input(default_text=PASSWORD[1],background_color='Grey90',text_color='Black',right_click_menu=MenuRI,size=(35,2))],
                                [sg.Text("PASSWORD:",size=(11,1)),sg.Input(default_text=PASSWORD[2],background_color='Grey90',text_color='Black',right_click_menu=MenuRI,size=(35,2))],
                                [sg.Text("CATEGORY:",size=(11,1)),sg.Input(default_text=PASSWORD[3],background_color='Grey90',text_color='Black',right_click_menu=MenuRI,size=(35,2))],
                                ]

                        layout2 += [[sg.Cancel(),sg.Save(bind_return_key=True)]]
                        window2 = sg.Window('{} Changing Page'.format(PASSWORD[0]), layout2, keep_on_top=True,)
                        x=True
                        while x==True:
                            event2, values2 = window2.read()
                            #print(event2)
                            if event2=='Save':
                                IndPas= PLD.index(PASSWORD)
                                Change=False
                                for i in range(4):
                                    if values2[i]!=PASSWORD[i]:
                                        if len(values2[i])==0 and i != 3:
                                            heads=['NAME','USERNAME','PASSWORD']
                                            sg.PopupTimed(f'{heads[i]} Can Not Be Empty.',auto_close_duration=5,keep_on_top=True)
                                        else:
                                            if len(values2[3])==0:
                                                values2[i]='Uncategorized'
                                            Change=True
                                            PLD[IndPas][i]=values2[i]
                                            Changed= values2[i]
                                            Changed= [ord(char) for char in Changed]
                                            PLE[IndPas][i]=Changed
                                            write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                                            Backup_CPD('PL') 
                                if Change==True:
                                    sg.PopupTimed('Saved!',keep_on_top=True,auto_close_duration=3,no_titlebar=True,font=(10,11))
                                    Backup_CPD('PL')
                                window2.close()         ### RESTART NASHE ###
                                window.close()
                                ShowPassName()
                                x=False

                            if event2 in ('Delete','Cut','Copy','Paste','Select All'): 
                                RCE(event2)
                                 
                            if event2 in ('Cancel',None,'None'):
                                window2.close()         ### RESTART NASHE ###
                                window.close()
                                ShowPassName()
                                x=False
            if not event in [item[0] for item in PaLi]:
                window.close()
        ShowPassName()

    elif Main_Event== 'Change Theme':
        if Main_Values['LIGHT_RADIO'] and THEME=='BLACK':
            write('.\\Files\\Theme','light')
            LAYOUT_BUTTON_BG= 'Green'
            sg.PopupTimed('Restart The App For Full Effect.',background_color='#FAFAFA',text_color='Black')
            #Main_Window.Reappear()
        elif Main_Values['DARK_RADIO'] and THEME=='LIGHT':
            write('.\\Files\\Theme','black')
            LAYOUT_BUTTON_BG= 'DarkGreen'
            sg.PopupTimed('Restart The App For Full Effect.',background_color='Black',text_color='#FAFAFA')
            #Main_Window.Refresh()

  ########################################
  #               MENUBAR                #
  ########################################
   #] 'File' Menu
    if Main_Event=='Your INFO':
        YI_Layout= [[sg.T(f'NAME:{" "*15}'),sg.InputText(InfoD[0],size=(30,1))],
                    [sg.T(f'Email:{" "*16}'),sg.InputText(InfoD[1],size=(30,1))],
                    [sg.T(f'PASSWORD:{" "*5}'),
                     sg.InputText('PASSWORD IS PROTECTED',font=('',10,'bold'),
                                  size=(30,1),disabled=True,background_color='Grey',text_color='Black')],
                    [sg.Exit(size=(4,1)),sg.Save(size=(4,1))]]
        YIwindow = sg.Window('Your Account Information', YI_Layout,keep_on_top=True,resizable=True)
        YIE,YIV= YIwindow.read()
        YIwindow.close()

        if YIE=='Save':
            CH=False
            if YIV[0]!=InfoD[0]:
                if len(YIV[0])!=0:
                    InfoD[0]=YIV[0]
                    InfoE[0]=[ord(char) for char in YIV[0]]
                    CH=True
                else:
                    sg.PopupTimed('Name Can Not Be Empty.',auto_close_duration=7)
            if YIV[1]!=InfoD[1]:
                if len(YIV[1])!=0:
                    InfoD[1]=YIV[1]
                    InfoE[1]=[ord(char) for char in YIV[1]]
                    CH=True
                else:
                    sg.PopupTimed('Email Can Not Be Empty.',auto_close_duration=7)
            if CH:
                write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                sg.PopupTimed('Your Information Have Been Changed.')

    elif Main_Event=='Save as':
        SaveAs()

    elif Main_Event=='Email Backup':
        if internet():
            sg.PopupTimed('Sending Request...',auto_close_duration=1)
            try:
                Send_INFO(InfoE[1],InfoE[0],InfoE[2],'Backup')
            except:
                sg.Popup('Failed to Send Email.\nTry Again Later.')
        else:
            sg.Popup('Email Backup Needs Internet Connection')
   #] 'Apps' Menu
    elif Main_Event=='Password Validator':
        subprocess.Popen('PVS.bat')
        '''import string
        LC= string.ascii_lowercase
        UC= string.ascii_uppercase
        Nom= string.digits
        Sym= "._!@#$%&*"
        XSym= "<>,;'\"()[]}{=+-:~^"

        #sg.theme('LightGrey')
        Vlayout=[
                [sg.Text('Type Your Password:'),sg.InputText('',background_color='LightGrey',text_color='Black',size=(30,3))],
                [sg.Button('Check',bind_return_key=True)]

                ]
        window= sg.Window('Password Validator',Vlayout)
        x=True
        while x:
            VE,VV=window.read()
            #print(VE)
            #print(VV)
            if VV and VE:
                #print(VV[0])
                Password=VV[0]
                Valid=0
                if len(Password)>=8:
                    Valid+=40
                if len(Password)>=12:
                    Valid+=15    
                if len(Password)>=15:
                    Valid+=15
                NLC=10
                NUC=15
                NN =15
                NS =20
                NXS=10
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
                if Valid>=125:
                    VP='The Most Strong Password'    
                if 125>Valid>=100:
                    VP='Very Strong'
                if 100>Valid>=80:
                    VP='Strong'
                if 80>Valid>=60:
                    VP='Normal'
                if 60>=Valid>=40:
                    VP='Weak'
                if 40>Valid:
                    VP='Very Weak'
                windowV['Check'].update(f'{Password} is {VP}')                        
            else:
                x=False
                window.close()'''

    elif Main_Event=='Password Generator':
        subprocess.Popen('PGS.bat')
        '''import string
        LC= string.ascii_lowercase
        UC= string.ascii_uppercase
        Nom= string.digits
        Sym= "._!@#$%&*"
        XSym= "<>,;'\"()[]}{=+-:~^"
        FN=''
        #sg.theme('LightGrey')
        def PAllF(lngth): 
            return "".join(random.sample(FN,lngth))
        def Main():
            layout=[
                    [sg.Text('')],
                    [sg.Checkbox('Lower Case', default=True), sg.Checkbox('Upper Case'), sg.Checkbox('Number'), sg.Checkbox('Symbol')],
                    [sg.Text('Password Length:\t\t      '), sg.Spin([i for i in range(1,21)], initial_value=8, size=(25,5))],
                    [sg.Button('Generate Password',button_color=('White',LAYOUT_BUTTON_BG),size=('44','2'),font=(10,14,))],
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
                    if int(PassLen) > int(20):
                        sg.Popup('Password Length Can Not Be Higher Than 20.',keep_on_top=True)
                    if int(PassLen) < int(1):
                        sg.Popup('Password Length Can Not Be Lower Than 1.',keep_on_top=True)
                    x=PAllF(PassLen)
                    window['PASSW'].Update(x)
        Main()'''
   
    elif Main_Event=='CLI Version':
        os.system('start "" "Password Saver (CLI)"')

   #] 'Help' Menu
    elif Main_Event=='RX7':
        webbrowser.open_new_tab('http://rx7.ir/')
    elif Main_Event=='Donate':
        webbrowser.open_new_tab('https://zarinp.al/@ripgroup')
    elif Main_Event=='Contact Us':
        webbrowser.open_new_tab('mailto:raminj.rx7@gmail.com')
    elif Main_Event=='About':
        sg.popup('''
        "Passafe Password Saver" Is Created in Python By RX7.
        This App Apply Secure Algoritm To Your Passwords
        And You Don't Need No Worry About Your Passwords.
        Also There is 'Email Backup' Feature That
        Send Your (Encrypted) Passwords To Your Email.
        You Can Find New Realeases in RX7.ir and
        Official Github Page of 'Passafe'.
        ''',title='About')
    elif Main_Event=='Help':
        webbrowser.open_new_tab('https://github.com/Ramin-RX7/Passafe')


    '''if Main_Event=='Costomize':
        CL=[[sg.T('Menu Button Colors'),sg.B('Choose Color',key='MenButF',button_type=sg.BUTTON_TYPE_COLOR_CHOOSER),
             sg.B('Choose Color',key='MenButB',button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
            [sg.Button('Save')]]
        CW=sg.Window('title',CL)
        E,V= CW.read()
        if V['MenButF']:
            Menu_Button_Color[0]=V['MenButF']
        if V['MenButB']:
            Menu_Button_Color[1]=V['MenButB']
        new= str(Menu_Button_Color)[1:-1]
        new1= new[:new.index(',')]
        new2= new[new.index('')+1:]
        write('.\\Files\\Customize',f'{new1}-{new2}')
        print(E,V)'''


    if Main_Event in (None,'Exit'):
        exit()


