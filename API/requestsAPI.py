import requests
import json

API_KEY = 'bd4b05c8898a3da836213a90623338b7'


def __getArtistsInfo(method, artist):
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload = {
        'method': 'artist.{}'.format(method),
        'artist': artist,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = json.loads(requests.get(url, params=payload).text)
    return response


def getArtistsGenre(artist):
    genre = __getArtistsInfo('getInfo', artist)['artist']['tags']['tag'][0]['name']

    return genre


def __getTopArtists(howMany):
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


def getTopAlbum(artist):
    info = __getArtistsInfo('getTopAlbums', artist)

    return info['topalbums']['album'][0]['name']

