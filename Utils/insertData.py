import random
import Utils.connection as uticon


def insertAllData(users):
    insertRandomUsers(users)
    insertBands()


def insertRandomUsers(users):
    cursor = uticon.__getDBCursor()

    usernames = ['user{}'.format(i) for i in range(users)]

    addUser = "INSERT INTO users (username, age, gender) VALUES (%(username)s, %(age)s, %(gender)s)"

    for user in usernames:
        dataUser = {
            'username': user,
            'age': random.randint(18, 65),
            'gender': random.choice(['M', 'F'])
        }

        cursor.execute(addUser, dataUser)
        print("User \"{}\" inserted.".format(user))

    uticon.__commitDB()
    cursor.close()


def insertBands():
    cursor = uticon.__getDBCursor()

    bands = {
        'Moderat': 'Dance/Electronic',
        'Tale Of Us': 'Melodic Techno',
        'Artic Monkeys': 'Indie Rock',
        'The Weeknd': 'Pop',
        'ACDC': 'Heavy Metal',
        'NSYNC': 'Pop'
    }

    addBand = "INSERT INTO bands (name, genre) VALUES (%(name)s, %(genre)s)"

    for band, genre in bands:
        dataBand = {
            'name': band,
            'genre': genre
        }

        cursor.execute(addBand, dataBand)
        print("\"{}\" successfully inserted!".format(band))

    uticon.__commitDB()
    cursor.close()

