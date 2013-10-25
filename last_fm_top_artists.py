__author__ = 'zhoutuoyang'
import json
import requests

last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
try:
    with open('last_fm_api_key.txt') as f:
        api_key = f.read()
except IOError:
    print "There is something wrong with api key file."
    exit()


def get_top_artists(country="UNITED STATES", pages=10):
    """
        Get top artists from a specific country, by default it is United States, using Last.fm API
        Pages argument specifies the front pages of top artists to be fetched, each page contains 50 artists
        If the page argument is over the real limit of page number, the function will stop automatically
        It returns a list of top artists, sorted by popularity, each entry has two properties,
        1. name of artist
        2. mbid, musicbrainz unique ID for the aritist
    """
    artists_container = []
    for page in range(pages):
        response = requests.get(last_fm_url, params={
            'api_key': api_key,
            'method': 'geo.getTopArtists',
            'country': country,
            'format': 'json',
            'page': page
        })
        top_artists = json.loads(response.text)
        artists = top_artists['topartists']['artist']
        attr = top_artists['topartists']['@attr']
        # check whether the current page is the page requested
        # e.g. if there are only 10 pages, when requested the 11th one,
        # Last.fm will still return 10th page
        if int(attr['page']) != page:
            break
        # put artists in the format needed
        # only name and mbid are necessary
        for artist in artists:
            artists_container.append({
                'name': artist['name'],
                'mbid': artist['mbid']
            })
    return artists_container


def get_top_albums(mbid):
    """
        Get top albums of an artist specifiy by the mbid (musicbrainz ID).
        The maxium number of albums returned will be less or equal to 10.
    """
    limit = 10
    album_container = []
    # request Last.fm by using mbid
    response = requests.get(last_fm_url, params={
        'api_key': api_key,
        'method': 'artist.getTopAlbums',
        'mbid': mbid,
        'format': 'json',
        'limit': limit
    })
    top_albums = json.loads(response.text)
    albums = top_albums['topalbums']['album']
    # generate albums with specific format
    # each entry with name and mbid
    for album in albums:
        album_container.append({
            'name': album['name'],
            'mbid': album['mbid']
        })
    return albums


def get_album_info(mbid):
    """
        Get album information bsaed on mbid from Last.fm
    """
    # request the album info
    response = requests.get(last_fm_url, params={
        'api_key': api_key,
        'method': 'album.getInfo',
        'mbid': mbid,
        'format': 'json',
    })
    # load text into dict
    album = json.loads(response.text)['album']
    album_trimed = {
        'name': album['name'],
        'mbid': album['mbid'],
        'releaseDate': album['releasedate']
    }
    ## load the tracks into album
    #album_trimed['tracks'] = [];
    return album_trimed
