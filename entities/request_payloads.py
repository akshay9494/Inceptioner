from marshmallow import Schema, fields, post_load

class RecognitionRequestSchema(Schema):
    id = fields.Str(required=True)
    base64String = fields.Str(required=True)