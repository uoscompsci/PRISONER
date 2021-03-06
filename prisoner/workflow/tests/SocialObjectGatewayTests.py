import json
import os
try:
	import unittest2 as unittest
except:
	import unittest

from prisoner import SocialObjects
from prisoner.gateway.FacebookGateway import FacebookServiceGateway
from prisoner.workflow import SocialObjectGateway
from prisoner.workflow.Exceptions import *
from prisoner.workflow.PolicyProcessor import PolicyProcessor

import jsonpickle
from mock import MagicMock, patch
from nose.tools import *



class BaseSocialObjectGatewayTestCase(unittest.TestCase):
	""" This test suite ensures:
		- caching behaves as expected
		- service gateway authentication flows are delegated correctly
		- object requests are delegated correctly
	"""

	def setUp(self):
		dir = os.path.dirname(__file__)

		self.good_policy = os.path.join(dir, "good-policy.xml")
		self.bad_policy = os.path.join(dir, "bad-policy.xml")
		self.disallow_policy = os.path.join(dir, "disallow-policy.xml")

		self.good_design = os.path.join(dir, "good-design.xml")

		self.test_object = SocialObjects.Person()
		self.test_object.displayName = "Test Object"
		self.sog = SocialObjectGateway.SocialObjectsGateway(server_url="")

	@patch('prisoner.workflow.SocialObjectGateway.SocialObjectsGateway.GetObject')
	def GetObject_returns_object(*args, **kwargs):
		test_object = SocialObjects.Person()
		test_object.displayName = "Test Object"
		return test_object

	@patch('prisoner.workflow.PolicyProcessor.PolicyProcessor._infer_object')
	def ProcessorInferObject_returns_Person(*args, **kwargs):

		test_object = SocialObjects.Person()
		return test_object



class CacheObjectTestCase(BaseSocialObjectGatewayTestCase):
	def test_cache_hit(self):
		pris_id = self.sog.cache_object(self.test_object)

		cached = self.sog.cached_objects[pris_id]

		assert cached.displayName == "Test Object"

	@raises(KeyError)
	def test_cache_miss(self):
		cached = self.sog.cached_objects["noobject"]


class ProvidePoliciesTestCase(BaseSocialObjectGatewayTestCase):
	def test_provide_good_privacy_policy(self):
		self.sog.provide_privacy_policy(self.good_policy)
		assert self.sog.policy_processor.privacy_policy # is validated

	@raises(InvalidPolicyProvidedError)
	def test_provide_invalid_privacy_policy(self):
		self.sog.provide_privacy_policy(self.bad_policy)

	def test_provide_good_exp_design(self):
		pass

	def test_provide_invalid_exp_design(self):
		pass

class GetObjectJSONTestCase(BaseSocialObjectGatewayTestCase):

	def test_good_get(self):
		self.sog.provide_privacy_policy(self.good_policy)
		with patch.object(self.sog, 'GetObject',
			return_value=self.test_object) as mock_json:
			obj = self.sog.GetObjectJSON("Facebook", "User", "session:Facebook.id","")
			obj_json = jsonpickle.decode(obj)

			assert obj_json.displayName == "Test Object"


	@patch.object(PolicyProcessor,"_infer_object",return_value=SocialObjects.Person())
	def test_bad_get(self, object_name):
		self.sog.provide_privacy_policy(self.good_policy)
		with patch.object(SocialObjectGateway.SocialObjectsGateway, 'GetObject',
			return_value=None) as mock_json:
			obj = self.sog.GetObjectJSON("Facebook", "User", "session:Facebook.id","")
			obj_json = None
			try:
				obj_json = jsonpickle.decode(obj)
			except:
				pass

			assert obj_json == None
