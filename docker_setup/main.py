import psycopg2

import currency_requests as currency_requests
import db_conn as db_conn


def print_options():
    print("""Choose an of the options: 
    1.To exchange the currency.
    2.To show history of transactions
    3. To quit the program.
    """)


def main():

    while True:
        print_options()
        user_input = input()

        if user_input == "1":
            db_conn.insert_into_db(currency_requests.Currency_converter.currency_exchange())

        elif user_input == "2":
            db_conn.transaction_history()
        elif user_input == "3":
            break
        else:
            print("wrong choice, enter it again\n")


main()
