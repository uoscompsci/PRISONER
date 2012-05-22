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
import SocialObjects

PRIVACY_POLICY_XSD = "/home/lhutton/svn/progress2/lhutton/projects/sns_arch/src/xsd/privacy_policy.xsd"
op_match = {"GET": "retrieve", "POST": "publish", "PUT": "store"}

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

	Most criteria is onl considered when the object is returned (we only
	know about many aspects of the object once it comes back.
	Up-front however, we make sure we have an allow="retrieve" policy for
	the object, and that the provider is allowed.

	This is an internal function.
	"""
	def _validate_object_request(self, operation, provider, object_type, payload):
		if not self.privacy_policy:
			raise NoPrivacyPolicyProvidedError()
		
		query_path = ("//policy[@for='%s']"%
		object_type)

		if operation not in ["GET","POST","PUT"]:
			raise OperationNotImplementedError(operation)

		# is there a <policy for="object"> element?
		attrs = self.privacy_policy.xpath(query_path, namespaces=self.namespaces)
		if not attrs:
			query_path = ("//policy[@for='%s:%s']"%
			(provider, object_type))
			attrs = self.privacy_policy.xpath(query_path)
			if not attrs:
				exp = "This privacy policy contains no policy" + \
				" element for %s - no requests will be" % object_type +  \
				" allowed."
				raise DisallowedByPrivacyPolicyError(exp)
			else:
				ns = True
		else:
			ns = False
		
		# is there an object or attribute criteria with an
		# allow=retrieve attribute?
		if ns:
			object_type = "%s:%s" % (provider, object_type)
		att_path=("//policy[@for='%s']//attribute-policy[@allow='%s']"
		% (object_type, op_match[operation]))
		
		obj_path=("//policy[@for='%s']//object-policy[@allow='%s']"
		% (object_type, op_match[operation]))

		attrs_obj = self.privacy_policy.xpath(att_path)
		obj_obj = self.privacy_policy.xpath(obj_path)
		if(not attrs_obj and not obj_obj):
			exp =("At least an attribute-policy or " + \
			"object-policy with an allow='%s' attribute " % op_match[operation]+ \
			"needed to make %s requests on this object" % operation)
			raise DisallowedByPrivacyPolicyError(exp)

		# TODO: explicitly validate the provider is allowed
		# this might get abstracted out to a higher-level (eg. set
		# providers on an experiment-policy to avoid repetition for each
		# object - so hold off until those primitives exist

		return self.__get_clean_object_name(object_type)
		return True # you made it this far

	"""
	To disambiguate base, overriden, and gateway-specific types, we use
	namespace to denote concrete object implementations (eg. Lastfm:Track)
	
	This method strips out any namespace components from an object type
	string so it can be directly accessed from the gateway
	"""
	def __get_clean_object_name(self, object_type):
		if ":" not in object_type:
			return object_type
		else:
			return object_type.split(":")[1]
	"""
	Alternative interface to _infer_object
	Given an optionally qualified object reference, such as Image or
	Lastfm:Track, infer
	def __infer_object_name(self, object_name):
	"""

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

		try:
			obj_components = object_name.split(":")
		except ValueError:
			raise RuntimePrivacyPolicyParserError("%s " % object_name + \
			"is not a valid object definition")
		
		ns = obj_components[0]
		if len(obj_components) == 1 or len(obj_components[1]) < 1:
			raise RuntimePrivacyPolicyParserError("No valid object "+ \
			"reference supplied in %s" % obj_components)
		if ns not in base_namespaces:
			try:
				provider_gateway = globals()["%sServiceGateway" %			
				ns]()
			except:
				raise ServiceGatewayNotFoundError(ns)	
			try:
				ns_object = getattr(
				provider_gateway, obj_components[1])
			except:
				raise SocialObjectNotSupportedError(ns,obj_components[1])
			return ns_object#.obj_components[1]
		elif ns == "literal":
			if len(obj_components[1]) > 0:
				return obj_components[1]
			else:
				raise RuntimePrivacyPolicyParserError("Empty \
				string literal")
		elif ns == "session":
			# TODO: SESSION LAYER
			pass
		elif ns == "base":
			try:
				ns_obj = getattr(SocialObjects, obj_components[1])()
			except:
				raise SocialObjectNotSupportedError("base",obj_components[1])
			return ns_obj
		else:
			raise RuntimePrivacyPolicyParserError("%s " % object_name + \
			"is not a valid object definition")
	
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
	Takes a ElementTree (must be a validated privacy policy) and walks its
	logical structure, validating the criteria.
	The root of the incoming tree should be an x-criteria element - its
	immediate children must be the criteria. An invalid structure will
	prevent requests being sanctioned.

	This is an internal function.
	"""
	def __validate_criteria(self, response, tree):
		logical_elements = ["and-match","or-match"]
		criteria_stack = []
		last_element = None
		last_parent = None

		criteria_type = None
		if tree.tag == "attribute-criteria":
			criteria_type = "attribute"
		elif tree.tag == "object-criteria":
			criteria_type = "object"
		else:
			raise RuntimePrivacyPolicyParserError("Unexpected criteria")
		tree = tree[0]
		criteria_walk = etree.iterwalk(tree,
		events=("start","end"))

		for action, element in criteria_walk:
			if action == "start":
				criteria_stack.append(element)	
			elif action == "end" and element.tag in logical_elements:
				# pop from stack until reach logical operator or
				# empty stack. add match elements to
				# working_stack_set so they can be evaluated as
				# a logical group
				
				#print("reached end of %s - " % element.tag + \
				#"evaluate everything earlier on the stack")
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
						#print("evaluating %s for %s" % 
						#(working_stack_set,
						#top_element.tag))
						
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
				#print action, element
				pass
			#print criteria_stack		
		
		if len(criteria_stack) > 1:
			raise RuntimePrivacyPolicyParserError("Criteria "+\
			"produced an unexpected result - is it well-formed?")
		elif criteria_stack[0] == False:
			return None
		else:
			return True


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
		print response.headers.object_type

		# try to get a service-specific policy for this object type
		# otherwise, fall-back on a base object type
		xpath = "//policy[@for='%s:%s']//object-policy[@allow='%s']//object-criteria" \
		% (response.content.provider, response.headers.object_type,
		op_match[response.headers.operation])
		xpath_res = self.privacy_policy.xpath(xpath)

		if not xpath_res:
			xpath = "//policy[@for='%s']//object-policy[@allow='%s']//object-criteria" \
			% (response.headers.object_type,
			op_match[response.headers.operation])
			xpath_res = self.privacy_policy.xpath(xpath)
			ns = False
		else:
			ns = True
		if ns:
			object_type = "%s:%s" % (response.content.provider,
			response.headers.object_type)
		else:
			object_type = response.headers.object_type

		valid_object_policy = self.__validate_criteria(response,
		xpath_res[0])

		if not valid_object_policy:
			print "Object policy failed for request"

		# recompose object - only include attributes with an
		# attribute-policy
		sanitised_object = response.content.__class__()
			
		xpath = "//policy[@for='%s']//attributes" % object_type
		attributes_collection = self.privacy_policy.xpath(xpath)
		for attribute in attributes_collection[0]:
			curr_attribute = attribute.get("type")
			xpath = "attribute-policy[@allow='%s']//attribute-criteria" % op_match[response.headers.operation]
			att_path = attribute.xpath(xpath)
			if att_path:
				# TODO: block requests without any criteria
				valid_attr_policy = self.__validate_criteria(response,
				att_path[0])
			else:
				valid_attr_policy = True
			if not valid_attr_policy:
				print "Attribute policy %s failed for request" % curr_attribute
			else:
				# apply any transforms for this attribute
				transforms = attribute.xpath("attribute-policy/transformations")
				if transforms:
					for transform in transforms[0]:
							#obj_ref = getattr(response.content,curr_attribute)
							obj_ref = response.content
							trans_ref = getattr(obj_ref,
							"transform_%s" % curr_attribute)
							trans_ref(transform.get("type"),
							transform.get("level"))
							transformed = getattr(obj_ref, curr_attribute)
							setattr(sanitised_object, 
							curr_attribute,
							transformed)
				else:
					setattr(sanitised_object,
					curr_attribute,
					getattr(response.content, curr_attribute))
		
		return sanitised_object
		
 
			


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
