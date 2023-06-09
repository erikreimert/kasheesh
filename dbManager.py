import pandas as pd
import sqlite3
from sqlite3 import Error

from constants import constants


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)


def generateDfPurchaseReturns():
    transactions = pd.read_csv(constants.get('combined_transactions.csv'))

    purchases = transactions.loc[transactions['transaction_type'] == 'PurchaseActivity']
    returns = transactions.loc[transactions['transaction_type'] == 'ReturnActivity']

    return purchases, returns


def dbInit():
    database = constants.get("dbName")

    sql_create_purchases_table = """ CREATE TABLE IF NOT EXISTS purchases (
                                        user_id integer PRIMARY KEY,
                                        transaction_type text,
                                        merchant_type_code int,
                                        amount_cents int,
                                        datetime text
                                    ); """

    sql_create_returns_table = """CREATE TABLE IF NOT EXISTS returns (
                                        user_id integer PRIMARY KEY,
                                        transaction_type text,
                                        merchant_type_code int,
                                        amount_cents int,
                                        datetime text
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create purchases table
        create_table(conn, sql_create_purchases_table)

        # create returns table
        create_table(conn, sql_create_returns_table)
    else:
        print("Error! cannot create the database connection.")

    purchases, returns = generateDfPurchaseReturns()

    purchases.to_sql('purchases', conn, if_exists='replace', index=False)
    returns.to_sql('returns', conn, if_exists='replace', index=False)
    conn.close()
