from sql_query import SqlAtm


class ATM():

    def atm_logic(self):
        SqlAtm.create_table()
        SqlAtm.insert_user((1234, 1111, 10000)) #1234 2345 111 2222
        number_card = input("Enter the card number: ")

        while True:
            if SqlAtm.input_card(number_card):
                if SqlAtm.input_code(number_card):

                    SqlAtm.input_operation(number_card)
                    break

                else:
                    break

            else:
                break


start = ATM()
start.atm_logic()
