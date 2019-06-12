from marshmallow import Schema, fields, post_load

class RecognitionRequestSchema(Schema):
    base64_payload = fields.Str(required=True)