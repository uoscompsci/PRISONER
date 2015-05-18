import lxml.etree as etree
import urllib2

import os

from prisoner.workflow.Exceptions import *
from prisoner.gateway import *  	# import all known service gateways
import prisoner.SocialObjects

dir = os.path.dirname(__file__)
PRIVACY_POLICY_XSD = os.path.join(dir, "../xsd/privacy_policy.xsd")

op_match = {"GET": "retrieve", "POST": "publish", "PUT": "store"}


class PolicyProcessor(object):
	""" The Policy Processor is responsible for validating and sanitising all
	requests to retrieve and publish Social Objects.

	It requires a well-formed privacy policy XML file to be supplied. If
	this is missing or invalid, all requests will fail.

	The PolicyProcessor is an internal object. Service gateways and
	participation clients do not need to directly interact with it.
	See the SocialObjectGateway for a friendly interface to these innards.

	PolicyProcessor needs an instance of SocialObjectGateway so it can
	evaluate the current session scope of service gateways.
	"""
	def __init__(self, policy=None, sog=None):
		""" Do not instantiate your own PolicyProcessor.

		However, if you choose to ignore that and instantiate your own
		anyway, provide the path to an XML file, which will be
		immediately validated.
		"""
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

	def _validate_object_request(self, operation, provider, object_type, payload):
		""" Validates a request to perform an operation on Social
		Objects (whether retrieving from a service gateway,
		publishing back to a service
		gateway, or putting data to a database).

		A request will only be allowed in the first instance if
		there is an object-policy for this object, for the appropriate operation.

		:param operation: The type of request.
		:type operation: str.
		:param provider:
			The name of the provider of this object. There must be a
			ServiceGateway class corresponding to this provider.
		:type provider: str.
		:param object_type:
			The type of object being processed. This should not be
			prefixed with a provider namespace. The method will attempt to find an
			implementation of this object by the Service Gateway, otherwise
			attempting to
			find an implementation from the base social objects library.
		:type object_type: str.
		:param payload:
		A dictionary of parameters, or instance of a Social
		Object, used to determine the query criteria, or object to write. The
		payload is
		specific to the request - see the documentation for the appropriate gateway
		request for the expected format. :type payload: SocialObject or dictionary
		:returns: str -- a clean object_type for this request (used in later
		stages of
		sanitisation process) """
		if not self.privacy_policy:
			raise NoPrivacyPolicyProvidedError()

		if operation not in ["GET","POST","PUT"]:
			raise OperationNotImplementedError(operation)

		orig_object_type = object_type
		object_type = self.__get_most_specialised_policy_for_class(provider, object_type)

		if not object_type:
			raise DisallowedByPrivacyPolicyError("Privacy policy contains no policy element" + \
			" for %s - no requests will be allowed" % orig_object_type)


		query_path = ("//policy[@for='base:%s']"%
		object_type)



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
		else:
			object_type = "base:%s" % object_type
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

		return self.__get_clean_object_name(orig_object_type)
		return True # you made it this far

	def __get_clean_object_name(self, object_type):
		""" Return an object's type without a namespace component, if one is provided

		"""
		if ":" not in object_type:
			return object_type
		else:
			return object_type.split(":")[1]


	def _infer_object(self, object_name):
		""" Infers object type based on object definition in a privacy policy.

		:param object_name: Object name with an optional namespace component
		:type object_name: str.
		:returns: instance of an object
		:raises: RuntimePrivacyPolicyParserError, ServiceGatewayNotFoundError
		"""
		base_namespaces = ["literal","session","participant","base"]

		try:
			obj_components = object_name.split(":")
		except ValueError:
			raise RuntimePrivacyPolicyParserError("%s " % object_name + \
			"is not a valid object definition")

		if len(obj_components) == 1:
			obj_components = ["base",obj_components[0]]

		ns = obj_components[0]

		if len(obj_components) == 1 or len(obj_components[1]) < 1:
			raise RuntimePrivacyPolicyParserError("No valid object "+ \
			"reference supplied in %s. Did you use the right namespace?" % obj_components+\
			" Base objects use"+\
			" the 'base' namespace")

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
			obj_ref = obj_components[1].split(".")
			# split again on . - 1st component is service gateway,
			# rest is session obj ref
			gateway = self.sog.get_service_gateway(obj_ref[0])
			gateway_session = gateway.Session()

			concat_attrs = ""
			# for each remaining attr, concat a string to getattr
			for comp in obj_ref[1:]:
				concat_attrs = "%s%s." % (concat_attrs, comp)
			concat_attrs = concat_attrs[:-1]

			return getattr(gateway_session, concat_attrs)
		elif ns == "participant":
			# get a reference to the current participant object
			participant = self.sog.get_participant()
			return participant[obj_components[1]]
		elif ns == "base":
			try:
				ns_obj = getattr(SocialObjects, obj_components[1])
			except:
				raise SocialObjectNotSupportedError("base",obj_components[1])
			return ns_obj
		else:
			raise RuntimePrivacyPolicyParserError("%s " % object_name + \
			"is not a valid object definition")


	def _infer_attributes(self, object_attr, source):
		""" Maps a string representation of an object and its attributes back to an instance of a source object, to return its value.

		:param object_attr: object_attributes references (can be many deep)
		:type object_attr: str.
		:param source: the object to search on
		:type source: object
		:returns: attribute value searched for
		"""
		parsed_object = object_attr.split(".")
		print "parsed object: %s" % parsed_object
		parse_rec = None
		for meth in parsed_object:
			if not parse_rec:
				parse_rec = getattr(source, meth)
			else:
				parse_rec = getattr(parse_rec,meth)
				print "parse_rec: %s" % parse_rec 
		return parse_rec

	def __validate_criteria(self, response, tree):
		""" Validates an object against the object and attribute criteria in the given policy.

		:param response: The response object to test
		:type response: SocialObject
		:param tree: A valid privacy policy subtree
		:type tree: ElementTree
		:raises: RuntimePrivacyPolicyParserError
		:returns: boolean - whether or not object passed criteria
		"""
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
		criteria_walk = etree.iterwalk(tree,
		events=("start","end"))
		criteria_walk.next()
		for action, element in criteria_walk:
			if action == "start":
				criteria_stack.append(element)
			elif action == "end" and element.tag in logical_elements:
				# pop from stack until reach logical operator or
				# empty stack. add match elements to
				# working_stack_set so they can be evaluated as
				# a logical group

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
					# TODO: if unevaluated "implicit"
					# elements remain, calculate result!
			else:
				continue
		# evaluate whatever is left as an implicit and
		if (len(criteria_stack) > 1 or criteria_stack[0] not in [True,False]):
			working_set = []
			while(len(criteria_stack) > 0):
				top_element = criteria_stack.pop()
				working_set.append(self.__test_criteria(top_element,
				response))
			if False in working_set:
				criteria_stack.append(False)
			else:
				criteria_stack.append(True)


		if len(criteria_stack) > 1:
			raise RuntimePrivacyPolicyParserError("Criteria "+\
			"produced an unexpected result - is it well-formed?")
		elif criteria_stack[0] == False:
			raise NotImplementedError("tried to validate as none")
		else:
			return True

	def __get_most_specialised_policy_for_object(self, provider, test_object):
		""" Returns the name of the most-specialised superclass of this
		object which has a policy element.
		If I have a Playlist which subclasses Collection, and only a
		policy for Collection, this will return Collection.

		:param test_object: Object to find policy for
		:type test_object: str
		:returns: str -- matching policy object
		"""
		classes = test_object.__class__.__bases__
		classes = list(classes)
		classes.insert(0, test_object.__class__)
		# for each superclass (and original object):
		for obj in classes:
			# is a provider namespaced policy available?
			xpath = "//policy[@for='%s:%s']" % (provider,
			obj.__name__)
			xpath_res = self.privacy_policy.xpath(xpath)
			if xpath_res:
				return obj.__name__
			# is a non-namespaced policy?

			xpath = "//policy[@for='base:%s']" % obj.__name__

			xpath_res = self.privacy_policy.xpath(xpath)
			if xpath_res:

				return obj.__name__
		return False

	def __get_most_specialised_policy_for_class(self, provider, class_name):
		""" Similar to get_most_specialised_policy_for_object except
		class_name is a string, not an instance of the object to test.
		Attempts to infer the class before getting the best-fitting
		policy
		"""
		# try inferring namespaced object
		try:
			provider_gateway = globals()["%sGateway" %
			provider]
			obj = getattr(
			provider_gateway, class_name)

		except:
			obj = self._infer_object(class_name)

		inst = obj()
		# call get_most_specialised with this instance
		return self.__get_most_specialised_policy_for_object(provider,
		inst)



	def _sanitise_object_request(self, response):
		"""
		Sanitises a request - this reduces a Social Object to only the
		fields allowed by the privacy policy, and applies any transformations required by the policy.

		:param response: Object to sanitise
		:type response: SocialActivityResponse
		:returns: SocialObject -- sanitised object
		"""
		if response.headers == None:
			raise Exception("Response has no headers, so cannot " + \
			"be sanitised. No object will be returned.")

		policy_object_type = self.__get_most_specialised_policy_for_object(response.headers.provider,
		response.content)
		response.headers.object_type = policy_object_type

		# did the object policy allow us to collect this?

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
			return None

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
				pass
			else:
				# apply any transforms for this attribute
				transforms = attribute.xpath("attribute-policy/transformations")
				if transforms:
					for transform in transforms[0]:
							#obj_ref = getattr(response.content,curr_attribute)
							obj_ref = response.content

							if transform.tag is etree.Comment:
								continue
							trans_ref = getattr(obj_ref,
							"transform_%s" % transform.get("type"))
							to_transform = getattr(obj_ref, curr_attribute)
							transformed = trans_ref(to_transform, transform.get("level"))
							setattr(sanitised_object, curr_attribute, transformed)


				else:
					setattr(sanitised_object,
					curr_attribute,
					getattr(response.content, curr_attribute))

		sanitised_object.provider = response.content.provider
		return sanitised_object

	def __test_criteria(self, element, response):
		""" Tests that an object passes a single logical test within object or attribute criteria.
		Used internally when validating objects

		:param element: XML element with logical criterion
		:type element: lxml Element
		:param response: Contains object to test
		:type response: SocialActivityResponse
		:returns: bool -- did object pass criteria?
		"""
		if element.tag == "attribute-match":
			to_match = element.get("match")
			on_object = element.get("on_object")

			on_object_obj = self._infer_object(on_object)
			to_match_obj =	self._infer_attributes(to_match,
			response.content)

			print "object id: %s" % response.content.id
			print "response content: %s" % response.content
			print "does %s equal %s" % (to_match_obj, on_object_obj)
			if to_match_obj == on_object_obj:
				return True
			else:
				return False
