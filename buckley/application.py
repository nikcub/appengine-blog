from google.appengine.ext.webapp import *
import logging

class AppAuthError(Exception):
	pass
	
class Application(WSGIApplication):

	_Application__debug = True
	
	def __call__(self, environ, start_response):
		"""Called by WSGI when a request comes in."""
		request = self.REQUEST_CLASS(environ)
		response = self.RESPONSE_CLASS()

		WSGIApplication.active_instance = self

		handler = None
		groups = ()
		for regexp, handler_class in self._url_mapping:
			match = regexp.match(request.path)
			if match:
				try:
					handler = handler_class()
					handler.initialize(request, response)
					groups = match.groups()
					break
				except AppAuthError:
					logging.info('caught AppAuthError')

		self.current_request_args = groups

		if handler:
			try:
				method = environ['REQUEST_METHOD']
				if method == 'GET':
					handler.get(*groups)
				elif method == 'POST':
					handler.post(*groups)
				elif method == 'HEAD':
					handler.head(*groups)
				elif method == 'OPTIONS':
					handler.options(*groups)
				elif method == 'PUT':
					handler.put(*groups)
				elif method == 'DELETE':
					handler.delete(*groups)
				elif method == 'TRACE':
					handler.trace(*groups)
				else:
					handler.error(501)
			except Exception, e:
				handler.handle_exception(e, self.__debug)
		else:
			response.set_status(404)

		response.wsgi_write(start_response)
		return ['']