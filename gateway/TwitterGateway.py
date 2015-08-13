from prisoner.gateway.ServiceGateway import ServiceGateway, WrappedResponse
import prisoner.SocialObjects as SocialObjects


import json
import urlparse
import oauth2
import datetime
import urllib


class TwitterServiceGateway(ServiceGateway):
	""" Service Gateway for Twitter.

	This gateway supports reading a user's timeline and publishing tweets on
	their behalf, with support for geo-tagged content.
	"""
	def __init__(self, policy=None, props=None):
		self.props = props
		self.service_name = "Twitter"
		self.service_description = "Micro-blogging service"

		self.consumer_key = props['api_key']
		self.consumer_secret = props['api_secret']

		self.request_token_url = 'https://api.twitter.com/oauth/request_token'
		self.access_token_url = 'https://api.twitter.com/oauth/access_token'
		self.authorize_url = 'http://twitter.com/oauth/authorize'
		self.user_details_url = 'https://api.twitter.com/1/account/verify_credentials.json'

		self.consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
		self.client = oauth2.Client(self.consumer)

		self.access_token = None

	def request_handler(self, request, operation, payload, extra_args=None):
		""" Wrapper around object requests. Used to inject any necessary debug headers
		"""
		self.props['args'] = extra_args
		resp = request(operation, payload)
		headers = {}
		if "debug" in self.props:
			pass

		return WrappedResponse(resp, headers)

	def request_authentication(self, callback):
		"""
		Initiates Facebook's authentication process.
		Returns a URI at which the user can confirm access to their profile by the application.

		:param callback: PRISONER's authentication flow URL. User must be redirected here after registering with Facebook
		in order to continue the flow.
		:type callback: str
		:return: URI the user must visit in order to authenticate.
		"""

		self.callback_url = urllib.urlencode({'oauth_callback':callback})

		self.resp, self.content = self.client.request(self.request_token_url, "POST", body=self.callback_url)
		if self.resp['status'] != '200':
		    raise Exception("Invalid response %s." % str(self.content))

		self.request_token = dict(urlparse.parse_qsl(self.content))

		return "%s?oauth_token=%s" % (self.authorize_url, self.request_token['oauth_token'])

	def complete_authentication(self, request):
		"""
		Completes authentication. Extracts the "code" param that Facebook provided and exchanges it for an
		access token so we can make authenticated calls on behalf of the user.

		:param request: Response from the first stage of authentication.
		:type request: HTTPRequest
		:returns: Unique access token that should persist for this user.
		"""
		if (request.args.has_key("oauth_verifier")):
			self.oauth_verifier = request.args['oauth_verifier']

		self.token = oauth2.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
		self.token.set_verifier(self.oauth_verifier)
		self.client = oauth2.Client(self.consumer, self.token)

		self.resp, self.content = self.client.request(self.access_token_url, "POST")
		self.content_json = dict(urlparse.parse_qsl(self.content))
		self.access_token_secret = self.content_json['oauth_token_secret']
		self.access_token = self.content_json['oauth_token']


		self.token = oauth2.Token(self.access_token, self.access_token_secret)
		self.client = oauth2.Client(self.consumer, self.token)

		auth_user = Person()
		auth_user.id = self.content_json['user_id']
		self.session = auth_user

		# self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'
		# self.timeline_params = {"user_id": self.content_json['user_id'],
		# 						"count": 50}
		# 						#"include_rts": 1,
		# 						#"exclude_replies":1}
		#
		# self.timeline_request = self.timeline_url + urllib.urlencode(self.timeline_params)
		#
		# self.resp, self.content = self.client.request(self.timeline_request, "GET")
		#


		return self.access_token

	def restore_authentication(self, access_token):
		"""
		Provides a mechanism to restore a session. (Essentially refresh an access token)
		Twitter does not allow access tokens to be refreshed. However, if the user is
		forced to go through the
		authentication process again, it will be done transparently so long as the PRISONER app has not requested
		additional permissions.

		:param access_token: The current access token held for this user.
		:type access_token: str
		:returns: False, thus forcing the authentication process to take place again. (Transparently)
		"""

		return False

	def Session(self):
		"""
		The Facebook session exposes the authenticated user as an instance of User().
		Can also be accessed in the same way as Person() as this class simply extends it.
		"""

		return self.session

	def Person(self, operation, payload):
		""" Gets the user profile of a user.

		:param operation: (GET) user
		:type operation: str
		:param payload: A Person or User whose ID is a Twitter user ID
		:type payload: Person
		:returns: User object populated by profile
		"""

		api_url = "https://api.twitter.com/1.1/users/show.json?"
		api_params = {'user_id':payload}


		api_request = api_url + urllib.urlencode(api_params)

		resp, content = self.client.request(api_request,"GET")
		user = Person()

		user_json = json.loads(content)
		print "user json: %s" % user_json
		user.id = payload
		user.displayName = user_json['name']

		return user


	def Note(self, operation, payload):
		""" Requests all
		tweets by a given user.

		:param operation: (GET) tweets
		:type operation: str
		:param payload: A Person whose ID is a Twitter ID
		:type payload: Person
		:returns: A list of Tweet objects
		"""
		self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'
		self.timeline_params = {"user_id": payload,
								"count": 50}
								#"include_rts": 1,
								#"exclude_replies":1}

		self.timeline_request = self.timeline_url + urllib.urlencode(self.timeline_params)

		self.resp, self.content = self.client.request(self.timeline_request, "GET")

		timeline = Timeline()
		tweet_list = []

		author = SocialObjects.Person()
		author.id = payload

		tweets = json.loads(self.content)
		for tweet in tweets:
			this_tweet = Note()
			this_tweet.author = author
			this_tweet.published = tweet['created_at']
			this_tweet.content = tweet['text']
			tweet_list.append(this_tweet)

		timeline.objects = tweet_list

		print "returning timeline!"
		return timeline

	# def Timeline(self, operation, payload):
	# 	"""
	# 	Performs operations relating to people's musical tastes.
	# 	Currently only supports GET operations, so we can just get the bands a person / user likes.
	#
	# 	:param operation: The operation to perform. (GET)
	# 	:type operation: str
	# 	:param payload: A User() or Person() whose ID is either a Facebook UID or username.
	# 	:type payload: SocialObject
	# 	:returns: A list of the bands this person likes.
	# 	"""
	#
	# 	self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'
	# 	self.timeline_params = {"user_id": payload,
	# 							"count": 50}
	# 							#"include_rts": 1,
	# 							#"exclude_replies":1}
	#
	# 	self.timeline_request = self.timeline_url + urllib.urlencode(self.timeline_params)
	#
	# 	self.resp, self.content = self.client.request(self.timeline_request, "GET")
	#
	# 	# Get user ID and query Facebook for their info.
	# 	timeline_id = payload
	# 	# Create user object.
	# 	timeline = Timeline()
	# 	timeline.id = timeline_id
	#
	# 	# Create author object for future use.
	# 	author = SocialObjects.Person()
	# 	author.id = timeline_id
	# 	timeline.author = author
	#
	# 	url_user = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&user_id="
	# 	return timeline

class Person(SocialObjects.Person):
	""" A Twitter User
	"""

	def __init__(self):
		super(Person, self).__init__()

class Timeline(SocialObjects.Collection):
	""" A collection of Tweets
	"""

	def __init__(self):
		super(Timeline, self).__init__()

class Note(SocialObjects.Note):
	""" A tweet is a single post shared to Twitter, derived from the base
	Note object.
	"""

	def __init__(self):
		super(Note, self).__init__()

# class Timeline(SocialObjects.Collection):
# 	"""
# 	Timelines are collections of
# 	"""
#
# 	def __init__(self):
# 		super(Timeline, self).__init__()
# 		self._provider = "Twitter"	# String
# 		self._id = None	# String
#
# 	@property
# 	def id(self):
# 		return self._id
#
# 	@id.setter
# 	def id(self, value):
# 		self._id = value
