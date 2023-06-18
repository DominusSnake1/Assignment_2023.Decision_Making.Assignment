import DBCreation.connection as dbcon
import Utils.checkers as chk
import random
import Utils.statistics as stats


def insertRandomUsers(users):
    cursor = dbcon.__getDBCursor()

    usernames = [
        'Nancy', 'George', 'Freddie', 'Maggie', 'Rick',
        'Negan', 'Michonne', 'Lillian', 'Andrea', 'Daryl',
        'Natalie', 'Carl', 'Glenn', 'Lester', 'Lori',
        'George', 'Alex', 'James', 'Nick', 'John'
    ]

    addUser = "INSERT INTO users (username, age, gender) VALUES (%(username)s, %(age)s, %(gender)s)"

    for user in range(0, users):
        username = random.choice(usernames)

        dataUser = {
            'username': username,
            'age': random.randint(18, 65),
            'gender': random.choice(['M', 'F'])
        }

        cursor.execute(addUser, dataUser)
        print("[User] \"{}\" inserted.".format(username))

    chk.checkDataIssues('users')
    dbcon.__commitDB()
    cursor.close()


def insertRandomUserLikes(num_likes):
    cursor = dbcon.__getDBCursor()

    cursor.execute("SELECT user_id FROM Users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT artist_id FROM artists")
    artist_ids = [row[0] for row in cursor.fetchall()]

    addUserLikes = "INSERT INTO userLikes (user_id, artist_id) VALUES (%(user_id)s, %(artist_id)s)"

    for _ in range(num_likes):
        user_id = random.choice(user_ids)
        artist_id = random.choice(artist_ids)

        dataUserLikes = {
            'user_id': user_id,
            'artist_id': artist_id
        }

        cursor.execute(addUserLikes, dataUserLikes)
        print("[User] with ID \"{}\" likes [Artist] with ID \"{}\".".format(user_id, artist_id))

    chk.checkDataIssues('userLikes')
    dbcon.__commitDB()
    cursor.close()

    for id in artist_ids:
        stats.insertStatistics(id)


def insertUserOwnsAlbum():
    cursor = dbcon.__getDBCursor()

    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT album_id FROM albums")
    album_ids = [row[0] for row in cursor.fetchall()]

    addOwnership = "INSERT INTO userOwnsAlbum (user_id, album_id) VALUES (%(user_id)s, %(album_id)s)"

    for _ in range(len(user_ids)):
        user_id = random.choice(user_ids)
        album_id = random.choice(album_ids)

        dataOwnership = {
            'user_id': user_id,
            'album_id': album_id
        }

        cursor.execute(addOwnership, dataOwnership)
        print("[User] with ID \"{}\" owns [Album] with ID \"{}\".".format(user_id, album_id))

    chk.checkDataIssues('userOwnsAlbum')
    dbcon.__commitDB()
    cursor.close()