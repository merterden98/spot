import requests
import json
import oauth2 as oauth
import six
import six.moves.urllib.parse as urllibparse
import webbrowser
import base64

RURI = 'https://example.com/callback/'

CLIENTID = 'abdd03cd5c1c4dc79d15cbf50b0641ad'

CSE = '5b1d951d01464ccea685a5fc35977d33'

def auth_url(client_id, redirect_uri):

    packet = {'client_id': client_id,
                   'response_type': 'code',
                   'redirect_uri': redirect_uri}
    params = urllibparse.urlencode(packet)
    url = 'https://accounts.spotify.com/authorize?' + params
    return url

def get_token(response, client_id, redirect_uri):

    r = response.split("?code=")[1].split("&")[0]
    
    packet = {'grant_type': 'authorization_code',
                   'code': r,
                   'redirect_uri': RURI}
    
    
    b = CLIENTID + ':' + CSE
    print(b)
    encoded = base64.b64encode(six.text_type(b).encode('ascii'))
    print(encoded.decode('ascii'))
    #encoded = encoded.decode('ascii')
    #print(encoded)
    auth = 'Basic ' + str(encoded.decode('ascii'))
    header = {'Authorization': auth}
    auth_header = base64.b64encode(six.text_type(CLIENTID + ':' + CSE).encode('ascii'))
    h = {'Authorization': 'Basic ' + auth_header.decode('ascii')}
    r = requests.post('https://accounts.spotify.com/api/token', data=packet,headers=h, verify=True)
    return r

url = auth_url('abdd03cd5c1c4dc79d15cbf50b0641ad','https://example.com/callback/')
webbrowser.open(url)

response = input("Input URL\n")

r = get_token(response, CLIENTID, RURI)



# url = "https://accounts.spotify.com/authorize"
# info = {"client_id":"abdd03cd5c1c4dc79d15cbf50b0641ad", "redirect_uri": 'https://example.com/callback/', 'response_type': 'code'}
# r = requests.get(url, params=info)
