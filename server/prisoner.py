from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request, Response, BaseRequest
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect, cached_property

from jinja2 import Environment, FileSystemLoader

from workflow import PolicyProcessor, SocialObjectGateway, ExperimentBuilder
import SocialObjects

import csv
import datetime
import json
import jsonpickle
import os
import subprocess
import thread
import urllib
import urllib2

#SERVER_URL = "http://localhost:5000"
SERVER_URL = "https://prisoner.cs.st-andrews.ac.uk/prisoner"
#TEMPLATE_URL = "/home/sam/Dropbox/PRISONER/static" # LOCAL
TEMPLATE_URL = "/home/lhutton/prisoner/prisoner/static"

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

	def run_command(self, command):
	    p = subprocess.Popen(command,
	                         stdout=subprocess.PIPE,
	                         stderr=subprocess.STDOUT,
	                         shell=True)
	    return iter(p.stdout.readline, b'')
		
	def on_restart(self, request):
		""" This call should not be publicly exposed.
		Does a hg pull from the prisoner repo, updates prisoner's server code then
		forces a wsgi restart. If the pull does not succeed or otherwise leaves the
		server in an inconsistent state, things may be broken.
		The output from the shell when updating from hg is piped to the response
		"""
		output_pipe = ""
		commands = "cd /home/lhutton/prisoner; ./invoke.sh"

		output_pipe="Attempting to update prisoner...\n\n"
		output_pipe="%s\nRunning: %s\nOutput:\n\n" % (output_pipe, commands)

		for line in self.run_command(commands):
			output_pipe="%s\n%s" % (output_pipe,line)

		return Response(output_pipe)

		




	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype="text/html")

	def get_builder_reference(self, request):
		""" Each session has its own instance of PRISONER's internals,
		keyed on the session cookie.
		"""
		#return self.session_internals[request.cookies.get("PRISession")]
		return self.session_internals[request.args["PRISession"]]

	def set_builder_reference(self, request, builder):
		prisession = request.args["PRISession"]
		self.session_internals[prisession] = builder
		print "set session for %s" % prisession
		return self.get_builder_reference(request)

	def on_invalidate(self, request):
		""" Invalidate the current session, removing it from memory.
		Call this  at the end of the experiment to remove its footprint,
		or in the event of an irrecoverable error, from which you do not want the
		participant to recover without restarting the experiment flow
		"""
		priSession = request.args["PRISession"]
		self.session_internals[priSession].sog.persistence.close_connection()

		del self.session_internals[priSession]
		return Response("session invalidated")
		
	
	def on_cancel(self, request):
		builder = self.get_builder_reference(request)
		return self.render_template("cancel.html",
		exp_contact=builder.contact, exp_name=builder.title)
		

	def on_register(self, request):
		""" Register a participant. Requires a URL for the experimental
		design and privacy policy, and a form of columns to insert about this participant.
		"""	
		builder = self.set_builder_reference(request,
		ExperimentBuilder.ExperimentBuilder(SERVER_URL))
		
		exp_design = request.form["design"]
		policy = request.form["policy"]

		builder.provide_privacy_policy(policy)

		builder.provide_db_string(request.form["db"])
		builder.provide_experimental_design(exp_design)


		schema = request.form["schema"]

		write_out = {}
		for key in request.form.keys():
			if key not in ["design","policy","schema"]:
				write_out[key] = request.form[key]
		participant = builder.sog.register_participant(schema,
		write_out)
		print "PRISONER registered participant %s" % participant
		return Response(str(participant[0]))
		



	def on_session_write(self, request):
		""" Writes arbitrary data to a temporary session. A
		session is bound to a PRISession, and is intended to retain state data
		during an experiment before committing to database.
		There is no guarantee how long the session will be
		valid for, so gracefully handle instances where expected data cannot
		be retrieved.

		To write session data, provide a POST form with a
		"key" value (used to retrieve the data later) and
		"data" (the arbitrary session data to store).
		"""
		builder = self.get_builder_reference(request)
		builder.session[request.args["PRISession"]][request.form["key"]] = request.form["data"]	
		return Response()

	def on_session_read(self, request):
		""" Read the session data corresponding to the given key
		parameter. Session data is bound to the active PRISession. """
		builder = self.get_builder_reference(request)
		if request.args["key"] not in builder.session[request.args["PRISession"]]:
			return Response("Key not in session",status=404)
		return Response(json.dumps(builder.session[request.args["PRISession"]][request.args["key"]]))

	def on_handshake(self, request):
		""" This initial call provides the client with their session
		token. If response is good, call /begin providing the given
		PRISession value.
		"""
		return Response("Welcome to PRISONER. Now call /begin to "+\
		"initialise your experiment, supplying the PRISession parameter.")		

	def on_begin(self, request):
		builder = self.set_builder_reference(request,ExperimentBuilder.ExperimentBuilder(SERVER_URL))
	
		privacy_policy = request.form["policy"]
		exp_design = request.form["design"]
		builder.provide_privacy_policy(privacy_policy)

		builder.provide_title(request.form["title"])
		builder.provide_contact(request.form["contact"])

		builder.provide_db_string(request.form["db"])
		print "got db: %s" % request.form["db"]
		builder.provide_experimental_design(exp_design)

		participant = builder.authenticate_participant("participant",request.form["participant"])	
	
		providers = request.form["providers"].strip().split(",")
		builder.authenticate_providers(providers)

		callback = request.args["callback"]

		consent_url = builder.build(callback)	
	
		if consent_url != True: # we got a callback url
			re = Response(consent_url)
			return re
		else:
			#return self.consent_flow_handler(request, callback)
			#return redirect("start_consent?pctoken=%s" % builder.token)
			return Response("%s/start_consent?pctoken=%s&PRISession=%s" % (SERVER_URL,
			builder.token, request.args["PRISession"]))
		#return redirect(consent_url)
	
	def on_post_response(self, request):
		builder = self.get_builder_reference(request)
		schema = request.form["schema"]
		response = request.form["response"]
		post_response = builder.sog.persistence.post_response_json(builder.sog, schema,
		response)

		return Response(post_response)	

	def on_publish_object(self, request, provider, object_name):
		builder = self.get_builder_reference(request)

		payload = request.form["payload"]
		publish_response = builder.sog.PostObjectJSON(provider, object_name, payload)
		



	def threaded_get_object(self, request, provider, object_name, payload,
	criteria=None):
		jsonpickle.handlers.registry.register(datetime.datetime,
		SocialObjects.DateTimeJSONHandler)

		builder = self.get_builder_reference(request)
		response = builder.sog.GetObjectJSON(provider, object_name, payload,
		criteria)

		resp = Response(response)
		resp.headers["Content-Type"] = "application/json"

		#return Response(response)
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
		"""
		builder = self.get_builder_reference(request)
		#builder.last_touch = datetime.now()
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
	
		return self.threaded_get_object(request, provider, object_name,
		payload, criteria)
		
		"""
		jsonpickle.handlers.registry.register(datetime.datetime,
		SocialObjects.DateTimeJSONHandler)
	
		builder = self.get_builder_reference(request)
		response = builder.sog.GetObjectJSON(provider, object_name, payload,
		criteria)

		resp = Response(response)
		resp.headers["Content-Type"] = "application/json"

		#return Response(response)
		return resp
		"""

	""" START server handlers migrated from ExpBuilder """
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

			"""
			resp += "(human readable consent here) <br/><br />" +\
			"Go <a href='%s'>here</a> if you agree to " % confirm_url+\
			"the invisible information here."
			#return Response(resp)
			re = Response(resp)
			re.content_type = "text/html"
			return re
			"""	
			return self.render_template("start.html",next_link = confirm_url,
			exp_contact=builder.contact, exp_name=builder.title)


	def on_confirm(self, request):
		builder = self.get_builder_reference(request)
		token = request.args["pctoken"]
		providers = builder.providers
		
		try:
			current_provider = request.args["provider"]
			if current_provider not in providers:
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
		url = urllib.unquote(request.url)
		dup_mark = self.find_nth(url, "?", 2)
		urlli = list(url)
		urlli[dup_mark] = "&"
		url = ''.join(urlli)
		#url = url.replace("?token","&token") # this is an insane shim for a bug in LFM
		#url = url.replace("?state","&state") # temp FB shim
		
		return redirect(url)

	def find_nth(self, haystack, needle, n):
		start = haystack.find(needle)
		while start >= 0 and n > 1:
			start = haystack.find(needle, start+len(needle))
			n -= 1
		return start
	
	
	""" END ExpBuilder migration"""

	def on_session_timeout(self, request):
		return self.render_template("session.html")

	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, "on_" + endpoint)(request,
			**values)
		except HTTPException, e:
			return e
		except KeyError, e:
			return self.on_session_timeout(request)
	
	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		#sid = request.cookies.get("PRISession")
		try:
			sid = request.args["PRISession"]
		except:
			sid = None
		if sid == "":
			sid = None
		#print "sid: %s" % sid
		if not sid:
			request.session = self.session_store.new()
			request.session["active"] = True
			print "set session"
		else:
			request.session = self.session_store.get(sid)


		#print request.session.modified

		response = self.dispatch_request(request)
		if request.session.should_save:
			print "saving session"
			self.session_store.save(request.session)
			#response.set_cookie("PRISession", request.session.sid)
			response.headers.add("PRISession", request.session.sid)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)


def create_app():
	app = PRISONER()
	return app

if __name__ == "__main__":
	from werkzeug.serving import run_simple
	app = create_app()
	print app
	run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True,
	static_files={"/static": TEMPLATE_URL})
