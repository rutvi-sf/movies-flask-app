from marshmallow import Schema, fields


class MoviesSerializer(Schema):
    """Serialize/Deserialize Movie Objects"""

    id = fields.UUID(dump_only=True)
    director = fields.String(allow_none=False)
    name = fields.String(allow_none=False)
    imdb_score = fields.Float(allow_nan=False)
    popularity = fields.Float(data_key="99popularity")
