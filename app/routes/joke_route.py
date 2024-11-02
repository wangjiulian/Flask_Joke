from flask import blueprints, request, jsonify
from flasgger import swag_from
from werkzeug.exceptions import BadRequest

from app.services.joke_service import JokeService
from app.utils.response import Response
from app.utils.util import *

joke = blueprints.Blueprint(JokeBlueprint, __name__)


@joke.route(API_INDEX, methods=[HTTP_GET])
def index():
    try:
        return JokeService.get_random_joke()
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@joke.route(API_GET_JOKE_SEARCH, methods=[HTTP_GET])
def get_joke_search():
    try:
        query = request.args.get(QUERY)
        if query:
            query = query.strip()
            if query and len(query) > 0:
                if len(query) < QUERY_MIN_LENGTH or len(query) > QUERY_MAX_LENGTH:
                    return Response.bad_request(ERROR_INVALID_QUERY_LENGTH)

        return JokeService.search_jokes(query)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@joke.route(API_GET_JOKE_DETAIL, methods=[HTTP_GET])
def get_joke_detail(joke_id):
    try:
        joke_id = joke_id.strip()
        if not joke_id:
            return Response.bad_request(ERROR_NO_ID)

        return JokeService.get_joke_by_id(joke_id)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@joke.route(API_POST_JOKE_ADD, methods=[HTTP_POST])
def add_joke():
    try:
        value, icon_url, error = _check_data()
        if error is not None:
            return error

        return JokeService.add_joke(value, icon_url)

    except BadRequest as e:
        return Response.bad_request(ERROR_INVALID_JSON)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@joke.route(API_PUT_JOKE_UPDATE, methods=[HTTP_PUT])
def update_joke(joke_id):
    try:
        joke_id = joke_id.strip()
        if not joke_id:
            return Response.bad_request(ERROR_NO_ID)

        value, icon_url, error = _check_data()
        if error is not None:
            return error

        return JokeService.update_joke(joke_id, value, icon_url)

    except BadRequest as e:
        return Response.bad_request(ERROR_INVALID_JSON)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@joke.route(API_DELETE_JOKE_REMOVE, methods=[HTTP_DELETE])
def remove_joke(joke_id):
    try:
        joke_id = joke_id.strip()
        if not joke_id:
            return Response.bad_request(ERROR_NO_ID)

        return JokeService.delete_joke(joke_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _check_data():
    data = request.get_json()
    error = _check_data_required_fields(data)
    if error is not None:
        return "", "", error

    value = data.get(VALUE).strip()
    icon_url = data.get(ICON_URL).strip()

    return value, icon_url, None


def _check_data_required_fields(data):
    # check if JSON is valid
    if not data:
        return Response.bad_request(ERROR_NO_JSON)

    # Check if Value is valid
    if not data.get(VALUE) or not data.get(VALUE).strip():
        return Response.bad_request(ERROR_NO_VALUE)
    if len(data.get(VALUE).strip()) < VALUE_MIN_LENGTH or len(data.get(VALUE).strip()) > VALUE_MAX_LENGTH:
        return Response.bad_request(ERROR_INVALID_VALUE_LENGTH)

    # Check if Icon URL is valid
    if not data.get(ICON_URL) or not data.get(ICON_URL).strip():
        return Response.bad_request(ERROR_NO_ICON_URL)
    if len(data.get(ICON_URL).strip()) > ICON_URL_MAX_LENGTH:
        return Response.bad_request(ERROR_INVALID_ICON_URL_LENGTH)
    if not is_image_url(data.get(ICON_URL).strip()):
        return Response.bad_request(ERROR_INVALID_ICON_URL_FORMAT)
    if not check_image_accessible(data.get(ICON_URL).strip()):
        return Response.bad_request(ERROR_INVALID_ICON_URL_ACCESS)

    return None
