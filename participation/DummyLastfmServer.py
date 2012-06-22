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
import json
import requests
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
		self.cj = cookielib.LWPCookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)

	def on_start(self, request):

		# initial handshake - get session cookie
		handshake = urllib2.urlopen(url_fix(PRISONER_URI))
		resp_info = handshake.info()

		request_url = "%s/begin?callback=%s/start" % (PRISONER_URI, SELF_URI)
		
		post_data = {"policy": "http://pvnets.cs.st-andrews.ac.uk/prisoner/demo/lastfm_privacy_policy_test.xml",
		"design": "http://pvnets.cs.st-andrews.ac.uk/prisoner/demo/lastfm_exp_design_test.xml",
		"participant": "2",
		"providers": "Lastfm"
		}

		
		start_request = urllib2.Request(url_fix(request_url),
		data=urllib.urlencode(post_data))
		start_response = urllib2.urlopen(start_request)
	
		print "re: %s" % start_response.read()	
		return redirect(start_response.read())

	def on_auth_done(self, request):
		""" Run the dummy experiment here """
		
		request_url = "%s/get/%s/%s/%s/%s" % (PRISONER_URI, "Lastfm", "Track",
		"session:Lastfm.id",'x.artist=="Cajun Dance Party"')
		request = urllib2.Request(url_fix(request_url))

	
		api_response = urllib2.urlopen(request)
		resp = api_response.read()

		json_resp = json.loads(resp)

		# publish a dummy response based on this
		req_url = "%s/post" % PRISONER_URI
		po_data =  {"answer": "Test",
		"track": (json_resp['_objects'][0]['prisoner_id'])}

		post_full = {'schema': "response", "response":
		json.dumps(po_data)}

		post_request = urllib2.Request(url_fix(req_url),
		data = urllib.urlencode(post_full))
		post_response = urllib2.urlopen(post_request)

	

		
	


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
