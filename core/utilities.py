from configuration.instance import config
import base64
import os
from entities.request_payloads import RecognitionRequestSchema
import logging
import tensorflow as tf
from core.inceptioner import Inceptioner
import socket


inceptioner_instance = Inceptioner()
graph = tf.get_default_graph()


def process_request(json_request):
    schema = RecognitionRequestSchema()

    result = schema.loads(json_request)

    logging.debug('Unmarshalling result: {}'.format(result))

    if result.errors:
        return "wrong payload supplied"

    uid = result.data['id']
    file_name = uid + '.jpg'
    file_path = os.path.join(config.home_dir, file_name)

    base64_string = result.data['base64String']

    try:
        image = base64.decodebytes(str.encode(base64_string))
        with open(file_path, 'wb') as img:
            img.write(image)
    except Exception as e:
        logging.error(e)
        return str(e)

    try:
        with graph.as_default():
            recognition_response = inceptioner_instance.predict(file_path)
        recognition_response['id'] = uid
        recognition_response['hostname'] = socket.gethostname()
        return recognition_response
    except Exception as e:
        logging.error(e)
        return str(e)