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

    """Enter the card number"""

    @staticmethod
    def input_card(number_card):
        try:
            with sqlite3.connect("atm") as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card};""")
                result_card = cur.fetchone()
                if result_card == None:
                    print("Card invalid")
                    return False
                else:
                    print(f'Card number entered successfully: {number_card}')
                    return True

        except:
            print("Card number not found")

    """PINCODE method"""

    @staticmethod
    def input_code(number_card):
        pin_code = input("Enter the card pin-code: ")
        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card};""")
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print("Pin-code correct")
                    return True
                else:
                    print("Pin-code incorrect")
                    return False
            except:
                print("Pin-code incorrect")
                return False

    """Card balance method"""

    @staticmethod
    def info_balance(number_card):

        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card};""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f'Balance your card: {balance_card}')

    """Withdraw method"""

    @staticmethod
    def withdraw_money(number_card):

        amount = input("Enter the amount you want to withdraw from your card balance ")
        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card};""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) > balance_card:
                    print("There are insufficient funds on your card")
                    return False
                else:
                    cur.execute(f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    return True
            except:
                print("Attempt to perform an invalid action")
                return False
