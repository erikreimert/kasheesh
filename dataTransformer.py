import pandas as pd


def allByUserTransform(res: list) -> str:
    """
    Transforms the result of a database query into JSON representation for allByUser function.

    Args:
        res (list): The result of the database query, a list of tuples representing transaction records.

    Returns:
        str: JSON representation of the transformed data.

    Example:
        res = [
            (1, 1000, '2023-06-01 10:00:00', 123),
            (1, 2000, '2023-06-02 10:00:00', 456),
            (1, 3000, '2023-06-03 10:00:00', 789)
        ]
        allByUserTransform(res) -> '[{"user_id":1,"datetime":"2023-06-01 10:00:00","merchant_type_code":123,"amount_in_dollars":10.0},'
                                    '{"user_id":1,"datetime":"2023-06-02 10:00:00","merchant_type_code":456,"amount_in_dollars":20.0},'
                                    '{"user_id":1,"datetime":"2023-06-03 10:00:00","merchant_type_code":789,"amount_in_dollars":30.0}]'
    """

    df = pd.DataFrame(res, columns=['user_id', 'amount_cents', 'datetime', 'merchant_type_code'])
    df['amount_in_dollars'] = df['amount_cents'] / 100
    df.drop('amount_cents', axis=1, inplace=True)

    return df.to_json(orient='records')


def netMerchantTransform(res: list) -> str:
    """
    Transforms the result of a database query into JSON representation for netMerchant function.

    Args:
        res (list): The result of the database query, a list of tuples representing net merchant records.

    Returns:
        str: JSON representation of the transformed data.

    Example:
        res = [
            ('2023-06-01', 5000, 123),
            ('2023-06-02', 3000, 123),
            ('2023-06-03', 2000, 123)
        ]
        netMerchantTransform(res) -> '[{"date":"2023-06-01","merchant_type_code":123,"net_amount_in_dollars":50.0},'
                                      '{"date":"2023-06-02","merchant_type_code":123,"net_amount_in_dollars":30.0},'
                                      '{"date":"2023-06-03","merchant_type_code":123,"net_amount_in_dollars":20.0}]'
    """

    df = pd.DataFrame(res, columns=['date', 'net_amount_in_cents', 'merchant_type_code'])
    df['net_amount_in_dollars'] = df['net_amount_in_cents'] / 100
    df.drop('net_amount_in_cents', axis=1, inplace=True)

    return df.to_json(orient='records')

