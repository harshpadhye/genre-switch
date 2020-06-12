import spotipy
import spotipy.util as util

# Required scopes to access top tracks, modify playlists
scope = "user-top-read playlist-modify-public playlist-modify-private "

username = input("Provide a username / Spotify ID: ")

token = util.prompt_for_user_token(username, scope)

if token:
    # Creates Spotipy client
    sp = spotipy.Spotify(auth=token)

    # Gets the top ten tracks for the user in the last 4 weeks
    results = sp.current_user_top_tracks(limit=10, time_range="short_term")
    for i, item in enumerate(results["items"]):
        # Allows console to print all artists of a track
        artists = [art_obj["name"] for art_obj in item["artists"]]
        print("\n" + str(i+1) + ".", item["name"], "-", *artists)

    # Searches for a dedicated "My Recent Favorites" playlist
    user_playlists = sp.current_user_playlists(limit=50, offset=0)
    
    pl_exists = False
    pl_id = None
    
    # Iterates through playlist objects and finds the appropriate playlist id
    for pl in user_playlists["items"]:
        if pl["name"] == "My Recent Favorites":
            pl_id = pl["id"]
            pl_exists = True
            break
    # Dedicated playlist does not exist; let's create it
    if not pl_exists:
        pl_id = sp.user_playlist_create(user=username, name="My Recent Favorites",
         public=True, description="My top ten most played tracks in the last month")["id"]

    # Now that we have the correct playlist ID, we can rewrite its contents
    track_ids = [item["id"] for item in results["items"]]
    sp.user_playlist_replace_tracks(user=username, playlist_id=pl_id, tracks=track_ids)

    print("\nAll done! Check your Spotify playlist library.")
