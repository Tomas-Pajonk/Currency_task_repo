import psycopg2

from config import config


def insert_into_db(conversion):

    connection = None
    columns = "date, currency_from, currency_to, currency_ratio"

    try:
        params = config()
        print("Connecting to postgresql")
        connection = psycopg2.connect(**params)
        curr = connection.cursor()

        curr.execute('''Create table if not exists currency_transactions(
            date varchar(128),
            currency_from varchar(128),
            currency_to varchar(128),
            currency_ratio varchar(128))
            ''')

        curr.execute(f"INSERT INTO currency_transactions({columns}) VALUES{conversion}")

        connection.commit()

        curr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    if connection is not None:
        connection.close()
        


def transaction_history():
    connection = None
    try:
        params = config()
        print("Connecting to postgresql")
        connection = psycopg2.connect(**params)
        curr = connection.cursor()

        curr.execute("Select * from currency_transactions")
        for i in curr.fetchall():
            print(i)
        connection.commit()

        curr.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    if connection is not None:
        connection.close()
        