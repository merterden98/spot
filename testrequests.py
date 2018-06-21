import requests
import json
import oauth2 as oauth
import six
import six.moves.urllib.parse as urllibparse
import webbrowser
import base64
import urllib.request

# RURI = 'https://example.com/callback/'

# CLIENTID = 'abdd03cd5c1c4dc79d15cbf50b0641ad'

# CSE = '5b1d951d01464ccea685a5fc35977d33'


class SpotAuth():

    def __init__(self, clientid=None, clientsecret=None, redirect=None):
        self.clientid = clientid
        self.clientsecret = clientsecret
        self.redirect = redirect
        self.token = self._token()

    def _token(self):

        url = auth_url(self.clientid, self.redirect)
        print("You Are Being Redirected to login to Spotfiy")
        print("Please Copy and Paste Redirected Link")
        webbrowser.open(url)
        code = input()
        response = get_token(response=code, client_id=self.clientid, redirect_uri=self.redirect, secret=self.clientsecret)
        print(response)
        return response.json()['access_token']

    
def auth_url(client_id, redirect_uri):

    packet = {'client_id': client_id,
                   'response_type': 'code',
                   'redirect_uri': redirect_uri,
                   'scope': 'user-read-private user-modify-playback-state'+\
            ' user-read-recently-played user-read-playback-state'+\
            ' playlist-read-private playlist-modify-public'+\
            ' user-read-currently-playing user-top-read playlist-modify-private '+\
            ' playlist-read-collaborative'}
    params = urllibparse.urlencode(packet)
    url = 'https://accounts.spotify.com/authorize?' + params
    return url

def get_token(response=None, client_id=None, redirect_uri=None, secret=None):

    r = response.split("?code=")[1].split("&")[0]
    packet = {'grant_type': 'authorization_code',
                   'code': r,
                   'redirect_uri': redirect_uri}
    
    b = client_id + ':' + secret
    encoded = base64.b64encode(six.text_type(b).encode('ascii'))
    auth = 'Basic ' + str(encoded.decode('ascii'))
    header = {'Authorization': auth}
    r = requests.post('https://accounts.spotify.com/api/token', data=packet,headers=header, verify=True)
    return r


s = SpotAuth(clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
