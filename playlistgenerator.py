### MAIN FILE ###

import sys
import requests
import json
import ast
    
# convert time from ms to minutes and seconds 
def convert_time(ms):
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return minutes, seconds 

# use microservice A (Random Quote)
def random_microservice():
    response = requests.get('http://localhost:8080/quote')
    return response.json()

# greetings 
def greetings(stored_playlists_txt):
    print()
    try:
        with open(stored_playlists_txt, 'r') as file:
            content = file.read()
            if not content:
                reply = input("Hello User! There are no playlists. Would you like to create one? (1.Yes  2.No): ")
            else:
                reply = input("Hello User! What would you like to do? (3.Create playlist  4.View playlists  5.Leave): ")
        
        print()
        return reply
        
    except FileNotFoundError:
        print("File not found. Be sure to create txt file named 'stored_playlists.txt'.")

# create a new playlist
def create(stored_playlist_txt):
    name = input('Name of Playlist: ')
    print()

    response = True
    while response:
        answer = input('Would you like to use a random quote for your description or choose your own? (1.Random  2.Own) ')
        if answer == '1':
            description = random_microservice()
            description = description['value']
            response = False
        elif answer == '2':
            print()
            description = input('Description: ')
            response = False
        else:
            print('That is not one of the choices')
            print()

    tracks = []
    playlist = {
        'Playlist Name' : name,
        'Description' : description,
        'Tracks' : tracks
    }

    # writes new playlist into txt file 
    with open(stored_playlist_txt, 'a') as file:
        file.write(json.dumps(playlist))
        file.write('\n')
    
    print()
    print(f'Successfully created the playlist {name}')
    print()

# add song(s) to playlist
def add(stored_playlist_txt, playlist_select, playlists):
    for playlist in playlists:
        if playlist['Playlist Name'] == playlist_select:
            name = input('Enter the name of the track: ')
            print()
            # uploads/retreives info via microservice B
            data = {'name': name}
            result = requests.post('http://127.0.0.1:5000/search', data=data)
            data = ast.literal_eval(result.text)
            print('Results:')

            for item in data:
                print()
                print(item['Track'])
                print(f'Name: {item['Name']}')
                print('Artist(s): ')
                for artist in item['Artist']:
                    print(artist)
                print(f'Album: {item['Album']}')

            # lists 10 songs and will get info based on resposne 
            artists = []
            run = True
            while run:
                print()
                option = input('Enter the number associated with the track for which song you want to add or enter Back to research: ')
                if option in ['1','2','3','4','5','6','7','8','9','10']:
                    run = False
                    index = int(option) - 1
                    name = data[index]['Name']
                    for artist in data[index]['Artist']:
                        artists.append(artist)
                    album = data[index]['Album']
                    duration = data[index]['Duration']
                    i_d = data[index]['ID']

                elif option == 'Back':
                    run = False
                    print()
                    add(stored_playlist_txt, playlist_select, playlists)
                
                else:
                    print('That is not a correct input')

            minutes, seconds = convert_time(duration)
            track = {'Name': name, 'Artist': artists, 'Album': album, 'Duration': f'{minutes}:{seconds}', 'ID':  i_d}
            
            # add track to tracks section in playlist 
            if not playlist['Tracks']:
                track_1 = {'Track 1': track}
                playlist['Tracks'].append(track_1)
            else:
                length = len(playlist['Tracks'])
                number = length + 1
                track_i = {f'Track {number}': track}
                playlist['Tracks'].append(track_i)

            print()
            print('Added new song to playlist')
            print()

    # erase txt file 
    with open(stored_playlist_txt, 'w') as file:
        pass

    # add playlists to txt 
    with open(stored_playlist_txt, 'a') as file:
        for i in range(0, len(playlists)):
            line = playlists[i]
            file.write(json.dumps(line))
            file.write('\n')   

