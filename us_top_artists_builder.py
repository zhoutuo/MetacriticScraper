__author__ = 'zhoutuoyang'
import os
import json
import last_fm_top_artists

"""
    This script will build a huge JSON file for top 500 artists in United Artists.
    The artists are sorted by their popularity
    Each entry comes with corresponding top albums, mbid, name
    Each album comes with title, mbid, release date
"""

data_dir = './data/'


def dataDirCheck():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def writeArtistJSON(artist):
    if 'name' not in artist:
        print "illegal artist object without a name"
        return
    filename = artist['name'] + '.json'
    try:
        with open(os.path.join(data_dir, filename), 'w+') as f:
            f.write(json.dumps(artist, indent=4))
    except IOError as e:
        print e.message
        print "failed to write file " + filename + ".json."


def buildArtistsJSON():
    # get all the artists
    artists = last_fm_top_artists.get_top_artists("UNITED STATES", 1) # by default it is 10 pages, each with 50 aritists
    for artist in artists:
        # for each artist, grab top albums
        artist_args = {}
        # arguments process
        if 'mbid' in artist and artist['mbid'] != '':
            artist_args['mbid'] = artist['mbid']
        elif 'name' in artist:
            artist_args['artist'] = artist['name']
        # get top albums
        top_albums = last_fm_top_artists.get_top_albums(**artist_args)
        top_albums_enhanced = []
        # for each album get release dates
        for album in top_albums:
            # process album arguments
            album_args = {}
            if 'mbid' in album and album['mbid'] != '':
                album_args['mbid'] = album['mbid']
            elif 'name' in album and 'name' in artist:
                album_args['artist'] = artist['name']
                album_args['album'] = album['name']
            album_info = last_fm_top_artists.get_album_info(**album_args)
            # if album info is not empty
            if album_info:
                top_albums_enhanced.append(album_info)
            # album info could be empty if something is missing
            # it is the case for many albums
            # we append the old album info which misses release date
            else:
                top_albums_enhanced.append(album)
        # assign top album back to the artist
        artist['topAlbums'] = top_albums_enhanced
        writeArtistJSON(artist)


# execuation section
if __name__ == '__main__':
    dataDirCheck()
    buildArtistsJSON()