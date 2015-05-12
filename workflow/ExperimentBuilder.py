from collections import defaultdict
import datetime
import sys
import threading
import tornado.ioloop
import tornado.web
import urllib
import uuid

from prisoner.workflow import PolicyProcessor, SocialObjectGateway

SERVER_URL = "http://localhost:8888"

class ExperimentBuilder(object):
	""" The ExperimentBuilder is the interface for bootstrapping an
	experiment with PRISONER. After instantiating an ExperimentBuilder,
	complete the following steps:

	- call provide_privacy_policy() with the path to your privacy policy XML
	  file
	- call provide_experimental_design() with the path to your experimental
	  design XML file
	- call authenticate_participant() with the id of the participant in this
	  session
	- call authenticate_providers() with a list of services which the
	  participant must authenticate with to participate
	- call build() to generate a pre-experiment flow, which allows
	  participants to review a human-readable version of your privacy 
	  policy, and to authenticate themselves with providers as needed. 	
	"""
	def __init__(self, server_url):
		self.sog = SocialObjectGateway.SocialObjectsGateway(server_url)
		self.participant = None
		self.providers = None
		self.token = str(uuid.uuid4())
		self.session = defaultdict(dict)
		self.title = None
		self.contact = None
		self.connection_string = None
		self.last_touch = None

	def get_props(self, who_for=None):
		props = self.sog.persistence.props

		if not who_for:
			return props
		else:
			return props[who_for]

	def provide_db_string(self, db_string):
		self.connection_string = db_string
		#self.sog.persistence.rebuild_engine(db_string)

	def provide_title(self, title):
		""" The title of the experiment as presented to your
		participants.
		:param title: Friendly experiment title
		:type title: str """
		self.title = title

	def provide_contact(self, contact):
		""" How to contact someone in connection with this experiment,
		eg. an email address. This should be provided in a form that fits the following
		sentence construction:
			"Contact the researcher at <contact>."
		:param contact: Contact information
		:type contact: str
		"""
		self.contact = contact

	def provide_privacy_policy(self, policy):
		""" Provide the privacy policy for this experiment.
		
		:param policy: Path to privacy policy file
		:type policy: str
		"""
		self.sog.provide_privacy_policy(policy)

	def provide_experimental_design(self, exp_design):
		""" Provide the experimental design for this experiment.
		
		:param exp_design: Path to experimental design file
		:type exp_design: str
		"""
		self.sog.provide_experimental_design(exp_design,
		self.connection_string)

	def authenticate_participant(self, schema, participant_id):
		""" Provide the ID of the participant in this experiment. This
		participant must exist in the participant table for this
		experiment.

		:param participant_id: ID of participant
		:type participant_id: int
		"""
		participant = self.sog.persistence.get_participant(schema, participant_id)	
		self.participant = participant
		self.sog.participant = participant
		return self.participant

	def authenticate_providers(self, providers):
		""" Provide a list of provider names this participant needs to
		be authenticated with to participate (eg. if they are only using
		a subset of providers all participants will be using, only include that subset
		in this list). When the experiment is built, each gateway will inject its own
		authentication logic.

		:param providers: List of providers to authenticate with
		:type providers: list[str]
		"""
		self.providers = providers

	def build_schema(self):
		""" Constructs the database schema (destroying whatever data
		might already exist). This places the database in a state in which participants
		may be registered, and experiments run, but does not return usable interfaces to
		the rest of the workflow (such as the SocialObjectGateway) """ 
		
		self.sog.persistence.do_build_schema(drop_first=True)
		print "Schema built without error"
	
	
	def build(self, callback_url):
		""" Using the information provided by the participation client,
		instigate the experiment consent process. This does the
		following:

		- parse the experimental design and privacy policy and generate
		  a human-readable document, relevant to the participant, which
		  also lists which providers the participant will be asked to authenticate with
		- creates a temporary web server - the participation client must
		  access the returned URL using the cookie provided when the
		  ExperimentBuilder was instantiated
		- when the user consents to the policies, each service gateway
		  for which authentication is needed provides a URL to
		  authenticate with which the participant is asked to visit in
		turn (decorated by additional context from PRISONER for participants'
		confidence). Note, this URL must contain the entire
		authentication flow, so you may need to host this yourself, particularly if this
		involves two (or more) factor authentication as users are bounced between URLs
		(many authentication flows expect a URL callback). This flow
		must return a token to persist alongside the Participant.

		: param callback: A callable to be invoked only when consent is
		confirmed - ie. the entrypoint for the participation client
		:type callback: callable
		: returns: URL participant must visit to begin consent flow
		"""
		# does authenticated participant already have a meta row?
		# if so, consent already given, so skip consent and load auth,
		for provider in self.providers:
			provider_auth = self.sog.persistence.get_existing_provider_auth(self.sog.participant[0],
			provider)
			if provider_auth:
				can_auth = self.sog.restore_authentication(provider,
				provider_auth)
				if can_auth:
					print "Already authenticated with %s" % provider
					self.providers.remove(provider)	

		# no providers to authenticate
		if not self.providers:
			#callback()
			print "no authent! go to %s" % callback_url
			return callback_url

		# indicate server needs to do a consent flow
		self.exp_callback = callback_url
		return True

		# start server
		# DEPRECATED: No more ad-hoc server - this is handled
		# by the PRISONER WS server now!
		application = tornado.web.Application([
		(r"/", ConsentFlowHandler),
		(r"/confirm", ProviderAuthentHandler),
		(r"/complete", CompleteConsentHandler),
		(r".*",CallbackHandler),
		], builder=self)
		application.listen(8888)
		t = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
		t.start()
		return "%s/?pctoken=%s" % (SERVER_URL, self.token)
		# serve human readable policies
	
	def consent_confirmed(cookie):
		""" Called when user with given cookie accepts consent. If
		cookie is valid, continue the authentication flow for that participant.
		"""
		pass

