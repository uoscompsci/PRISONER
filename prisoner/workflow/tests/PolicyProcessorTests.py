from datetime import datetime
import os
try:
	import unittest2 as unittest
except:
	import unittest

from prisoner.gateway import *
from prisoner import SocialObjects
from prisoner.workflow import PolicyProcessor
from prisoner.workflow.Exceptions import *

"""
This test suite ensures:
	- the PolicyProcessor validates XML files correctly
	- requests for objects are validated and sanitised appropriately
"""
class BasePolicyProcessorTestCase(unittest.TestCase):
	def setUp(self):
		self.policy_processor = PolicyProcessor.PolicyProcessor()
		dir = os.path.dirname(__file__)

		self.good_policy = os.path.join(dir, "good-policy.xml")
		self.bad_policy = os.path.join(dir, "bad-policy.xml")
		self.disallow_policy = os.path.join(dir, "disallow-policy.xml")

		self.good_response = None
		self.good_response_bad_headers = None
		self.bad_response_no_headers = None
		self.bad_response_bad_headers = None

	""" Returns a Policy Processor with a valid policy which approves the
	requests in the test suite"""
	def get_good_processor(self):
		return PolicyProcessor.PolicyProcessor(self.good_policy)

	""" Returns a Policy Processor with a valid policy which disallows the
	requests in the test suite"""
	def get_disallow_processor(self):
		return PolicyProcessor.PolicyProcessor(self.disallow_policy)

	""" Returns a Policy Processor with an invalid policy. This should raise
	an Exception on instantiation"""
	def get_bad_processor(self):
		return PolicyProcessor.PolicyProcessor(self.bad_policy)

class ValidatePolicyTestCase(BasePolicyProcessorTestCase):
	def test_good_policy(self):
		self.policy_processor = PolicyProcessor.PolicyProcessor()
		policy = self.policy_processor.validate_policy(self.good_policy)
		self.assertTrue("privacy-policy" in policy.getroot().tag)
	
	def test_bad_policy(self):
		self.policy_processor = PolicyProcessor.PolicyProcessor()
		with self.assertRaises(Exception) as exp:
			is_valid = self.policy_processor.validate_policy(self.bad_policy)
	
	def test_no_policy(self):
		self.policy_processor = PolicyProcessor.PolicyProcessor()
		with self.assertRaises(IOError) as exp:
			is_valid = self.policy_processor.validate_policy(None)

class InferObjectTestCase(BasePolicyProcessorTestCase):
	def test_good_literal(self):
		policy_proc = self.get_good_processor()
		obj = policy_proc._infer_object("literal:word")
		self.assertEqual(obj,"word")

	def test_invalid_literal(self):
		policy_proc = self.get_good_processor()
		with self.assertRaises(RuntimePrivacyPolicyParserError):
			obj = policy_proc._infer_object("literal:")

	def test_valid_social_gateway(self):
		policy_proc = self.get_good_processor()
		obj = policy_proc._infer_object("Lastfm:Image")
	#	self.assertTrue(isinstance(obj,LastfmServiceGateway.Image))

		# TODO: Assert social gateway objects
		# This is going to be refactored soon (so instances of gateways
		# aren't constantly being generated, so hold off with tests for
		# now

	def test_valid_base(self):
		policy_proc = self.get_good_processor()
		obj = policy_proc._infer_object("base:Image")()
		self.assertTrue(isinstance(obj, SocialObjects.Image))

	def test_invalid_base(self):
		policy_proc = self.get_good_processor()
		with self.assertRaises(SocialObjectNotSupportedError):
			obj = policy_proc._infer_object("base:NotAObject")

	def test_missing_base(self):
		policy_proc = self.get_good_processor()
		with self.assertRaises(RuntimePrivacyPolicyParserError):
			obj = policy_proc._infer_object("base:")

	def test_invalid_social_gateway(self):
		policy_proc = self.get_good_processor()
		with self.assertRaises(ServiceGatewayNotFoundError):
			obj = policy_proc._infer_object("blah:bleh")	


