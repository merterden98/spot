import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os
import types

#1295709267


class Playlist():

    def __init__(self, user_id=None, playlist_id=None, playlist_name="Does Not Exist", tracks=[], spotipy=None):
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.tracks = tracks
        self.s = spotipy

    def __str__(self):
        return "Playlist Object\nUser Id {}\nPlaylist Id {}\nPlaylist Name {}".format(self.user_id,\
        self.playlist_id, self.playlist_name)

    def add_tracks(self, tracks):
        #track is either track id, url or uri
        ##TODO Update self.tracks
        return self.s.user_playlist_add_tracks(self.user_id, self.playlist_id, tracks)    

    def replace_tracks(self, tracks):
        ##TODO Update self.tracks
        return self.s.user_playlist_replace_tracks(self.user_id, self.playlist_id, tracks)

    def remove_tracks(self, tracks):
        ##TODO Update self.tracks
        return self.s.user_playlist_remove_all_occurences_of_tracks(self.user_id, self.playlist_id, tracks)

    





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

    def __str__(self):
        return "Spot Object: \nUser: {}\n".format(self.username) +\
        "Scope {}\n".format(self.scope) +\
        "Token {}\n".format(self.token)
    def __repr__(self):
        return "Spot Object: \nUser: {}\n".format(self.username) +\
        "Scope {}\n".format(self.scope) +\
        "Token {}\n".format(self.token)

    #Parses Through returned JSON to add to myPlaylist info Dict
    def my_playlists(self, **kwargs):
        playlists = self.sp.current_user_playlists()
        l = []
        for items in playlists['items']:
           # info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sp.user_playlist_tracks(id, items['id'])
            songs = []
            totalS = items['tracks']['total']
            pprint.pprint(items)
           #pl break
            for i in range(0,totalS,50):

                for song in tracks['items']:
                    songs.append((song['track']['name'], song['track']['id']))
                
                if i % 50 == 0:
                    tracks = self.sp.user_playlist_tracks(id, items['id'], offset=i)


            pl = Playlist(id, items['id'], items['name'], songs, self.sp)
            l.append(pl)
        self.info["myPlaylists"] = l

    def user_playlists(self, **kwargs):
        #assert('user' in kwargs == False)
        playlists = self.sp.user_playlists(user=kwargs['user'])
        l = []
        for items in playlists['items']:
            #info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sp.user_playlist_tracks(id, items['id'])
            songs = []
            totalS = items['tracks']['total']
            
            for i in range(0,totalS,50):

                for song in tracks['items']:
                    if song['track'] is None:
                        pass
                    else:
                        songs.append((song['track']['name'], song['track']['id']))                
                
                if i % 50 == 0:
                    tracks = self.sp.user_playlist_tracks(id, items['id'], offset=i)

            pl = Playlist(id, items['id'], items['name'], self.sp)
            l.append(pl)
        self.info[kwargs['user'] + "Playlist"] = l
        

    def get_myplaylist(self, *args, **kwargs):
        
        playlist = []                                                          

        if len(args) == 0:
            try: 
                for pl in self.info["myPlaylists"]:
                    playlist.append(pl)
                return playlist
            except:
                print("Playlist Instance Does not Exist")
        
        else:
            argl = [v for v in args]
            for pl in self.info["myPlaylists"]:
                if pl.playlist_id in argl or pl.playlist_name in argl:
                    playlist.append(pl)
                else:
                    pass
            return playlist


    def get_userplaylist(self, *args, **kwargs):
        
        playlist = []

        if len(args) == 0:
            try: 
                for pl in self.info[kwargs['user'] + "Playlist"]:
                    playlist.append(pl)
                return playlist
            except:
                try:
                    print("{}'s Playlist Does Not Exist".format(kwargs['user']))
                except:
                    print("User Not Specified")
        else:
            argl = [v for v in args]
            for pl in self.info[kwargs['user'] + "Playlist"]:
                if pl.playlist_id in argl or pl.playlist_name in argl:
                    playlist.append(pl)
                else:
                    pass
            return playlist

#    def create_playlist(self, name, user=self.username, public=True, description):
#        pass




def splicename(uri):
        concaturi = uri[13:]
        i = 0
        while concaturi[i] != ':':
            i += 1
        concaturi = concaturi[:i]
        return concaturi
        

s = Spot("1295709267")
        
        
    