# delete song(s) from playlist
def delete(stored_playlist_txt, playlist_select, playlists):
    for playlist in playlists:
        if playlist['Playlist Name'] == playlist_select:
            track_to_delete = input('Enter the name of the track you want to delete: ')
            print()
            tracks = playlist['Tracks']

            i = 1
            present = False
            for track in tracks:
                if track[f'Track {i}']['Name'] == track_to_delete:
                    artist = track[f'Track {i}']['Artist']
                    album = track[f'Track {i}']['Album']
                    reply = input(f'Is {track_to_delete} by {artist}, part of album {album}, the one you want to delete? (1.Yes  2.No): ')
                    if reply == '1':
                        tracks.pop(i-1)
                        stored_track = tracks
                        playlist['Tracks'] = stored_track
                        present = True
                        print()
                        print('Song deleted from playlist')
                        print()

                    elif reply == '2':
                        present = True 

                i += 1

    if present == False:
        print('Song was not found in playlist. Please check spelling.')
        print()
        view(stored_playlist_txt)
        
    # erase txt file 
    with open(stored_playlist_txt, 'w') as file:
        pass

    # add playlists to txt 
    with open(stored_playlist_txt, 'a') as file:
        for i in range(0, len(playlists)):
            line = playlists[i]
            file.write(json.dumps(line))
            file.write('\n')     

# view stored playlists
def view(stored_playlists_txt):
    # add data from txt to playlist
    playlists = []
    with open(stored_playlists_txt, 'r') as file:    
        for line in file:
            playlist = json.loads(line)
            playlists.append(playlist)

    # prints lists of playlists and details 
    print('Here are the list of created playlists:')
    print()
    for i, playlist in enumerate(playlists, 1):
        print(f'Playlist {i}')
        print(f'Name: {playlist['Playlist Name']}')
        print(f'Description: {playlist['Description']}')
        if playlist['Tracks']:
            tracks = playlist['Tracks']
            j = 1
            for track in tracks:
                title = track[f'Track {j}']['Name']
                artist = track[f'Track {j}']['Artist']
                album = track[f'Track {j}']['Album']
                duration = track[f'Track {j}']['Duration']
                print(f'Track {j}: {title}, Artist: {artist}, Album: {album}, Duration: {duration}')
                j += 1
        else:
            print(f'Tracks: None')

        print()
    
    # ask user which playlist they want to select
    run = True
    present = False
    while run:
        playlist_select = input("Type the name of the playlist that you want to select? Or enter 'Back' to go back: ")
        print()
        if playlist_select == 'Back':
            run = False
            present = True
            main()
        else:  
            for playlist in playlists:
                if playlist['Playlist Name'] == playlist_select:
                    run = False
                    present = True
                    break
                else:
                    continue
            run = False

    # if playlist is not there, print error and go back to viewing playlists
    if present == False:
        print("Playlist does not exist. Check spelling")
        print()
        view(stored_playlists_txt)

    # ask user if they want to edit, add, delete, or go back 
    run = True
    while run:
        reply = input('Would you like to edit playlist, add or delete songs, view more info, or go back? (1.Edit  2.Add  3.Delete  4.More  5.Back): ')
        print()
        if reply == '1':
            playlist_select = edit(stored_playlists_txt, playlist_select, playlists)
            return
        elif reply == '2':
            add(stored_playlists_txt, playlist_select, playlists)
            continue
        elif reply == '3':
            delete(stored_playlists_txt, playlist_select, playlists)
            continue
        elif reply == '4':
            more_info(stored_playlists_txt, playlist_select)
            continue
        elif reply == '5':
            run = False 
            view(stored_playlists_txt)

# edit playlist name and description
def edit(stored_playlists_txt, playlist_select, playlists):
    new_playlist_name = None
    reply_name = input('Would you like to change the name of the playlist? (1.Yes  2.No): ')
    print()

    if reply_name == '1':
        new_playlist_name = input(f'What would you like the playlist name to be instead of {playlist_select}?: ')
        print()
    
    elif reply_name == '2':
        new_playlist_name = playlist_select
        print()

    else:
        print('That is not one of the choices')
        print()
        edit(stored_playlists_txt, playlist_select, playlists)

    run = True
    while run:
        new_description = None
        reply_description = input('Would you like to change the description of the playlist? (1.Yes  2.No): ')
        print()

        if reply_description == '1':
            run = False
            response = True
            while response:
                answer = input('Would you like to use a random quote for your description or choose your own? (1.Random  2.Own): ')
                print()
                if answer == '1':
                    # uses microservice A to get random quote
                    new_description = random_microservice()
                    new_description = new_description['value']
                    print()
                    response = False
                elif answer == '2':
                    new_description = input('What would you like the new description to be?: ')
                    print()
                    response = False
                else:
                    print('That is not one of the choices')
                    print()
        elif reply_description == '2':
            run = False
            for playlist in playlists:
                if new_playlist_name == playlist_select:
                    new_description = playlist['Description']
        else:
            print('That is not one of the choices')
            print()

    # gathers info and sends to microservice C to rename 
    data_1 = {'name': new_playlist_name, 'description': new_description, 'playlist_select': playlist_select}
    json_data_1 = json.dumps(data_1)
    json_data_2 = json.dumps(playlists)
    payload = {'data_1': json_data_1, 'data_2': json_data_2}
    result = requests.post('http://127.0.0.1:5000/rename', data=payload)
    playlists = json.loads(result.content)
    
    # erase txt file 
    with open(stored_playlists_txt, 'w') as file:
        pass

    # add playlists to txt 
    with open(stored_playlists_txt, 'a') as file:
        for i in range(0, len(playlists)):
            line = playlists[i]
            file.write(json.dumps(line))
            file.write('\n')   

    print('The playlist has been updated')
    print()

    if new_playlist_name:
        return new_playlist_name
    else:
        return playlist_select

