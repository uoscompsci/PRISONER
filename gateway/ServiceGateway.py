"""
PRISONER Service Gateway
========================

Abstract interface for PRISONER Service Gateways. Concrete implementations must
subclass this.
"""

class ServiceGateway(object):

        def __init__(self):
                pass

	""" Common interface for core Image Social Object """
	def Image(self, operation, payload): 
		raise NotImplementedError("Service Gateway does not support \
		Images")


""" 
The SocialActivityResponse contains two main elements:
	content - the object, or set of objects returned from a
	request. These are instances of Social Objects

	headers - contains information about the original request.
	This is immutable, and used to decide how to sanitise the data
	returned.
	See the SARHeaders object documentation for required fields.
"""
class SocialActivityResponse(object):
	def __init__(self, content, headers):
		self._content = content
		self._headers = headers

	@property
	def content(self):
		return self._content
	
	@property
	def headers(self):
		return self._headers

class SARHeaders(object):
	def __init__(self, operation, provider, object_type, payload):
		self._operation = operation
		self._provider = provider
		self._object_type = object_type
		self._payload = payload

	@property
	def operation(self):
		return self._operation
	
	@property
	def provider(self):
		return self._provider
	
	@property
	def object_type(self):
		return self._object_type

	@property
	def payload(self):
		return self._payload
	

	
