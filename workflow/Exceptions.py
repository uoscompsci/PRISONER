""" Raised by an object if it requires a privacy policy to be provided before
any further interaction can occur.
PRISONER requires a valid privacy policy XML file to allow interactions between
social activity clients and participation clients.

See the Privacy Policy XML Schema documentation for more information.
"""
class NoPrivacyPolicyProvidedError(Exception):
	def __init__(self):
		pass
	def __str__(self):
		return("A privacy policy must be supplied before interacting "+\
			"with this object")

""" Raised if an operation attempts to contravene the requirements set out in a
privacy policy XML file already provided.
"""
class DisallowedByPrivacyPolicyError(Exception):
	def __init__(self, error):
		self.error = error
	def __str__(self):
		return self.error

""" Raised if an application tries to connect with a social activity client
which is not registered with PRISONER"""
class ServiceGatewayNotFoundError(Exception):
	def __init__(self, gateway):
		self.gateway = gateway
	def __str__(self):
		return("The Service Gateway %s is not registered with PRISONER" %
		self.gateway)

""" Raised if a service gateway does not recognise a given social object.
If this is a base object, this can still be raised if the service simply does
not implement that object """
class SocialObjectNotSupportedError(Exception):
	def __init__(self, gateway, object):
		self.gateway = gateway
		self.object = object

	def __str__(self):
		return("%s does not implement the Social Object %s" %
		(self.gateway, self.object))

""" Raised if a service gateway does not implement a request operation """
class OperationNotImplementedError(Exception):
	def __init__(self, operation):
		self.operation = operation
	
	def __str__(self):
		return("This service gateway does not implement the operation %s"
		% self.operation)

""" Raised if at runtime, a privacy policy fails to pass more complex
validation - eg. does not resolve to a specified object type, or a value is
malformed """
class RuntimePrivacyPolicyParserError(Exception):
	def __init__(self, error):
		self.error = error

	def __str__(self):
		return self.error
