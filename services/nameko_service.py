# from nameko.web.handlers import http
from nameko.messaging import consume
from kombu.messaging import Exchange, Queue
import json
from entities.request_payloads import RecognitionRequestSchema
import logging

import json
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response
from nameko.exceptions import safe_for_serialization


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class InvalidArgumentsError(HttpError):
    error_code = 'INVALID_ARGUMENTS'


class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator


class Service:
    name = "http_service"

    @http('GET', '/other')
    def other_method(self, request):
        return json.dumps({'value': 12})


class InceptionerService:
    """Service endpoint for Inceptioner"""
    name = "inceptioner_service"

    test_exchange = Exchange('nameko_test_exchange', type='direct')
    test_queue = Queue('nameko_test_queue', exchange=test_exchange)

    @http('GET', '/get/<int:value>')
    def get_method_for_test(self, request, value):
        return json.dumps({'value': value})

    @http('GET', '/custom_exception')
    def custom_exception(self, request):
        raise InvalidArgumentsError("Argument `foo` is required.")

    @http('POST', '/recognize/base64')
    def do_post(self, request):
        logging.info('Received Request on recognition from base64')
        request_data = request.data
        logging.debug('Data Received: {}'.format(request_data))

        schema = RecognitionRequestSchema()

        result = schema.loads(request_data)

        if result.errors:
            return "wrong payload supplied"

        return u"received: {}".format(result.data)

    @consume(test_queue)
    def handle_event(self, payload):
        schema = RecognitionRequestSchema()
        result = schema.load(payload)
        print('Received message: {}'.format(payload))
