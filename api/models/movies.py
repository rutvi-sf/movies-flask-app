import uuid

from sqlalchemy import Float, String
from sqlalchemy.orm import mapped_column

from api import db


class Movies(db.Model):
    """
    DB Model for Movies
    """

    id = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    director = mapped_column(String(200), nullable=False, index=True)
    name = mapped_column(String(200), nullable=False, index=True)
    imdb_score = mapped_column(Float(1), nullable=False, default=0)
    popularity = mapped_column(Float(1), nullable=False, default=0)

    @staticmethod
    def bulk_insert(movies_list: list) -> None:
        movies_objs = [Movies(**movie) for movie in movies_list]

        db.session.bulk_save_objects(movies_objs)
        db.session.commit()

    @staticmethod
    def update(movie_id: str, updated_dictionary: dict) -> None:
        movie = Movies.query.get(movie_id)

        for key, value in updated_dictionary.items():
            setattr(movie, key, value)

        db.session.commit()
