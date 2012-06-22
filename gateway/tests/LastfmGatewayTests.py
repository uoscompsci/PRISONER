try:
	import unittest2 as unittest
except:
	import unittest
from gateway import LastfmServiceGateway
import SocialObjects

"""
This test case:
	- instantiates each type of Social Object
	- expects the gateway to:
		- return valid objects when appropriate
		- gracefully handle invalid requests

	- depends on network availability (TODO: offline proxy)
"""

class BaseLastfmServiceGatewayTestCase(unittest.TestCase):
	def setUp(self):
		self.gateway = LastfmServiceGateway()
		
		person = SocialObjects.Person()
		person.id = "lukeweb"
		self.good_person = person

		person = SocialObjects.Person()
		person.id = "fegrhgtjtrshrh"
		self.bad_person = person


class ImageTestCase(BaseLastfmServiceGatewayTestCase):
	def test_get_success(self):		
		response = self.gateway.Image("GET",self.good_person)
		self.assertEqual(response.author.id, "lukeweb")
		self.assertEqual(response.fullImage,
		"http://userserve-ak.last.fm/serve/34/66246694.jpg")

	def test_get_failure(self):
		response = self.gateway.Image("GET",self.bad_person)
		self.assertEqual(response.author,None)
		self.assertEqual(response.fullImage,None)

	
	


