import requests
import json

API_KEY = 'bd4b05c8898a3da836213a90623338b7'

# get information about the artists
def __getArtistsInfo(method, artist):
    """
        Get information about the artist from Last.fm API.

        Args:
            method (str): The Last.fm API method.
            artist (str): The name of the artist.

        Returns:
            dict: The response containing artist information.

    """
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload = {
        'method': 'artist.{}'.format(method),
        'artist': artist,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = json.loads(requests.get(url, params=payload).text)
    return response

# get the genre of the artist
def getArtistsGenre(artist):
    """
        Get the genre of the artist.

        Args:
            artist (str): The name of the artist.

        Returns:
            str: The genre of the artist.

    """
    genre = __getArtistsInfo('getInfo', artist)['artist']['tags']['tag'][0]['name']

    return genre

# get the top artists and their genres
def __getTopArtists(howMany):
    """
        Get the top artists and their genres from Last.fm API.

        Args:
            howMany (int): The number of top artists to retrieve.

        Returns:
            list: A list of dictionaries containing the name and genre of each top artist.

    """
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload = {
        'method': 'chart.getTopArtists',
        'api_key': API_KEY,
        'format': 'json'
    }

    response = json.loads(requests.get(url, params=payload).text)

    topArtists = []

    for i in range(0, howMany):
        name = response['artists']['artist'][i]['name']
        genre = getArtistsGenre(name)
        topArtists.append({'name': name, 'genre': genre})

    return topArtists

# get the top album of an artist
def getTopAlbum(artist):
    """
        Get the top album of an artist from Last.fm API.

        Args:
            artist (str): The name of the artist.

        Returns:
            str: The title of the top album.

    """
    info = __getArtistsInfo('getTopAlbums', artist)

    return info['topalbums']['album'][0]['name']

