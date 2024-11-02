import traceback

from flask import jsonify, current_app
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

    @staticmethod
    def InternalServerError(title, e):
        current_app.logger.error(f"{title} occurred error: %s\n%s", str(e), traceback.format_exc())
        return jsonify({ERROR: ERROR_INTERNAL_SERVER_ERROR}), HTTP_INTERNAL_SERVER_ERROR
