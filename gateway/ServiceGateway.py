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

	NEW in 0.2: ServiceGateways should expect a props dict in __init__, populated
	by an experiment's design policy, and a policy parameter with an instance of
	PolicyProcessor, allowing the experiment's privacy policy to be interrogated.

	NEW in 0.2: All gateways must implement a request_handler() - or use the
	superclass-provided implementation. This allows a dictionary of response
	headers to be added by the service gateway, provided to a WrappedResponse
	object.

	"""
	def __init__(self, props={}, policy=None):
		pass

	def request_handler(self, request, operation, payload):
		response = request(operation,payload)
		return WrappedResponse(response,{})

	def Session(self):
		""" Each ServiceGateway can maintain a Session object, which
		contains limited information that is needed to persist throughout the session
		with the service. This should *not* be used as a way of caching social objects
		to circumvent the usual GetObject interface. The session is intended to store,
		for example, metadata about the authenticated participant so that it is possible
		to relate the participant to their service username, etc.
		"""

		raise NotImplementedError("This Service Gateway does not expose"+\
		" a session")

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

	def restore_authentication(self, access_token):
		""" Similar to complete_authentication(), except directly
		providing the access token needed by the gateway to restore an existing session.
		We can't guarantee the token is still valid, so the gateway should return a
		boolean value to indicate whether the attempt was successful. If not, it may be
		necessary to complete the clientside request/complete flow.

		:param access_token:
			Object needed by service gateway to restore
			authentication
		:type access_token: object
		:returns: boolean - was authentication attempt succesful?
		"""
		raise NotImplementedError("Service gateway is not able to\
		restore existing authentication attempts. Go through clientside flow (starting\
		with request_authentication()) to authenticate with this service. Alternatively,\
		this service does not support authenticated requests at all.")

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

	@object_type.setter
	def object_type(self, value):
		self._object_type = value

	@property
	def payload(self):
		""" The criteria for a request, or object to publish. """
		return self._payload
	
	@property
	def wrapped_headers(self):
		""" The header component of a WrappedResponse. Allows service-specific headers
		to be surfaced
		"""
		return self._wrapped_headers

	@wrapped_headers.setter
	def wrapped_headers(self, value):
		self._wrapped_headers = value
	



class WrappedResponse(object):
	""" A Social Object returned by a service gateway is wrapped in this object
	which allows the gateway to inject additional metadata to be handled elsewhere
	"""

	def __init__(self, social_object, headers):
		self._social_object = social_object
		self._headers = headers

	@property
	def social_object(self):
	    return self._social_object

	@social_object.setter
	def social_object(self, value):
		self._social_object = value
