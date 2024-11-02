import pytest

from app import create_app
from app.db import db, init_db
from app.utils.util import *
from app.config import Config
from app.constants import *


@pytest.fixture
def app():
    Config.HTTP_SERVER_URL = 'http://localhost:5000'
    Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    app = create_app(open_docs=False)
    app.config['TESTING'] = True
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def database(app):
    with app.app_context():
        init_db(app)
        yield db
        db.session.remove()
        db.drop_all()


def test_api_index(client):
    """Test whether the response data from the API_INDEX endpoint meets expectations"""
    response = client.get(API_INDEX)

    assert response.status_code == HTTP_OK, "API_INDEX endpoint returned an incorrect status code"
    response_json = response.get_json()
    assert response_json, "API_INDEX endpoint did not return valid JSON"
    assert response_json, "API_INDEX endpoint did not return JSON data"
    assert response_json.get(ID), "ID field is missing in JSON response"
    assert response_json.get(ICON_URL), "ICON_URL field is missing in JSON response"
    assert response_json.get(VALUE), "VALUE field is missing in JSON response"
    assert response_json.get(URL), "URL field is missing in JSON response"
    assert response_json.get(URL).startswith(Config.REPLACE_URL), "URL field has an incorrect format"

    # Test if the returned URL is accessible
    assert client.get(response_json.get(URL)).status_code == HTTP_OK, "The returned URL is not accessible"


@pytest.mark.parametrize(
    "query, expected_status_code, expected_response",
    [
        ("", HTTP_OK, {"total": 0}),
        ("?query=", HTTP_OK, {"total": 0}),
        ("?query", HTTP_OK, {"total": 0}),
        ("?query=111", HTTP_OK, {"total": 1}),

    ]
)
def test_api_get_search(client, query, expected_status_code, expected_response):
    """Test whether the response data from the API_GET_JOKE_SEARCH endpoint meets expectations"""
    response = client.get(API_GET_JOKE_SEARCH + query)

    assert response.status_code == expected_status_code, f"unexpected status code for {query}"
    response_json = response.get_json()
    assert TOTAL in response_json, f"total field is missing in JSON response for {query}"
    assert RESULT in response_json, f"result field is missing in JSON response for {query}"
    assert response_json[TOTAL] == expected_response[TOTAL], f"total field is incorrect for {query}"


