from pprint import pprint

import rx7 as rx
import pyperclip
from tabulate import tabulate
from addict import Addict


"""
# TODO
    CRITICAL:
        > Encryption
    Hide Password in "List_Passwords"
    Login Attempts Log



# NOTE
    ? Different Users

"""







DB_PATH = "Passafe.db"


class Database:
    def __init__(self, path=DB_PATH):
        self.DB_PATH = path
        self.PASSWORD = None
        self.decrypted = self.decrypt()
        self.DB = self.get_user_db()

    def encrypt(self) -> str:
        pass
        return str(self.DB_PATH)

    def save(self) -> None:
        db = self.encrypt()
        rx.write(DB_PATH,db)

    def load(self) -> str:
        return rx.read(self.DB_PATH)

    def decrypt(self) -> Addict:
        db = self.load()
        db = eval(db)
        db = Addict(db)
        return db

    def get_user_db(self):
        return self.decrypted.User.DB

    def get_user_db_copy(self):
        return self.decrypt().User.DB

    # def __str__(self) -> str:  pass





def Menu(DB):
    user_db = DB.DB
    print(" Select an option:")
    print("   1) List Passwords")
    print("   2) List Passwords by Category")
    print("   3) Add Password")
    print("   4) Delete Password")
    
    inp = rx.io.selective_input(f"\n Passafe> ",["0","1","2","3"])
    
    if inp in ("1","2"):
        rx.cls()
        (table,n,keys) = List_Passwords(DB, False if inp=="1" else True)
        last_selected = None
        print('\n Select a password to copy it to clipboard (Type full "NAME" to see it)')
        options =  list(map(str,range(1,n+1))) + list(user_db.keys())
        item = rx.io.selective_input("\nPassafe>List> ",options)
        try:
            int(item)
            pyperclip.copy(table[int(item)-1][4])
            print(f'\nPassword of "{keys[int(item)-1]}" is copied to your clipboard')
        except ValueError:
            row = [[item] + user_db[item]]
            print(tabulate(row))

#] Print Passwords in Date/Category format
def List_Passwords(DB, by_category=False):
    user_db = DB.get_user_db_copy()
    if by_category:
        table =  {k: v for k, v in sorted(user_db.items(), key=lambda item: item[1][3])}
        keys  =  list(table.keys())
        table =  list(table.values())
    else:
        table = list(user_db.values())
        keys = list(user_db.keys())
    
    # Adding nom before the list in the table
    for i,item in enumerate(table,1):
        item.insert(0,i)
        item.insert(1,keys[i-1])
    # Changing Password when shown
    removed_pw = []
    for item in table:
        removed_pw.append(item[:4]+["XXXX"]+item[5:])
    print()
    print(tabulate(removed_pw,headers=["NO","NAME","URL","USERNAME","PASSWORD","CATEGORY"]))
    return (table,i,keys)




if __name__ == "__main__":
    DB = Database()
    
    rx.cls()
    
    Menu(DB)
    
    # print("\n\n\n")
    # pprint((DB.DB))
