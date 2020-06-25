import spotipy
import spotipy.util as util
from spotipy_client import SpotipyClient

# Required scopes to access top tracks, modify playlists
scope = "user-top-read playlist-modify-public playlist-modify-private "

username = input("Provide a username / Spotify ID: ")

token = util.prompt_for_user_token(username, scope)

if token:
    # Creates Spotipy client
    client = SpotipyClient(auth_token=token)

    # Gets the top ten tracks for the user in the last 4 weeks
    top_tracks = client.get_top_tracks(num_tracks=20, time_period="short_term")

    # Searches for a dedicated "My Recent Favorites" playlist
    my_recent_fav_playlist_id = client.create_new_playlist(pl_user=username, pl_name="My Recent Favorites",
                                                        pl_description="My most frequently replayed tracks", pl_public=True)

    # Now that we have the correct playlist ID, we can rewrite its contents
    top_track_ids = [track["id"] for track in top_tracks]
    client.rewrite_playlist(pl_user=username, pl_id=my_recent_fav_playlist_id, track_ids=top_track_ids)

    print("\nAll done! Check your Spotify playlist library.")

    print(f"Analyzing {username}'s indie factor...")

    indie_factor = 100 - client.get_average_track_popularity(user=username)
    print(f"{username} is {indie_factor}% indie")