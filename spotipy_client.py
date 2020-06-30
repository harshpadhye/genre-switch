# Wrapper class to consolidate Spotipy method and add some custom functionalities

import spotipy
import spotipy.util as util
import random


class SpotipyClient:

    # initializes the client with and authorization token
    def __init__(self, auth_token):
        self.sp = spotipy.Spotify(auth=auth_token)

    # retrieves the top tracks for the user based on
    # frequency of plays within a given time period
    # short_term, medium_term, long_term
    def get_top_tracks(self, num_tracks, time_period):

        results = self.sp.current_user_top_tracks(
            limit=num_tracks, time_range=time_period)["items"]

        # prints tracks and artists to console in order
        for i, item in enumerate(results):
            artists = [art_obj["name"] for art_obj in item["artists"]]
            print("\n" + str(i+1) + ".", item["name"], "-", *artists)

        # returns the list of Track Objects
        return [track["id"] for track in results]

    # Searches the user's playlist directory for the desired playlist name.
    # if the playlist doesn't exist, create it; then, return that playlist id
    def create_new_playlist(self, pl_user, pl_name, pl_description, pl_public):
        # first, search if the playlist name already exists
        # Spotify allows for the creation of duplicate playlist names
        user_playlists = self.sp.current_user_playlists(limit=50, offset=0)[
            "items"]
        exists = False
        pl_id = None

        # Iterates through playlist objects and finds the appropriate playlist id
        for pl in user_playlists:
            if pl["name"] == pl_name:
                pl_id = pl["id"]
                exists = True
                break

        # Dedicated playlist does not exist; let's create it
        if not exists:
            pl_id = self.sp.user_playlist_create(
                user=pl_user, name=pl_name, description=pl_description, public=pl_public)["id"]

        # return the new/dedicated playlist id
        return pl_id

    # Given a playlist id and a list of track ids,
    # replaces current tracks in the playlist with the new tracks
    def rewrite_playlist(self, pl_user, pl_id, track_ids):
        self.sp.user_playlist_replace_tracks(
            user=pl_user, playlist_id=pl_id, tracks=track_ids)

    # Returns the average track popularity across all songs in the user's playlists
    # Don't consider duplicate tracks across playlists
    def get_average_track_popularity(self, user):
        # first, retrieve the user's playlists (cap it at 30)
        user_playlists = self.sp.current_user_playlists(limit=30, offset=0)[
            "items"]

        # now combine all tracks from the user's playlists
        # removes duplicates via the dictionary
        dictionary = {}
        for playlist in user_playlists:
            tracks = self.sp.playlist_tracks(
                playlist['id'], fields='items.track.popularity,items.track.name')
            for item in tracks["items"]:
                name = str(item['track']['name'])
                pop = int(item['track']['popularity'])
                dictionary.setdefault(name, pop)

        # gets popularity values from dictionary
        popularity = dictionary.values()

        # returns the average of the tracks' popularities, rounded to two decimals
        return (100 - (round(sum(popularity) / len(popularity), 2)))

    def get_recommendations_by_genre(self, curr_track_ids):
        # get the list of genres that Spotify provides
        available_genres = self.sp.recommendation_genre_seeds()["genres"]

        # pick five genres to explore (Spotify limits unique seeds to five)
        genre_seeds = random.sample(available_genres, 5)
        print(f"Try out these genres for a change: {str(genre_seeds)}")

        # now we run a quick audio analysis for the top tracks
        # and average certain features (danceability, tempo, valence, etc.)
        avgs = {"danceability": 0, "energy": 0,
                "instrumentalness": 0, "speechiness": 0, "tempo": 0, "valence": 0}
        track_analysis = self.sp.audio_features(curr_track_ids)

        # loop through each song and accumulate the select values in the dictionary
        for analysis_obj in track_analysis:
            for stat in avgs:
                avgs[stat] += analysis_obj[stat]

        # Average the values, round to 2 decimals
        avgs.update((key, round(value / len(curr_track_ids), 2))
                    for key, value in avgs.items())

        # Finds new tracks based on genre seeds and tuneable track characteristics
        new_tracks = self.sp.recommendations(seed_genres=genre_seeds, limit=10, target_danceability=avgs["danceability"], target_energy=avgs[
                                             "energy"], target_instrumentalness=avgs["instrumentalness"], target_speechiness=avgs["speechiness"], target_tempo=avgs["tempo"], target_valence=avgs["valence"])


        return [track["id"] for track in new_tracks["tracks"]]
