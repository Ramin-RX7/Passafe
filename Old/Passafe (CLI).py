#from rx7 import *
import os,getpass,hashlib
import rx7 as rx
from rx7 import files,wait,write,cls,p

print = rx.style.print



#< Save Backup in C: >#
def Backup_CPD(DB, popup=False):
    if popup:
        import platform
        if platform.system() != 'Windows':
            print('Only Windows Supported for now','dodger_blue_1')
            return

    try:     os.mkdir('C:\\ProgramData')
    except:  pass
    try:     os.mkdir('C:\\ProgramData\\WindowsPS\\')
    except:  pass
    try:     files.remove('C:\\ProgramData\\WindowsPS\\PL')
    except:  pass
    try:     files.copy(DB,'C:\\ProgramData\\WindowsPS\\') 
    except:  pass
 
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


def wait_for_input(prompt):
    '''
    Prompt  input(prompt)  until sth is given
    '''
    answer= ''
    while not answer:
        answer = input(prompt)
    return answer


def Signup():
    if internet():
        Name= wait_for_input('Enter Your Name:  ')
        import re
        ECon=None
        while ECon == None:
            Email=    input('Email: ')
            ECon=     re.search(r'[^@]+@[^@]+\.[^@]+', Email) 
            if ECon == None:
                print('Wrong Email Address. Try again.','red')
        Password=''
        while len(Password)<4:
            Password=input('Type Your Main Password:  ')
            if len(Password)<4:
                print('Main Password Should Contain Atleast 4 Characters.','red')

        print('Creating Account...','dodger_blue_1')
        wait(0.15)
        print('Creating Database...','dodger_blue_1')

        Send_INFO(Email,Name,Password,'Signup')
        
        Enc_INFO=[]

        Enc_INFO.append([Decrypt(char,'4') for char in Name])
        Enc_INFO.append([Decrypt(char,'4') for char in Email])
        hashed = hashlib.sha3_256(bytes(Password,encoding='utf-8')).hexdigest()
        Enc_INFO.append([char for char in hashed])

        write('PL','InfoE={}\nPL=[]'.format(Enc_INFO))
        wait(0.15)


def XOR(word, key):
    for i in range(len(word)): 
        word = (word[:i] + chr(ord(word[i]) ^ ord(key)) + word[i + 1:])
    return word
def Decrypt(word,key):
    return XOR(word,key)
def Encrypt(word,key):
    return XOR(word,key)

#< Load Database >#
def Load_DB():
    while True:
        if files.exists('PL'):
            files.rename('PL','PL.py')
            from PL import PL,InfoE

            InfoD=[]
            for info in InfoE[:2]:
                NEW = ''.join([Decrypt(char,'4') for char in info])
                InfoD.append(NEW)
            InfoD.append(''.join(InfoE[2]))

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
            return PLE,PLD,InfoD,InfoE
        else:
            print('Error 404.1','red')
            if files.exists('PL.py'):
                files.rename('PL.py','PL')
            else:
                print('Error 404.2','red')
                if files.exists('C:\\ProgramData\\WindowsPS\\PL'):
                    files.copy('C:\\ProgramData\\WindowsPS\\PL','PL')
                else:
                    print('Error 404.L','red')
                    print('It seems there is no database.\nPlease Fill the Form Below to Use PASSWORD SAVER.')
                    print('(If You Already have account, Maybe Your Database Is Deleted.')
                    print(' If You Have Backup, Just contact us.')
                    print(" If You do not have backup, we're Sorry But You Lost All Of your Passwords.)")
                    print('\n')
                    getpass.getpass('Press Enter to Go to Signup Section')
                    cls()
                    Signup()
                    Backup_CPD('PL')
                    Load_DB()
PLE,PLD,InfoD,InfoE = Load_DB()


def GP():
    Main_Pass= input('Enter your main password:  ')
    while hashlib.sha3_256(bytes(Main_Pass,'utf-8')).hexdigest() != InfoD[2]:
        print('Wrong Password','red')
        Main_Pass= input('Enter your main password:  ')
GP()

##############
    ######
##############


