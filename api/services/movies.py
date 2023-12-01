from flask import request
from flask_restful import Resource, abort

from api import db
from api.models import Movies, UserRoles
from api.serializers import MoviesSerializer
from api.utils.decorators import allow_only_roles, dump_request, load_request


class ListCreateMoviesResource(Resource):
    """
    API Resource to Create and List Movies
    Allowed Verbs: GET/POST
    Request Payload:[
        {
            "99popularity": 83.0,
            "director": "Victor Fleming",
            "genre": [
                "Adventure",
                " Family",
                " Fantasy",
                " Musical"
            ],
            "imdb_score": 8.3,
            "name": "The Wizard of Oz"
        },
        {
            "99popularity": 88.0,
            "director": "George Lucas",
            "genre": [
                "Action",
                " Adventure",
                " Fantasy",
                " Sci-Fi"
            ],
            "imdb_score": 8.8,
            "name": "Star Wars"
        }
    ]

    Response Object:[
        {
            "id": "0161ba59-fd6b-4b64-82c6-70307a5d2128",
            "director": "John G. Avildsen",
            "name": "The Karate Kid",
            "imdb_score": 6.9,
            "99popularity": 69.0
        },
        {
            "id": "01b16896-1c8c-4cd5-888c-cad429bb0265",
            "director": "Lee Sholem",
            "name": "Tarzans Magic Fountain",
            "imdb_score": 5.5,
            "99popularity": 55.0
        }
    ]
    """

    @allow_only_roles(allowed_roles=[UserRoles.ADMIN])
    @load_request(MoviesSerializer(many=True, unknown="exclude"))
    def post(self, serialized_payload: list):
        Movies.bulk_insert(serialized_payload)
        return "Inserted", 201

    @dump_request(MoviesSerializer(many=True))
    def get(self):
        movies = Movies.query

        if request.args.get("search"):
            movies = movies.filter(Movies.name.like(f"%{request.args.get('search')}%"))
        return movies


class GetUpdateDeleteMoviesResource(Resource):
    """
    API Resource to Create and List Movies
    Allowed Verbs: GET/PATCH/DELETE
    Request Payload:{
        "99popularity": 83.0,
        "director": "Victor Fleming",
        "genre": [
            "Adventure",
            " Family",
            " Fantasy",
            " Musical"
        ],
        "imdb_score": 8.3,
        "name": "The Wizard of Oz"
    }

    Response Object:{
        "id": "0161ba59-fd6b-4b64-82c6-70307a5d2128",
        "director": "John G. Avildsen",
        "name": "The Karate Kid",
        "imdb_score": 6.9,
        "99popularity": 69.0
    }
    """

    @allow_only_roles(allowed_roles=[UserRoles.ADMIN])
    @load_request(MoviesSerializer(unknown="exclude"))
    def patch(self, movie_id: str, serialized_payload: list):
        Movies.update(movie_id, serialized_payload)
        return "Updated", 200

    @allow_only_roles(allowed_roles=[UserRoles.ADMIN])
    def delete(self, movie_id: str):
        Movies.query.filter(Movies.id == movie_id).delete()
        db.session.commit()
        return "DELETED", 204

    @dump_request(MoviesSerializer())
    def get(self, movie_id: str):
        return Movies.query.get(movie_id) or abort(404, message="Movie not found")
