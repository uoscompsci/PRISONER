from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.urls import url_fix

import SocialObjects
from gateway import LastfmServiceGateway
from workflow import ExperimentBuilder, SocialObjectGateway

import cookielib
import urllib
import urllib2

""" Dummy web-based Last.fm participation client """

PRISONER_URI = "http://127.0.0.1:5000"
SELF_URI = "http://127.0.0.1:1457"

class LastFmExperimentClient(object):
	def __init__(self):
		self.url_map = Map([
			Rule('/', endpoint="start"),
			Rule('/start', endpoint="auth_done")
		])

	def on_start(self, request):
		redir = "%s/begin?callback=%s/start" % (PRISONER_URI, SELF_URI)
		return redirect(redir)

	def on_auth_done(self, request):
		""" Run the dummy experiment here """
		# hold onto the PRISession so we use it in future requests
		self.cookie = request.cookies["PRISession"]	

		request_url = "%s/get/%s/%s/%s" % (PRISONER_URI, "Lastfm", "Track",
		"session:Lastfm.id")
		request = urllib2.Request(url_fix(request_url))
		request.add_header("Cookie","PRISession=%s" % self.cookie)

	
		api_response = urllib2.urlopen(request)
		resp = api_response.read()
		return Response(resp)
	

		
	


	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, "on_" + endpoint)(request,
			**values)
		except HTTPException, e:
			return e
	
	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)


def create_app():
	app = LastFmExperimentClient()
	return app

if __name__ == "__main__":
	from werkzeug.serving import run_simple
	app = create_app()
	run_simple("127.0.0.1", 1457, app, use_debugger=True, use_reloader=True)
