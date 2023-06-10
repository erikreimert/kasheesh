import pandas as pd
import sqlite3
from sqlite3 import Error
from constants import Constants


def create_connection(db_file):
    """
    Create a connection to the SQLite database specified by the db_file.

    Args:
        db_file (str): The file path of the SQLite database.

    Returns:
        sqlite3.Connection: The connection object to the SQLite database.

    Raises:
        Error: If an error occurs while creating the connection.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    Create a table in the SQLite database using the provided SQL statement.

    Args:
        conn (sqlite3.Connection): The connection object to the SQLite database.
        create_table_sql (str): The SQL statement to create the table.

    Returns:
        None

    Raises:
        Error: If an error occurs while executing the SQL statement.
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)


def generateDfPurchaseReturns(transactions: pd.DataFrame) -> [pd.DataFrame]:
    """
    Generate DataFrames for purchases and returns from a combined transactions CSV file.

    Args:
    transactions (pd.Dataframe): The pd.DataFrame to be transformed into the data for the purchases and returns table.

    Returns:
        tuple: A tuple containing two pandas DataFrames, purchases and returns.

    Raises:
        None
    """

    purchases = transactions.loc[transactions['transaction_type'] == 'PurchaseActivity'].reset_index(drop=True)
    returns = transactions.loc[transactions['transaction_type'] == 'ReturnActivity'].reset_index(drop=True)

    return purchases, returns


def executeQuery(query: str, database: str) -> list:
    try:
        conn = create_connection(database)

        curs = conn.cursor()
        curs.execute(query)

        res = curs.fetchall()
        curs.close()
        conn.close()

        return res

    except Exception as e:
        print("An error occurred:", str(e))


def dbInit():
    """
    Initialize the database by creating tables and filling them with data.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the database connection, table creation, or data insertion.
    """
    try:
        database = Constants.dbName.value

        sql_create_purchases_table = Constants.createPurchases.value

        sql_create_returns_table = Constants.createReturns.value

        # create a database connection
        conn = create_connection(database)

        # create tables
        if conn is not None:
            # create purchases table
            create_table(conn, sql_create_purchases_table)

            # create returns table
            create_table(conn, sql_create_returns_table)
        else:
            raise Exception("Error! Cannot create the database connection.")

        # generates the DataFrames to fill up the purchase and returns tables
        transactions = pd.read_csv(Constants.combined_transactions.value)
        purchases, returns = generateDfPurchaseReturns(transactions)

        # uses the DataFrames to fill the purchase and returns tables
        purchases.to_sql('purchases', conn, if_exists='replace', index=False)
        returns.to_sql('returns', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print("An error occurred:", str(e))
