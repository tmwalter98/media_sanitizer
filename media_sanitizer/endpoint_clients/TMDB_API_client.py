

from tmdbv3api import TMDb
from tmdbv3api import Movie, TV, Season, Episode

import os


class API:
    def __init__(self):
        # key = self.load_api_key()
        tmdb = TMDb()
        tmdb.api_key = '76796d972576af7067d952e53839883b'
        tmdb.language = 'en'
        tmdb.debug = True
        self.tmdb = tmdb

    def load_api_key(self):
        # Attempts to load API key
        api_key_path = 'media_sanitizer/data/arangodb_creds'
        api_key_path_abs = os.path.abspath(api_key_path)
        try:
            with open(api_key_path_abs, 'r') as tmdb_api_key_f:
                tmdb_api_key = tmdb_api_key_f.readline().strip()
        except OSError:
            tmdb_api_key = input('Enter your TMDB API key: ').strip()
        # Attempts to save API key (Without asking)
        try:
            with open(api_key_path, 'w+') as tmdb_api_key_f:
                tmdb_api_key_f.write(tmdb_api_key)
        except OSError:
            pass

        return tmdb_api_key

    def get_movie_inst(self):
        return Movie()

    def get_tv_inst(self):
        return TV()

    def get_season_inst(self):
        return Season()

    def get_episode_inst(self):
        return Episode()
