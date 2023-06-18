import mysql.connector as sqlcon
from mysql.connector import errorcode

# Configuration settings for connecting to the MySQL database
config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'music',
    'raise_on_warnings': True
}

# get the database from the configuration
def __getDBName():
    """
       Returns the name of the database from the configuration.

       Returns:
           str: The name of the database.

       """
    return config.get('database')

# get the cursor of the database
def __getDBCursor():
    """
        Returns a cursor object for executing queries in the database.

        Returns:
            cursor: A cursor object.

        Raises:
            sqlcon.Error: If an error occurs while executing the query.
        """
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(__getDBName()))
    except sqlcon.Error as err:
        print(err)

    return cursor

# get a sql connection error
def __getSQLConError():
    """
        Returns the `sqlcon.Error` class for SQL connection errors.

        Returns:
            sqlcon.Error: The `sqlcon.Error` class.

    """
    return sqlcon.Error

# get a sql connection error code
def __getSQLConErrorcode():
    """
       Returns the `sqlcon.errorcode` module for SQL connection error codes.

       Returns:
           module: The `sqlcon.errorcode` module.

    """
    return sqlcon.errorcode

# commmit the changes to the database
def __commitDB():
    """
       Commits the changes to the database.

    """
    cnx.commit()

#test the connection to the database
def testConnection():
    """
        Tests the connection to the database.

    """
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

# create the database
def createDatabase():
    """
        Creates the database if it does not exist.

    """
    cursor = __getDBCursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(__getDBName()))
        print("Database \"{}\" was created successfully!".format(__getDBName()))
        cursor.execute("USE {}".format(__getDBName()))
    except sqlcon.Error as err:
        print("Failed creating/accessing DBCreation: {}".format(err))
        exit(1)
