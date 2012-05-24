class ServiceGateway(object):
	""" Service Gateways make external providers of social data accessible to
	the rest of PRISONER. They accept sanitised requests for Social Objects, and
	make the appropriate API calls to return well-formed social objects. They also
	accept requests to publish social objects to services, converting these to the
	representations expected by that API.

	This is an abstract interface - concrete implementations subclass this
	and provide methods corresponding to each Social Object they implement,
	with the signature def ObjectType(self, operation, payload).

	See examples of concrete implementations for examples of this.

	ServiceGateways must adhere to the following conventions:
	
	- exist as a package <GatewayName>ServiceGateway.py within the gateway
	  module
	- contain a class called <GatewayName>ServiceGateway which subclasses
	  ServiceGateway
	"""
        def __init__(self):
                pass

	def Image(self, operation, payload): 
		""" Perform operations on ServiceGateway to publish and retrieve
		Image objects

		:param operation: The operation to perform (eg. GET, POST)
		:type operation: str
		:param payload:
			Object to perform operation with, eg. GET
			objects matching criteria, or POST this object to service
		:type payload: SocialObject
		"""
		raise NotImplementedError("Service Gateway does not support \
		Images")

	def request_authentication(self, callback=None):
		""" First stage of two-stage authentication. Participation
		client has requested that participant is authenticated with this service.

		For most authentication schemes, return a URL the participant can visit to
		authenticate themselves with the service. After completing this stage, the user
		must be redirected to the callback URL.

		Do not implement this method if the service does not perform
		authenticated requests.

		:param callback:
			URL that PRISONER has determined participant
			must visit after authenticating with service.
		:type callback: str

		"""
		raise NotImplementedError("Service Gateway does not support "+\
		"authenticated requests")

	def complete_authentication(self, request):
		""" Second stage of authentication. Request contains the
		response from the client-side authentication, which should
		contain access tokens required to complete the authentication process.

		Do not implement this method if the service does not perform
		authenticated requests.

		:param request: Request with clientside authentication tokens
		:type request: HTTPRequest

		"""
		raise NotImplementedError("Service Gateway does not support "+\
		"authenticated requests")

class SocialActivityResponse(object):
	""" SocialActivityResponse wraps a SocialObject received from a service
	gateway. It provides the original object alongside headers relating to the
	request from the participation clients. These headers are used to validate the
	request, and sanitise the response object.
	"""
	def __init__(self, content, headers):
		""" Instantiate a SocialActivityResponse with the content
		SocialObject and headers. If these change, generate a new SAR.
		
		:param content: The SocialObject returned from a gateway
		:type content: SocialObject	
		:param headers: The headers from the original request.
		:type headers: SARHeaders
		"""
		self._content = content
		self._headers = headers

	@property
	def content(self):
		return self._content
	
	@property
	def headers(self):
		return self._headers

class SARHeaders(object):
	""" SARHeaders contain information about the request for a SocialObject.
	They are used within the validation/sanitisation process as part of a
	SocialActivityResponse. They may also be used to audit the requests made for
	objects.
	"""
	def __init__(self, operation, provider, object_type, payload):
		self._operation = operation
		self._provider = provider
		self._object_type = object_type
		self._payload = payload

	@property
	def operation(self):
		""" The operation to be performed by this request. These map to
		HTTP methods (GET, POST etc.)
		"""
		return self._operation
	
	@property
	def provider(self):
		""" The provider this request is intended for. Must map to a
		ServiceGateway
		"""
		return self._provider
	
	@property
	def object_type(self):
		""" The name of the SocialObject type to use. This must be a
		core SocialObject or provided by the ServiceGateway indicated in the provider
		attribute."""
		return self._object_type

	@property
	def payload(self):
		""" The criteria for a request, or object to publish. """
		return self._payload
	

	
