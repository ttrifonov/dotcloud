import django.core.handlers.wsgi
import os
import random
import logging
import sys

from threading import Lock
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django import http
from django.core import signals
from django.core.handlers import base
from django.core.urlresolvers import set_script_prefix
from django.utils import datastructures
from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.log import getLogger

logger = getLogger('django.request')
STATUS_CODE_TEXT = {
	    100: 'CONTINUE',
	    101: 'SWITCHING PROTOCOLS',
	    102: 'PROCESSING',
	    200: 'OK',
	    201: 'CREATED',
	    202: 'ACCEPTED',
	    203: 'NON-AUTHORITATIVE INFORMATION',
	    204: 'NO CONTENT',
	    205: 'RESET CONTENT',
	    206: 'PARTIAL CONTENT',
	    207: 'MULTI-STATUS',
	    208: 'ALREADY REPORTED',
	    226: 'IM USED',
	    300: 'MULTIPLE CHOICES',
	    301: 'MOVED PERMANENTLY',
	    302: 'FOUND',
	    303: 'SEE OTHER',
	    304: 'NOT MODIFIED',
	    305: 'USE PROXY',
	    306: 'RESERVED',
	    307: 'TEMPORARY REDIRECT',
	    400: 'BAD REQUEST',
	    401: 'UNAUTHORIZED',
	    402: 'PAYMENT REQUIRED',
	    403: 'FORBIDDEN',
	    404: 'NOT FOUND',
	    405: 'METHOD NOT ALLOWED',
	    406: 'NOT ACCEPTABLE',
	    407: 'PROXY AUTHENTICATION REQUIRED',
	    408: 'REQUEST TIMEOUT',
	    409: 'CONFLICT',
	    410: 'GONE',
	    411: 'LENGTH REQUIRED',
	    412: 'PRECONDITION FAILED',
	    413: 'REQUEST ENTITY TOO LARGE',
	    414: 'REQUEST-URI TOO LONG',
	    415: 'UNSUPPORTED MEDIA TYPE',
	    416: 'REQUESTED RANGE NOT SATISFIABLE',
	    417: 'EXPECTATION FAILED',
	    422: 'UNPROCESSABLE ENTITY',
	    423: 'LOCKED',
	    424: 'FAILED DEPENDENCY',
	    426: 'UPGRADE REQUIRED',
	    500: 'INTERNAL SERVER ERROR',
	    501: 'NOT IMPLEMENTED',
	    502: 'BAD GATEWAY',
	    503: 'SERVICE UNAVAILABLE',
	    504: 'GATEWAY TIMEOUT',
	    505: 'HTTP VERSION NOT SUPPORTED',
	    506: 'VARIANT ALSO NEGOTIATES',
	    507: 'INSUFFICIENT STORAGE',
	    508: 'LOOP DETECTED',
	    510: 'NOT EXTENDED',
	}


SETTINGS = [
    "app1.settings",
    "app2.settings",
]

class HandlerWrapper(django.core.handlers.wsgi.WSGIHandler):
    def __call__(self, environ, start_response):
	print environ
        ind = random.randint(1, 10) % 2
        logging.error("before: %s" % os.environ.get('DJANGO_SETTINGS_MODULE', "Unknown"))
        os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS[ind]
        logging.error("after: %s" % os.environ.get('DJANGO_SETTINGS_MODULE', "Unknown"))

        from django.conf import settings

        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._request_middleware is None:
            self.initLock.acquire()
            try:
                try:
                    # Check that middleware is still uninitialised.
                    if self._request_middleware is None:
                        self.load_middleware()
                except:
                    # Unload whatever middleware we got
                    self._request_middleware = None
                    raise
            finally:
                self.initLock.release()

        set_script_prefix(base.get_script_name(environ))
        signals.request_started.send(sender=self.__class__)
        try:
            try:
                request = self.request_class(environ)
            except UnicodeDecodeError:
                logger.warning('Bad Request (UnicodeDecodeError)',
                    exc_info=sys.exc_info(),
                    extra={
                        'status_code': 400,
                    }
                )
                response = http.HttpResponseBadRequest()
            else:
                response = self.get_response(request)
        finally:
            signals.request_finished.send(sender=self.__class__)

        try:
            status_text = STATUS_CODE_TEXT[response.status_code]
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        status = '%s %s' % (response.status_code, status_text)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append(('Set-Cookie', str(c.output(header=''))))
        start_response(status, response_headers)
        return response

application = HandlerWrapper()

