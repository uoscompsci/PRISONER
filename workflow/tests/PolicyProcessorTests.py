import os
import unittest2 as unittest

import SocialObjects
from workflow import PolicyProcessor
from workflow.Exceptions import *

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
		
		with self.assertRaises(DisallowedByPrivacyPolicyError) as exp:
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
		
