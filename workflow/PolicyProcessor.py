"""
PRISONER - Policy Processor
===========================

The Policy Processor validates XML privacy policies, for schema adherence and
runtime scope validation.
"""
import lxml.etree as etree
from optparse import OptionParser

PRIVACY_POLICY_XSD = "../xsd/privacy-policy.xsd"

class PolicyProcessor(object):

	def __init__(self):
		pass

	def validate_policy(self, policy_path):
		print "Validating policy at %s" % policy_path
		xsd_file = open(PRIVACY_POLICY_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		policy_file = open(policy_path)
		policy = etree.parse(policy_file)

		validation = schema.validate(policy)		
		if validation:
			print "Privacy policy validates!"
		else:
			print "Privacy policy failed validation."
			
			
		

parser = OptionParser()
parser.add_option("-p","--policy", type="string",dest="policy",
help="Path to privacy policy")
(options, args) = parser.parse_args()

if __name__ == "__main__":
	print "PRISONER Policy Processor 0.1"
	policy = options.policy
	
	proc = PolicyProcessor()
	proc.validate_policy(policy)
	

	
		

