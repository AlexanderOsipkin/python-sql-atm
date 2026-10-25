from sql_query import SqlAtm


class ATM:

    def atm_logic(self):
        # Создаём таблицы, если их ещё нет
        SqlAtm.create_table()

        # Создаём двух пользователей для проверки работы банкомата
        # SqlAtm.insert_user((1234, 1111, 10000))
        # SqlAtm.insert_user((2345, 2222, 10000))

        # Ввод номера карты
        number_card = input("Enter the card number: ")

        # Проверяем номер карты
        if not SqlAtm.input_card(number_card):
            return

        # Проверяем PIN-код
        if not SqlAtm.input_code(number_card):
            return

        # Запускаем меню банкомата
        SqlAtm.input_operation(number_card)


start = ATM()
start.atm_logic()
