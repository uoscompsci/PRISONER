"""
PRISONER Social Object Gateway

Participation clients talk to me to request access to objects, or to publish
objects back to services.
I evaluate the request in accordance with the experimental design, and construct
a request to the appropriate service gateway. 
I sanitise the objects it returns and hand them back to participation clients.
"""
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

	def __init__(self):
		self.privacy_policy = None
		self.exp_design = None
		# dict keyed on provider names, with values access tokens. this
		# should be ethically persisted so auth not needed on each
		# session for the same participant
		self.keychain = {'Lastfm':'a78ab9d8a03c60a7e3579fa517dee618'}
		# dict keyed on provider names, instances of service gateways
		self.gateways = {}

		# maintains a PersistenceManager for DB interaction
		self.persistence = None 
		self.policyProcessor = None
	
	def request_authentication(self, provider):
		if provider in self.keychain:
			return None
		# attempt to find this gateway
		gateway = self.__getServiceGateway(provider)
		authent_url = gateway.request_authentication()
		return authent_url
		# what url do i need to authetnicate?
		# let the user consume the authent url and come back in their
		# own time

	def complete_authentication(self, provider, access_token=None):
		if provider in self.keychain:
			return self.keychain[provider]
		gateway = self.__getServiceGateway(provider)
		ret_access_token = gateway.complete_authentication(access_token)
		self.keychain[provider] = ret_access_token
	"""
	Supply the privacy policy used by this experiment.
	This can only be set once, and must be set before any requests are
	allowed.
	
	privacy_policy - path to an XML file containing the privacy policy
	"""
	def provide_privacy_policy(self, privacy_policy):
		if self.privacy_policy:
			raise Exception("Privacy policy already defined. If \
			you need to change it, start a new instance of PRISONER")
	#	processor = PolicyProcessor()
	#	policy = processor.validate_policy(privacy_policy)
		self.privacy_policy = privacy_policy	
		self.policy_processor = PolicyProcessor(self.privacy_policy)

	"""
	Bootstraps the PersistenceManager.
	This can only be set once, and must be set before any attempts to write
	are allowed.

	experimental_design - path to XML file containing valid experimental
	design
	"""
	def provide_experimental_design(self, experimental_design):
		if self.persistence:
			raise Exception("Experimental design already defined."+\
			"If you need to change it, start a new instance of PRISONER")
		self.persistence = PersistenceManager.PersistenceManager(experimental_design,
		self.policy_processor)

	"""
	Attempts to write the response dictionary to the given schema.
	An experimental design must be supplied, containing a table matching the
	name schema of type 'response'.
	
	The supplied data may be sanitised before persistence and must match the
	expected types. For example, well-formed instances of social objects
	must be given where appropriate to allow sanitisation, or the request will fail.

	This interface is only for schemas of response types - not for
	persisting objects/participant data
	"""
	def post_response(self, schema, response):
		if not self.persistence:
			raise Exception("No experimental design supplied")
	
		self.persistence.post_response(schema, response)	
		

	"""
	GetObject allows participation clients to request objects from social
	activity clients.

	provider - name of the provider (sometimes referred to
	as namespace. Examples include "Facebook" and "Lastfm"

	object_type - class of Social Object to return, whether base
	types (Person, Image etc.) or provider-specific (eg. Playlist). In the
	case of the latter, if provider does not recognise the name given, an
	error is raised

	payload - dictionary of criteria for objects returned. Keys correspond
	to attributes of the object to be returned, and again may make use of
	provider-specific extensions

	allow_many - if True, multiple objects may be returned (whether 1 or
	more, a list will always be returned). If false, only the first matching
	object is returned (reproducibility cannot be guaranteed)
	"""
	def GetObject(self, provider, object_type, payload, allow_many=False):
		headers = SARHeaders("GET", provider, object_type, payload)
		
		if not self.privacy_policy:
			raise Exception("Provide a privacy policy before"\
			" making requests.")
		try:
			provider_gateway = globals()["%sServiceGateway" %			
			provider]()
		except:
			raise ServiceGatewayNotFound(provider)
		
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
			for resp in response.objects:
				response_obj = SocialActivityResponse(resp, headers)
				sanitised_response = processor._sanitise_object_request(response_obj)
				sanitised_set.append(sanitised_response)
			new_coll.objects = sanitised_set
			return new_coll
		else:
			response_obj = SocialActivityResponse(resp, headers)
			sanitised_response = processor._sanitise_object_request(response_obj)
			return sanitised_response

			
		
	def __getServiceGateway(self, provider):
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
		
