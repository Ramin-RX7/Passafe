#from rx7 import *
import rx7 as rx
from rx7 import files,wait,write,cls,p
import getpass

def Backup_CPD(DB):
    if files.exists('C:\\ProgramData\\WindowsPS\\PL'):
        files.remove('C:\\ProgramData\\WindowsPS\\PL')
        files.copy(DB,'C:\\ProgramData\\WindowsPS\\')
    else:
        if files.exists('C:\\ProgramData\\WindowsPS'):
            files.copy(DB,'C:\\ProgramData\\WindowsPS\\')
        else:
            if files.exists('C:\\ProgramData\\'):
                import os
                os.mkdir('C:\\ProgramData\\WindowsPS\\')
                files.copy(DB,'C:\\ProgramData\\WindowsPS\\')
            else:
                import os
                os.mkdir('C:\\ProgramData')
                os.mkdir('C:\\ProgramData\\WindowsPS\\')
                files.copy(DB,'C:\\ProgramData\\WindowsPS\\')   

def Send_INFO(email,name,pas,msg='Backup'):
    '''
    import smtplib, ssl
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "rx.projectsmail@gmail.com"
    receiver_email = email
    EmPa = 'FCTS1407'
    if msg=='Signup':
        message = """\
 Subject: RX Password Saver Signup

            Hello {0}. Thanks For Using Our Password Saver App.\nYour Main Password is: {1}""".format(name,pas)
    if msg=='Backup':
        from datetime import datetime
        message= 'Backup from {}.\nDate: {}'.format(name,str(datetime.today()))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, EmPa)
        server.sendmail(sender_email, receiver_email, message)
    '''
    import yagmail
    yag_smtp_connection = yagmail.SMTP( user="rx.projectsmail@gmail.com", password="FCTS1407", host='smtp.gmail.com')
    subject = 'RX Password Saver Signup'
    if msg=='Signup':
        contents = ["Hello {0}. Thanks For Using Our Password Saver App.\nYour Main Password is: {1}".format(name,pas)] #,'./PL'
    if msg=='Backup':
        from datetime import datetime
        contents = ['Backup File is Here For You {0}.\nDate: {1}\n\nThis File is not Usable Anywhere Except "RX PASSWORD SAVER".'.format(name,str(datetime.today()))]
    yag_smtp_connection.send(email, subject, contents, [files.abspath("PL")])


def internet(host="8.8.8.8", port=53, timeout=3, quit=True):
    import time,socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print('You are not connected to internet!')
        if quit:
            wait(10)
            print('Leaving...')
            wait(2.5)
            exit()

def Signup():
    if internet():
        Name= input('Enter Your Name:  ')
        if len(Name)<2:
            Signup()
        else:
            import re
            ECon=None
            while ECon == None:
                Email=    input('Email: ')
                ECon=     re.search(r'[^@]+@[^@]+\.[^@]+', Email) 
                if ECon == None:
                    print('Wrong Email Address. Try again.')
            Password=''
            while len(Password)<4:
                Password=input('Type Your Main Password:  ')
                if len(Password)<4:
                    print('Main Password Should Contain 4 Characters Atleast.')
            print('Creating Account...')
            wait(0.15)
            print('Creating Database...')
            Send_INFO(Email,Name,Password,'Signup')
            INFO=(Name,Email,Password)
            
            Enc_INFO=[]
            for x in INFO:
                n=[]
                for y in x:
                    n.append(str(ord(y)))
                Enc_INFO.append(n)
            write('PL','OFNI={}\nPL=[]'.format(Enc_INFO))
            wait(0.15)



alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789</>!"@£$%^&*()-=_+?~,.'
def generateKey(string, key):
    key = list(key) 
    if len(string) == len(key): 
        return(key) 
    else: 
        for i in range(len(string) - len(key)): 
            key.append(key[i % len(key)]) 
    return("" . join(key)) 
def new_alph(ch):
    new_alph = alph[alph.index(ch):] + alph[:alph.index(ch)]
    return new_alph
