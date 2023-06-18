import DBCreation.connection as dbcon
import Utils.checkers as chk
import API.requestsAPI as api
import Entities.Genres.genresData as gendat

# method which inserts artists in the database
def insertArtists():
    """
       Inserts artists into the artists table in the database.

    """
    cursor = dbcon.__getDBCursor()

    # get the top artists from the api
    artists = api.__getTopArtists(10)

    # sql code to insert a new artist to the artists table
    addArtist = "INSERT INTO artists (name, genre) VALUES (%(name)s, %(genre)s)"

    for artist in artists:
        name = artist['name']
        genre = artist['genre']

        # Prepare the data for inserting an artist
        dataArtist = {
            'name': name,
            'genre': genre
        }

        # insert the artist's genre
        gendat.insertGenre(genre)

        # insert the artist's data if it doesn't exist in the database
        try:
            cursor.execute(addArtist, dataArtist)
        except dbcon.__getSQLConError() as err:
            if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Artist] \"{}\" already exists.".format(name))
        else:
            print("[Artist] \"{}\" successfully inserted!".format(name))

    # check for any data issues in the artists table
    chk.checkDataIssues('artists')
    dbcon.__commitDB()
    cursor.close()
