import DBCreation.connection as dbcon
import Utils.checkers as chk
import API.requestsAPI as api

# function which inserts the albums in the database
def insertAlbums():
    """
       Inserts albums into the albums table in the database.

    """
    cursor = dbcon.__getDBCursor()

    # select all the artists in the database
    cursor.execute("SELECT name FROM artists")
    artists = [row[0] for row in cursor.fetchall()]

    # sql code to insert a new album in the albums table
    addAlbum = "INSERT INTO albums (title, artist_id) VALUES (%(title)s, (SELECT artist_id FROM artists WHERE artists.name = %(artist)s))"

    # get the top album of an artist
    for artist in artists:
        album = api.getTopAlbum(artist)
        dataAlbum = {
            'title': album,
            'artist': artist
        }

        # insert the album with its data if it doesn't exist in the database
        try:
            cursor.execute(addAlbum, dataAlbum)
        except dbcon.__getSQLConError() as err:
            if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Album] \"{}\" by \"{}\" already exists.".format(album, artist))
        else:
            print("[Album] \"{}\" by \"{}\" inserted.".format(album, artist))

    # check for any data issues in the albums table
    chk.checkDataIssues('albums')
    dbcon.__commitDB()
    cursor.close()