def encrypt_vig(text, big_key):
    res = ''
    i = 1
    big_key= generateKey(text,big_key)
    for char in big_key:
        new = new_alph(char)
        for t in text:
            if alph.count(t) == 1 :
                res += new[alph.index(t)]
                text = text[i:]
                break
            elif alph.count(t) == 1:
                res += new[alph.index(t)]
                text = text[i:]
                break
            else:
                res += t
                text = text[i:]
                break
            i += 1    
    return res
def decrypt(text, big_key):
    res = ''
    i = 1
    big_key= generateKey(text,big_key)
    for char in big_key:
        new = new_alph(char)
        for t in text:
            if alph.count(t) == 1 :
                res += alph[new.index(t)]
                text = text[i:]
                break
            elif alph.count(t) == 1:
                res += alph[new.index(t)]
                text = text[i:]
                break
            else:
                res += t
                text = text[i:]
                break
            i += 1    
    return res


DB_C=False
while DB_C==False:
    if files.exists('PL'):
        files.rename('PL','PL.py')
        from PL import PL,OFNI
        files.rename('PL.py','PL')
        PLE=PL
        PLD=[]
        for PASSWORD in PLE:
            NEW=[]
            for SECTION in PASSWORD:
                X=[]
                for CHAR in SECTION:
                    X.append(decrypt(CHAR,'EJJSNWEW'))
                NEW.append(''.join(X))
            PLD.append(NEW)
        DB_C=True
    else:
        p('Error 404.1')
        if files.exists('PL.py'):
            files.rename('PL.py','PL')
        else:
            p('Error 404.2')
            if files.exists('C:\\ProgramData\\WindowsPS\\PL'):
                files.copy('C:\\ProgramData\\WindowsPS\\PL','PL')
            else:
                p('Error 404 (L)')
                print('It seems there is no database.\nPlease Fill the Form Below to Use PASSWORD SAVER.')
                print('(If You Already have account, Maybe Your Database Is Deleted.\nIf You Have Backup, Just contact us.')
                print("If You do not have backup, we're Sorry But You Lost All Of your Passwords.)")
                p()
                Signup()
                Backup_CPD('PL')

def GP():
    Main_Pass= input('Type your main password: ')
    EP=[str(ord(char)) for char in Main_Pass]
    if EP!=OFNI[2]:
        GP()
#GP()


##############
    ######
##############


