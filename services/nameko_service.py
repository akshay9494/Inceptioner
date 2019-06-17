from nameko.web.handlers import http
from nameko.messaging import consume
from kombu.messaging import Exchange, Queue
import logging
import json
from core.utilities import process_request




class InceptionerService:
    """Service endpoint for Inceptioner"""
    name = "inceptioner_service"

    test_exchange = Exchange('nameko_test_exchange', type='direct')
    test_queue = Queue('nameko_test_queue', exchange=test_exchange)

    @http('GET', '/get/<int:value>')
    def get_method_for_test(self, request, value):
        return json.dumps({'value': value})


    @http('POST', '/recognize/base64')
    def do_post(self, request):
        logging.info('Received Request on recognition from base64')
        request_data = request.data
        logging.debug('Data Received: {}'.format(request_data))
        res = process_request(request.data)
        print(res)
        return str(res)


    @consume(test_queue)
    def handle_event(self, payload):
        logging.info('Received request on recognition on the queue')
        logging.debug('Data received: {}'.format(payload))

        res = process_request(payload)
        print(res)
        return res
