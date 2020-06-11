import spotipy
import spotipy.util as util

scope = 'user-top-read'

username = input("Provide a username: ")

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    for i, item in enumerate(results['items']):
        print(str(i+1) + ".", item['name'], '-', item['artists'][0]['name'])
        print()
