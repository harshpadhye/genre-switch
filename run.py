import os
from spotifyclient import SpotifyClient

def run():
    # accesses web API with OAuth token
    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTH_TOKEN"))

    # gets the top tracks for the user (last 4 weeks, 10 track limit)
    top_tracks = spotify_client.get_top_tracks("short_term", 10)

    # extracts the unique track id from the returned track objects
    track_ids = [track["id"] for track in top_tracks]

    # add them to the top tracks playlist
    # added_to_playlist = spotify_client.add_top_tracks(track_ids)

    # prints out the track names and their artists
    # if added_to_playlist:
    for track in top_tracks:
        print(f"Added {track['name']} by", end = " ")
        # grabs the artists that wrote this track and prints them comma-separated
        artists = [art_obj['name'] for art_obj in track['artists']]
        print(*artists, sep = ", ")

if __name__ == "__main__":
    run()