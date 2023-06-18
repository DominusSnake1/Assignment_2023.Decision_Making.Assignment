import DBCreation.connection as dbcon
import Utils.checkers as chk


def insertGenre(genre):
    cursor = dbcon.__getDBCursor()

    addGenre = "INSERT INTO genres (genre) VALUES (%(genre)s)"

    dataGenre = {
        'genre': genre
    }

    try:
        cursor.execute(addGenre, dataGenre)
    except dbcon.__getSQLConError() as err:
        if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
            print("[Genre] \"{}\" already exists.".format(genre))
        else:
            print(err.msg)
    else:
        print("[Genre] \"{}\" successfully inserted!".format(genre))

    chk.checkDataIssues('genres')
    dbcon.__commitDB()
    cursor.close()
