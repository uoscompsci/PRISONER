import os
try:
	import unittest2 as unittest
except:
	import unittest

from prisoner.workflow import SocialObjectGateway


class SocialObjectGatewayTests(unittest.TestCase):
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


class CacheObjectTestCase(SocialObjectGatewayTests):
	def test_cache_hit(self):
		pass

	def test_cache_miss(self):
		pass
		
		