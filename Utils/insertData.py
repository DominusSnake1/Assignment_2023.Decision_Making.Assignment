import random
import Utils.connection as uticon


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

    bands = ['Moderat', 'Tale Of Us', 'Artic Monkeys', 'The Weeknd', '', '']

    addBand = "INSERT INTO bands (name, genre) VALUES (%(name)s, %(genre)s)"




