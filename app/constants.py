""" Constants for the application. """
JokeBlueprint = 'joke'
API_PREFIX = "/api/jokes"
API_ID_SUFFIX = "<string:joke_id>"
API_INDEX = "/"
API_GET_JOKE_DETAIL = f"{API_PREFIX}/{API_ID_SUFFIX}"
API_GET_JOKE_SEARCH = f"{API_PREFIX}/search"
API_POST_JOKE_ADD = API_PREFIX
API_PUT_JOKE_UPDATE = f"{API_PREFIX}/{API_ID_SUFFIX}"
API_DELETE_JOKE_REMOVE = f"{API_PREFIX}/{API_ID_SUFFIX}"

DATABASE_URL = "DATABASE_URL"
HTTP_SERVER_URL = "HTTP_SERVER_URL"
DEFAULT_SERVER_URL = "http://127.0.0.1:5000"
DEFAULT_SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

# Models Column Length
ID_MAX_LENGTH = 30
VALUE_MIN_LENGTH = 3
VALUE_MAX_LENGTH = 200
ICON_URL_MAX_LENGTH = 200
URL_MAX_LENGTH = 100
DEFAULT_LIMIT = 10

# HTTP Methods
HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"

# Request Parameters
ID = "id"
VALUE = "value"
ICON_URL = "icon_url"
URL = "url"
RESULT = "result"
TOTAL = "total"
QUERY = "query"
QUERY_MIN_LENGTH = 3
QUERY_MAX_LENGTH = 120

# HTTP Status Codes
HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500
# Error Messages
ERROR = "error"
ERROR_NO_ID = "No id provided"
ERROR_NOT_FOUND = "not found"
ERROR_INVALID_JSON = "Invalid JSON"
ERROR_NO_JSON = "No JSON provided"
ERROR_NO_VALUE = "No value provided"
ERROR_NO_ICON_URL = "No icon url provided"
ERROR_INVALID_ICON_URL_FORMAT = "Invalid icon url format provided"
ERROR_INVALID_ICON_URL_ACCESS = "Invalid icon url access provided"
ERROR_NO_QUERY = "No query provided"
ERROR_INVALID_QUERY_LENGTH = f"query size must be between {QUERY_MIN_LENGTH} and {QUERY_MAX_LENGTH}"
ERROR_INVALID_VALUE_LENGTH = f"value size must be between {VALUE_MIN_LENGTH} and {VALUE_MAX_LENGTH}"
ERROR_INVALID_ICON_URL_LENGTH = f"icon url size must not be more than {ICON_URL_MAX_LENGTH}"

""" Chuck Norris constants. """
# Chuck Norris API
API_CHUNK_NORRIS_URL = "https://api.chucknorris.io/"
API_CHUNK_NORRIS_RANDOM = API_CHUNK_NORRIS_URL + "jokes/random"
API_CHUNK_NORRIS_DETAIL = API_CHUNK_NORRIS_URL + "jokes/{}"
API_CHUNK_NORRIS_SEARCH = API_CHUNK_NORRIS_URL + "jokes/search?query={}"

REPLACE_CHUNK_NORRIS_URL = f"{API_CHUNK_NORRIS_URL}jokes/"
