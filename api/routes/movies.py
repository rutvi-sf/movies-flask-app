from api import api
from api.services import GetUpdateDeleteMoviesResource, ListCreateMoviesResource

api.add_resource(ListCreateMoviesResource, "/movies")
api.add_resource(GetUpdateDeleteMoviesResource, "/movies/<string:movie_id>")
