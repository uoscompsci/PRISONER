from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request, Response, BaseRequest
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect, cached_property

from workflow import PolicyProcessor, SocialObjectGateway, ExperimentBuilder

import csv
import os

class PRISONER(object):
	""" PRISONER Web Service
	Exposes the functionality of PRISONER through a RESTful API.	
	Participation clients should use this API to manage social objects.

	The PRISONER web service requires the following flow:

	1) Call / to handshake with PRISONER. Use returned PRISession cookie
	in future requests

	2) Call /begin with the following POST payload:
		'policy': URL to your experiment's privacy policy
		'design': URL to your experimental design
		'participant': The ID of the current participant
		'providers': A comma-seperated list of services the participant
		must be authenticated with

	3) PRISONER will return a URL your participant must visit to complete
	their consent and authentication flow. Call this and append an (escaped)
	argument "callback" - this is the URL your participant should be
	returned to, to begin using your experiment

	4) From this point onwards, use PRISONER to request objects:
		/get/<provider>/<object_name>/<payload>/<criteria>
	
		eg. to get a participant's favourite tracks by Pixies on Last.fm we query:
		/get/Lastfm/Track/session:Lastfm.id/x.artist=="Pixies"
		
		(for readability we have not escaped this query string - this
		must be safely encoded before making requests!)

	  To publish objects:
		/post/<provider>/<object_name>
		with a form-encoded payload of the data to publish.
	
		eg. to publish a comment to my own Last.fm profile, we query:
		/post/Lastfm/Comment
		{'author': session:Lastfm.id,
		'inReplyTo': session:Lastfm.id,
		'content': "Test comment" }	

	 To store experimental responses:
		/response
		with a form-encoded payload matching the response schema in your
		experimental design.
	
		eg. to publish a response to a question about a favourite track,
		we query:
		/response
		{'track': 246746,
		'answer': "My response",
		}	

	Note that the PRISONER Web Service returns JSON objects corresponding to
	instances of Social Objects. Each object in a JSON response includes a "prisoner_id"
	attribute. Use this to subsequently relate a request to a previous
	object you received. PRISONER will lookup the original object based on
	this identifier. For example, in our experimental response above, we
	provided a track ID. This allows requests to be lightweight while
	PRISONER temporarily stores the complete version of that object.
	"""

	def __init__(self):
		self.url_map = Map([
			Rule('/', endpoint="handshake"),
			Rule('/begin', endpoint="begin"),
			Rule('/get/<string:provider>/<string:object_name>/<string:payload>/<string:criteria>',
			endpoint="get_object"),
			Rule('/get/<string:provider>/<string:object_name>/<string:payload>',
			endpoint="get_object"),
			Rule('/post', endpoint="post_response"),
			Rule('/publish', endpoint="publish_object")
			

		])
		self.session_store = FilesystemSessionStore()
		self.session_internals = {}

	def get_builder_reference(self, request):
		""" Each session has its own instance of PRISONER's internals,
		keyed on the session cookie.
		"""
		return self.session_internals[request.cookies.get("PRISession")]

	def set_builder_reference(self, request, builder):
		self.session_internals[request.cookies.get("PRISession")] = builder
		print "set session for %s" % request.cookies.get("PRISession")
		return self.get_builder_reference(request)

	def on_handshake(self, request):
		""" This initial call provides the client with their session
		token. If response is good, call /begin with cookie set
		"""
		return Response("Welcome to PRISONER. Now call /begin to "+\
		"initialise your experiment, supplying the PRISession cookie.")		

	def on_begin(self, request):
		builder = self.set_builder_reference(request,ExperimentBuilder.ExperimentBuilder())
	

		# test with hard-coded
		"""
		privacy_policy = "../lib/lastfm_privacy_policy_test.xml"
		exp_design = "../lib/lastfm_exp_design_test.xml"

		builder.provide_privacy_policy(privacy_policy)
		builder.provide_experimental_design(exp_design)
		participant = builder.authenticate_participant("participant",1)
		builder.authenticate_providers(["Lastfm"])
		"""
		privacy_policy = request.form["policy"]
		exp_design = request.form["design"]
		builder.provide_privacy_policy(privacy_policy)
		builder.provide_experimental_design(exp_design)
		participant = builder.authenticate_participant("participant",request.form["participant"])	
	
		providers = request.form["providers"].strip().split(",")
		builder.authenticate_providers(providers)

		callback = request.args["callback"]

		consent_url = builder.build(callback)	
		return Response(consent_url)
		#return redirect(consent_url)
	
	def on_post_response(self, request):
		builder = self.get_builder_reference(request)
		schema = request.form["schema"]
		response = request.form["response"]
		post_response = builder.sog.persistence.post_response_json(builder.sog, schema,
		response)

		return Response(post_response)	

	def on_publish_object(self, request):
		pass

	def on_get_object(self, request, provider, object_name, payload,
	criteria=None):
		
		builder = self.get_builder_reference(request)
		response = builder.sog.GetObjectJSON(provider, object_name, payload,
		criteria)

		return Response(response)


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
		sid = request.cookies.get("PRISession")
		print "sid: %s" % sid
		if not sid:
			request.session = self.session_store.new()
			request.session["active"] = True
			print "set session"
		else:
			request.session = self.session_store.get(sid)


		print request.session.modified

		response = self.dispatch_request(request)
		if request.session.should_save:
			self.session_store.save(request.session)
			response.set_cookie("PRISession", request.session.sid)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)


def create_app():
	app = PRISONER()
	return app

if __name__ == "__main__":
	from werkzeug.serving import run_simple
	app = create_app()
	run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)
