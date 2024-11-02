import uuid
from app.constants import *
from app.config import Config
import re
import requests


# Replaces the Chuck Norris URL with the server URL.
def replace_chunk_norris_url(obj):
    url = str.replace(obj[URL], REPLACE_CHUNK_NORRIS_URL, Config.REPLACE_URL)
    obj[URL] = url


def generate_uuid_string(length=30):
    return str(uuid.uuid4()).replace('-', '')[:length]


def check_image_accessible(url):
    try:
        response = requests.head(url)
        # 检查状态码和内容类型
        return response.status_code == HTTP_OK and 'image' in response.headers.get('Content-Type', '')
    except requests.RequestException:
        return False


def is_image_url(url):
    pattern = r'^https?:\/\/.*\.(jpg|jpeg|png|gif|bmp|webp|tiff)$'
    return re.match(pattern, url, re.IGNORECASE) is not None
