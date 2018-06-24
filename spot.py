import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os
import types
import spotback

#1295709267


class Playlist():

    def __init__(self, user_id=None, playlist_id=None, playlist_name="Does Not Exist", tracks=[], sb=None):
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.tracks = tracks
        self.s = sb

    def __str__(self):
        return "Playlist Object\nUser Id {}\nPlaylist Id {}\nPlaylist Name {}".format(self.user_id,\
        self.playlist_id, self.playlist_name)

    def add_tracks(self, tracks):
        #track is either track id
        ##TODO 


        if type(tracks) == type('str'):
            t = tracks
            if (len(tracks) == 22):
                pass
            
            if (len(tracks) == 36):
                t = tracks[14:]
               
            track = self.s.single_track(t)
            self.tracks.append((track['name'],track['id']))
            self.s.add_track_user_playlists(self.user_id, self.playlist_id, track['id'])

        else:
            pl = []
            for track in tracks:
                t = track
                if (len(t) == 22):
                    pass
            
                if (len(t) == 36):
                    t = tracks[14:]
    
                track = self.s.single_track(t)
                pl.append((track['name'],track['id']))
                self.s.add_track_user_playlists(self.user_id, self.playlist_id, track['id'])

            self.tracks = self.tracks + pl
            

    def replace_tracks(self, tracks):
        ##TODO Update self.tracks
        return self.s.user_playlist_replace_tracks(self.user_id, self.playlist_id, tracks)

    def remove_tracks(self, tracks):
        ##TODO Update self.tracks

        if type(tracks) == type('str'):
            for cur_tracks in self.tracks:
                if tracks == cur_tracks[1]:
                    self.s.remove_playlist_track(self.user_id,self.playlist_id,tracks)

        else:
            for cur_tracks in self.tracks:
                for rem_tracks in tracks:
                    if cur_tracks[1] == rem_tracks:
                         self.s.remove_playlist_track(self.user_id,self.playlist_id,rem_tracks)

    





class Spot():

    def __init__(self, username, clientid=None, clientsecret=None, redirect=None):
        self.username = username
        self.scope = 'user-read-private user-modify-playback-state'+\
            ' user-read-recently-played user-read-playback-state'+\
            ' playlist-read-private playlist-modify-public'+\
            ' user-read-currently-playing user-top-read playlist-modify-private '+\
            ' playlist-read-collaborative'
        
        #self.token = util.prompt_for_user_token(self.username, self.scope,client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33', redirect_uri='https://example.com/callback/')
        #self.sp = spotipy.Spotify(auth=self.token)
        self.sb = spotback.SpotBack(clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
        self.info = {}

    def __str__(self):
        return "Spot Object: \nUser: {}\n".format(self.username) +\
        "Scope {}\n".format(self.scope) +\
        "Token {}\n".format(self.token)
    def __repr__(self):
        return "Spot Object: \nUser: {}\n".format(self.username) +\
        "Scope {}\n".format(self.scope) +\
        "Token {}\n".format(self.token)


    """
        Requests Happen In The Form of Set and Get
        In Order for get_foo(x), foo(x) needs to be called
    """
    

    #Parses Through returned JSON to add to myPlaylist info Dict
    def my_playlists(self, **kwargs):
        playlists = self.sb.get_my_playlist()
        l = []

        for items in playlists['items']:
           # info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sb.get_tracks(id, items['id'])
            songs = []
            totalS = items['tracks']['total']
           #pl break
            for i in range(0,totalS,50):

                for song in tracks['items']:
                    songs.append((song['track']['name'], song['track']['id']))
                
                if i % 50 == 0:
                    tracks = self.sb.get_tracks(id, items['id'], offset=i)


            pl = Playlist(id, items['id'], items['name'], songs, self.sb)
            l.append(pl)
        self.info["myPlaylists"] = l

    #Parses Through returned JSON to add to a user info dict
    def user_playlists(self, user_id=None):
        #assert('user' in kwargs == False)
        playlists = self.sb.get_user_playlists(user_id)
        l = []
        for items in playlists['items']:
            #info = (items['name'], items['id'], items['uri'])
            id = splicename(items['uri'])
            tracks = self.sb.get_tracks(id, items['id'])
            songs = []
            totalS = items['tracks']['total']
            
            for i in range(0,totalS,50):

                for song in tracks['items']:
                    if song['track'] is None:
                        pass
                    else:
                        songs.append((song['track']['name'], song['track']['id']))                
                
                if i % 50 == 0:
                    tracks = self.sb.get_tracks(id, items['id'], offset=i)

            pl = Playlist(id, items['id'], items['name'], songs, self.sb)
            l.append(pl)
        self.info[user_id + "Playlist"] = l
        

    def get_myplaylists(self, *args, **kwargs):
        
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


    def get_userplaylists(self, *args, **kwargs):
        
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
        

s = Spot("1295709267", clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
s.my_playlists()
pl = s.get_myplaylists()
p = pl[1]
p.remove_tracks('6JzzI3YxHCcjZ7MCQS2YS1')        
        
    