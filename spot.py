import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os
import types

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

    #Parses Through returned JSON to add to myPlaylist info Dict
    def my_playlists(self, **kwargs):
        playlists = self.sp.current_user_playlists()
        l = []
        for items in playlists['items']:
            info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sp.user_playlist_tracks(id, items['id'])
            songs = []
            for song in tracks['items']:
                songs.append((song['track']['name'], song['track']['id']))
            l.append({info : songs})
        self.info["myPlaylists"] = l

    def user_playlists(self, **kwargs):
        #assert('user' in kwargs == False)
        playlists = self.sp.user_playlists(user=kwargs['user'])
        l = []
        for items in playlists['items']:
            info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sp.user_playlist_tracks(id, items['id'])
            songs = []
            for song in tracks['items']:
                if song['track'] is None:
                    pass
                else:
                    songs.append((song['track']['name'], song['track']['id']))
            l.append({info : songs})
        print(kwargs['user'] + "Playlist")
        self.info[kwargs['user'] + "Playlist"] = l
        


    def get_myplaylist(self, *args, **kwargs):
        
        playlist = []

        if len(args) == 0:
            try: 
                for pl in self.info["myPlaylists"]:
                    dtup = [*pl]
                    dtup = dtup[0]
                    dtup = [dtup[i] for i in range(len(dtup))]
                    if  'uri' not in kwargs or kwargs['uri'] == False:
                        del dtup[2]
                    if 'id' not in kwargs or kwargs['id'] == False:
                        del dtup[1]
                    tmpl = [l for l in pl.values()]
                    playlist.append([dtup, tmpl])
                return playlist
            except:
                print("Playlist Instance Does not Exist")
        
        else:
            argl = [v for v in args]
            print(argl)
            for pl in self.info["myPlaylists"]:
                dtup = [*pl]
                dtup = dtup[0]
                dtup = [dtup[i] for i in range(len(dtup))]
                if dtup[0] in argl or dtup[1] in argl:
                    if  'uri' not in kwargs or kwargs['uri'] == False:
                        del dtup[2]
                    if 'id' not in kwargs or kwargs['id'] == False:
                        del dtup[1]
                    tmpl = [l for l in pl.values()]
                    playlist.append([dtup, tmpl])
                else:
                    pass
            return playlist


    def get_userplaylist(self, *args, **kwargs):
        
        playlist = []

        if len(args) == 0:
            try: 
                for pl in self.info[kwargs['user'] + "Playlist"]:
                    dtup = [*pl]
                    dtup = dtup[0]
                    dtup = [dtup[i] for i in range(len(dtup))]
                    if  'uri' not in kwargs or kwargs['uri'] == False:
                        del dtup[2]
                    if 'id' not in kwargs or kwargs['id'] == False:
                        del dtup[1]
                    tmpl = [l for l in pl.values()]
                    playlist.append([dtup, tmpl])
                return playlist
            except:
                try:
                    print("{}'s Playlist Does Not Exist".format(kwargs['user']))
                except:
                    print("User Not Specified")
        else:
            argl = [v for v in args]
            print(argl)
            for pl in self.info[kwargs['user'] + "Playlist"]:
                dtup = [*pl]
                dtup = dtup[0]
                dtup = [dtup[i] for i in range(len(dtup))]
                if dtup[0] in argl or dtup[1] in argl:
                    if  'uri' not in kwargs or kwargs['uri'] == False:
                        del dtup[2]
                    if 'id' not in kwargs or kwargs['id'] == False:
                        del dtup[1]
                    tmpl = [l for l in pl.values()]
                    playlist.append([dtup, tmpl])
                else:
                    pass
            return playlist


def splicename(uri):
        concaturi = uri[13:]
        i = 0
        while concaturi[i] != ':':
            i += 1
        concaturi = concaturi[:i]
        return concaturi
        

s = Spot("1295709267")
        
        
    