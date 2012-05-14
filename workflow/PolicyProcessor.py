"""
PRISONER - Policy Processor
===========================

The Policy Processor validates XML privacy policies, for schema adherence and
runtime scope validation.
"""
import lxml.etree as etree
from optparse import OptionParser
from gateway import *  	# import all known service gateways

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
	
	""" Tests whether the request is allowed by the privacy policy for this
	object. If there is no privacy policy, or the policy has no criteria,
	the request is denied.

	To allow the request, we only look for a relevant 'allow=retrieve' rule.
	Subsequently, when the data is returned from the relevant provider, it
	is fully sanitised in accordance with the policy

	This is an internal function.
	"""
	def _validate_object_request(self, operation, provider, object_type, payload):
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
			raise Exception("At least an attribute-policy or " + \
			"object-policy with an allow='retrieve' attribute " + \
			"needed to make requests on this object")
	
	"""
	PRISONER exposes a namespace-heavy interface to allow complex, abstract
	objects be referenced in an appropriate scope.
	For example, "fb:Likes" is interpreted as referring to the Likes Social
	Object provided by the Facebook service gateway, and "literal:me" is
	interpreted as a literal string.
	This allows complex object references to be contained within strings.
	This method is responsbile for relating that back to an appropriate Pythonic
	object reference.

	This is an internal function.
	"""
	def _infer_object(self, object_name):
		base_namespaces = ["literal","session","base","pickle"]

		obj_components = object_name.split(":")
		ns = obj_components[0]
		if ns not in base_namespaces:
			try:
				provider_gateway = globals()["%sServiceGateway" %			
				ns]()
			except:
				raise Exception("Namespace %s can not be " % ns + \
				"resolved to a service gateway")	
			try:
				ns_object = hasattr(
				provider_gateway, obj_components[1])
			except:
				raise Exception("Service gateway %s " % ns + \
				"does not implement object %s" % obj_components[1])
			return ns_object.obj_components[1]
		elif ns == "literal":
			return obj_components[1]
		elif ns == "session":
			# TODO: SESSION LAYER
			pass
		elif ns == "base":
			try:
				ns_obj = globals()[obj_components[1]]()
			except:
				raise Exception("%s is not a base social object" %
				obj_components[1])
			return ns_obj
		elif ns == "pickle":
			# TODO: pickle support
			pass	
	
	"""
	Use to map a string representation of an object.attrs back to a source
	object.
	eg. given (object_attr="Person.id",source=<instance of Person>)
	verifies that the source object has the attribute
	""" 
	def _infer_attributes(self, object_attr, source):
		parsed_object = object_attr.split(".")
		parse_rec = None
		for meth in parsed_object:
			if not parse_rec:
				parse_rec = getattr(source, meth)
				print source
			else:
				parse_rec = getattr(parse_rec,meth)
		return parse_rec

	""" 
	Takes a SocialActivityResponse and applies the appropriate sanitisation,
	based on the experimental privacy policy, and the headers embedded in
	the object.

	This is an internal function.
	"""
	def _sanitise_object_request(self, response):
		if response.headers == None:
			raise Exception("Response has no headers, so cannot " + \
			"be sanitised. No object will be returned.")
		
		# did the object policy allow us to collect this?
		xpath = "//policy[@for='%s']//object-policy[@allow='retrieve']//object-criteria" \
		% response.headers.object_type

		xpath_res = self.privacy_policy.xpath(xpath)
		for element in xpath_res[0]:
			if element.tag == "attribute-match":
				to_match = element.get("match")
				on_object = element.get("on_object")
			
				on_object_obj = self._infer_object(on_object)
				to_match_obj =	self._infer_attributes(to_match,
				response.content)
				print on_object_obj
				if to_match_obj == on_object_obj:
					return response
				else:
					return None
				
				
		# if so, what transformations do we need to make?

		# TODO: for each attribute policy, what do we need to do to this
		# object


		# return response
		



parser = OptionParser()
parser.add_option("-p","--policy", type="string",dest="policy",
help="Path to privacy policy")
(options, args) = parser.parse_args()

if __name__ == "__main__":
	print "PRISONER Policy Processor 0.1"
	policy = options.policy
	
	proc = PolicyProcessor()
	proc.validate_policy(policy)
	

	
		