@pytest.mark.parametrize(
    "headers,data, expected_status_code, expected_response",
    [
        ({}, {}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, "", HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, {}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, {VALUE: ""}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_VALUE}),
        ({"Content-Type": "application/json"}, {VALUE: " "}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_VALUE}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(1)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(2)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        (
                {"Content-Type": "application/json"},
                {VALUE: generate_random_string(VALUE_MAX_LENGTH + random.randint(1, 10))},
                HTTP_BAD_REQUEST,
                {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string()}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_NO_ICON_URL}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: ""}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_NO_ICON_URL}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: generate_random_string(
            ICON_URL_MAX_LENGTH + random.randint(1, 10))}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: generate_random_string(
            ICON_URL_MAX_LENGTH)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_FORMAT}),
        ({"Content-Type": "application/json"},
         {VALUE: generate_random_string(), ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris1.png"},
         HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_ACCESS}),
        ({"Content-Type": "application/json"},
         {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"},
         HTTP_OK,
         {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"},),

    ]
)
def test_api_post_add(client, headers, data, expected_status_code, expected_response):
    """Test whether the response data from the API_POST_ADD endpoint meets expectations"""
    response = client.post(API_POST_JOKE_ADD, headers=headers, json=data)

    assert response.status_code == expected_status_code, f"unexpected status code for {data}"
    response_json = response.get_json()
    if response.status_code == HTTP_BAD_REQUEST:
        assert response_json, f"did not return valid JSON for {data}"
        assert ERROR in response_json, f"error field is missing in JSON response for {data}"
        assert response_json[ERROR] == expected_response[ERROR], f"error field is incorrect for {data}"

    if response.status_code == HTTP_OK:
        assert VALUE in response_json, f"value field is missing in JSON response for {data}"
        assert response_json[VALUE] == expected_response[VALUE], f"value field is incorrect for {data}"
        assert ICON_URL in response_json, f"icon_url field is missing in JSON response for {data}"
        assert response_json[ICON_URL] == expected_response[ICON_URL], f"icon_url field is incorrect for {data}"
        assert URL in response_json, f"icon_url field is missing in JSON response for {data}"
        assert ID in response_json, f"id field is missing in JSON response for {data}"

    if ID in response_json:
        # Get the ID and return it for further tests
        return response_json[ID]


def test_api_get_joke(client):
    """Test whether the response data from the API_GET_JOKE_DETAIL endpoint meets expectations"""
    # Get with valid ID
    response = client.get(str.replace(API_GET_JOKE_DETAIL, API_ID_SUFFIX, generate_random_string(ID_MAX_LENGTH)))
    response_json = response.get_json()

    assert response.status_code == HTTP_NOT_FOUND, "API_GET_JOKE_DETAIL endpoint returned an incorrect status code"
    assert response_json, "API_GET_JOKE_DETAIL endpoint did not return valid JSON"
    assert ERROR in response_json, "error field is missing in JSON response"
    assert response_json[ERROR] == ERROR_NOT_FOUND, "unexpected error message"

    # Create a new joke
    data = {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"}
    joke_id = test_api_post_add(client, headers={"Content-Type": "application/json"}, data=data,
                                expected_status_code=HTTP_OK,
                                expected_response=data)

    # Get with valid ID
    response = client.get(str.replace(API_GET_JOKE_DETAIL, API_ID_SUFFIX, joke_id))
    response_json = response.get_json()

    assert response.status_code == HTTP_OK, "API_GET_JOKE_DETAIL endpoint returned an incorrect status code"
    assert response_json, "API_GET_JOKE_DETAIL endpoint did not return valid JSON"
    assert VALUE in response_json, "value field is missing in JSON response"
    assert response_json[VALUE] == data[VALUE], "value field is incorrect"
    assert ICON_URL in response_json, "icon_url field is missing in JSON response"
    assert response_json[ICON_URL] == data[ICON_URL], "icon_url field is incorrect"


@pytest.mark.parametrize(
    "headers,put_data, expected_status_code, expected_response",
    [
        ({}, {}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, "", HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, {}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_JSON}),
        ({"Content-Type": "application/json"}, {VALUE: ""}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_VALUE}),
        ({"Content-Type": "application/json"}, {VALUE: " "}, HTTP_BAD_REQUEST, {ERROR: ERROR_NO_VALUE}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(1)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(2)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        (
                {"Content-Type": "application/json"},
                {VALUE: generate_random_string(VALUE_MAX_LENGTH + random.randint(1, 10))},
                HTTP_BAD_REQUEST,
                {ERROR: ERROR_INVALID_VALUE_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string()}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_NO_ICON_URL}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: ""}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_NO_ICON_URL}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: generate_random_string(
            ICON_URL_MAX_LENGTH + random.randint(1, 10))}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_LENGTH}),
        ({"Content-Type": "application/json"}, {VALUE: generate_random_string(), ICON_URL: generate_random_string(
            ICON_URL_MAX_LENGTH)}, HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_FORMAT}),
        ({"Content-Type": "application/json"},
         {VALUE: generate_random_string(), ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris1.png"},
         HTTP_BAD_REQUEST,
         {ERROR: ERROR_INVALID_ICON_URL_ACCESS}),
        ({"Content-Type": "application/json"},
         {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"},
         HTTP_NOT_FOUND,
         {ERROR: ERROR_NOT_FOUND}),

    ]
)
def test_api_put_update(client, headers, put_data, expected_status_code, expected_response):
    """Test whether the response data from the API_PUT_UPDATE endpoint meets expectations"""
    # Update with invalid ID
    response = client.put(str.replace(API_PUT_JOKE_UPDATE, API_ID_SUFFIX, generate_random_string(ID_MAX_LENGTH)),
                          headers=headers, json=put_data)
    response_json = response.get_json()

    assert response.status_code == expected_status_code, "API_PUT_UPDATE endpoint returned an incorrect status code"
    assert response_json, "API_PUT_UPDATE endpoint did not return valid JSON"
    assert ERROR in response_json, "error field is missing in JSON response"
    assert response_json[ERROR] == expected_response[ERROR], "unexpected error message"

    # Create a new joke
    data = {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"}
    joke_id = test_api_post_add(client, headers={"Content-Type": "application/json"}, data=data,
                                expected_status_code=HTTP_OK,
                                expected_response=data)

    # Update with valid ID
    update_data = {VALUE: "Hello My World",
                   ICON_URL: "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"}
    response = client.put(str.replace(API_PUT_JOKE_UPDATE, API_ID_SUFFIX, joke_id),
                          headers={"Content-Type": "application/json"}, json=update_data)
    response_json = response.get_json()

    assert response.status_code == HTTP_OK, "API_PUT_UPDATE endpoint returned an incorrect status code"
    assert response_json == {}, "API_PUT_UPDATE endpoint did not return valid JSON"

    # Verify the update
    response = client.get(str.replace(API_GET_JOKE_DETAIL, API_ID_SUFFIX, joke_id))
    response_json = response.get_json()

    assert response.status_code == HTTP_OK, "API_GET_JOKE_DETAIL endpoint returned an incorrect status code"
    assert response_json, "API_GET_JOKE_DETAIL endpoint did not return valid JSON"
    assert VALUE in response_json, "value field is missing in JSON response"
    assert response_json[VALUE] == update_data[VALUE], "expected value is incorrect"
    assert ICON_URL in response_json, "icon_url field is missing in JSON response"
    assert response_json[ICON_URL] == update_data[ICON_URL], "expected icon_url value is incorrect"


def test_api_delete(client):
    """Test whether the response data from the API_DELETE endpoint meets expectations"""
    # Delete with invalid ID
    response = client.delete(str.replace(API_DELETE_JOKE_REMOVE, API_ID_SUFFIX, generate_random_string(ID_MAX_LENGTH)))
    response_json = response.get_json()

    assert response.status_code == HTTP_NOT_FOUND, "API_DELETE endpoint returned an incorrect status code"
    assert response_json, "API_DELETE endpoint did not return valid JSON"
    assert ERROR in response_json, "error field is missing in JSON response"
    assert response_json[ERROR] == ERROR_NOT_FOUND, "unexpected error message"

    # Create a new joke
    data = {VALUE: "Hello World", ICON_URL: "https://api.chucknorris.io/img/avatar/chuck-norris.png"}
    joke_id = test_api_post_add(client, headers={"Content-Type": "application/json"}, data=data,
                                expected_status_code=HTTP_OK,
                                expected_response=data)

    # Delete with valid ID
    response = client.delete(str.replace(API_DELETE_JOKE_REMOVE, API_ID_SUFFIX, joke_id))
    response_json = response.get_json()

    assert response.status_code == HTTP_OK, "API_DELETE endpoint returned an incorrect status code"
    assert response_json == {}, "API_DELETE endpoint did not return valid JSON"

    # Query the deleted joke
    response = client.get(str.replace(API_GET_JOKE_DETAIL, API_ID_SUFFIX, joke_id))
    response_json = response.get_json()

    assert response.status_code == HTTP_NOT_FOUND, "API_GET_JOKE_DETAIL endpoint returned an incorrect status code"
    assert response_json, "API_GET_JOKE_DETAIL endpoint did not return valid JSON"
    assert ERROR in response_json, "error field is missing in JSON response"
    assert response_json[ERROR] == ERROR_NOT_FOUND, "unexpected error message"


if __name__ == '__main__':
    pytest.main()
