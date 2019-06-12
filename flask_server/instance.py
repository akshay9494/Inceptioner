from flask import Flask
from flask_restplus import Api, Namespace
from configuration.instance import config
from waitress import serve


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            version='1.0',
            title='Inception Image Recognition API',
            description='Recognize images based on the inception model trained on imagenet data',
            doc='/api/swagger'
        )
        self.inceptioner_ns = Namespace('inceptioner', description='Image recognition with Inception V3')
        self.api.add_namespace(self.inceptioner_ns)

    def run(self):
        serve(self.app, host='0.0.0.0', port=config.port)


server = Server()