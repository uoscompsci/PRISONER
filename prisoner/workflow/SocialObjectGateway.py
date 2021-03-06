from prisoner.gateway import *  	# import all known service gateways
from prisoner.workflow.PolicyProcessor import PolicyProcessor
import prisoner.SocialObjects
from prisoner.persistence import PersistenceManager

import copy
import json
import jsonpickle
import uuid

class ServiceGatewayNotFound(Exception):
	def __init__(self,gateway):
		self.gateway = gateway
	def __str__(self):
		return "No service gateway for %s is registered" % self.gateway

class InvalidPrivacyPolicy(Exception):
	def __init__(self,error):
		self.error = error
	def __str__(self):
		return "The privacy policy you supplied is invalid. Reason: \n \
		%s" % self.error

class SocialObjectsGateway(object):
	"""
	This is a friendlier interface to PRISONER's internals,
	which participation clients should access.
	This coordinates access to other service gateways, and the management of experimental responses.

	A single instance of this object should be maintained throughout the lifecycle of an experimental application.
	"""
	def __init__(self, server_url=None):
		self.privacy_policy = None
		self.exp_design = None
		# dict keyed on provider names, with values access tokens. this
		# should be persisted so auth not needed on each
		# session for the same participant
		self.keychain = {}
		# dict keyed on provider names, instances of service gateways
		self.gateways = {}

		# maintains a PersistenceManager for DB interaction
		self.persistence = None
		self.policy_processor = None

		self.participant = None

		# stores instances of SocialObjects under a unique id so clients
		# can refer to previous instances. TODO: this needs a simple
		# layer of authentication. is the current user the owner of this
		# cached object?
		self.cached_objects = {}
		# internal cache used to store *unsanitised*
		# responses to avoid making duplicate network
		# requests. ONLY for internal use, NEVER directly
		# access the cache
		self.internal_cache = {}

		self.server_url = server_url

	def cache_object(self, object_to_cache):
		""" Generates a unique identifier for this object, caches it,
		and returns the identifier.

		:param object_to_cache: SocialObject to cache
		:type object_to_cache: SocialObject
		:returns: str -- object's identifier
		"""
		ident = str(uuid.uuid4())
		while(ident in self.cached_objects):
			ident = str(uuid.uuid4())
		object_to_cache.prisoner_id = ident
		self.cached_objects[ident] = object_to_cache
		return ident



	def request_authentication(self, provider, callback):
		""" Call this if it is necessary to perform authenticated API
		calls with a service gateway (usually required to write data as a person or to
		read sensitive data).

		Each service gateway has its own res
		mechanism. Calling this will return a token needed to proceed with
		authentication. Authentication is completed by presenting a relevant interface
		to users, then calling complete_authentication() with its token.

		:param provider: Name of provider to authenticate with.
		:type provider: str.
		:param callback: URL to let PRISONER authentication server know
		user has provided authentication
		:type callback: str.
		:returns: URL required to complete authentication"""
		if provider in self.keychain:
			return None
		# attempt to find this gateway
		gateway = self.__getServiceGateway(provider)
		authent_url = gateway.request_authentication(callback)

		return authent_url
		# what url do i need to authetnicate?
		# let the user consume the authent url and come back in their
		# own time

	def register_participant(self, schema, participant):
		participant= self.persistence.register_participant(schema,
		participant)
		self.participant = participant
		return participant

	def get_participant(self):
		return self.participant

	def complete_authentication(self, provider, request=None):
		"""
		Completes the second stage of authentication with a provider.

		:param provider: Name of provider to authenticate with.
		:type provider: str.
		:param request: The request received from the provider when it
		called the PRISONER callback. This should contain any parameters needed to
		complete authentication
		:type request: werkzeug Request
		"""
		gateway = self.__getServiceGateway(provider)
		ret_access_token = gateway.complete_authentication(request)
		self.persistence.register_participant_with_provider(self.participant[0],
		provider, ret_access_token)
		return None



	def restore_authentication(self, provider, access_token):
		""" Attempt to provide a service gateway with an existing access
		token (eg. stored in DB) to authenticate without going through clientside flow.
		Returns boolean value to indicate success. If False, a call
		should be made to requst_authentication() to begin clientside flow.

		:param provider: Name of provider to authenticate with
		:type provider: str
		:param access_token: Object used to authenticate with this provider
		:type access_token: object
		:returns boolean - was authentication attempt successful?
		"""
		gateway = self.__getServiceGateway(provider)
		auth_success = gateway.restore_authentication(access_token)
		return auth_success


	def provide_privacy_policy(self, privacy_policy):
		"""
		Provide the privacy policy for this experiment. Used to instantiate an instance
		of PolicyProcessor. This can only be done once for an instance of SocialObjectGateway.
		This must be called before attempting to read or write Social Objects.

		:param privacy_policy: path to a privacy policy XML file
		:type privacy_policy: str
		"""
		if self.privacy_policy:
			raise Exception("Privacy policy already defined. If \
			you need to change it, start a new experiment.")

		self.privacy_policy = privacy_policy
		self.policy_processor = PolicyProcessor(self.privacy_policy,
		self)

	def provide_experimental_design(self, experimental_design,
	connection_string):
		"""
		Provide the experimental design for this experiment.
		Used to instantiate a PersistenceManager.
		Can only be done once per instance of SocialObjectGateway.
		This must be called before attemtping to persist any response data.

		:param experimental_design: path to an experimental design XML file
		:type experimental_design: str
		:param connection_string:
			database connection string for persisting data
		:type connection_string: str
		"""
		if self.persistence:
			raise Exception("Experimental design already defined."+\
			"If you need to change it, start a new experiment")
		self.persistence = PersistenceManager.PersistenceManager(experimental_design,
		self.policy_processor, connection_string)
		self.props = self.persistence.props

	def post_response(self, schema, response):
		""" Passes the response to the PersistenceManager to write to the
		internal database. There must be an experimental design bound first.

		:param schema: Name of the response table to write to
		:type schema: str.
		:param response: The response dictionary to write to the specified schema
		:type response: dict
		"""
		if not self.persistence:
			raise Exception("No experimental design supplied")

		self.persistence.post_response(schema, response)

	def GetObjectJSON(self, provider, object_type, payload, criteria,
	extra_args=None):
		""" Interface for retrieving objects from a service gateway, for
		consumption by web services.

		This differs from GetObject in some fundamental ways. GetObject
		is more pythonic - you request objects by supplying relevant SocialObjects, and
		you get SocialObject instances in return. This method however, receives
		plain-text responses, and returns
		JSON objects. Whereas GetObject expects a
		semantically-appropriate SocialObject as the payload (eg. supply an instance of Person to
		receive objects of a given type owned by that Person), this method expects a
		payload expressed as a query string, using the namespaced syntax found in the
		privacy policy spec. For example, a payload of "session:Lastfm.id" will
		be evaluated as "get objects authored by the user ID in the Last.fm session.
		"literal:lukeweb", similarly, returns objects owned by that literal user.
		JSON objects are returned, with the same fields as the Pythonic counterparts. A
		key difference is that the returned object has an additional attribute injected
		- prisoner_id. This is a unique identifier for the returned object *that is
		  valid for the duration of this session*. Rather than passing around full
		instances of objects, subsequent queries, or publication of experimental
		responses, need only refer to this ID to ensure PRISONER is able to relate your
		requests back to the full representation of the data. Note that subsequent
		attempts to retrieve the cached object are subject to the privacy policy
		sanitisation process of the *original* request.
		"""
		# evaluate payload
		eval_payload = self.policy_processor._infer_object(payload)
		eval_payload_obj = SocialObjects.SocialObject()
		eval_payload_obj.id = eval_payload

		# use this to passthrough original object, not wrapped
		# as a dumb SocialObject
		eval_payload_obj = eval_payload

		# call getobject with cleaned object
		ret_object = self.GetObject(provider, object_type,
		eval_payload_obj, True, criteria, extra_args)
		# cache the object under a unique id, JSONify, return
		if ret_object != None:
			ident = self.cache_object(ret_object)
			try:
				return jsonpickle.encode(self.cached_objects[ident])
			except:
				return None
		else:
			return None

	def PostObjectJSON(self, provider, object_type, payload):
		""" Used by web services interface for pushing objects to a service gateway.

		Expects a payload as a JSON dictionary, where the keys are the appropriate fields of <object_type>
		This method converts the dictionary to a native object and pushes it through the PRISONER pipe for sanitisation and publication
		"""
		dumb_social = SocialObjects.SocialObject()
		payload = json.loads(payload)
		for key, value in payload.items():
			setattr(dumb_social,key,value)

		self.PostObject(provider, object_type, dumb_social)

	def __add_to_cache(self, key, to_cache):
		""" Make a deep copy of the given object and write it to the
		internal cache.

		:param key: Key to cache object under
		:type key: str
		:param to_cache: Object to cache
		:type to_cache: object
		"""
		self.internal_cache[key] = copy.deepcopy(to_cache)

	def GetObject(self, provider, object_type, payload, allow_many=False,
	criteria = None, extra_args = None):
		"""
		Interface for retrieving an object from a service gateway.
		Requests are verified against the privacy policy, and returned objects are sanitised as appropriate.
		The payload and filter arguments are semantically distinct. See
		the documentation for each argument to understand how to use them.

		:param provider: name of provider to get object from
		:type provider: str
		:param object_type: name of object to get
		:type object_type: str
		:param payload:
			This must contain a SocialObject or dictionary of
			arguments necessary for the ServiceGateway to make a meaningful request. For
			example, it may be a user ID to retrieve their photos, however it should not
			contain criteria for filtering the objects returned
			(see criteria).
			The expected payload depends on the ServiceGateway and
			the objects you are requesting. See the documentation for each object exposed by
			the ServiceGateway to see the payload it requests.
		:type payload: object
		:param criteria:
			Optional criteria for filtering the objects returned by the
			ServiceGateway. This expression is run on all objects returned by
			gateway, and only where it evaluates as True is the
			object returned. Uses syntax similar to lambda expressions, without prefix. x is used
			to refer to each instance of an object.
			eg. '"party" in x.tags'
		:type filter: str
		:returns: SocialObject -- sanitised for consumption by participation client
		"""
		headers = SARHeaders("GET", provider, object_type, payload)

		if not self.privacy_policy:
			raise Exception("Provide a privacy policy before"\
			" making requests.")
		provider_gateway = self.__getServiceGateway(provider)

		processor = self.policy_processor

		object_type = processor._validate_object_request("GET",
		provider, object_type, payload)

		if "%s_%s" % (object_type, payload) not in self.internal_cache:
			gateway_attr = getattr(provider_gateway,object_type)
			request_handler = getattr(provider_gateway,"request_handler")
			response = request_handler(gateway_attr,"GET",payload, extra_args)
			self.__add_to_cache("%s_%s" % (object_type,
			payload), response)
		else:
			response = self.internal_cache["%s_%s" %
			(object_type, payload)]

		sanitised_set = []
		if hasattr(response.social_object, "objects"): #is a Collection
			new_coll = response.social_object
			if criteria:
				lambda_func = eval("lambda x: %s" % criteria)
				response.social_object.objects = filter(lambda_func, response.social_object.objects)
			for resp in response.social_object.objects:
				resp.provider = provider
				response_obj = SocialActivityResponse(resp, headers)
				sanitised_response = processor._sanitise_object_request(response_obj)
				sanitised_response.prisoner_id = self.cache_object(sanitised_response)
				sanitised_set.append(sanitised_response)
			new_coll.objects = sanitised_set
			new_coll.prisoner_id = self.cache_object(new_coll)
			return new_coll
		else:
			if criteria:
				response_set = [response.social_object]
				response.social_object = filter(eval("lambda x: %s" % criteria),
				response.social_object.objects)
			response.provider = provider
			headers.wrapped_headers = response.headers

			response_obj = SocialActivityResponse(response.social_object, headers)
			sanitised_response = processor._sanitise_object_request(response_obj)
			sanitised_response.prisoner_id = self.cache_object(sanitised_response)
			sanitised_response.headers = headers
			return sanitised_response

	def get_service_gateway(self, provider):
		""" External wrapper to internal function """
		return self.__getServiceGateway(provider)

	def __getServiceGateway(self, provider):
		""" Given the name of a provider, return an instance of the appropriate service gateway

			:param provider: Provider name
			:type provider: str
			:raises: ServiceGatewayNotFound
			:returns: ServiceGateway
		"""
		if provider in self.gateways:
			return self.gateways[provider]	

		if provider in self.props:
			props = self.props[provider]
		else:
			props = None


		try:
			provider_gateway = globals()["%sServiceGateway" %
			provider](policy=self.policy_processor,props=props)
		except:
			raise
			#raise ServiceGatewayNotFound(provider)
		self.gateways[provider] = provider_gateway
		return provider_gateway

	def PostObject(self, provider, object_type, payload):
		"""
		Request to write a Social Object to a given provider.
		Requests are verified against the privacy policy, and outgoing objects are sanitised as necessary.

		:param provider: Provider name
		:type provider: str
		:param object_type: Type of object to write
		:type object_type: str
		:param payload: Object to post to provider
		:type payload: Social Object
		"""
		headers = SARHeaders("POST", provider, object_type, payload)
		if not self.privacy_policy:
			raise Exception("Provide a privacy policy before"\
			" making requests.")

		provider_gateway = self.__getServiceGateway(provider)

		processor = PolicyProcessor(self.privacy_policy)
		request_valid = processor._validate_object_request("POST",
		provider, object_type, payload)

		gateway_attr = getattr(provider_gateway, object_type)
		response = gateway_attr("POST",payload)
		response_obj = SocialActivityResponse(response, headers)

		sanitised_response = processor._sanitise_object_request(response_obj)
