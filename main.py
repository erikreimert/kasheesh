import dbManager


if __name__ == '__main__':
    conn = dbManager.dbInit()

    conn.close()