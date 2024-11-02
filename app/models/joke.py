from app.db import db
from app.constants import *
from app.config import Config


def update():
    db.session.commit()


class Joke(db.Model):
    id = db.Column(db.String(ID_MAX_LENGTH), primary_key=True)
    value = db.Column(db.String(VALUE_MAX_LENGTH), nullable=False)
    icon_url = db.Column(db.String(ICON_URL_MAX_LENGTH), nullable=False)
    url = db.Column(db.String(ICON_URL_MAX_LENGTH), nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, value, icon_url):
        self.value = value
        self.icon_url = icon_url
        db.session.commit()

    @staticmethod
    def get_by_id(joke_id):
        return Joke.query.get(joke_id)

    @staticmethod
    def search_jokes(query, limit=DEFAULT_LIMIT):
        if not query:
            return Joke.query.limit(limit).all()

        return Joke.query.filter(Joke.value.contains(query)).limit(limit).all()

    @staticmethod
    def to_joke_dict(obj):
        # Replace the Chuck Norris URL with the server URL
        url = str.replace(obj[URL], REPLACE_CHUNK_NORRIS_URL, Config.REPLACE_URL)
        return {ID: obj[ID], URL: url, VALUE: obj[VALUE], ICON_URL: obj[ICON_URL]}

    def model_to_dict(self):
        # Add the server URL to the URL
        self.url = f"{Config.HTTP_SERVER_URL}{self.url}"
        return {ID: self.id, URL: self.url, VALUE: self.value, ICON_URL: self.icon_url}
