from spotauth import SpotAuth
import requests
import json

class SpotBack():

    def __init__(self, clientid=None, clientsecret=None, redirect=None):
        self.token = SpotAuth(clientid, clientsecret, redirect)._gettoken()
        self.authheader = {"Authorization": "Bearer " + self.token}
    def get_my_playlist(self):
        
        header = {"Authorization": "Bearer " + self.token}
        res = requests.get('https://api.spotify.com/v1/me/playlists', headers=header)
        return res.json()

    def get_tracks(self, user_id, playlist_id, offset=None):
        url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists/' + playlist_id + '/tracks'
        
        if offset:
            ofstr = '?offset=' + str(offset)
            #packet = json.dumps(packet)
            url = url + ofstr
            header = self.authheader
            #header['Content-Type'] = 'application/json'
            
            res = requests.get(url, headers=header)
            print(res)
            return requests.get(url, headers=header).json()
        else:
            return requests.get(url, headers=self.authheader).json()



#s = SpotBack(clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