class InferAttributesTestCase(BasePolicyProcessorTestCase):
	def test_good_obj(self):
		policy_proc = self.get_good_processor()
		person = SocialObjects.Person()
		person.id = "me"

		obj = policy_proc._infer_attributes("id",person)
		self.assertEqual(obj,"me")

	def test_bad_obj(self):
		policy_proc = self.get_good_processor()
		person = SocialObjects.Person()

		#with self.assertRaises(AttributeError):
		obj = policy_proc._infer_attributes("id",person)
		self.assertEqual(obj,None)

	def test_bad_attribute(self):
		policy_proc = self.get_good_processor()
		person = SocialObjects.Person()
		person.id = "me"
		
		with self.assertRaises(AttributeError):
			obj = policy_proc._infer_attributes("blah",person)

	def test_bad_format(self):
		policy_proc = self.get_good_processor()
		with self.assertRaises(AttributeError):
			obj = policy_proc._infer_attributes("blah",None)

	def test_good_nested_obj(self):
		policy_proc = self.get_good_processor()
		test_obj = SocialObjects.Person()
		test_obj.updated = datetime.datetime.fromtimestamp(0)
		
		obj = policy_proc._infer_attributes("updated.year",test_obj)
		self.assertEqual(obj,1970)

	def test_bad_nested_obj(self):
		policy_proc = self.get_good_processor()
		test_obj = SocialObjects.Person()
		test_obj.updated = datetime.datetime.fromtimestamp(0)

		with self.assertRaises(AttributeError):
			obj = policy_proc._infer_attributes("updated.blah", test_obj)

class SanitiseObjectRequestTestCase(BasePolicyProcessorTestCase):
	def test_good_response(self):
		policy_proc = self.get_good_processor()
		
	def test_malformed_headers(self):
		pass
	def test_missing_headers(self):
		pass
	def test_malformed_response(self):
		pass
	def test_no_allow_attribute(self):
		pass
	def test_logic_failOnAnd(self):
		pass
	def test_logic_failOnOr(self):
		pass
	def test_logic_failOnNested(self):
		pass
	def test_logic_failOnImplicitAnd(self):
		pass
	

class ValidateObjectRequestTestCase(BasePolicyProcessorTestCase):
	def test_good_validation(self):
		policy_proc = self.get_good_processor()
		test_person = SocialObjects.Person()
		test_person.id = "lukeweb"

		request = policy_proc._validate_object_request("GET", "Lastfm",
		"Image", test_person)
		
		self.assertTrue(request)

	def test_fail_validation(self):
		policy_proc = self.get_disallow_processor()
		test_person = SocialObjects.Person()
		test_person.id = "lukeweb"

		with self.assertRaises(DisallowedByPrivacyPolicyError) as exp:
			request = policy_proc._validate_object_request("GET", "Lastfm",
			"Image", test_person)
		
	def test_bad_request_badOperation(self):
		policy_proc = self.get_good_processor()
		test_person = SocialObjects.Person()
		test_person.id = "lukeweb"
		
		with self.assertRaises(OperationNotImplementedError) as exp:
			request = policy_proc._validate_object_request("BLAH", 
			"Lastfm", "Image", test_person)

	"""
	def test_bad_request_badProvider(self):
		policy_proc = self.get_good_processor()
		test_person = SocialObjects.Person()
		test_person.id = "lukeweb"
		
		with self.assertRaises(ServiceGatewayNotFoundError) as exp:
			request = policy_proc._validate_object_request("GET",
			"NotAProvider", "Image", test_person)
	"""

	def test_bad_request_badObject(self):
		policy_proc = self.get_good_processor()
		test_person = SocialObjects.Person()
		test_person.id = "lukeweb"
		
		with self.assertRaises(SocialObjectNotSupportedError) as exp:
			request = policy_proc._validate_object_request("GET",
			"Lastfm", "NotAObject", test_person)
	
	"""
	def test_bad_request_badPayload(self):
		policy_proc = self.get_good_processor()
		test_person = SocialObjects.Person()

		with self.assertRaises(DisallowedByPrivacyPolicyError) as exp:
			request = policy_proc._validate_object_request("GET",
			"Lastfm", "Image", test_person)
	"""
		
