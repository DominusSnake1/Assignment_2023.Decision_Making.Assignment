import DBCreation.connection as dbcon
import Utils.checkers as chk

# function which inserts a genre in the database
def insertGenre(genre):
    """
        Inserts a genre into the genres table in the database.

        Args:
            genre (str): The genre to be inserted.

    """
    cursor = dbcon.__getDBCursor()

    # sql code to insert a genre to the genres table
    addGenre = "INSERT INTO genres (genre) VALUES (%(genre)s)"

    # prepare the data for the insertion of a genre
    dataGenre = {
        'genre': genre
    }

    # insert the genre with its data if it doesn't exist in the database
    try:
        cursor.execute(addGenre, dataGenre)
    except dbcon.__getSQLConError() as err:
        if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
            print("[Genre] \"{}\" already exists.".format(genre))
        else:
            print(err.msg)
    else:
        print("[Genre] \"{}\" successfully inserted!".format(genre))

    # check for any data issues in the genres table
    chk.checkDataIssues('genres')
    dbcon.__commitDB()
    cursor.close()
