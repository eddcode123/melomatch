import requests
import json
api_key = 'afa8075b695333e63279bf9ab0bf8be8'
def get_top_artist():
    url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={api_key}&format=json"
    req = requests.get(url=url)
    if req.status_code == 200:
        data = req.json()
    else:
        print(f"The request to api failed with code : {req.status_code}")
    
    return data if data else None


my_data = get_top_artist()
# print(my_data)

def get_top_5(data):
    if data and 'artists' in data and 'artist' in  data['artists']:
        top_artist = data['artists']['artist'][:5]

        return [artist['name'] for artist in top_artist]
    else:
        print("wrong format or data is empty")
        return None

print(get_top_5(my_data))