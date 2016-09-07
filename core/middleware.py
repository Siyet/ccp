from time import time
from logging import getLogger

class LoggingMiddleware(object):
    def __init__(self):
        self.logger = getLogger('request')

    def process_response(self, request, response):
        self.logger.info(request.path)
        self.logger.info(request.GET)
        self.logger.info(request.POST)
        self.logger.info('%s\n%s' % (response.status_code, response.content))
        return response