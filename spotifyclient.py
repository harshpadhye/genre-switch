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
        print(response_json)
        tracks = [track_item for track_item in response_json["items"]]

        return tracks

    # modifies the user's "top tracks playlist" and replaces the existing tracks
    # if the playlist does not already exist, create it and continue to add tracks
    def add_top_tracks(self, track_ids):
        pass

    # creates a playlist dedicated to the user's top tracks
    def create_top_tracks_playlist(self):
        pass
   
