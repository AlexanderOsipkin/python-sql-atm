from sql_query import SQL_atm


class ATM():

    def atm_logic(self):
        SQL_atm.create_table()
        SQL_atm.insert_user((1234, 1111, 10000))


start = ATM()
start.atm_logic()
