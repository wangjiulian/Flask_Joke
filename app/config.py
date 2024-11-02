import os
from app.constants import *


class Config:
    """ Configuration class for the application. """
    LOGGING_LEVEL = os.environ.get(LOGGING_LEVEL) or DEFAULT_LOGGING_LEVEL
    SQLALCHEMY_DATABASE_URI = os.environ.get(DATABASE_URL) or DEFAULT_SQLALCHEMY_DATABASE_URI
    HTTP_SERVER_URL = os.environ.get(HTTP_SERVER_URL) or DEFAULT_SERVER_URL
    REPLACE_URL = HTTP_SERVER_URL + API_PREFIX + "/"
