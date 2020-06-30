import spotipy
import spotipy.util as util
from spotipy_client import SpotipyClient

# Required scopes to access top tracks, modify playlists
scope = "user-top-read playlist-modify-public playlist-modify-private playlist-read-private"

username = input("Provide a username / Spotify ID: ")

token = util.prompt_for_user_token(username, scope)

if token:
    # Creates Spotipy client
    client = SpotipyClient(auth_token=token)

    print("First, let's find out your recent favorite tracks:")

    # Gets the top ten tracks for the user in the last 4 weeks
    top_track_ids = client.get_top_tracks(
        num_tracks=10, time_period="short_term")

    # Searches for a dedicated "My Recent Favorites" playlist
    my_recent_fav_playlist_id = client.create_new_playlist(pl_user=username, pl_name="My Recent Favorites",
                                                           pl_description="My most frequently replayed tracks", pl_public=True)

    # Now that we have the correct playlist ID, we can rewrite its contents
    client.rewrite_playlist(
        pl_user=username, pl_id=my_recent_fav_playlist_id, track_ids=top_track_ids)

    print(f"\nAnalyzing {username}'s indie factor...")

    indie_factor = client.get_average_track_popularity(user=username)
    print(f"{username} is {indie_factor}% indie.")
    print("We recommend checking out some new music! We curated a playlist for you based on your listening habits.")

    # Gets recommendations for the user and adds them to a dedicated playlist
    rec_tracks_ids = client.get_recommendations_by_genre(curr_track_ids=top_track_ids)
    my_recent_rec_playlist_id = client.create_new_playlist(pl_user=username, pl_name="My Recent Recommendations",
                                                           pl_description="Songs suggestions based on the characteristics of your recent favorite tracks", pl_public=True)
    client.rewrite_playlist(pl_user=username, pl_id=my_recent_rec_playlist_id, track_ids=rec_tracks_ids)

    print("\nAll done! Check your Spotify playlist library.")