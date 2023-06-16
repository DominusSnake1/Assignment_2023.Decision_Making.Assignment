import mysql.connector as sqlcon
from mysql.connector import errorcode
import Utils.connection as uticon

TABLES = {
    'users': (
        """
            CREATE TABLE users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                age INT,
                gender CHAR(1) CHECK (gender = 'M' or gender = 'F')
            )
        """
    ),
    'bands': (
        """
            CREATE TABLE bands (
                band_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                genre VARCHAR(50)
            )
        """
    ),
    'albums': (
        """
            CREATE TABLE albums (
                album_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100),
                band_id INT,
                FOREIGN KEY (band_id) REFERENCES bands(band_id)
            )
        """
    ),
    'userLikes': (
        """
            CREATE TABLE userLikes (
                user_id INT,
                band_id INT,
                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                FOREIGN KEY (band_id) REFERENCES Bands (band_id)
            )
        """
    ),
    'userOwnsAlbum': (
        """
            CREATE TABLE userOwnsAlbum (
                user_id INT,
                album_id INT,
                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                FOREIGN KEY (album_id) REFERENCES Albums (album_id)
            )
        """
    )}


def createTables():
    cursor = uticon.__getDBCursor()
    cursor.execute("USE {}".format(uticon.__getDBName()))

    for tableName in TABLES:
        tableDescription = TABLES[tableName]
        try:
            print("Creating table \"{}\".".format(tableName))
            cursor.execute(tableDescription)
        except sqlcon.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table \"{}\" already exists.".format(tableName))
            else:
                print(err.msg)
        else:
            print("Table \"{}\" created.".format(tableName))

    cursor.close()
