from gateway import *  	# import all known service gateways
from PolicyProcessor import PolicyProcessor
import SocialObjects
from persistence import PersistenceManager

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
	def __init__(self):
		self.privacy_policy = None
		self.exp_design = None
		# dict keyed on provider names, with values access tokens. this
		# should be ethically persisted so auth not needed on each
		# session for the same participant
		#self.keychain = {'Lastfm':'a78ab9d8a03c60a7e3579fa517dee618'}
		self.keychain = {}
		# dict keyed on provider names, instances of service gateways
		self.gateways = {}

		# maintains a PersistenceManager for DB interaction
		self.persistence = None 
		self.policy_processor = None

		self.participant = None	
	
	def request_authentication(self, provider, callback):
		""" Call this if it is necessary to perform authenticated API
		calls with a service gateway (usually required to write data as a person or to
		read sensitive data).

		Each service gateway has its own authentication
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
		:type request: tornado.httpserver.HTTPRequest
		"""
		gateway = self.__getServiceGateway(provider)
		ret_access_token = gateway.complete_authentication(request)
		self.persistence.register_participant_with_provider(self.participant[0],
		provider, ret_access_token)

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
		Provide the privacy policy for this experiment. Used to instantiate an instance of PolicyProcessor. This can only be done once for an instance of SocialObjectGateway. This must be called before attempting to read or write Social Objects.

		:param privacy_policy: path to a privacy policy XML file
		:type privacy_policy: str
		"""
		if self.privacy_policy:
			raise Exception("Privacy policy already defined. If \
			you need to change it, start a new instance of PRISONER")
	#	processor = PolicyProcessor()
	#	policy = processor.validate_policy(privacy_policy)
		self.privacy_policy = privacy_policy	
		self.policy_processor = PolicyProcessor(self.privacy_policy,
		self)

	def provide_experimental_design(self, experimental_design):
		"""
		Provide the experimental design for this experiment.
		Used to instantiate a PersistenceManager.
		Can only be done once per instance of SocialObjectGateway.
		This must be called before attemtping to persist any response data.

		:param experimental_design: path to an experimental design XML file
		:type experimental_design: str
		"""
		if self.persistence:
			raise Exception("Experimental design already defined."+\
			"If you need to change it, start a new instance of PRISONER")
		self.persistence = PersistenceManager.PersistenceManager(experimental_design,
		self.policy_processor)

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
		
	def GetObject(self, provider, object_type, payload, allow_many=False,
	criteria = None):
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
		"""
		try:
			provider_gateway = globals()["%sServiceGateway" %			
			provider]()
		except:
			raise ServiceGatewayNotFound(provider)
		"""
		provider_gateway = self.__getServiceGateway(provider)
		
		#processor = PolicyProcessor(self.privacy_policy)
		processor = self.policy_processor

		object_type = processor._validate_object_request("GET",
		provider, object_type, payload)
			
		# TODO: reconcile with session
		
		gateway_attr = getattr(provider_gateway,object_type)
		response = gateway_attr("GET",payload)		

		sanitised_set = []
		if hasattr(response, "objects"): #is a Collection
			new_coll = response
			if criteria:
				lambda_func = eval("lambda x: %s" % criteria)
				response.objects = filter(lambda_func, response.objects)				
			for resp in response.objects:
				resp.provider = provider
				response_obj = SocialActivityResponse(resp, headers)
				sanitised_response = processor._sanitise_object_request(response_obj)
				sanitised_set.append(sanitised_response)
			new_coll.objects = sanitised_set
			return new_coll
		else:
			if criteria:
				response_set = [response]
				response = filter(eval("lambda x: %s" % criteria),
				response.objects)
			response.provider = provider
			response_obj = SocialActivityResponse(response, headers)
			sanitised_response = processor._sanitise_object_request(response_obj)
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
		try:	
			provider_gateway = globals()["%sServiceGateway" %
			provider]()
		except:
			raise ServiceGatewayNotFound(provider)
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
		print sanitised_response
		