# view more info via microservice D
def more_info(stored_playlists_txt, playlist_select):
    print()
    print(f'Here is more info on {playlist_select}:')
    print()

    with open(stored_playlists_txt, 'r') as file: 
        for line in file:   
            playlist = json.loads(line)
            if playlist['Playlist Name'] == playlist_select:
                playlist = line

    # uploads/returns info via microservice D
    data = {'playlist': playlist}
    result = requests.post('http://127.0.0.1:5000/playlist_info', data=data)
    data = json.loads(result.content)
    total_songs = data['total_songs']
    total_duration = data['total_duration']

    print(f'The total amount of songs in {playlist_select} is: {total_songs}')
    print(f'The total time duration of {playlist_select} is: {total_duration}')

    run = True
    while run:
        print()
        response = input("Do you want to get more info on a particular song in the playlist? (1. Yes  2. No): ")
        if response == '2':
            run = False
            print()
            view(stored_playlists_txt)
        elif response == '1':
            print()
            song = input('Which song do you want to get more info on?: ')
            playlist = json.loads(playlist)
            true = False
            i = 1
            for track in playlist['Tracks']:
                if track[f'Track {i}']['Name'] == song:
                    true = True
                    info = track[f'Track {i}']
                i += 1
            if true == False:
                print()
                print('That track does not exist. Please check spelling/errors.')
            else:
                run = False
        else:
            print()
            print('That is not a correct response.')

    run = True
    while run:
        # uploads/returns info via microservice D
        data = json.dumps(info)
        result = requests.post('http://127.0.0.1:5000/song_info', json=data)
        data = json.loads(result.content)

        artist = info['Artist']
        artist = ', '.join(artist)
        album = info['Album']
        duration = info['Duration']
        explicit = data['explicit']
        popularity = data['popularity']
        release = data['release_date']

        print()
        print(f'Here is more info on {song}:')
        print()
        print(f'Artist: {artist}')
        print(f'Album: {album}')
        print(f'Duration: {duration}')
        print(f'Explicit: {explicit}')
        print(f'Popularity: {popularity} out of 100')
        print(f'Release: {release}')
        print()

        choice = True
        while choice:
            response = input("Do you want to get more info on another song in the playlist? (1. Yes  2. No): ")
            if response == '1':
                print()
                song = input('Which song do you want to get more info on?: ')
                true = False
                i = 1
                for track in playlist['Tracks']:
                    if track[f'Track {i}']['Name'] == song:
                        true = True
                        info = track[f'Track {i}']
                    i += 1
                if true == False:
                    print()
                    print('That track does not exist. Please check spelling/errors.')
                else:
                    choice = False

            elif response == '2':
                choice = False
                run = False
                print()
                view(stored_playlists_txt)

            else:
                print()
                print('That is not a correct response.')

# main function
def main():
    stored_playlist = "stored_playlists.txt"

    run = True
    while run:
        print()
        print("If there is a number next to the options, then type out that number. Other wise, you can type freely.")
        reply = greetings(stored_playlist)

        if reply == '1': 
            create(stored_playlist)
            continue
        elif reply == '2':
            print('Goodbye!')
            print()
            run = False
            sys.exit()
        elif reply == '3':
            create(stored_playlist)
            continue
        elif reply == '4':
            view(stored_playlist)
            continue
        elif reply == '5':
            print('Goodbye')
            print()
            run = False
            sys.exit()
        else:
            print('Unknown reponse. Please respond with numbers.')
            print()
            continue
    
if __name__ == "__main__":
    main()




