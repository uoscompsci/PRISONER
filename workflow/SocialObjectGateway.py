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
		# dict keyed on provider names, with values access tokens
		self.keychain = {}		
	
	def request_authentication(self, provider):
		if provider in self.keychain:
			exp = "This provider is already authenticated. " + \
			"Explicitly revoke(provider)"
			raise Exception(exp)
		
		# attempt to find this gateway
		gateway = __getServiceGateway(provider)
		authent_url = gateway.request_authentication()
		return authent_url
		# what url do i need to authetnicate?
		# let the user consume the authent url and come back in their
		# own time

	def provide_authentication(self, provider, access_token):
		if provider in self.keychain:
			exp = "This provider is already authenticated. " + \
			"Explicitly call revoke(provider)."
			raise Exception(exp)
		self.keychain[provider] = access_token	

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
		
		processor = PolicyProcessor(self.privacy_policy)
		request_valid = processor._validate_object_request("GET",
		provider, object_type, payload)
			
		# TODO: reconcile with session
		
		gateway_attr = getattr(provider_gateway,object_type)
		response = gateway_attr("GET",payload)		
		# produce a full response object
		response_obj = SocialActivityResponse(response, headers)
	

		# TODO: sanitise response against policy	
		sanitised_response = processor._sanitise_object_request(response_obj)

		print sanitised_response
	
	def __getServiceGateway(self, provider):
		try:	
			provider_gateway = globals()["%sServiceGateway" %
			provider]()
		except:
			raise ServiceGatewayNotFoundError(provider)
		return provider_gateway

	def PutObject(self, provider, object_type, payload):
		headers = SARHeaders("PUT", provider, object_type, payload)
		
