from flask_restplus import Resource, Namespace, reqparse
from flask_server.instance import server
from api_models.recogntion import recognition_request, recognition_response
import logging
import base64
from flask import abort
from configuration.instance import config
from core.inceptioner import Inceptioner
import tensorflow as tf
import os
import werkzeug
import uuid
import socket

file_upload = reqparse.RequestParser()
file_upload.add_argument(
    'image_file',
    type=werkzeug.datastructures.FileStorage,
    location='files',
    required=True,
    help='image file'
)


inceptioner_instance = Inceptioner()
graph = tf.get_default_graph()

ns = Namespace('inceptioner', description='Image recognition with Inception V3')

app, api = server.app, server.inceptioner_ns


@api.route('/recognize/base64')
class RecognizeBase64(Resource):
    @api.expect(recognition_request)
    @api.marshal_with(recognition_response)
    def post(self):
        logging.info('received post request for classification with base64')

        uid = self.api.payload['id']
        file_name = uid+'.jpg'
        file_path = os.path.join(config.home_dir, file_name)

        base64_string = self.api.payload['base64String']

        try:
            image = base64.decodebytes(str.encode(base64_string))
            with open(file_path, 'wb') as img:
                img.write(image)
        except Exception as e:
            logging.error(e)
            abort(400, str(e))

        try:
            with graph.as_default():
                recognition_response = inceptioner_instance.predict(file_path)
            recognition_response['id'] = uid
            recognition_response['hostname'] = socket.gethostname()
            return recognition_response
        except Exception as e:
            logging.error(e)
            abort(500, str(e))


@api.route('/recognize/file')
class RecognizeFile(Resource):
    @api.expect(file_upload)
    @api.marshal_with(recognition_response)
    def post(self):
        logging.info('received post request for classification with file')

        args = file_upload.parse_args()
        file_extension = args['image_file'].filename.split('.')[-1]

        uid = uuid.uuid4()

        file_name = str(uid) + '.{}'.format(file_extension)
        file_path = os.path.join(config.home_dir, file_name)

        args['image_file'].save(file_path)

        try:
            with graph.as_default():
                recognition_response = inceptioner_instance.predict(file_path)
            recognition_response['id'] = uid
            recognition_response['hostname'] = socket.gethostname()
            return recognition_response
        except Exception as e:
            logging.error(e)
            abort(500, str(e))