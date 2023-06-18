import DBCreation.connection as dbcon
import Utils.checkers as chk
import API.requestsAPI as api


def insertAlbums():
    cursor = dbcon.__getDBCursor()

    cursor.execute("SELECT name FROM artists")
    artists = [row[0] for row in cursor.fetchall()]

    addAlbum = "INSERT INTO albums (title, artist_id) VALUES (%(title)s, (SELECT artist_id FROM artists WHERE artists.name = %(artist)s))"

    for artist in artists:
        album = api.getTopAlbum(artist)
        dataAlbum = {
            'title': album,
            'artist': artist
        }

        try:
            cursor.execute(addAlbum, dataAlbum)
        except dbcon.__getSQLConError() as err:
            if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Album] \"{}\" by \"{}\" already exists.".format(album, artist))
        else:
            print("[Album] \"{}\" by \"{}\" inserted.".format(album, artist))

    chk.checkDataIssues('albums')
    dbcon.__commitDB()
    cursor.close()