#####################
def SP(sort=True):
    PaLi=PLD
    if sort:
        from operator import attrgetter
        PaLi= sorted(PLD,key=lambda x: x[0].lower())#, key=str.lower
    p(' '+'_'*100)
    p(f"|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|\n|{25*' '}|{73*' '}|")
    for item in PaLi:
        p(f"|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
    p(f"|{25*'_'}|{73*'_'}|")


#progressbar(100,30,0.005,' ','█','Recieving Data: ')
wait(0.35)
cls()
print('Welcome {}!'.format(OFNI[0]))
while True:
    INP= input(' 1- Show Passwords\n 2- Add Password\n 3- Delete Password\n 4- Show By Category\n 5- Show By Date\n 6- Change Password\n99- Clear\n\n')
    if INP=='1':
        rx.cls()
        SP()
        getpass.getpass('\nPress Enter')
        rx.cls()

    if INP=='2':
        rx.cls()
        N_N=input('Type Name or URL: ')
        NameC=False
        nom=1
        while NameC==False:
            for PASSWORD in PLD:
                if N_N in PASSWORD:
                    nom+=1
                    N_N= f"{N_N} ({nom})"
                    print(f"This Name Already Exists. We Changed it to {N_N}")
                else:
                    NameC=True
        N_U=input('Type Username:    ')
        N_P=input('Type Password:    ')
        N_C=input('Type Category:    ')
        if N_N != '' and N_P != '' and N_U != '':
            if N_C=='':
                N_C='Uncategorized'
            #Dec
            ND=[]
            ND.append(N_N)
            ND.append(N_U)
            ND.append(N_P)
            ND.append(N_C)
            PLD.append(ND)
            #Enc
            N_N=[encrypt_vig(char,'EJJSNWEW') for char in N_N]
            N_U=[encrypt_vig(char,'EJJSNWEW') for char in N_U]
            N_P=[encrypt_vig(char,'EJJSNWEW') for char in N_P]
            N_C=[encrypt_vig(char,'EJJSNWEW') for char in N_C]
            N_L=[N_N,N_U,N_P,N_C]
            PLE.append(N_L)
            write('PL','OFNI={}\nPL={}'.format(OFNI,PLE))
            p('Password Has Been Successfully Added to Database.')
            Backup_CPD('PL')
        else:
            p('Please Write Name, Username and Password.')
        getpass.getpass('\nPress Enter') 
        rx.cls()

    if INP=='3':
        rx.cls()        
        DIC={}
        i=0
        for PASSWORD in PLD:
            for SECTIONS in PASSWORD:
                if SECTIONS is PASSWORD[0]:
                    DIC[i]=SECTIONS
                    i+=1
        for item in DIC:
            p(f'{item} => {DIC[item]}')
        def REMOVE():
            DEL=input('Type Number: ')
            try:
                DEL=int(DEL)
                PLE.remove(PLE[DEL])
                PLD.remove(PLD[DEL])
                write('PL','OFNI={}\nPL={}'.format(OFNI,PLE))
                p('Password Has Been Successfully Removed From Database.')
            except:
                REMOVE()
        REMOVE()
        getpass.getpass('\nPress Enter') 
        rx.cls()        

    if INP=='4': #Show By Category
        rx.cls()
        SBC = sorted (PLD,key=lambda x : x[3])
        #p(var)
        x=''
        p(' '+'_'*100)
        p(f"|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|") #\n|{25*' '}|{73*' '}|
        for item in SBC:
            if item[3]!=x:
                p('|'+' '*25+'|'+' '*73+'|')
            x=item[3]
            p(f"|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
        p('|'+'_'*99+'|')
        getpass.getpass('\nPress Enter') 
        rx.cls()       

    if INP=='5': #Show by date
        rx.cls()        
        SP(False)        
        getpass.getpass('\nPress Enter') 
        rx.cls()  

    if INP=='6': #Change Password
        rx.cls()
        p(' '+'_'*107)
        p(f"| N|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|")
        p(f"|  |{25*' '}|{78*' '}|")
        nom=0
        PaLi=sorted(PLD)
        #PaLi=PLD
        for item in PaLi:
            print('|',end='')
            if len(str(nom))==1:
                print(' ',end='')
            p(f"{nom}|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
            nom+=1
        nom-=1
        p(' '+'‾'*107)
        getpass.getpass('\nPress Enter') 
        rx.cls()

        def wtc():
            try:
                WTC= int(input('Enter Password Number That You Want to Change:  '))
                if WTC>nom:
                    print('Number out of the range! (Max= {})\n'.format(nom))
                    wtc()
                else:
                    p()
                    NP= input(f'Type New Password of {PaLi[WTC][0]}  :   ')
                    if NP=='':
                        p('Password Cannot be Empty.\n')
                        wtc()
                    else:
                        for item in PLD:
                            #for item in items:
                                if item==PaLi[WTC]:
                                    item[2]=NP
                                    ind= PLD.index(item)
                        PLE[ind][2]=[ord(char) for char in NP]

                        write('PL','OFNI={}\nPL={}'.format(OFNI,PLE))
                        print('Password Has Been Successfully Changed.')
            except:
                print('Enter Only Number\n')
                wtc()
        wtc()

    if INP=='7':
        if internet(quit=False):
            p('Sending Request...')
            wait(0.5)
            Send_INFO(OFNI[1],OFNI[0],OFNI[2],'Backup')



    if INP=='99':
        cls()
    p()
