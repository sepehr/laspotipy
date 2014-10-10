#Laspotipy

Migrates Last.fm playlists to Spotify where they can grow old!

###Note
Under active development, there will be bugs!

###Introduction
Laspotipy is a utility to migrate your (or others) Last.fm playlists to your
Spotify account where you can ACTUALLY play them, collaborate on them with
your friends, etc.  

Unlike similar tools/services Laspotipy needs no manual export of playlists,
no manual uploading, no manual nothing! Plus it implements much more precise
algorithm of finding Spotify tracks.  

It first conncects to Last.fm API and fetches the playlists found for the
specified user. No authorization is required and so you can add other user
playlists to your Spotify account.  

On the other hand, you need to authorize Laspotipy to access to your Spotify
account in order to be able to create playlists. After processing Last.fm playlists
and the tracks, you will be presented with a new page opened in your browser. You
need to login to Spotify service (if not logged in) and grant the required permissions
to Laspotipy. If granted, you will be redirected to a new URL (sepehr.github.io/laspotipy),
copy the whole URL and paste it to Laspotipy CLI application where it waits and waits
for you, the lord, to be blessed by the permissions.  

OK, no more bullshit. Have fun, and listen to good music :)  

P.S. Find my music profiles at:  
http://last.fm/user/lajevardi  
http://play.spotify.com/user/sepehrlajevardi  

###Usage
`python laspotipy.py LASTFM_USERNAME SPOTIFY_USERNAME`

###Requirements
- spotipy  
- lastfmapi  
- requests  

###Installation
    pip install requests spotipy lastfmapi
    git clone https://github.com/sepehr/laspotipy.git
    chmod +x ./laspotipy/laspotipy.py

###TODOs
- Improve search algorithm  
- Wrap each endpoint logic as classes  
- Provide verbosity CLI options  
- Provide the option to save playlists to file  
- Provide the option to read Last.fm playlists to file  
- Provide the option to read laspotipy error logs and retry creating the Spotify playlist  
- Provide option to create PRIVATE Spotify playlists  
- Handle HTTP errors, be graceful  
- Check for existing playlists, sync!  
- Restructure, more abstraction, cleanup!  
- Add license info, copyright, etc.  
- Write installation instructions, and requirements  
- Ability to migrate user favorite tracks  
- Interactive mode  
