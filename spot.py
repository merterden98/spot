import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os

#1295709267


class Spot():

    def __init__(self, username):
        self.username = username
        self.scope = 'user-read-private user-modify-playback-state'+\
            ' user-read-recently-played user-read-playback-state'+\
            ' playlist-read-private playlist-modify-public'+\
            ' user-read-currently-playing user-top-read playlist-modify-private '+\
            ' playlist-read-collaborative'
        
        self.token = util.prompt_for_user_token(self.username, self.scope,client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33', redirect_uri='https://example.com/callback/')
        self.sp = spotipy.Spotify(auth=self.token)
        self.info = {}

    def __repr__(self):
        return "Spot Object: \nUser: {}\n".format(self.username) +\
        "Scope {}\n".format(self.scope) +\
        "Token {}\n".format(self.token)

    def my_playlists(self, **kwargs):
        playlists = self.sp.current_user_playlists()
        for items in playlists['items']:
            info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            #tracks = self.sp.user_playlist_tracks()
                
                 
    def get_info(self, **kwargs):
        print(self.info['myplaylists'])



def splicename(uri):
        concaturi = uri[13:]
        i = 0
        while concaturi[i] != ':':
            i += 1
        concaturi = concaturi[:i]
        return concaturi
        

s = Spot("1295709267")
        
        
    