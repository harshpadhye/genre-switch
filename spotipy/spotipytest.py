import spotipy
import spotipy.util as util

scope = "user-top-read"

username = input("Provide a username: ")

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=10, time_range="short_term")
    for i, item in enumerate(results["items"]):
        # Allows console to print all artists of a track
        artists = [art_obj["name"] for art_obj in item["artists"]]
        print("\n" + str(i+1) + ".", item["name"], "-", *artists)
