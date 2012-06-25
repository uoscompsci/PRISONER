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

import Cookie
import cookielib
import json
import requests
import time
import urllib
import urllib2
import urlparse

""" Dummy web-based Last.fm participation client """

PRISONER_URI = "http://127.0.0.1:5000"
SELF_URI = "http://127.0.0.1:1457"


class LastFmExperimentClient(object):
	def __init__(self):
		self.url_map = Map([
			Rule('/', endpoint="start"),
			Rule('/start', endpoint="auth_done")
		])
		#self.cj = cookielib.LWPCookieJar()
		#self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		#urllib2.install_opener(self.opener)

	def __append_session_to_url(self, url, session):
		if urlparse.urlparse(url)[4]:
			return "%s&PRISession=%s" % (url, session)
		else:
			return "%s?PRISession=%s" % (url, session)

	def on_start(self, request):

		# initial handshake - get session cookie
		handshake = urllib2.urlopen(url_fix(PRISONER_URI))
		resp_info = handshake.info()
		print "handshake: %s" % resp_info
		prisession = resp_info["PRISession"]		
	
		request_url = self.__append_session_to_url("%s/begin?callback=%s/start?PRISession=%s" % (PRISONER_URI,
		SELF_URI, prisession), prisession)
		print request_url
		
		post_data = {"policy": "http://pvnets.cs.st-andrews.ac.uk/prisoner/demo/lastfm_privacy_policy_test.xml",
		"design": "http://pvnets.cs.st-andrews.ac.uk/prisoner/demo/lastfm_exp_design_test.xml",
		"participant": "2",
		"providers": "Lastfm"
		}
	
		start_request = urllib2.Request(url_fix(request_url),
		data=urllib.urlencode(post_data))
		start_response = urllib2.urlopen(start_request)
		#re = Response(start_response.read())
		re = redirect(start_response.read())
		re.content_type = "text/html"
		print "response heads: %s" % re.headers
		return re

	def on_auth_done(self, request):
		""" Run the dummy experiment here """
		prisession = request.args["PRISession"]
		# get tracks matching criteria	
		request_url = "%s/get/%s/%s/%s/%s?async" % (PRISONER_URI, "Lastfm", "Track",
		"session:Lastfm.id",'x.artist=="Cajun Dance Party"')
		request_url = self.__append_session_to_url(request_url, prisession)
		request = urllib2.Request(url_fix(request_url))
		api_response = urllib2.urlopen(request)
		resp = api_response.read()
		json_resp = json.loads(resp)

		time.sleep(1)

		# repeat that to test caching
		request_url = "%s/get/%s/%s/%s/%s?isready" % (PRISONER_URI, "Lastfm", "Track",
		"session:Lastfm.id",'x.artist=="Cajun Dance Party"')
		request_url = self.__append_session_to_url(request_url,
		prisession)
		request = urllib2.Request(url_fix(request_url))
		api_response = urllib2.urlopen(request)
		resp = api_response.read()
		print "cache resp: %s" % resp
		json_resp = json.loads(resp)
	
		# test writing and reading session
		post_session = {"key": "test", "data": "session test"}
		session_url = "%s/session/write" % PRISONER_URI
		session_url = self.__append_session_to_url(session_url,
		prisession)
		session_request = urllib2.Request(url_fix(session_url),
		data=urllib.urlencode(post_session))
		session_response = urllib2.urlopen(session_request)

		session_read_url = "%s/session/read?key=test" % PRISONER_URI
		session_read_url = self.__append_session_to_url(session_read_url, prisession)
		session_read_req = urllib2.Request(url_fix(session_read_url))
		session_read_resp = urllib2.urlopen(session_read_req)
		session_text = session_read_resp.read()

		# publish a dummy response based on this
		req_url = "%s/post" % PRISONER_URI
		req_url = self.__append_session_to_url(req_url, prisession)
		po_data =  {"answer": "Test",
		"track": (json_resp['_objects'][0]['prisoner_id'])}

		post_full = {'schema': "response", "response":
		json.dumps(po_data)}

		post_request = urllib2.Request(url_fix(req_url),
		data = urllib.urlencode(post_full))
		post_response = urllib2.urlopen(post_request)
		
		return Response("Done. got from session: %s" % session_text)

	

		
	


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
