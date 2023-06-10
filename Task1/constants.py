from enum import Enum


def getAllByUsersCall(user_id: int) -> str:
    allByUserCall = f'''SELECT user_id, amount_cents, datetime, merchant_type_code 
                    FROM purchases 
                    WHERE user_id = {user_id} 
                    UNION ALL 
                    SELECT user_id, amount_cents, datetime, merchant_type_code 
                    FROM returns
                    WHERE user_id = {user_id};'''
    return allByUserCall


def getNetMerchantCall(merchant_type_code: int) -> str:
    netMerchantCall = f'''SELECT DATE(p.datetime) AS date, SUM(p.amount_cents - COALESCE(r.amount_cents, 0)) 
                            AS net_amount_in_cents, p.merchant_type_code
                            FROM purchases p
                            LEFT JOIN returns r ON DATE(p.datetime) = DATE(r.datetime) 
                            AND p.merchant_type_code = r.merchant_type_code
                            WHERE p.merchant_type_code = {merchant_type_code}
                            GROUP BY DATE(p.datetime)
                            '''
    return netMerchantCall


# Define an Enum class
# Note: I konw that the common practice is to use Enums for repeated values, and even those most of these appear once in
# code I think keeping them here makes the code more readable
class Constants(Enum):
    dbName = r"pythonsqlite.db"
    combined_transactions = "combined_transactions.csv"

    createPurchases = """ CREATE TABLE IF NOT EXISTS purchases (
                                        user_id integer PRIMARY KEY,
                                        transaction_type text,
                                        merchant_type_code int,
                                        amount_cents int,
                                        datetime text
                                    ); """
    createReturns = """CREATE TABLE IF NOT EXISTS returns (
                                        user_id integer PRIMARY KEY,
                                        transaction_type text,
                                        merchant_type_code int,
                                        amount_cents int,
                                        datetime text
                                );"""
