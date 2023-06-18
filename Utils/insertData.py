import Entities.Artists.artistsData as artdat
import Entities.Albums.albumsData as albdat
import Entities.Users.usersData as usedat


def insertDataInDB():
    """
        Inserts data into the database.

    """

    # insert artists in the database
    artdat.insertArtists()
    # insert albums in the database
    albdat.insertAlbums()

    # ask the user if he wants to use random user data
    userinput = input("\nDo you want random user data? (Yes / No):\n")

    if userinput.lower() == 'yes':
        # if the answer is yes the user is asked how many users he wants to be created
        howMany = int(input("How many randomly generated users do you want?\n"))

        # Create the specified number of random users
        print("Creating {} random users...".format(howMany))
        usedat.insertRandomUsers(howMany)

        # Insert random user likes
        usedat.insertRandomUserLikes(howMany)

        # Insert user ownership information
        usedat.insertUserOwnsAlbum()

