"""
PRISONER - Policy Processor
===========================

The Policy Processor validates XML privacy policies, for schema adherence and
runtime scope validation.
"""
import lxml.etree as etree
from optparse import OptionParser

PRIVACY_POLICY_XSD = "../xsd/privacy_policy.xsd"

class PolicyProcessor(object):

	def __init__(self, policy=None):
		self.privacy_policy = policy
		self.namespaces = {"p":
		"http://pvnets.cs.st-andrews.ac.uk/prisoner/privacy-policy"}

	def validate_policy(self, policy_path):
		print "Validating policy at %s" % policy_path
		xsd_file = open(PRIVACY_POLICY_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		policy_file = open(policy_path)
		policy = etree.parse(policy_file)

		validation = schema.assertValid(policy)		
		return policy

		if validation:
			print "Privacy policy validates!"
			return policy
		else:
			print "Privacy policy failed validation."
		
	def validate_object_request(self, operation, provider, object_type, payload):
		if not self.privacy_policy:
			raise Exception("Privacy policy required before any \
			objects can be requested")

		query_path = ("//policy[@for='%s']"%
		object_type)

		# is there a <policy for="object"> element?
		attrs = self.privacy_policy.xpath(query_path, namespaces=self.namespaces)
		if not attrs:
			exp = "This privacy policy contains no policy" + \
			" element for this object - no requests will be" +  \
			" allowed."
			raise Exception(exp)
		
		# is there an object or attribute criteria with an
		# allow=retrieve attribute?
		att_path=("//policy[@for='%s']//attribute-policy[@allow='retrieve']"
		% object_type)
		obj_path=("//policy[@for='%s']//object-policy[@allow='retrieve']"
		% object_type) 

		attrs_obj = self.privacy_policy.xpath(att_path)
		obj_obj = self.privacy_policy.xpath(obj_path)
		if(not attrs_obj and not obj_obj):
			raise Exception("At least an attribute-policy or" + \
			"object-policy with an allow='retrieve' attribute" + \
			"needed to make requests on this object")

parser = OptionParser()
parser.add_option("-p","--policy", type="string",dest="policy",
help="Path to privacy policy")
(options, args) = parser.parse_args()

if __name__ == "__main__":
	print "PRISONER Policy Processor 0.1"
	policy = options.policy
	
	proc = PolicyProcessor()
	proc.validate_policy(policy)
	

	
		

