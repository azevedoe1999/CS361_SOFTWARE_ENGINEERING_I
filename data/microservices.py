### MICROSERVICES B,C,D ###

from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

app = Flask(__name__)

# connects to Spotfiy API via Spotipy with client id and client secret 
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id='60b64e7e08fb495090c340979db96f64',
    client_secret='fd49ed00f76f4cd783f0e117c46e314f'
))

# Will search up a song (Microservice B)
@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']  
    results = sp.search(name, limit=10, offset=0, type='track')
    result = []

    for i in range(0, len(results['tracks']['items'])):
        item = results['tracks']['items'][i]
        song = item['name']
        artist = []
        for j in range(0, len(item['artists'])):
            artist.append(item['artists'][j]['name'])
        album = item['album']['name']
        duration = item['duration_ms']
        i_d = item['id']
        result.append({
            'Track': f'Track {i+1}',
            'Name': song,
            'Artist': artist,
            'Album': album,
            'Duration': duration,
            'ID': i_d
            })
    
    return result 

# Will gather more info on playlist (Microservice D)
@app.route('/playlist_info', methods=['POST'])
def playlist_info():
    playlist = request.form['playlist'] 
    playlist = json.loads(playlist)
    total_duration = 0
    total_songs = len(playlist['Tracks'])

    i = 1
    for track in playlist['Tracks']:
        time = track[f'Track {i}']['Duration']
        seconds = convert_time_to_seconds(time)
        total_duration += seconds
        i += 1
    
    total_duration = convert_time_to_minutes_seconds(total_duration)

    data = {'total_songs': total_songs, 'total_duration': total_duration}
    return data


# Will gather more info on a song (Microservice D)
@app.route('/song_info', methods=['POST'])
def song_info():
    track = request.json
    track = json.loads(track)
    track_id = track['ID']
    results = sp.track(track_id)
    release_date = results['album']['release_date']
    popularity = results['popularity']
    explicit = results['explicit']
    data = {'release_date': release_date, 'popularity': popularity, 'explicit': explicit}
    return data 

# renames name of playlist and description
@app.route('/rename', methods=['POST'])
def rename():
    data_1 = request.form['data_1']
    data_2 = request.form['data_2']

    data = json.loads(data_1)
    playlists = json.loads(data_2)

    name = data['name']
    description = data['description']
    playlist_select = data['playlist_select']
    name = str(name)
    description = str(description)
    playlist_select = str(playlist_select)
    
    # change the names
    for playlist in playlists:
        if playlist['Playlist Name'] == playlist_select:
            if name == None:
                continue
            else:
                playlist['Playlist Name'] = name
            if description == None:
                continue
            else:
                playlist['Description'] = description
    
    return playlists


def convert_time_to_seconds(time):
    minutes, seconds = map(int, time.split(':'))
    return (minutes*60) + seconds

def convert_time_to_minutes_seconds(time): 
    minutues = time // 60
    seconds = time % 60
    return (f'{minutues}:{seconds}')


if __name__ == '__main__':
    app.run()