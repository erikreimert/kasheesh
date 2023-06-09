import pandas as pd
from constants import constants
from dbManager import create_connection


def allByUser(userId):
    database = constants.get("dbName")
    conn = create_connection(database)

    if conn is not None:
        curs = conn.cursor()
        sqlCall = '''SELECT user_id, amount_cents, datetime, merchant_type_code 
                    FROM purchases 
                    WHERE user_id = ? 
                    UNION ALL 
                    SELECT user_id, amount_cents, datetime, merchant_type_code 
                    FROM returns
                    WHERE user_id = ?;'''

        curs.execute(sqlCall, (userId, userId,))

        res = curs.fetchall()
        curs.close()
        conn.close()

        df = pd.DataFrame(res, columns=['user_id', 'amount_cents', 'datetime', 'merchant_type_code'])
        df['amount_in_dollars'] = df['amount_cents'] / 100
        df.drop('amount_cents', axis=1, inplace=True)

        json_data = df.to_json(orient='records')

        return json_data
    else:
        print("Error! cannot create the database connection.")


def netMerchant(merchantTypeCode):
    database = constants.get("dbName")
    conn = create_connection(database)

    if conn is not None:
        curs = conn.cursor()

        # subtracting purchases from returns to reflect that no profit was made
        sqlCall = query = f'''SELECT DATE(p.datetime) AS date, SUM(p.amount_cents - COALESCE(r.amount_cents, 0)) 
                            AS net_amount_in_cents, p.merchant_type_code
                            FROM purchases p
                            LEFT JOIN returns r ON DATE(p.datetime) = DATE(r.datetime) 
                            AND p.merchant_type_code = r.merchant_type_code
                            WHERE p.merchant_type_code = ?
                            GROUP BY DATE(p.datetime)
                            '''

        curs.execute(sqlCall, (merchantTypeCode,))

        res = curs.fetchall()
        curs.close()
        conn.close()

        df = pd.DataFrame(res, columns=['date', 'net_amount_in_cents', 'merchant_type_code'])
        df['net_amount_in_dollars'] = df['net_amount_in_cents'] / 100
        df.drop('net_amount_in_cents', axis=1, inplace=True)

        json_data = df.to_json(orient='records')

        return json_data
    else:
        print("Error! cannot create the database connection.")
