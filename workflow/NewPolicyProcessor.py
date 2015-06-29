import lxml.etree as etree
import urllib2

from prisoner.workflow.Exceptions import *
from prisoner.gateway import *  	# import all known service gateways
import prisoner.SocialObjects

PRIVACY_POLICY_XSD = os.path.join(dir, "../xsd/privacy_policy.xsd")

op_match = {"GET": "retrieve", "POST": "publish", "PUT": "store"}

class PolicyRule(object):
    """ Encodes the policy for a single social object.
    """

    def __init__(self, policy_for):
        pass

    @def for_object():
        doc = "The for_object property."
        def fget(self):
            return self._for_object
        def fset(self, value):
            self._for_object = value
        def fdel(self):
            del self._for_object
        return locals()
for_object = property(**for_object())


class PolicyProcessor(object):
    """ This is a replacement for the old PolicyProcessor. It is NOT API
    compatible with the old one.
    It uses a higher-level abstraction of policy elements rather than constantly parsing the XML. Object requests are sanitised against this model.
    """

    def __init__(self, policy=None, sog=None):
    	self._privacy_policy = None
    	if policy:
    		self.privacy_policy = policy
    	self.namespaces = {"p":
    	"http://prisoner.cs.st-andrews.ac.uk/prisoner/privacy-policy"}

    	self.sog = sog

	@property
	def privacy_policy(self):
		""" Get the privacy policy bound to this PolicyProcessor."""
		return self._privacy_policy

	@privacy_policy.setter
	def privacy_policy(self, value):
		"""Bind a privacy policy to this PolicyProcessor. The privacy
		policy is validated before bound.

		:param value: Path to the privacy policy XML file.
		:type value: str.
		"""
		self._privacy_policy = self.validate_policy(value)

	def validate_policy(self, policy):
		""" Validates a privacy policy against the XML Schema.

		:param policy: Path to privacy policy XML file.
		:type policy: str.
		:returns: ElementTree -- policy object
		:raises: IOError
		"""
		if not policy:
			raise IOError("Privacy policy not found at path")
		xsd_file = open(PRIVACY_POLICY_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		try:
			policy_file = open(policy)
		except IOError:
			policy_file = urllib2.urlopen(policy)
		policy = etree.parse(policy_file)

		try:
			validation = schema.assertValid(policy)
		except Exception as e:
			raise InvalidPolicyProvidedError(e.message)
		return policy

		if validation:
			return policy
		else:
			raise InvalidPolicyProvidedError()



    def build_policy_model(self):
        """ Builds a representation of the policy as a collection of rules
        """

        pass


    def permit_request(self, operation, provider, object_type, payload):
        """ Receive a request for an object, and quickly check we have an appropriate object policy first to avoid collecting data that will be immediately scrubbed clean
        """

        pass

    def sanitise_object(self, response):
        """ Sanitise this object recursively to ensure all nested social objects are handled appropriately
        """

        # walk the attribute tree of the object

        # at each node, if attribute is an instance of a social object, sanitise it in-place
