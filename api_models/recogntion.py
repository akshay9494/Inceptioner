from flask_restplus import fields
from flask_server.instance import server

recognition_request = server.api.model('RecognitionRequest', {
    'id': fields.String(description='UID for maintaining traceability', required=True),
    'base64String': fields.String(description='Base64 encoded image string for the image', required=True)
})

recognition_response = server.api.model('RecognitionResponse', {
    'id': fields.String(description='UID for maintaining traceability'),
    'prediction': fields.String(description='Prediction from the image using inception'),
    'confidence': fields.Float(description='Prediction Confidence'),
    'hostname': fields.String(description='hostname from where the execution happened to check for load balancing')
})