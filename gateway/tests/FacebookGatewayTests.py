import os
try:
	import unittest2 as unittest
except:
	import unittest

from nose.tools import *
from prisoner import SocialObjects
from prisoner.gateway import *
from prisoner.workflow import PolicyProcessor

import random
import urllib2

"""
These tests:
	- try to retrieve each type of social object from Facebook
	- make sure bad requests are handled gracefully
	- test version mappings

Running these tests requires a Facebook App ID and Secret. 
The test runner will create a test user at setup for that app populated with
enough content to test endpoints.
"""

class BaseFacebookGatewayTestCase(unittest.TestCase):
	def setUp(self):
		"""
		### These values must be set before running these tests!
		"""
		self.APP_ID = "462365643919501"
		self.APP_SECRET = "e927a00c03bb1e280f2bcb6f3cb88628"
		self.CURRENT_API = "2.0"

		# Renew this at https://developers.facebook.com/tools/accesstoken/
		self.APP_ACCESS_TOKEN = "462365643919501|a0P4eQttNhsKvV7TX6O4FjYXUCw"

		self.graph_uri = "https://graph.facebook.com/v%s/" % self.CURRENT_API
		self.auth_request_uri = "https://www.facebook.com/dialog/oauth?"
		self.auth_token_uri = "https://graph.facebook.com/oauth/access_token?"
		self.facebook_uri = "https://www.facebook.com"

		
	def get_good_processor(self):
		good_policy_path = os.path.join(os.path.dirname(__file__), "good-policy.xml")
		proc = PolicyProcessor.PolicyProcessor(good_policy_path)
		return proc

	def get_bad_processor(self):
		policy_path = os.path.join(os.path.dirname(__file__), "bad-policy.xml")
		proc = PolicyProcessor.PolicyProcessor(policy_path)
		return proc

	def get_empty_processor(self):
		policy_path = ""
		proc = PolicyProcessor.PolicyProcessor(policy_path)
		return proc

	def get_good_props(self):		
		# props to test app versions and providing app IDs etc.
		return {'app_id': self.APP_ID,
				'app_secret': self.APP_SECRET,
				'api_version': self.CURRENT_API}

		

	def create_user_all_permissions(self):
		""" Creates a test user who has every relevant FB permission enabled
		"""
		if not self.gateway:
			raise Exception("Test runner needs to initialise an appropriate gateway \
				first")
		perms = []
		for key in self.gateway.perm_maps:
			if self.gateway.perm_maps[key][0] not in perms:
				perms.append(self.gateway.perm_maps[key][0])

		perm_string = ""
		for perm in perms:
			perm_string = "%s%s," % (perm_string, perm)
		perm_string = perm_string[:-1]

		# create test user
		user = {'installed': True,
				'permissions': perm_string,
				'name':"Bob Tester"}

		endpoint = "%s/accounts/test-users" % self.APP_ID
		self.user = self.__post_graph_data(endpoint,user)
		self.gateway.access_token = self.user['access_token']

	def create_user_no_permissions(self):
		""" Creates a test user who has no FB permission enabled
		"""
		if not self.gateway:
			raise Exception("Test runner needs to initialise an appropriate gateway \
				first")

		# create test user
		user = {'installed': True,
				#'permissions': perm_string,
				'name':"Fail Tester"}

		endpoint = "%s/accounts/test-users" % self.APP_ID
		self.user = self.__post_graph_data(endpoint,user)
		self.gateway.access_token = self.user['access_token']

		set_test_user_attributes()


	def set_test_user_attributes(self):
		""" sets some attributes for testing common to all test objects
		"""
		# create a status update
		# call_dict = {
		# "message":"Test status",
		# "link":""
		# }
		# response = self.__post_graph_data("/me/feed", call_dict)


	def __post_graph_data(self, query, params):
		"""
			Internal Function.
			Post the params dictionary to the given query path on the Graph API
			Use for creating, deleting, updating content
			All calls must be authenticated

			:param query: Graph API query to perform
			:type query: str
			:param params: Dictionary of data to publish to this endpoint
			:type params: dict
		"""
		# If query doesn't start with https://, we assume it is relative.
		if (not query.startswith("https://")):
			query = self.graph_uri + query + "?access_token=" + self.APP_ACCESS_TOKEN
		
		# Retrieve and parse result.
		data_req = urllib2.Request(query,
		data = urllib.urlencode(params))

		#print query
		#print urllib.urlencode(params)

		try:
			data_resp = urllib2.urlopen(data_req)
		except urllib2.HTTPError as e:
			contents = e.read()
			print "error"
			print contents
		data = data_resp.read()
		json_obj = json.loads(data)

		print json_obj

		return json_obj

	def __get_graph_data(self, query):
		"""
		Internal function.
		Queries Facebook's Graph API and returns the result as a dict.
		
		:param query: The Graph API query to perform. (Eg: /me/picture?access_token=...)
		:type query: str
		:returns: A Dict containing the parsed JSON response from Facebook. Attributes are accessed through their name.
		"""
		
		# If query doesn't start with https://, we assume it is relative.
		if (not query.startswith("https://")):
			if "?" not in query:
				token = "?"
			else:
				token = "&"

			query = self.graph_uri + query + token + "access_token=" + self.access_token
		
		# Retrieve and parse result.
		data = urllib2.urlopen(query).read()
		json_obj = self.parse_json(data)

		return json_obj

