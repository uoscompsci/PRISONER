class InvalidPolicyProvidedError(Exception):
	def __init__(self, error):
		self.error = error

	def __str__(self):
		return("The policy file provided could not be validated, because of the\
			following: %s" % self.error )

class NoPrivacyPolicyProvidedError(Exception):
	""" Raised if a privacy policy is required before the operation can be
	completed. See the SocialObjectGateway or ExperimentBuilder to provide a privacy
	policy.

	A Privacy policy is required to read or write data to/from service
	gateways. """
	def __init__(self):
		pass
	def __str__(self):
		return("A privacy policy must be supplied before interacting "+\
			"with this object")

class DisallowedByPrivacyPolicyError(Exception):
	""" Raised if a method attempts to perform an action not allowed by the
	current privacy policy.
	"""
	def __init__(self, error):
		self.error = error
	def __str__(self):
		return self.error

class ServiceGatewayNotFoundError(Exception):
	""" Raised if a participation client attempts to connect to a service
	without a corresponding ServiceGateway class in the gateway module. """
	def __init__(self, gateway):
		self.gateway = gateway
	def __str__(self):
		return("The Service Gateway %s is not registered with PRISONER" %
		self.gateway)

class SocialObjectNotSupportedError(Exception):
	""" Raised if a service gateway doesn't know how to handle the given
	social object. """
	def __init__(self, gateway, object):
		self.gateway = gateway
		self.object = object

	def __str__(self):
		return("%s does not implement the Social Object %s" %
		(self.gateway, self.object))

class OperationNotImplementedError(Exception):
	""" Raised if a service gateway does not implement a request operation
	(GET, POST, PUT etc.) """
	def __init__(self, operation):
		self.operation = operation
	
	def __str__(self):
		return("This service gateway does not implement the operation %s"
		% self.operation)

class RuntimePrivacyPolicyParserError(Exception):
	""" Raised if a privacy policy which passed schema validation fails
	complex validation - eg. an invalid object reference is provided, or logical
	criteria is incorrectly expressed"""
	def __init__(self, error):
		self.error = error

	def __str__(self):
		return self.error
