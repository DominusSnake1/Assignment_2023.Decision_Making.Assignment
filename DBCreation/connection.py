import mysql.connector as sqlcon
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'music',
    'raise_on_warnings': True
}


def __getDBName():
    return config.get('database')


def __getDBCursor():
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(__getDBName()))
    except sqlcon.Error as err:
        print(err)

    return cursor


def __getSQLConError():
    return sqlcon.Error


def __getSQLConErrorcode():
    return sqlcon.errorcode


def __commitDB():
    cnx.commit()


def testConnection():
    global cnx
    try:
        cnx = sqlcon.connect(user='root', password='password')
        con = sqlcon.connect(**config)
    except sqlcon.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Make sure the username and password are correct!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("!!! Database \"{}\" does not exist !!!".format(__getDBName()))
            createDatabase()
        else:
            print(err)
    else:
        print("Successfully connected to the DBCreation!")
        con.close()


def createDatabase():
    cursor = __getDBCursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(__getDBName()))
        print("Database \"{}\" was created successfully!".format(__getDBName()))
        cursor.execute("USE {}".format(__getDBName()))
    except sqlcon.Error as err:
        print("Failed creating/accessing DBCreation: {}".format(err))
        exit(1)
