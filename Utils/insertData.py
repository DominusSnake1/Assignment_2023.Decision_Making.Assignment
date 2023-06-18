import random
import Utils.connection as uticon
import API.requestsAPI as api
import Utils.checkers as chk


def insertDataInDB():
    insertArtists()
    insertAlbums()

    userinput = input("\nDo you want random user data? (Yes / No):\n")

    if userinput.lower() == 'yes':
        howMany = int(input("How many randomly generated users do you want?\n"))

        print("Creating {} random users...".format(howMany))
        insertRandomUsers(howMany)
        insertRandomUserLikes(howMany)
        insertUserOwnsAlbum()


def insertArtists():
    cursor = uticon.__getDBCursor()

    artists = api.__getTopArtists(10)

    addArtist = "INSERT INTO artists (name, genre) VALUES (%(name)s, %(genre)s)"

    for artist in artists:
        name = artist['name']
        genre = artist['genre']

        dataArtist = {
            'name': name,
            'genre': genre
        }

        insertGenre(genre)

        try:
            cursor.execute(addArtist, dataArtist)
        except uticon.__getSQLConError() as err:
            if err.errno == uticon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Artist] \"{}\" already exists.".format(name))
        else:
            print("[Artist] \"{}\" successfully inserted!".format(name))

    chk.checkDataIssues('artists')
    uticon.__commitDB()
    cursor.close()


def insertGenre(genre):
    cursor = uticon.__getDBCursor()

    addGenre = "INSERT INTO genres (genre) VALUES (%(genre)s)"

    dataGenre = {
        'genre': genre
    }

    try:
        cursor.execute(addGenre, dataGenre)
    except uticon.__getSQLConError() as err:
        if err.errno == uticon.__getSQLConErrorcode().ER_DUP_ENTRY:
            print("[Genre] \"{}\" already exists.".format(genre))
        else:
            print(err.msg)
    else:
        print("[Genre] \"{}\" successfully inserted!".format(genre))

    chk.checkDataIssues('genres')
    uticon.__commitDB()
    cursor.close()


def insertAlbums():
    cursor = uticon.__getDBCursor()

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
        except uticon.__getSQLConError() as err:
            if err.errno == uticon.__getSQLConErrorcode().ER_DUP_ENTRY:
                print("[Album] \"{}\" by \"{}\" already exists.".format(album, artist))
        else:
            print("[Album] \"{}\" by \"{}\" inserted.".format(album, artist))

    chk.checkDataIssues('albums')
    uticon.__commitDB()
    cursor.close()


def insertRandomUsers(users):
    cursor = uticon.__getDBCursor()

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
    uticon.__commitDB()
    cursor.close()


def insertRandomUserLikes(num_likes):
    cursor = uticon.__getDBCursor()

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
    uticon.__commitDB()
    cursor.close()

    for id in artist_ids:
        insertStatistics(id)


def insertStatistics(artist_id):
    cursor = uticon.__getDBCursor()

    getArtistsFans = 'SELECT COUNT(user_id) FROM userlikes WHERE artist_id = %(artist_id)s'

    cursor.execute(getArtistsFans, {'artist_id': artist_id})
    artists_fans = cursor.fetchone()

    getGenreID = """
        SELECT genres.genre_id
            FROM genres
            JOIN artists ON genres.genre = artists.genre
            WHERE artists.artist_id = {}
    """.format(artist_id)

    cursor.execute(getGenreID, {'artist_id': artist_id})
    genreid = cursor.fetchone()[0]

    getGenreFans = """
            SELECT COUNT(userlikes.user_id) AS genre_fans
                FROM genres
                JOIN artists ON genres.genre = artists.genre
                JOIN userlikes ON artists.artist_id = userlikes.artist_id
                WHERE genres.genre_id = {}
                GROUP BY genres.genre
    """.format(genreid)

    cursor.execute(getGenreFans, {'genre_id': genreid})
    genreFans = cursor.fetchone()

    insertStats = 'INSERT INTO stats (artist_id, artists_fans, genre_id, genres_fans) VALUES (%(artist_id)s, %(artists_fans)s, %(genre_id)s, %(genres_fans)s) ON DUPLICATE KEY UPDATE artists_fans = artists_fans + 1, genres_fans = genres_fans + 1'

    statsData = {
        'artist_id': artist_id,
        'artists_fans': artists_fans[0],
        'genre_id': genreid,
        'genres_fans': genreFans[0]
    }

    try:
        cursor.execute(insertStats, statsData)
    except uticon.__getSQLConError() as err:
        if err.errno == uticon.__getSQLConErrorcode().ER_DUP_ENTRY:
            print("[Genre] with an ID \"{}\" already exists.".format(statsData['genre_id']))
    else:
        print("[Artist] with an ID \"{}\" has {} fans.".format(statsData['artist_id'], statsData['artists_fans']))
        print("[Genre] with an ID \"{}\" has {} fans.".format(statsData['genre_id'], statsData['genres_fans']))

    chk.checkDataIssues('stats')
    uticon.__commitDB()
    cursor.close()


def insertUserOwnsAlbum():
    cursor = uticon.__getDBCursor()

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
    uticon.__commitDB()
    cursor.close()
