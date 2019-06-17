from flask import Flask
from flask_restplus import Api, Namespace

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Inception Image Recognition API',
    description='Recognize images based on the inception model trained on imagenet data',
    doc='/api/swagger'
)
inceptioner_ns = Namespace('inceptioner', description='Image recognition with Inception V3')
api.add_namespace(inceptioner_ns)