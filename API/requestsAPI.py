import requests
import json


def lastfm_Get(payload):
    # define headers and URL
    headers = {'user-agent': 'DeciMak'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = 'bd4b05c8898a3da836213a90623338b7'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


r = lastfm_Get({'method': 'chart.gettopartists'})
jprint(r.json())
jprint(r.json()['artists']['@attr'])
print(r.status_code)
