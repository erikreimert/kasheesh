import dbManager, sqlCalls


if __name__ == '__main__':
    dbManager.dbInit()
    sqlCalls.allByUser(38493)
    sqlCalls.netMerchant(5200)
