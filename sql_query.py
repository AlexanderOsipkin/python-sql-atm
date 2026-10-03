import sqlite3


class SQL_atm:
    """Create table Users_data"""

    @staticmethod
    def create_table():
        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INETEGER NOT NULL);""")
            print("Data Base create successfully")

    """Create new user"""

    @staticmethod
    def insert_user(data_users):
        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data (Number_card, Pin_code, Balance)
            VALUES(?, ?, ?);""", data_users)
            print("Add new user")