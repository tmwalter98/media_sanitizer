import os
import endpoint_clients.arangodb_client as Arango_API
import endpoint_clients.TMDB_API_client as TMDB_API
from media_scanner import MediaScanner


print('What kind of files are we going to be working on today?')
print('1) Movies\n2) TV Shows\n3) both')
print(os.path.dirname(__file__))

# Insert while for validation
# type_selection = int(input("Select one:\t(1, 2, or 3): "))

movie_dirs = []
movie_dirs.append('/home/tim/Desktop/12TB_Drive/Movies')
movie_dirs.append('/home/tim/Desktop/12TB_Drive/Not-HD_Movies')
movie_dirs.append('/home/tim/Desktop/12TB_Drive/4K_Movies')

tv_dirs = []
tv_dirs.append('/home/tim/Desktop/12TB_Drive/TV_Shows')
# extra_dir = input('tell me that special place (: ')
# tv_dirs.append(extra_dir)


arango_db = Arango_API.Arango_Interface()
arango_db.initialize_db_connection()

tmdb_interface = TMDB_API.API()

media_scanner = MediaScanner(arango_db, tmdb_interface)

media_scanner.add_movie_dirs(movie_dirs)
media_scanner.add_tv_dirs(tv_dirs)
media_scanner.scan_movies()
media_scanner.scan_tv()

media_scanner.match_titles()


# Update database
print('Would you like to update IMDB database?')
# Insert while for validation
# update_selection = input('Last updated: Never\t(y/n): ')
