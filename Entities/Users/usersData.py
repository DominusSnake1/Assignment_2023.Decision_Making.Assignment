import DBCreation.connection as dbcon
import Utils.checkers as chk
import random
import Utils.statistics as stats

# function which inserts random users in the database
def insertRandomUsers(users):
    """
        Inserts randomly generated user data into the database.

        Args:
            users (int): The number of randomly generated users to be inserted.

    """
    cursor = dbcon.__getDBCursor()

    # list of pre-set usernames
    usernames = [
        'Nancy', 'George', 'Freddie', 'Maggie', 'Rick',
        'Negan', 'Michonne', 'Lillian', 'Andrea', 'Daryl',
        'Natalie', 'Carl', 'Glenn', 'Lester', 'Lori',
        'George', 'Alex', 'James', 'Nick', 'John'
    ]

    # sql code to insert a user in the users table
    addUser = "INSERT INTO users (username, age, gender) VALUES (%(username)s, %(age)s, %(gender)s)"

    # generate random user data
    for user in range(0, users):
        username = random.choice(usernames)

        dataUser = {
            'username': username,
            'age': random.randint(18, 65),
            'gender': random.choice(['M', 'F'])
        }

        cursor.execute(addUser, dataUser)
        print("[User] \"{}\" inserted.".format(username))

    # check for any data issues in the users table
    chk.checkDataIssues('users')
    dbcon.__commitDB()
    cursor.close()

# function which assigns randomly user likes to artists
def insertRandomUserLikes(num_likes):
    """
        Assigns random user likes to artists in the database.

        Args:
            num_likes (int): The number of random user likes to be assigned.

    """
    cursor = dbcon.__getDBCursor()

    cursor.execute("SELECT user_id FROM Users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT artist_id FROM artists")
    artist_ids = [row[0] for row in cursor.fetchall()]

    # sql code to insert the user likes to the userLikes tables
    addUserLikes = "INSERT INTO userLikes (user_id, artist_id) VALUES (%(user_id)s, %(artist_id)s)"

    for _ in range(num_likes):

        # Choose a random user ID and artist ID
        user_id = random.choice(user_ids)
        artist_id = random.choice(artist_ids)

        # Prepare the data for inserting user likes
        dataUserLikes = {
            'user_id': user_id,
            'artist_id': artist_id
        }
        # Execute the SQL query to insert user likes
        cursor.execute(addUserLikes, dataUserLikes)

        print("[User] with ID \"{}\" likes [Artist] with ID \"{}\".".format(user_id, artist_id))

    # Check for any data issues in the userLikes table
    chk.checkDataIssues('userLikes')
    dbcon.__commitDB()
    cursor.close()

    # Insert statistics for the artists
    for id in artist_ids:
        stats.insertStatistics(id)

# function which randomly assigns albums ownership to users
def insertUserOwnsAlbum():
    """
        Randomly assigns album ownership to users in the database.
    """
    cursor = dbcon.__getDBCursor()

    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT album_id FROM albums")
    album_ids = [row[0] for row in cursor.fetchall()]

    # sql code to insert user ownership of albums to the userOwnsAlbum table
    addOwnership = "INSERT INTO userOwnsAlbum (user_id, album_id) VALUES (%(user_id)s, %(album_id)s)"

    for _ in range(len(user_ids)):
        # select a user and an album randomly
        user_id = random.choice(user_ids)
        album_id = random.choice(album_ids)

        # prepare data to insert it to the table
        dataOwnership = {
            'user_id': user_id,
            'album_id': album_id
        }

        # insert the ownership data to the database
        cursor.execute(addOwnership, dataOwnership)
        print("[User] with ID \"{}\" owns [Album] with ID \"{}\".".format(user_id, album_id))

    # Check for any data issues in the userOwnsAlbum table
    chk.checkDataIssues('userOwnsAlbum')
    dbcon.__commitDB()
    cursor.close()