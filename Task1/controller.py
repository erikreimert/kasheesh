from constants import getAllByUsersCall, getNetMerchantCall, Constants
from dbManager import executeQuery
from dataTransformer import allByUserTransform, netMerchantTransform


def allByUser(userId: int) -> str:
    """
    Retrieves all transactions associated with a given user ID from the database.

    Args:
        userId (int): The ID of the user.

    Returns:
        str: JSON representation of the retrieved transactions.
    """

    # Parse query with userID
    query = getAllByUsersCall(userId)
    # Execute the query against the SQL table
    res = executeQuery(query, Constants.dbName.value)

    # Parse data accordingly
    json_data = allByUserTransform(res)

    return json_data


def netMerchant(merchantTypeCode: int) -> str:
    """
    Calculates the net amount of transactions for a specific merchant type from the database.

    Args:
        merchantTypeCode (int): The code representing the merchant type.

    Returns:
        str: JSON representation of the calculated net amount of transactions.
    """

    # Parse query with userID
    query = getNetMerchantCall(merchantTypeCode)
    # Execute the query against the SQL table
    res = executeQuery(query, Constants.dbName.value)

    # Parse data accordingly
    json_data = netMerchantTransform(res)

    return json_data
