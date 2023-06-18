import DBCreation.connection as dbcon
import Utils.checkers as chk
import API.requestsAPI as api
import Entities.Genres.genresData as gendat


def insertArtists():
    cursor = dbcon.__getDBCursor()

    artists = api.__getTopArtists(10)

    addArtist = "INSERT INTO artists (name, genre) VALUES (%(name)s, %(genre)s)"

    for artist in artists:
        name = artist['name']
        genre = artist['genre']

        dataArtist = {
            'name': name,
            'genre': genre
        }

        gendat.insertGenre(genre)

        try:
            cursor.execute(addArtist, dataArtist)
        except dbcon.__getSQLConError() as err:
            if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Artist] \"{}\" already exists.".format(name))
        else:
            print("[Artist] \"{}\" successfully inserted!".format(name))

    chk.checkDataIssues('artists')
    dbcon.__commitDB()
    cursor.close()
