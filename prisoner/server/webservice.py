from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request, Response, BaseRequest
from werkzeug.routing import Map, Rule
from werkzeug.exceptions  	import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect, cached_property

from jinja2 import Environment, FileSystemLoader

from prisoner.workflow import PolicyProcessor, SocialObjectGateway,ExperimentBuilder
from prisoner.workflow.Exceptions import *
from prisoner import SocialObjects

import csv
import datetime
import json
import jsonpickle
import os
import subprocess
import thread
import urllib
import urllib2


# set this to the URL of your PRISONER instance
#SERVER_URL = "https://prisoner.cs.st-andrews.ac.uk/prisoner"
SERVER_URL = "http://localhost:5000"

COOKIE_KEY = os.urandom(20)

dir = os.path.dirname(__file__)
TEMPLATE_URL =  os.path.join(dir, "../static")


class PRISONER(object):
	""" PRISONER Web Service
	Exposes the functionality of PRISONER through a RESTful API.
	Participation clients should use this API to manage social objects.

	The PRISONER web service requires the following flow:

	1) Call / to handshake with PRISONER. Returns a PRISession header whose
	value must be passed to all future requests as a PRISession argument

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

		Append a '?async' parameter to perform this request
		asynchronously.
		Call the same URL, but with a '?isready' parameter to get the
		result (if it's not ready yet, expect blank response)

	  To publish objects:
		/publish/<provider>/<object_name>
		with a form-encoded payload of the data to publish.

		eg. to publish a comment to my own Last.fm profile, we query:
		/publish/Lastfm/Comment
		{'author': session:Lastfm.id,
		'inReplyTo': session:Lastfm.id,
		'content': "Test comment" }

	 To store experimental responses:
		/post
		with a form-encoded payload matching the response schema in your
		experimental design.

		eg. to publish a response to a question about a favourite track,
		we query:
		/response
		{'track': 5343gt32-g43519500-223f,
		'answer': "My response",
		}

	5) PRISONER provides a simple session layer for *temporarily* storing
	state information (eg. one set of responses by a participant in a multi-step
	form). To write to the session store call:
		/session/write/
		with a form-encoded 'key' and 'data' (any arbitrary data can be
		stored)

	Later, to retrieve session data, call:
		/session/read/<key>

	Note that the session store is *not* persistent, and there are no
	guarantees how long this data will be accessible. For permanent data, use the
	experiment response interface.

	Note that the PRISONER Web Service returns JSON objects corresponding to
	instances of Social Objects. Each object in a JSON response includes a "prisoner_id"
	attribute. Use this to subsequently relate a request to a previous
	object you received. PRISONER will lookup the original object based on
	this identifier. For example, in our experimentntal response above, we
	provided a track ID. This allows requests to be lightweight while
	PRISONER temporarily stores the complete version of that object.
	"""

	def __init__(self):
		self.url_map = Map([
			Rule('/', endpoint="handshake"),
			Rule('/begin', endpoint="begin"),
			Rule('/register', endpoint="register"),
			Rule('/schema', endpoint="schema"),
			Rule('/get/<string:provider>/<string:object_name>/<string:payload>/<string:criteria>',
			endpoint="get_object"),
			Rule('/get/<string:provider>/<string:object_name>/<string:payload>',
			endpoint="get_object"),
			Rule('/post', endpoint="post_response"),
			Rule('/publish/<string:provider>/<string:object_name>', endpoint="publish_object"),
			Rule('/session/write',
			endpoint="session_write"),
			Rule('/session/read',
			endpoint="session_read"),
			# start old ExpBuilder server migration
			Rule('/start_consent', endpoint="consent"),
			Rule('/confirm', endpoint="confirm"),
			Rule('/complete', endpoint="complete"),
			Rule('/<string:wildcard>', endpoint="fallback"),
			Rule('/cancel', endpoint="cancel"),
			Rule('/invalidate', endpoint="invalidate")
			#Rule('/instancewsgirestart',endpoint="restart")


		])
		self.session_store = FilesystemSessionStore()
		self.session_internals = {}
		self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_URL), autoescape=True)

	def render_template(self, template_name, **context):
		"""
		Return the given template populated with content
		:param template_name: Name of the template file to render
		:type template_name: str
		:param context: Additional context
		:returns: Response
		"""

		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype="text/html")

	def get_builder_reference(self, request):
		""" Each session has its own instance of PRISONER's internals,
		keyed on the session cookie.

		:param request: Current HTTP request
		:returns: The ExperimentBuilder for this session
		"""
		return self.session_internals[request.sessionid]

	def set_builder_reference(self, request, builder):
		""" Attach this ExperimentBuilder to the current session.

		:param request: Current HTTP request
		:param builder: Instance of ExperimentBuilder to Attach
		:type builder: ExperimentBuilder
		:returns: ExperimentBuilder
		"""

		prisession = request.sessionid
		self.session_internals[prisession] = builder
		return self.get_builder_reference(request)

	def on_invalidate(self, request, session):
		""" Invalidate the current session, removing it from memory.
		Call this  at the end of the experiment to remove its footprint,
		or in the event of an irrecoverable error, from which you do not want the
		participant to recover without restarting the experiment flow

		:param request: Current HTTP request
		:param session: Session ID to invalidate
		:type session: str
		"""
		priSession = session

		self.session_internals[priSession].sog.persistence.close_connection()

		del self.session_internals[priSession]
		return Response("session invalidated")


	def on_cancel(self, request):
		""" Call if the participant does not provide consent and revokes
		participation. Should also invalidate and remove any session identifiers.

		:param request: Current HTTP request
		"""

		builder = self.get_builder_reference(request)
		return self.render_template("cancel.html",
		exp_contact=builder.contact, exp_name=builder.title)

	def __validate_secret(self, builder, request):
			""" Validates that the secure request provided the correct secret.

			:param builder: The current ExperimentBuilder
			:type builder: ExperimentBuilder
			:param request: The current HTTP request
			"""

			secret = request.form['secret']
			design_secret = builder.get_props("PRISONER")['secret']
			if secret != design_secret:
				raise IncorrectSecretError()



	def on_register(self, request):
		""" Register a participant. Requires a URL for the experimental
		design and privacy policy, and a form of columns to insert about this participant.

		:param request: Current HTTP request
		:returns: HTTP response to confirm the ID of the registered participant
		"""

		builder = self.set_builder_reference(request,
		ExperimentBuilder.ExperimentBuilder())



		exp_design = request.form["design"]
		policy = request.form["policy"]

		builder.provide_privacy_policy(policy)

		builder.provide_db_string(request.form["db"])
		builder.provide_experimental_design(exp_design)

		self.__validate_secret(builder,request)
		schema = request.form["schema"]

		write_out = {}
		for key in request.form.keys():
			if key not in ["design","policy","schema"]:
				write_out[key] = request.form[key]
		participant = builder.sog.register_participant(schema,
		write_out)
		return Response(str(participant[0]))

	def on_schema(self, request):
		""" Builds the database schema matching this experimental design.

		:param request: Current HTTP request
		:returns: Response to confirm the schema was built successfully.
		"""

		builder = self.set_builder_reference(request,
		ExperimentBuilder.ExperimentBuilder())

		exp_design = request.form["design"]
		policy = request.form["policy"]


		builder.provide_privacy_policy(policy)
		builder.provide_db_string(request.form["db"])
		builder.provide_experimental_design(exp_design)

		self.__validate_secret(builder,request)

		builder.build_schema()

		return Response("Schema built")


	def on_session_write(self, request, session):
		""" Writes arbitrary data to a temporary session. A
		session is bound to a PRISession, and is intended to retain state data
		during an experiment before committing to database.
		There is no guarantee how long the session will be
		valid for, so gracefully handle instances where expected data cannot
		be retrieved.

		To write session data, provide a POST form with a
		"key" value (used to retrieve the data later) and
		"data" (the arbitrary session data to store).

		:param request: Current HTTP request including session data to write
		:param session: The session to write data to
		:returns: Empty response if successful
		"""

		builder = self.get_builder_reference(request)
		builder.session[session][request.form["key"]] = request.form["data"]
		return Response()

	def on_session_read(self, request, session):
		""" Read the session data corresponding to the given key
		parameter. Session data is bound to the active PRISession.

		:param request: Current HTTP request with a key argument of which data to read
		:param session: Session we're reading data from
		:returns: HTTP response with JSON object of returned data
		 """

		builder = self.get_builder_reference(request)
		if request.args["key"] not in builder.session[session]:
			return Response("Key not in session",status=404)
		return Response(json.dumps(builder.session[session][request.args["key"]]))

	def on_handshake(self, request):
		""" This initial call provides the client with their session
		token. If response is good, call /begin providing the given
		PRISession value.

		:param request: Current HTTP response
		:returns: HTTP response to confirm handshake.
		"""

		response = Response("Welcome to PRISONER. Now call /begin to "+\
		"initialise your experiment, supplying the PRISession parameter.")
		return response

	def on_begin(self, request):
		""" 
		Initialises the flow of an experiment. This endpoint must be provided with the
		following arguments:

		policy: the URL to the privacy policy XML file

		design: the URL to the experimental design XML file

		title: the name of the experiment

		contact: the email address of the researcher

		db: a connection string (must have SQLAlchemy bindings to be supported) for
		PRISONER to store data to
		participant: form data to register the current participant

		providers: a comma-delimited list of all social network sites this experiment
		connects to

		callback: which URL for your experiment to redirect the participant to after
		successful authentication

		:type request: HTTP Request containing all outlined data
		:returns: Response for participant to be redirected to
		"""
		session = request.sessionid

		builder = self.set_builder_reference(request,ExperimentBuilder.ExperimentBuilder())

		privacy_policy = request.form["policy"]
		exp_design = request.form["design"]
		builder.provide_privacy_policy(privacy_policy)

		builder.provide_title(request.form["title"])
		builder.provide_contact(request.form["contact"])

		builder.provide_db_string(request.form["db"])
		builder.provide_experimental_design(exp_design)

		self.__validate_secret(builder,request)

		participant = builder.authenticate_participant("participant",request.form["participant"])

		providers = request.form["providers"].strip().split(",")
		builder.authenticate_providers(providers)

		callback = request.args["callback"]

		consent_url = builder.build(callback)

		if consent_url != True: # we got a callback url
			re = Response(consent_url)
			return re
		else:
			response = Response("%s/start_consent?pctoken=%s&PRISession=%s" % (SERVER_URL,
			builder.token, session))

			return response

	def on_post_response(self, request):
		"""
		Writes response data to the given response schema. Provide a form with:
		schema: the name of the schema to write to
		response: json data of response to write

		:type request: HTTP response with schema and response data
		:returns: HTTP Response with the written data
		"""

		builder = self.get_builder_reference(request)
		schema = request.form["schema"]
		response = request.form["response"]
		post_response = builder.sog.persistence.post_response_json(builder.sog, schema,
		response)

		return Response(post_response)

	def on_publish_object(self, request, provider, object_name):
		"""
		Publishes the given data as a social object to the given service.

		:param request: HTTP request with the required payload as a HTTP form
		:param provider: the name of the service to publish to
		:type provider: str
		:param object_name: The class of object being published
		:type object_name: str
		"""

		builder = self.get_builder_reference(request)

		payload = request.form["payload"]
		publish_response = builder.sog.PostObjectJSON(provider, object_name, payload)




	def threaded_get_object(self, request, provider, object_name, payload,
	criteria=None, extra_args=None):
		"""
		Wrapper around the SocialObjectGateway GetObjectJSON method to retrieve social
		objects as JSON, then return as response. This should not be called directly,
		but is intended to be called by the on_get_object handler.

		:param request: Current HTTP request
		:param provider: The service to retreive data from
		:type provider: str
		:param object_name: The class of object being retrieved
		:type object_name: str
		:param payload: The criteria to retrieve objects by
		:param criteria: Optional lambda function to filter request by
		:param extra_args: Dictionary of generic arguments to filter on. Currently
		only limit is (partially) supported
		:type extra_args: dict
		:returns: Response with a JSON object of requested data
		"""

		jsonpickle.handlers.registry.register(datetime.datetime,
		SocialObjects.DateTimeJSONHandler)

		builder = self.get_builder_reference(request)
		response = builder.sog.GetObjectJSON(provider, object_name, payload,
		criteria, extra_args)

		resp = Response(response)
		resp.headers["Content-Type"] = "application/json"

		return resp

	def on_get_object(self, request, provider, object_name, payload,
	criteria=None):
		""" Returns a SocialObject of given type (object_name) from a
		given provider.
		The payload is the primary criteria for evaluating a request for
		the object, and must be interpretable by the receiving ServiceGateway. For
		example, providing a user ID may return instances of objects created by that
		user. Provide a lambda expression (criteria) to filter this
		request further (eg. only return objects matching a certain
		attribute value).

		For larger requests, an asynchronous request pattern is also
		provided (for AJAX calls). Make your request as usual, but
		append the argument 'async'. This will immediately return if
		your request was valid. Periodically, call your request URL
		again, instead with the additional argument 'isready'. This will
		return an empty response if the request has not been completed, or the full
		response object when it is.

		:param request: Current HTTP request. If a limit argument is provided this
		will be pushed to an extra_args dictionary for filtering in gateways. Provide
		an async parameter to perform request asynchronously, or an isready parameter
		to check if a previous async request for the same data is ready.
		:param provider: The service to retrieve data from
		:type provider: str
		:param object_name: The class name of object being retrieved
		:param payload: Query argument of object to be retrieved, ie. object ID
		:param criteria: Lambda function for filtering objects before being returned
		:returns: A JSON response of the returned object, or an empty JSON object if
		request is happening asynchronously, or existing async request is not ready
		"""

		builder = self.get_builder_reference(request)
		if "async" in request.args:
			thread.start_new_thread(self.threaded_get_object, (request,
			provider, object_name, payload, criteria))
			return Response("{}")
		elif "isready" in request.args:
			payload_key = builder.sog.policy_processor._infer_object(payload)
			key = "%s_%s" % (object_name, payload_key)
			try:
				cache_obj = builder.sog.internal_cache[key]
			except:
				return Response("{}")

		extra_args = {}
		if "limit" in request.args:
			limit = int(request.args["limit"])
			extra_args["limit"] = limit


		return self.threaded_get_object(request, provider, object_name,
		payload, criteria, extra_args)


	def on_consent(self, request):
		builder = self.get_builder_reference(request)
		token = request.args["pctoken"]
		#token = builder.token
		resp = "Stand back. We're doing science.<br />"
		if(token != builder.token):
			resp += "Token %s is not %s" % (token, builder.token)
			return Response(resp)
		else:
			confirm_url = "%s/confirm?pctoken=%s&PRISession=%s" % (SERVER_URL,
			builder.token, request.args["PRISession"])

			return self.render_template("start.html",next_link = confirm_url,
			exp_contact=builder.contact, exp_name=builder.title)


	def on_confirm(self, request):
		"""
		Provides the authentication flow to redirect participant through
		authentication for each requested provider.
		Request must provide the following arguments:

		pctoken: the authentication token provided earlier in the flow
		provider: the name of the service participant is being authenticated against
		PRISession: current session identifier from cookie

		:param request: HTTP request with above arguments provided
		:returns: Redirect response to service authentication or to complete
		authentication flow
		"""

		builder = self.get_builder_reference(request)
		token = request.args["pctoken"]
		providers = builder.providers

		try:
			current_provider = request.args["provider"]
			if current_provider not in providers:
				#TODO: friendly error here				
				resp = "Invalid provider."
				return Response(resp)
			providers.pop()
		except:
			current_provider = None
			resp = "For this experiment, we need you to login to some services.<br />"

			try:
				provider = providers[len(providers)-1]

				confirm_url = "%s/confirm?provider=%s&pctoken=%s&PRISession=%s" % (SERVER_URL, provider,
				token, request.args["PRISession"])
				"""
				resp += "<a href='%s'>Login to" % confirm_url+\
				 " %s</a>" % provider
				re = Response(resp)
				re.content_type = "text/html"
				return re
				"""
				return self.render_template("service.html",
				provider=provider, next_link = confirm_url,
				exp_contact=builder.contact, exp_name=builder.title)
			except:
				pass

		if providers:
			callback = "%s/confirm?pctoken=%s&provider=%s&cbprovider=%s&PRISession=%s" % (SERVER_URL, token,
			providers[len(providers)-1], current_provider, request.args["PRISession"])
		else:
			callback = "%s/complete?pctoken=%s&cbprovider=%s&PRISession=%s" % (SERVER_URL, token,
			current_provider, request.args["PRISession"])

		try:
			callback_provider = request.args["cbprovider"]
			auth_code = builder.sog.complete_authentication(callback_provider,
			self.request)
			if auth_code == None:
				return redirect(builder.exp_callback)
			else:
				return redirect("%s/cancel?PRISession=%s" % (SERVER_URL, request.args["PRISession"]))

		except:
			pass

		url = builder.sog.request_authentication(current_provider,
		callback=urllib.quote(callback,safe=":/"))
		return redirect(url)

	def on_complete(self, request):
		""" Called at the end of the authentication flow. Redirects participant to the
		callback provided at the start of the experiment.
		Request must provide cbprovider and PRISession arguments to identify this
		session and provider flow.

		:param request: The current HTTP request
		:returns: redirect to experiment callback or /cancel if participant
		invalidates entry
		"""

		builder = self.get_builder_reference(request)

		callback_provider = request.args["cbprovider"]
		auth_code = builder.sog.complete_authentication(callback_provider,
		request)

		# evoke callback
		if auth_code == None:
			return redirect(builder.exp_callback)
		else:
			return redirect("%s/cancel?PRISession=%s" % (SERVER_URL, request.args["PRISession"]))


	def on_fallback(self, request, wildcard):
		""" If an invalid URL is provided, try to rewrite and redirect it in case
		something malformed it.

		:param request: current HTTP request
		:param wildcard: Not used
		:returns: redirect to rewritten URL
		"""

		url = urllib.unquote(request.url)
		dup_mark = self.find_nth(url, "?", 2)
		urlli = list(url)
		urlli[dup_mark] = "&"
		url = ''.join(urlli)

		return redirect(url)

	def find_nth(self, haystack, needle, n):
		""" 
		Utility method for fallback endpoint.

		:param haystack: search for nth item in here
		:param needle: search nth this in haystack
		:param n: this is n!
		:returns: found needle
		"""

		start = haystack.find(needle)
		while start >= 0 and n > 1:
			start = haystack.find(needle, start+len(needle))
			n -= 1
		return start

	def on_session_timeout(self, request):
		"""
		Participant is redirected here if their session key is not found

		:param request: Current HTTP request
		:returns: Response rendering the expired session template
		"""
		return self.render_template("session.html")

	def dispatch_request(self, request):
		""" Internal handler to get from URL mapping to the right response handler
		:param request: Current HTTP request
		"""

		adapter = self.url_map.bind_to_environ(request.environ)

		try:
			endpoint, values = adapter.match()
			return getattr(self, "on_" + endpoint)(request,
			**values)
		except HTTPException, e:
			return e
		except KeyError, e:
			raise
			return self.on_session_timeout(request)

	def wsgi_app(self, environ, start_response):
		""" Exposes the server as a WSGI application. Handles session injection and
		request dispatch.

		":param environ: The environment for this request
		:param start_response: Initial response for app
		:returns: Response
		"""
		request = Request(environ)

		sid = request.cookies.get("PRISession")
		if sid == "":
			sid = None
		if not sid:
			request.session = self.session_store.new()
			request.session["active"] = True
		else:
				request.session = self.session_store.get(sid)


		request.sessionid = sid

		response = self.dispatch_request(request)

		if "RequestRedirect" in type(response).__name__:
			return response(environ,start_response)

		if request.session.should_save:
			self.session_store.save(request.session)
			response.set_cookie("PRISession", request.session.sid)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		""" Internal method for dispatching WSGI app.
		"""
		return self.wsgi_app(environ, start_response)


def create_app():
	""" Instantiates server instance.
	"""
	app = PRISONER()
	return app

if __name__ == "__main__":
	# initialise WSGI app for testing. Not for production use.
	from werkzeug.serving import run_simple
	app = create_app()
	run_simple("localhost", 5000, app, use_debugger=True, use_reloader=True,
	static_files={"/static": TEMPLATE_URL})
