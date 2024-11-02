from flask import jsonify
from app.constants import *


class Response:
    @staticmethod
    def success(obj):
        return jsonify(obj), HTTP_OK

    @staticmethod
    def not_found():
        return jsonify({ERROR: ERROR_NOT_FOUND}), HTTP_NOT_FOUND

    @staticmethod
    def bad_request(obj):
        return jsonify({ERROR: obj}), HTTP_BAD_REQUEST
