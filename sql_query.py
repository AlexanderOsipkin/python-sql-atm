import os
import sqlite3
import csv
from datetime import datetime


class SqlAtm:
    """Create table Users_data"""

    # создаем новую таблицу в БД, если ее нет
    @staticmethod
    def create_table():

        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL UNIQUE,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);""")
            print("Data Base create successfully")

    # Создаем нового пользователя
    @staticmethod
    def insert_user(data_users):
        """Create new user"""

        try:
            with sqlite3.connect("atm") as db:
                cur = db.cursor()
                cur.execute("""INSERT INTO Users_data (Number_card, Pin_code, Balance)
                    VALUES (?, ?, ?);""",
                            data_users)

                db.commit()
                print("Add new user")

        except sqlite3.IntegrityError:
            print("This card number already exists")

    # Создаем метод для ввода номера карты
    @staticmethod
    def input_card(number_card):
        """Enter the card number"""

        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute(
                """SELECT Number_card
                FROM Users_data
                WHERE Number_card = ?;""",
                (number_card,))

            result_card = cur.fetchone()

            if result_card is None:
                print("Card invalid")
                return False

            print(f"Card number entered successfully: {number_card}")
            return True

    # Создаем метод для ввода пин-кода от карты пользователя
    @staticmethod
    def input_code(number_card):
        """PINCODE method"""

        pin_code = input("Enter the card pin-code: ")
        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""SELECT Pin_code 
                FROM Users_data 
                WHERE Number_card = ?;""",
                        (number_card,))
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print("Pin-code correct")
                    return True
                else:
                    print("Pin-code incorrect")
                    return False
            except ValueError:
                print("Pin-code incorrect")
                return False

    # Создаем метод для просмотра баланса по карте текущего пользователя
    @staticmethod
    def info_balance(number_card):
        """Card balance method"""

        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance 
                FROM Users_data 
                WHERE Number_card = ?;""",
                        (number_card,))

            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f'Balance your card: {balance_card}')

    # Создаем метод снятия наличных с карты текущего пользователя
    @staticmethod
    def withdraw_money(number_card):
        """Withdraw method"""

        amount = int(input("Enter the amount you want to withdraw from your card balance: "))

        if amount <= 0:
            print("The withdrawal amount must be greater than zero")
            return False

        with sqlite3.connect("atm") as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance 
                FROM Users_data 
                WHERE Number_card = ?;""",
                        (number_card,))
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]

            try:
                if int(amount) > balance_card:
                    print("There are insufficient funds on your card")
                    return False

                else:
                    cur.execute(
                        """UPDATE Users_data 
                        SET Balance = Balance - ?
                        WHERE Number_card = ?;""",
                        (amount, number_card))
                    db.commit()
                    SqlAtm.info_balance(number_card)
                    return True

            except ValueError:
                print("Attempt to perform an invalid action")
                return False

    # Создаем метод для пополнения карты текущего пользователя
    @staticmethod
    def depositing_money(number_card):
        """Deposit method"""

        try:
            amount = int(input("Enter the amount you wish to deposit into the account: "))

            if amount <= 0:
                print("The deposit amount must be greater than zero")
                return False

            with sqlite3.connect("atm") as db:
                cur = db.cursor()
                cur.execute(
                    """UPDATE Users_data
                    SET Balance = Balance + ?
                    WHERE Number_card = ?;""",
                    (amount, number_card))

                db.commit()

                print("Money successfully deposited")
                SqlAtm.info_balance(number_card)

                return True

        except ValueError:
            print("Invalid deposit amount")
            return False

    # Report operation 1: отчет об операции
    @staticmethod
    def report_operation_1(now_date, number_card, type_operation, amount, payee):
        """Save transfer operation to report_1.csv"""

        try:
            with open("report_1.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")

                # Добавляем заголовки, если файл пустой
                if file.tell() == 0:
                    writer.writerow([
                        "Data",
                        "Number_card",
                        "Type_operation",
                        "Amount",
                        "Payee"
                    ])

                # Записываем данные о переводе
                writer.writerow([
                    now_date,
                    number_card,
                    type_operation,
                    amount,
                    payee
                ])

            print("The data is entered into the report_1.csv")
            return True

        except OSError as error:
            print(f"Error writing to  report_1.csv: {error}")
            return False

    # Report operation 2: добавляет информацию об успешном переводе в файл report_2.csv
    @staticmethod
    def report_operation_2(now_date, payee, type_operation, amount, number_card):

        try:
            with open("report_2.csv", "a", newline="") as file:
                writer = csv.writer(file, delimiter=";")

                # Добавляем заголовки, если файл пустой
                if file.tell() == 0:
                    user_data = [
                        ("Date", "Payee", "Type operation", "Amount", "Sender")
                    ]
                    writer.writerows(user_data)

                # Записываем данные об операции
                user_data = [
                    (now_date, payee, type_operation, amount, number_card)
                ]

                writer.writerows(user_data)

            print("The data is entered into the report_2.csv")
            return True

        except OSError as error:
            print(f"Error writing to  report_2.csv: {error}")
            return False

    # Создаем метод для перевода денежных средств между клиентами
    @staticmethod
    def transfer_money(number_card):
        """Transfer money method"""

        recipient_card = input("Enter the recipient's card number: ")
        amount_input = input("Enter the amount you want to transfer: ")

        try:
            amount = int(amount_input)
        except ValueError:
            print("Invalid transfer amount. Enter a whole number")
            return False

        if amount <= 0:
            print("The transfer amount must be greater than zero")
            return False

        if recipient_card == str(number_card):
            print("You cannot transfer money to your own card")
            return False

        with sqlite3.connect("atm") as db:
            cur = db.cursor()

            # Проверяем существование карты отправителя
            cur.execute("""SELECT Balance 
                    FROM Users_data 
                    WHERE Number_card = ?;""",
                        (number_card,))
            sender = cur.fetchone()

            if sender is None:
                print("Sender card not found")
                return False

            # Проверяем существование карты получателя
            cur.execute("""SELECT Number_card 
                    FROM Users_data 
                    WHERE Number_card = ?;""",
                        (recipient_card,))
            recipient = cur.fetchone()

            if recipient is None:
                print("Recipient card not found")
                return False

            # Запрещаем перевод самому себе
            if number_card == recipient_card:
                print("You cannot transfer money to your own card")
                return False

            # Проверяем наличие достаточного количества денег на балансе
            balance = sender[0]
            if amount > balance:
                print("There are insufficient funds on your card")
                return False

            # Списываем деньги с карты отправителя
            cur.execute("""UPDATE Users_data 
                    SET Balance = Balance - ? 
                    WHERE Number_card = ?;""",
                        (amount, number_card))

            # Зачисляем деньги на карту получателя
            cur.execute("""UPDATE Users_data
                    SET Balance = Balance + ?
                    WHERE Number_card = ?;""",
                        (amount, recipient_card))

            db.commit()

        # Создаем переменную для даты для использования в репортах
        now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payee = recipient_card
        type_operation = 3

        print(f"Transfer of {amount} successfully completed to card {recipient_card}")

        SqlAtm.report_operation_1(now_date, number_card, type_operation, amount, recipient_card)
        SqlAtm.report_operation_2(now_date, recipient_card, type_operation, amount, number_card)
        SqlAtm.info_balance(number_card)

        return True

    # Создаем метод для выбора операции с картой после запуска банкомата
    @staticmethod
    def input_operation(number_card):
        """Selecting a card transaction method"""

        while True:
            operation = input("Selecting a card transaction: \n"
                              "1. Find out the balance on the card\n"
                              "2. Withdraw funds from the card\n"
                              "3. Add funds to the card balance\n"
                              "4. Transfer funds\n"
                              "5. Complete card transactions\n")

            if operation == "1":
                SqlAtm.info_balance(number_card)

            elif operation == "2":
                SqlAtm.withdraw_money(number_card)

            elif operation == "3":
                SqlAtm.depositing_money(number_card)

            elif operation == "4":
                SqlAtm.transfer_money(number_card)

            elif operation == "5":
                print("Thank you for visiting us, all the best")
                return False


            else:
                print("This card transaction is unknown. Try selecting a different card transaction.")