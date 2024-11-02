import requests
from app.constants import *
from .exceptions import ChuckNorrisException


class ChuckNorrisAPI:
    """A class to interact with the Chuck Norris Joke API."""

    @staticmethod
    def get_random_joke():
        """Fetch a random joke."""
        return ChuckNorrisAPI._http_get(API_CHUNK_NORRIS_RANDOM)

    @staticmethod
    def get_joke_by_id(joke_id):
        """Fetch a joke by its ID."""
        url = API_CHUNK_NORRIS_DETAIL.format(joke_id)
        return ChuckNorrisAPI._http_get(url)

    @staticmethod
    def search_jokes(query):
        """Search for jokes based on a query."""
        if not query:
            return None
        url = API_CHUNK_NORRIS_SEARCH.format(query)
        return ChuckNorrisAPI._http_get(url)

    @staticmethod
    def _http_get(url):
        """Helper method to perform a GET request with error handling."""
        try:
            response = requests.get(url)
            if response.status_code == HTTP_OK:
                return response.json()

            elif response.status_code == HTTP_NOT_FOUND:
                return None

            else:
                """Only raise an error if the status code is not 200 or 404."""
                raise ChuckNorrisException(
                    f'Chuck Norris API Code Error: {response.status_code}, URL: {url}, text: {response.text}'
                )

        except Exception as e:
            raise ChuckNorrisException(f'Chuck Norris API Error: {e}, URL: {url}')