#####################
def SP(sort=True):
    PaLi=PLD
    if sort:
        from operator import attrgetter
        PaLi= sorted(PLD,key=lambda x: x[0].lower())#, key=str.lower
    print(' '+'_'*100)
    print(f"|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|\n|{25*' '}|{73*' '}|")
    for item in PaLi:
        print(f"|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
    print(f"|{25*'_'}|{73*'_'}|")


#progressbar(100,30,0.005,' ','█','Recieving Data: ')
wait(0.35)
cls()
print('Welcome {}!'.format(InfoD[0]))
while True:
    INP= input(' 1- Show Passwords\n 2- Add Password\n 3- Delete Password\n 4- Show By Category\n 5- Show By Date\n 6- Change Password\n99- Clear\n\n')
    cls()

    if INP=='1':
        SP()
        getpass.getpass('\nPress Enter')

    elif INP=='2':
        N_N=wait_for_input('Type Name or URL: ')
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
        N_U = wait_for_input('Type Username:    ')
        N_P = wait_for_input('Type Password:    ')
        N_C = input('Type Category:    ')
        
        if N_C=='':
            N_C='Uncategorized'

        #Dec
        PLD.append([N_N,N_U,N_P,N_C])
        #Enc
        N_N=[Encrypt(char,'7') for char in N_N]
        N_U=[Encrypt(char,'7') for char in N_U]
        N_P=[Encrypt(char,'7') for char in N_P]
        N_C=[Encrypt(char,'7') for char in N_C]
        N_L=[N_N,N_U,N_P,N_C]
        PLE.append(N_L)

        write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
        print('Password Has Been Successfully Added to Database.','green')
        Backup_CPD('PL')
        
        getpass.getpass('\nPress Enter')

    elif INP=='3':
        DIC={}
        i=0
        for PASSWORD in PLD:
            for SECTIONS in PASSWORD:
                if SECTIONS is PASSWORD[0]:
                    DIC[i]=SECTIONS
                    i+=1
        for item in DIC:
            print(f'{item} => {DIC[item]}')
        def REMOVE():
            DEL=input('Type Number: ')
            try:
                DEL=int(DEL)
                PLE.remove(PLE[DEL])
                PLD.remove(PLD[DEL])
                write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                print('Password Has Been Successfully Removed From Database.','green')
            except ValueError:
                print('Enter Only Number\n')
                REMOVE()
        REMOVE()
        getpass.getpass('\nPress Enter')    

    elif INP=='4': #Show By Category
        SBC = sorted (PLD,key=lambda x : x[3])
        #print(var)
        x=''
        print(' '+'_'*100)
        print(f"|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|") #\n|{25*' '}|{73*' '}|
        for item in SBC:
            if item[3]!=x:
                print('|'+' '*25+'|'+' '*73+'|')
            x=item[3]
            print(f"|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
        print('|'+'_'*99+'|')
        getpass.getpass('\nPress Enter')  

    elif INP=='5': #Show by date 
        SP(False)        
        getpass.getpass('\nPress Enter')

    elif INP=='6': #Change Password
        print(' '+'_'*107)
        print(f"| N|NAME{21*' '}|  USER{21*' '}PASS{21*' '}\tCATEGORY{12*' '}|")
        print(f"|  |{25*' '}|{78*' '}|")
        nom=0
        PaLi=sorted(PLD)
        #PaLi=PLD
        for item in PaLi:
            print('|',end='')
            if len(str(nom))==1:
                print(' ',end='')
            print(f"{nom}|{item[0]+' '*(25-len(item[0]))}|  {item[1]+' '*(25-len(item[1]))}{item[2]+' '*(25-len(item[2]))}\t{item[3]+' '*(20-len(item[3]))}|")
            nom+=1
        nom-=1
        print(' '+'‾'*107)
        getpass.getpass('\nPress Enter')

        def wtc():
            try:
                WTC= int(input('Enter Password Number That You Want to Change:  '))
                if WTC>nom:
                    print('Number out of the range! (Max= {})\n'.format(nom),'red')
                    wtc()
                else:
                    print()
                    NP= input(f'Type New Password of {PaLi[WTC][0]}  :   ')
                    if NP and NP != PaLi[WTC][2]:
                        for item in PLD:
                            #for item in items:
                                if item==PaLi[WTC]:
                                    item[2]=NP
                                    ind= PLD.index(item)
                        PLE[ind][2]=[ord(char) for char in NP]
                        write('PL','InfoE={}\nPL={}'.format(InfoE,PLE))
                        print('Password Has Been Successfully Changed.')                        
                    else:
                        print('Password did not change')
            except ValueError:
                print('Enter Only Number\n')
                wtc()
        wtc()

    elif INP=='7':
        if internet():
            print('Sending Request...')
            #wait(0.5)
            Send_INFO(InfoD[1],InfoD[0],InfoD[2],'Backup')
            getpass.getpass('\nPress Enter')


    if INP=='99':
        cls()

    
    cls()