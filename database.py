import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.db')
c = conn.cursor()


def exe(querys):
    return conn.execute(querys)

class table_creation:
    def dataTable(self):
        query = """CREATE TABLE IF NOT EXISTS machine_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TransID TEXT NOT NULL,
            Credit INTEGER DEFAULT 0 NOT NULL,
            Debit INTEGER DEFAULT 0 NOT NULL,
            Balance INTEGER,
            Date TEXT NOT NULL
        )"""
        return exe(query)

    def userTable(self):
        query = """CREATE TABLE IF NOT EXISTS userData (
            id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 1 NOT NULL,
            mobileno INTEGER DEFAULT 0 NOT NULL,
            secretpin INTEGER DEFAULT 1234 NOT NULL,
            attempts INTEGER DEFAULT 3 NOT NULL,
            resetkey INTEGER DEFAULT 4444 NOT NULL,
            accreset INTEGER DEFAULT 1122 NOT NULL
        )"""
        return exe(query)

class CRUD:
    def debitEntry(self, Debit, Date):
        self.__Debit = Debit
        self.__Date = Date
        Balance = CRUD.lastValue('Balance')
        TransID = CRUD.TransIDGen("WTH#")
        query = f"INSERT INTO machine_data (TransID, Debit, Balance, Date) VALUES ('{TransID}', {self.__Debit}, {Balance - self.__Debit}, '{self.__Date}')"
        exe(query)
        conn.commit()
        return (self.__Debit, TransID)

    def creditEntry(self, Credit, Date):
        self.__Credit = Credit
        self.__Date = Date
        Balance = CRUD.lastValue('Balance')
        TransID = CRUD.TransIDGen("REF#")
        query = f"INSERT INTO machine_data (TransID, Credit, Balance, Date) VALUES ('{TransID}', {self.__Credit}, {Balance+self.__Credit}, '{self.__Date}')"
        exe(query)
        conn.commit()
        return (self.__Credit, TransID)
    
    def userUpdate(self, db_table, data): # the order is as per database mobile, secretpin, attempts, reset, accreset
        exe(f"UPDATE userData SET {db_table} = {data}")
        conn.commit()        
    
    @staticmethod
    def lastValue(x, db='machine_data', custom_db=False, dataType=float): # returns last row value if string or integer
        preBalance = 0
        if custom_db:
            for y in exe(f"SELECT {x} FROM {db}"):
                return y[0]
        for x in exe(f"SELECT {x} FROM {db}"):
            preBalance = x[0]
        if dataType == str:
            return dataType(preBalance)
        return round(dataType(preBalance), 2)
    
    @staticmethod
    def Delete():
        query = "DELETE FROM machine_data"
        exe(query)
        conn.commit()
    
    @staticmethod
    def TransIDGen(prefix):
        for x in exe("SELECT TransID FROM machine_data"):
            if x:
                value = CRUD.lastValue('TransID', dataType=str)[len(prefix):]
                return f"{prefix}{int(value)+1}"
        return f"{prefix}{10000}"
    
    @staticmethod
    def defaultInsert():
        for x in exe("SELECT * FROM userData"):
            if x:
                return
        query = "INSERT INTO userData (id) VALUES (1)"
        exe(query)
        conn.commit()

#instantiate
CRUD = CRUD()
table_creation = table_creation()

# if __name__ == '__main__':
table_creation.dataTable()
table_creation.userTable()
CRUD.defaultInsert()
    