class CompleteConsentHandler(tornado.web.RequestHandler):
	""" Called when the user has authenticated themselves with the last
	provider necessary. This completes the authentication flow and allows the
	experimental application to begin. """
	def get(self):
		builder = self.application.settings["builder"]

		callback_provider = self.get_argument("cbprovider")
		builder.sog.complete_authentication(callback_provider,
		self.request)

		#self.write("Thanks. Now ready to start the experiment...")
		# evoke callback
		if "http" in builder.exp_callback:
			self.redirect(builder.exp_callback)
		else:
			self.write(builder.exp_callback)


class ConsentFlowHandler(tornado.web.RequestHandler):
	""" This renders the human-readable representation of the privacy
	policy and ensures the participant understands the data requirements of the
	experimental application before providing consent. """
	def get(self):
		builder = self.application.settings["builder"]
		token = self.get_argument("pctoken")
		self.write("Stand back. We're doing science.</br>")
		if(token != builder.token):
			self.write("Token %s is not %s" % (token, self.token))
			return

		else:
			self.write("(human readable consent here) </br></br>" +\
			"Go <a href='confirm?pctoken=%s'>here</a> if you agree to " %builder.token +\
			"the invisible information here.")

class CallbackHandler(tornado.web.RequestHandler):
	""" Takes a parameter (callback), and calls the unescaped version of
	that URL (useful for baking nested params in a callback URL)
	"""
	def get(self):
		url = urllib.unquote(self.request.uri)
		url = url.replace("?token","&token") # this is an insane shim for a bug in LFM
		url = url.replace("?state","&state") # temp FB shim
		self.redirect(url)

class ProviderAuthentHandler(tornado.web.RequestHandler):
	""" Called during the authentication flow for each provider. Informs the
	participant about the service they are about to authenticate themselves with,
	then redirects to the appropriate URL for that service. """
	def get(self):
		builder = self.application.settings["builder"]
		token = self.get_argument("pctoken")
		providers = builder.providers
		try:
			current_provider = self.get_argument("provider")
			if current_provider not in providers:
				self.write("Invalid provider.")
				return
			providers.pop()
		except:
			current_provider = None
			self.write("For this experiment, we need you to login to some services.</br>")
			provider = providers[len(providers)-1]
			self.write("<a href='confirm?provider=%s&pctoken=%s'>Login to"%(provider, token)+\
			 " %s</a>" % provider)
			return

		if providers:
			callback = "%s/confirm?pctoken=%s&provider=%s&cbprovider=%s" % (SERVER_URL, token,
			providers[len(providers)-1], current_provider)
		else:
			callback = "%s/complete?pctoken=%s&cbprovider=%s" % (SERVER_URL, token,
			current_provider)
		
		try:
			callback_provider = self.get_argument("cbprovider")
			builder.sog.complete_authentication(callback_provider,
			self.request)
		except:
			pass

		url = builder.sog.request_authentication(current_provider,
		callback=urllib.quote(callback,safe=":/"))
		self.redirect(url)
