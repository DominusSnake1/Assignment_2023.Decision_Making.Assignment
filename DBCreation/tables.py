import mysql.connector as sqlcon
from mysql.connector import errorcode
import DBCreation.connection as dbcon

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
    'artists': (
        """
            CREATE TABLE artists (
                artist_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE,
                genre VARCHAR(50)
            )
        """
    ),
    'albums': (
        """
            CREATE TABLE albums (
                album_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100),
                artist_id INT,
                FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
                CONSTRAINT UC_Album UNIQUE (title, artist_id)
            )
        """
    ),
    'userLikes': (
        """
            CREATE TABLE userLikes (
                user_id INT,
                artist_id INT,
                FOREIGN KEY FK_ULtoU (user_id) REFERENCES users (user_id),
                FOREIGN KEY FK_ULtoA (artist_id) REFERENCES artists (artist_id)
            )
        """
    ),
    'userOwnsAlbum': (
        """
            CREATE TABLE userOwnsAlbum (
                user_id INT,
                album_id INT,
                FOREIGN KEY FK_UOAtoU (user_id) REFERENCES users (user_id),
                FOREIGN KEY FK_UOAtoA (album_id) REFERENCES albums (album_id)
            )
        """
    ),
    'genres': (
        """
            CREATE TABLE genres (
                genre_id INT AUTO_INCREMENT PRIMARY KEY,
                genre VARCHAR(50) UNIQUE
            )
        """
    ),
    'stats': (
        """
            CREATE TABLE stats (
                stat_id INT AUTO_INCREMENT PRIMARY KEY,
                artist_id INT UNIQUE,
                artists_fans INT,
                genre_id INT,
                genres_fans INT,
                FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
            )
        """
    )}


def createTables():
    cursor = dbcon.__getDBCursor()
    cursor.execute("USE {}".format(dbcon.__getDBName()))

    for tableName in TABLES:
        tableDescription = TABLES[tableName]
        try:
            cursor.execute(tableDescription)
        except sqlcon.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("[Table] \"{}\" already exists.".format(tableName))
            else:
                print(err.msg)
        else:
            print("[Table] \"{}\" created.".format(tableName))

    cursor.close()
