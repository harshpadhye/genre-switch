import json
import requests
import urllib

class SpotifyClient(object):

    # default init constructor
    def __init__(self, api_token):
        self.api_token = api_token

    # gets the top 10 tracks of the last 4 weeks
    def get_top_tracks(self, time_range, limit):
        # constructs the url to access the web api
        url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}"

        # issues a GET request and records the response in JSON format
        response = requests.get(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()
        # retrieves list of track objects from the paging object response
        tracks = [track_item for track_item in response_json["items"]]

        return tracks

    # modifies the user's "top tracks playlist" and replaces the existing tracks
    # if the playlist does not already exist, create it and continue to add tracks
    def add_top_tracks(self, track_ids):
        # checks whether a dedicated playlist exists
        # first, fetch the json object from the Web API
        get_playlists_url = "https://api.spotify.com/v1/me/playlists"
        user_playlists_response = requests.get(
            get_playlists_url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        user_playlists_response_json = user_playlists_response.json()

        # Now, condense into an array of the user's playlist names (in lowercase)
        playlist_names = [item["name"].lower() for item in user_playlists_response_json["items"]]

        # Flags whether the dedicated playlist exists or not
        exists = "My Recent Favorites" in playlist_names 
        
        # if it doesn't, create the playlist and save its ID
        # otherwise, fetch that ID
        if(not exists):
            play_id = self.create_top_tracks_playlist()

        return playlist_names

    # creates a playlist dedicated to the user's top tracks
    def create_top_tracks_playlist(self):
        pass
   
