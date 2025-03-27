from app.utils.chuck_norris_api import ChuckNorrisAPI
from app.models.joke import Joke
from app.utils.response import Response
from app.utils.util import generate_uuid_string
from app.constants import *
from app.config import Config


class JokeService:

    @staticmethod
    def get_random_joke():
        joke = ChuckNorrisAPI.get_random_joke()
        if not joke:l
            return Response.not_found()

        return Response.success(Joke.to_joke_dict(joke))

    @staticmethod
    def search_jokes(query):
        result = []
        chunk_jokes = None
        # Get the jokes from the Chuck Norris API
        search_chunk_jokes = ChuckNorrisAPI.search_jokes(query)
        if search_chunk_jokes:
            if RESULT in search_chunk_jokes:
                chunk_jokes = search_chunk_jokes[RESULT]
                for joke in chunk_jokes:
                    result.extend([Joke.to_joke_dict(joke)])

        # Get the jokes from the local database
        local_jokes = Joke.search_jokes(query)
        if local_jokes:
            for joke in local_jokes:
                result.append(joke.model_to_dict())

        # Return the response
        resp = {
            TOTAL: 0,
            RESULT: []
        }

        if result:
            resp[TOTAL] = len(result)
            resp[RESULT] = result

        return Response.success(resp)

    @staticmethod
    def get_joke_by_id(joke_id):
        joke = Joke.get_by_id(joke_id)
        if joke:
            joke = joke.model_to_dict()

        if not joke:
            joke = ChuckNorrisAPI.get_joke_by_id(joke_id)
            if not joke:
                return Response.not_found()

        return Response.success(Joke.to_joke_dict(joke))

    @staticmethod
    def add_joke(value, icon_url):
        idStr = generate_uuid_string()
        url = f"{API_PREFIX}/{idStr}"
        joke = Joke(id=idStr, url=url, value=value, icon_url=icon_url)
        joke.add()

        return Response.success(joke.model_to_dict())

    @staticmethod
    def update_joke(joke_id, value, icon_url):
        joke = Joke.get_by_id(joke_id)
        if not joke:
            return Response.not_found()

        joke.update(value, icon_url)

        return Response.success({})

    @staticmethod
    def delete_joke(joke_id):
        joke = Joke.get_by_id(joke_id)
        if not joke:
            return Response.not_found()

        joke.remove()

        return Response.success({})