class InitialiseTestCase(BaseFacebookGatewayTestCase):
	""" Test handling of init parameters: tokens, props, and policies
	"""

	def test_good_token(self):
		pass

	def test_bad_token(self):
		pass

	def test_no_token(self):
		pass

	def test_good_props(self):
		pass

	def test_bad_props(self):
		pass

	def test_no_props(self):
		pass

	def test_good_policy(self):
		pass

	def test_bad_policy(self):
		pass

	def test_no_policy(self):
		pass

class GetPermissionsForPolicyTestCase(BaseFacebookGatewayTestCase):
	def test_good_policy(self):
		expect_perms = ["public_profile", "user_education_history",
		"user_work_history",
		"user_relationships", "user_relationship_details", "user_religion_politics",
		"user_hometown", "user_birthday", "user_about_me", "user_location",
		"user_likes", "user_status", "user_posts", "user_friends", "user_photos",
		"user_tagged_places"]

		self.gateway = FacebookGateway.FacebookServiceGateway(access_token=None,
			props=self.get_good_props(), policy=self.get_good_processor())

		perms = self.gateway.generate_permissions_list()
		assert set(expect_perms) == set(perms)
		
	def test_bad_policy(self):
		expect_perms = ["user_likes", "user_status", "user_posts", "user_friends", "user_photos",
		"user_tagged_places"]

		self.gateway = FacebookGateway.FacebookServiceGateway(access_token=None,
			props=self.get_good_props(), policy=self.get_bad_processor())

		perms = self.gateway.generate_permissions_list()

		assert set(expect_perms) == set(perms)

class UserTestCase(BaseFacebookGatewayTestCase):
	def test_good_get(self):
		self.gateway = FacebookGateway.FacebookServiceGateway(access_token=None,
		props=self.get_good_props(), policy=self.get_good_processor())

		self.create_user_all_permissions()
		self.gateway.access_token = self.user['access_token']
		user = self.gateway.User("GET",self.user['id'])

		assert user.firstName == "Bob"
			
	@raises(NotImplementedError)
	def test_post(self):
		self.gateway = FacebookGateway.FacebookServiceGateway(access_token=None,
		props=self.get_good_props(), policy=self.get_good_processor())

		self.create_user_all_permissions()
		self.gateway.access_token = self.user['access_token']
		user = self.gateway.User("POST",self.user['id'])
		

		


	
	


