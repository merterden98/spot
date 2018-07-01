import pprint
import json
import os
import types
import spotback



class Playlist():

    def __init__(self, user_id=None, playlist_id=None, playlist_name="Default", tracks=[], sb=None):
       
        assert type(sb) ==type(spotback.SpotBack()), "Need SpotBack Object"
        assert type(user_id) != type(None), "Need User ID"


        self.user_id = user_id
        self.playlist_name = playlist_name
        self.tracks = tracks
        self.s = sb
        #Checks If We Have to Create A new Playlist
        self.playlist_id = str(create_playlist(self.user_id, playlist_id, sb, playlist_name))


    def __str__(self):
        return "Playlist Object\nUser Id {}\nPlaylist Id {}\nPlaylist Name {}".format(self.user_id,\
        self.playlist_id, self.playlist_name)

    def add_tracks(self, tracks):

        if type(tracks) == type('str'):
            t = tracks
            if (len(tracks) == 22):
                pass
            
            if (len(tracks) == 36):
                t = tracks[14:]
            
            
            track = self.s.single_track(t)
            self.tracks.append((track['name'],track['id']))
            self.s.add_track_user_playlists(self.user_id, self.playlist_id, track['id'])


        elif isinstance(tracks, Song):
            track = self.s.single_track(tracks.id)
            self.tracks.append((track['name'],track['id']))
            self.more_info_tracks.append(tracks)
            self.s.add_track_user_playlists(self.user_id, self.playlist_id, track['id'])
            
            

        else:
            pl = []
            for track in tracks:
                
                if isinstance(track, Song):
                    t = self.s.single_track(track.id)
                    self.tracks.append((t['name'],t['id']))
                    self.more_info_tracks.append(track)
                    self.s.add_track_user_playlists(self.user_id, self.playlist_id, t['id'])
                
                else:
                    t = track


                    if (len(t) == 22):
                        pass
            
                    if (len(t) == 36):
                        t = tracks[14:]
    
                    track = self.s.single_track(t)
                    pl.append((track['name'],track['id']))
                    self.s.add_track_user_playlists(self.user_id, self.playlist_id, track['id'])
                self.tracks = self.tracks + pl
            

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


    def change_details(self, description=None, public=None, name=None):

        kwargs = {}

        if type(description) != type(None):
            kwargs['description'] = description
        
        if type(public) != type(None):
            kwargs['public'] = public
        
        if type(name) != type(None):
            kwargs['name'] = name

        self.s.change_playlist_details(self.user_id, self.playlist_id, **kwargs)
        

    def more_track_info(self):

        tmp = []

        for track in self.tracks:
            s = Song(track[1], self.s, track[0])
            tmp.append(s)

        self.more_info_tracks = tmp   

        

def create_playlist(user_id, playlist_id, s, playlist_name):

    if type(playlist_id) == type(None):
        return s.create_playlist(user_id, playlist_name)
        
    else:
        return playlist_id
    

class Song():

    def __init__(self, id, sb, name):
        self.id = id
        self.sb = sb
        self.name = name
        self.get_details()

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}".format(self.name)


    class Features():

        def __init__(self, id, sb):
            self.features = sb.get_track_features(id)
            self.features.pop('id')
            self.features.pop('track_href')
            self.features.pop('uri')
            self.features.pop('analysis_url')
            self.features.pop('type')
        
        def __getitem__(self, key):
            return self.features[key]

        def keys(self):
            return self.features.keys()
        
        def values(self):
            return self.features.values()

        def items(self):
            return self.features.items()

        
        def __repr__(self):
            pprint.pprint(self.features)
            return ""
    
    class Analysis():

        def __init__(self, id, sb):
            self.audio_analysis = sb.get_audio_analysis(id)
            self.audio_analysis.pop('meta')

        def __getitem__(self, key):
            return self.audio_analysis[key]

        def keys(self):
            return self.audio_analysis.keys()
        
        def values(self):
            return self.audio_analysis.values()

        def items(self):
            return self.audio_analysis.items()

        def __repr__(self):
            pprint.pprint(self.audio_analysis)
            return ""
    
    def get_details(self):

        self.features = self.Features(self.id, self.sb)
        
        self.audio_analysis = self.Analysis(self.id, self.sb)

    




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


    def get_track(self, tracks):
        
        if type(tracks) == type('str'):
            t = tracks
            if (len(tracks) == 22):
                pass
            
            if (len(tracks) == 36):
                t = tracks[14:]
            
            
            track = self.sb.single_track(t)
            
            s = Song(track['id'], self.sb, track['name'])
            return s
        
        else:
            pl = []
            for track in tracks:
                t = track
                if (len(t) == 22):
                    pass
            
                if (len(t) == 36):
                    t = tracks[14:]
    
                track = self.sb.single_track(t)
                s = Song(track['id'], self.sb, track['name'])
                pl.append(s)

            
            return pl

def splicename(uri):
        concaturi = uri[13:]
        i = 0
        while concaturi[i] != ':':
            i += 1
        concaturi = concaturi[:i]
        return concaturi
        

s = Spot("1295709267", clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
s.my_playlists()
#sb = s.sb

song = s.get_track('2gfBV96ou2PCp0VhvddOVQ')
pl = s.get_myplaylists()
p = pl[1]
#p.add_tracks('6JzzI3YxHCcjZ7MCQS2YS1')
#p.remove_tracks('6JzzI3YxHCcjZ7MCQS2YS1')        
        
#p = Playlist(user_id="1295709267", sb=sb, playlist_name="Testing Details")


# for i in range(100):
#     p.add_tracks('2gfBV96ou2PCp0VhvddOVQ')