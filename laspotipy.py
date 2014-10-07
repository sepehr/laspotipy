#!/usr/bin/python
#
# Usage:
# laspotipy.py LASTFM_USERNAME SPOTIFY_USERNAME

import spotipy
import lastfmapi
import csv
import sys
import pprint

LASTFM_API_KEY = 'f181e975265edd51e83182def6b5958a'

def spotify_uri(artist, track, album = False):
    """
    Returns spotify uri by artist and track names using Spotify Web API.
    """
    spotify  = spotipy.Spotify()

    if album:
        query = 'artist:%s album:%s %s' % (artist, album, track)
    else:
        query = 'artist:%s %s' % (artist, track)

    response = spotify.search(q = query, type = 'track', offset = 0, limit = 1)

    if len(response['tracks']['items']) > 0:
        return response['tracks']['items'][0]['uri']

    return False


# def spotify_playlist(filepath, delimiter = '\t'):
#     """
#     Gets a text file and prints out a Spotify playlist to copy and paste.
#     """
#     reader = csv.reader(open(filepath), delimiter = delimiter)

#     for line in reader:
#         # Skip file header
#         if line[0].lower() == 'track':
#             continue

#         track  = line[0]
#         artist = line[1]
#         uri    = spotify_uri(artist, track)

#         if uri:
#             print uri
#         else:
#             print 'NOT FOUND: %s - %s' % (track, artist)


def lastfm_playlists(username):
    """
    Return an array of Last.fm playlist IDs/Titles belong to the passed username.
    """
    lastfm    = lastfmapi.LastFmApi(LASTFM_API_KEY)
    response  = lastfm.user_getplaylists(user = username)

    if not response or len(response['playlists']['playlist']) < 1:
        return False

    playlists = []

    for playlist in response['playlists']['playlist']:
        playlists.extend([{
            'id':    playlist['id'],
            'title': playlist['title']
        }])

    return playlists


def lastfm_playlist_tracks(pl_id):
    """
    Gets playlist tracks using by Last.fm playlist ID
    """
    lastfm    = lastfmapi.LastFmApi(LASTFM_API_KEY)
    response = lastfm.playlist_fetch(playlistURL = 'lastfm://playlist/' + pl_id)

    if not response or len(response['playlist']['trackList']['track']) < 1:
        return False

    tracks = []

    for track in response['playlist']['trackList']['track']:
        tracks.extend([{
            'title':  track['title'],
            'album':  track['album'],
            'artist': track['creator'],
        }])

    return tracks


def main():
    # Check args
    if len(sys.argv) < 3:
        sys.exit('\nUSAGE: laspotipy.py LASTFM_USERNAME SPOTIFY_USERNAME\n')
    else:
        lastfm_username  = sys.argv[1]
        spotify_username = sys.argv[2]

    # Fetch user playlists
    playlists = lastfm_playlists(lastfm_username)

    if not playlists:
        sys.exit('ERROR: Could not fetch last.fm playlists, is there any?')

    print '\nFound %d playlists for %s.' % (len(playlists), lastfm_username)

    # Processing each playlist
    for pl in playlists:
        print '\nProcessing "%s"...' % pl['title']

        tracks = lastfm_playlist_tracks(pl['id'])

        if not tracks:
            print '\tERROR: Could not fetch tracks for this playlist, is there any? Skipping...'
            continue

        print '\tFound %d tracks in the playlist:' % len(tracks)

        failed = 0
        spotify_playlist = {
            'title':  pl['title'],
            'tracks': [],
            'failed': []
        }

        # Processing each track
        for track in tracks:
            uri = spotify_uri(track['artist'], track['title'], track['album'])
            print '\t\t"%s - %s"' % (track['artist'][:40], track['title'][:40])

            if uri:
                print '\t\t[FOUND] %s\n' % uri
                spotify_playlist['tracks'].extend([uri])

            else:
                print '\t\t[FAILED]\n'
                spotify_playlist['failed'].extend(['%s - %s - %s' % (track['artist'], track['album'], track['title'])])
                failed += 1

        print '\t%d tracks failed to be found on Spotify. Failures will be logged to file.' % failed

        # ---------------------------------------------------------------------
        # Printing Spotify playlist to file
        fp = file('/Users/Sepehr/Downloads/%s.txt' % spotify_playlist['title'], 'w+')
        fp.write('\n'.join(spotify_playlist['tracks']))

        # Print failures to file as well
        fp = file('/Users/Sepehr/Downloads/%s.failed.txt' % spotify_playlist['title'], 'w+')
        fp.write('\n'.join(spotify_playlist['failed']))


if __name__ == '__main__':
    main()
