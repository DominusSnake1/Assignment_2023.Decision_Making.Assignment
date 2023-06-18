import Entities.Artists.artistsData as artdat
import Entities.Albums.albumsData as albdat
import Entities.Users.usersData as usedat


def insertDataInDB():
    artdat.insertArtists()
    albdat.insertAlbums()

    userinput = input("\nDo you want random user data? (Yes / No):\n")

    if userinput.lower() == 'yes':
        howMany = int(input("How many randomly generated users do you want?\n"))

        print("Creating {} random users...".format(howMany))
        usedat.insertRandomUsers(howMany)
        usedat.insertRandomUserLikes(howMany)
        usedat.insertUserOwnsAlbum()

