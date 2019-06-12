# from services.nameko_service import Service, InceptionerService
# from services.http_exceptions import Service
from configuration import logging
from flask_server.instance import server
from services.flask_restplus_service import *
from configuration.instance import config


if __name__ == '__main__':
    server.run()