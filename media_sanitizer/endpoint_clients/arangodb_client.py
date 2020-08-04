from arango import ArangoClient
import os
import re
import getpass

cred_path = 'media_sanitizer/data/arangodb_creds'
creds_abs_path = os.path.abspath(cred_path)


class Arango_Interface:
    def __init__(self):
        self.req_cols = ['tmdb_movies', 'tmdb_shows', 'tmdb_seasons',
                         'tmdb_episodes', 'local_movies', 'local_episodes',
                         'questionable_files']

    def load_creds(self):
        try:
            creds_f = open(creds_abs_path, 'r')
            creds_f_in = creds_f.read()
            creds_f.close()
        except FileNotFoundError:
            print('file not found')

        try:
            user_reg = re.compile(r'user\:\s([^\n]+)')
            pass_reg = re.compile(r'pass\:\s([^\n]+)')
            user = re.search(user_reg, creds_f_in).group(1).strip()
            passwd = re.search(pass_reg, creds_f_in).group(1).strip()
        except AttributeError:
            print('creds are not in file! :(')
        return (user, passwd)

    def prompt_creds(self):
        print('ArangoDB credentials are required.')
        user = input('username: ')
        passwd = getpass.getpass(prompt='password: ', stream=None)

        print('Would you these credentials to be stored on disk?')
        print('WARNING: Credentials are stored in plaintext')
        store_creds_q = input('Response (y/n)').strip()
        if store_creds_q == 'y':
            creds_file = '-- Credentials for ArangoDB user --\
                \nuser: {}\npass: {}'.format(user, passwd)
            try:
                with open(creds_abs_path, 'w+') as creds_f:
                    creds_f.write(creds_file)
            except OSError:
                print('Couldn\'t save credentials')
        return (user, passwd)

    def initialize_db_connection(self):
        """ creds = self.load_creds()
        user = creds[0]
        passwd = creds[1] """
        user = 'root'
        passwd = 'password'
        # self.prompt_creds()

        # Initialize the ArangoDB client.
        client = ArangoClient()

        # Connect to "_system" database as root user.
        sys_db = client.db('_system', username=user, password=passwd)

        # Create a new database named "media_sanitizer" if it does not exist.
        if not sys_db.has_database('media_sanitizer'):
            sys_db.create_database('media_sanitizer')
        self.db_sync = client.db('media_sanitizer', username=user,
                                 password=passwd)

        # Initializes required collections
        self.initialize_collections()

        return self

    def initialize_collections(self):
        db_sync = self.db_sync
        # Ensure all required collections exist
        for col in self.req_cols:
            if db_sync.has_collection(col):
                # !!! IMPORTANT !!! #
                db_sync.delete_collection(col)  # DELETES COL EVERY RUN
                # !!! IMPORTANT !!! #
                db_sync.create_collection(col)
            else:
                db_sync.create_collection(col)
        return self

    def get_col(self, col):
        # retrieved_col = self.db_sync.collection(col)
        return self.db_sync.collection(col)

    def get_async_col(self, col):
        db_async = self.db_sync.begin_async_execution(return_result=True)
        return db_async.collection(col)

    def get_async_aql(self):
        db_async = self.db_sync.begin_async_execution(return_result=True)
        return db_async.aql
