import rx7 as rx



"""
# TODO
    CRITICAL:
        > Encryption
    Login Attempts Log


# NOTE
    ? Different Users

"""







DB_PATH = "Passafe.db"


class Database:
    def __init__(self, path=DB_PATH):
        self.DB_PATH = path
        self.PASSWORD = None
    

    def encrypt(self) -> str:
        pass
        return str(self.DB_PATH)

    def save(self) -> None:
        db = self.encrypt()
        rx.write(DB_PATH,db)

    def load(self) -> str:
        return rx.read(self.DB_PATH)

    def decrypt(self) -> dict:
        db = self.load()
        db = eval(db)
        return db














if __name__ == "__main__":
    DB = Database()
