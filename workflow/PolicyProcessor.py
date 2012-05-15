"""
PRISONER - Policy Processor
===========================

The Policy Processor validates XML privacy policies, for schema adherence and
runtime scope validation.
"""
import lxml.etree as etree
from optparse import OptionParser

from Exceptions import *
from gateway import *  	# import all known service gateways

PRIVACY_POLICY_XSD = "/home/lhutton/svn/progress2/lhutton/projects/sns_arch/src/xsd/privacy_policy.xsd"

class PolicyProcessor(object):

	def __init__(self, policy=None):
		self._privacy_policy = None
		if policy:
			self.privacy_policy = policy
		self.namespaces = {"p":
		"http://pvnets.cs.st-andrews.ac.uk/prisoner/privacy-policy"}

	@property
	def privacy_policy(self):
		return self._privacy_policy
	
	@privacy_policy.setter
	def privacy_policy(self, value):
		self._privacy_policy = self.validate_policy(value)

	def validate_policy(self, policy):
		if not policy:
			raise IOError("Privacy policy not found at path")
		print "Validating policy at %s" % policy
		xsd_file = open(PRIVACY_POLICY_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		policy_file = open(policy)
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
			raise NoPrivacyPolicyProvidedError()

		query_path = ("//policy[@for='%s']"%
		object_type)

		if operation not in ["GET"]:
			raise OperationNotImplementedError(operation)

		# is there a <policy for="object"> element?
		attrs = self.privacy_policy.xpath(query_path, namespaces=self.namespaces)
		if not attrs:
			exp = "This privacy policy contains no policy" + \
			" element for this object - no requests will be" +  \
			" allowed."
			raise DisallowedByPrivacyPolicyError(exp)
		
		# is there an object or attribute criteria with an
		# allow=retrieve attribute?
		att_path=("//policy[@for='%s']//attribute-policy[@allow='retrieve']"
		% object_type)
		obj_path=("//policy[@for='%s']//object-policy[@allow='retrieve']"
		% object_type) 

		attrs_obj = self.privacy_policy.xpath(att_path)
		obj_obj = self.privacy_policy.xpath(obj_path)
		if(not attrs_obj and not obj_obj):
			exp =("At least an attribute-policy or " + \
			"object-policy with an allow='retrieve' attribute " + \
			"needed to make requests on this object")
			raise DisallowedByPrivacyPolicyError(exp)

		return True # you made it this far
	
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
		base_namespaces = ["literal","session","base"]

		obj_components = object_name.split(":")
		ns = obj_components[0]
		if ns not in base_namespaces:
			try:
				provider_gateway = globals()["%sServiceGateway" %			
				ns]()
			except:
				raise ServiceGatewayNotFoundError(ns)	
			try:
				ns_object = hasattr(
				provider_gateway, obj_components[1])
			except:
				raise SocialObjectNotSupportedError(ns,obj_components[1])
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
				raise SocialObjectNotSupportedError("base",obj_components[1])
			return ns_obj
	
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
		"""
		Criteria can contain infinitely nested logical statements and
		actual criteria. Maintain a stack of each element so operations are combined
		correctly
		"""
		logical_elements = ["and-match","or-match"]
		criteria_stack = []
		last_element = None
		last_parent = None

		criteria_walk = etree.iterwalk(xpath_res[0][0],
		events=("start","end"))

		for action, element in criteria_walk:
			if action == "start":
				criteria_stack.append(element)	
			elif action == "end" and element.tag in logical_elements:
				# pop from stack until reach logical operator or
				# empty stack. add match elements to
				# working_stack_set so they can be evaluated as
				# a logical group
				print("reached end of %s - " % element.tag + \
				"evaluate everything earlier on the stack")
				working_stack_set = []
				while len(criteria_stack) > 0:
					top_element = criteria_stack.pop()
					if top_element in [True,False]:
						working_stack_set.append(top_element)
					elif top_element.tag not in logical_elements: 
						# evaluate element and add
						# result to working set
						working_stack_set.append(self.__test_criteria(top_element,response))
					else:
						print("evaluating %s for %s" % 
						(working_stack_set,
						top_element.tag))
						# evaluate everything in set
						# according to this operator,
						# then push the result back and
						# stop
						if(top_element.tag ==
						"and-match"):
							if(False in
							working_stack_set):
								criteria_stack.append(False)
							else:
								criteria_stack.append(True)
						elif(top_element.tag ==
						"or-match"):
							if(True in
							working_stack_set):
								criteria_stack.append(True)
							else:
								criteria_stack.append(False)
						break
			else:
				print action, element
			print criteria_stack		
							
 
						
					
		"""
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
		"""	
				
		# if so, what transformations do we need to make?

		# TODO: for each attribute policy, what do we need to do to this
		# object


		# return response
	"""
	Takes an single policy element (eg. attribute-match) and tests if this
	object passes it - use as part of more complex logical operations

	This is an internal function.
	"""
	def __test_criteria(self, element, response):
		if element.tag == "attribute-match":
			to_match = element.get("match")
			on_object = element.get("on_object")
		
			on_object_obj = self._infer_object(on_object)
			to_match_obj =	self._infer_attributes(to_match,
			response.content)
			if to_match_obj == on_object_obj:
				return True
			else:
				return False



parser = OptionParser()
parser.add_option("-p","--policy", type="string",dest="policy",
help="Path to privacy policy")
(options, args) = parser.parse_args()

if __name__ == "__main__":
	print "PRISONER Policy Processor 0.1"
	policy = options.policy
	
	proc = PolicyProcessor()
	proc.validate_policy(policy)
	

	
		

