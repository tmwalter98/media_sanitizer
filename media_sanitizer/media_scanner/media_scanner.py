import media_scanner.data_hooks as Data
from media_scanner.scanner import Scanner
from media_scanner.match_engine import MatchEngine


class MediaScanner:
    local_movie_dirs = []
    local_tv_dirs = []
    discovered_movie_files = []
    discovered_episode_files = []

    def __init__(self, db, tmdb_api):
        hooks = Data.Hooks()
        hooks.add_hook('arango', db)
        hooks.add_hook('tmdb_api', tmdb_api)
        self.hooks = hooks

        self.scanner = Scanner(self.hooks)
        self.matcher = MatchEngine(self.hooks)
        return

    def add_movie_dirs(self, dirs):
        for dir in dirs:
            self.local_movie_dirs.append(dir)

    def add_tv_dirs(self, dirs):
        for dir in dirs:
            self.local_tv_dirs.append(dir)

    def scan_movies(self):
        self.scanner.scan_files(self.local_movie_dirs)

    def scan_tv(self):
        self.scanner.scan_files(self.local_tv_dirs)

    def match_titles(self):
        self.matcher.match_titles()
