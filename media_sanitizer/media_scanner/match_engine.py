import PTN
import threading
import queue
import json


class MatchEngine:
    def __init__(self, hooks):
        self.hooks = hooks

    def match_titles(self):
        db = self.hooks.get('arango')
        tmdb = self.hooks.get('tmdb_api')

        # Instantiate queues
        analyze_queue = queue.Queue()
        search_queue = queue.Queue()
        search_results = queue.Queue()

        workers = dict()

        # Prepare Database Retriever Worker
        aql = db.get_async_aql()
        workers['retriever'] = Database_Retriever(1, aql, analyze_queue)

        # Prepare File Analyzer Worker
        workers['file_analyzer'] = File_Analyzer(2, analyze_queue,
                                                 search_queue)

        # Prepare Search Engine Worker
        workers['search_engine'] = Search_Engine(3, search_queue,
                                                 search_results, tmdb)

        # Start workers
        for title, instance in workers.items():
            instance.start()

        # Wait for workers to complete their jobs
        for title, instance in workers.items():
            instance.join()


class Database_Retriever (threading.Thread):
    def __init__(self, threadID, async_aql, analyze_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.async_aql = async_aql
        self.analyze_queue = analyze_queue

    def run(self):
        print('starting {}'.format(self.threadID))
        aql = self.async_aql
        analyze_queue = self.analyze_queue

        job = aql.execute(
            'FOR doc IN local_movies RETURN doc',
            batch_size=100
        )
        cursor = job.result()

        while cursor.has_more():
            cursor.fetch()
            for doc in cursor.batch():
                analyze_queue.put(doc)


class File_Analyzer (threading.Thread):
    def __init__(self, threadID, analyze_queue, search_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.analyze_queue = analyze_queue
        self.search_queue = search_queue

    def analyze_file(self, file):
        file_type = file.get('type')
        if file_type == 'video':
            title = file['title']
            parsed = PTN.parse(title)

            parsed_title = parsed.get('title')
            parsed_year = parsed.get('year')
            parsed_season = parsed.get('season')
            parsed_episode = parsed.get('episode')

            if parsed_season and parsed_episode:
                file['search_type'] = 'tv'
                file['parsed_title'] = parsed_title
                file['parsed_year'] = parsed_year
                file['parsed_season'] = parsed_season
                file['parsed_episode'] = parsed_episode

            elif parsed_title is not None and parsed_year:
                file['search_type'] = 'movie'
                file['parsed_title'] = parsed_title
                file['parsed_year'] = parsed_year
            else:
                file['search_type'] = 'skip'
        else:
            file['search_type'] = 'skip'
        return file

    def run(self):
        print('starting {}'.format(self.threadID))
        to_analyze = self.analyze_queue
        to_search = self.search_queue

        while True:
            if to_analyze.qsize() > 0:
                file = to_analyze.get()
                analysis = self.analyze_file(file)
                to_search.put(analysis)


class Search_Engine (threading.Thread):
    def __init__(self, threadID, search_queue, search_results, tmdb_api):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.search_queue = search_queue
        self.search_results = search_results
        self.movie = tmdb_api.get_movie_inst()

    def search_movie(self, title):
        print('searching... {}\n'.format(title))
        response = self.movie.search(title)
        results = []
        for res in response:
            movie = dict()
            movie['id'] = res.id
            movie['title'] = res.title
            movie['overview'] = res.overview
            movie['poster_path'] = res.poster_path
            results.append(movie)
            # print(json.dumps(movie, indent=2), '\n\n')
        return results

    def search_episode(file):
        print('FUCK! lol')

    def run(self):
        print('starting {}'.format(self.threadID))
        to_search = self.search_queue
        search_results = self.search_results

        while True:
            if to_search.qsize() > 0:
                specemin = to_search.get()

                search_type = specemin.get('search_type')

                if search_type != 'skip':
                    if search_type == 'movie':
                        query = specemin['parsed_title']
                        results = self.search_movie(query)

                        if len(results) > 1:
                            print('Not sure about {}'.format(query))
                        elif len(results) is 0:
                            print('No match found for {}'.format(query))
                        else:
                            specemin['match'] = results
                            print(json.dumps(specemin, indent=2), '\n\n\n\n')
                            search_results.put(specemin)
