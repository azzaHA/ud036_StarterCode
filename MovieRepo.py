"""
Import Movies Data from The Movies Database API "TMDB",
using the python API wrapper "tmdbsimple"
"""
import tmdbsimple as tmdb
from media import Movie


class MoviesRepository():
    """
    Methods:
    __init__: instantiates new MoviesRepository object
    now_playing: returns a list of Movie objects,
                 representing current movies in theatres
    """

    def __init__(self, api_key):
        tmdb.API_KEY = api_key

    def __find_youtube_id(self, trailers):
        """search the trailers list for "official trailer"
        youtube video
        """

        youtube_id = ""
        for trailer in trailers:
            if (trailer['site'] == 'YouTube'):
                youtube_id = trailer['key']
                if (trailer['name'].lower().startswith('official trailer')):
                    return trailer['key']
        return youtube_id

    def now_playing(self):
        """return a list of Movie objects,
        representing current movies in theatres
        """

        movies = tmdb.Movies()
        # get the current movies
        response = movies.now_playing()
        # response holds multiple data, including 'results' list
        # for each result in 'results' list, extract the movie data
        movies_list = []
        for r in response['results']:
            movie_id = r['id']
            movie_title = r['title']
            story = r['overview']
            image = 'https://image.tmdb.org/t/p/w342/' + r['poster_path']

            # use movie_id to get the movie trailers
            # using videos() method,
            # and store the 'results' list
            trailers = tmdb.Movies(movie_id).videos()['results']

            youtube_id = self.__find_youtube_id(trailers)
            if youtube_id != "":
                movie_object = Movie(movie_title, story, youtube_id, image)
                movies_list.append(movie_object)
        return movies_list
