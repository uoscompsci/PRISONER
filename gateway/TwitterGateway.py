from ServiceGateway import ServiceGateway
import SocialObjects
import urlparse
import oauth2
import datetime
import urllib


class TwitterServiceGateway(ServiceGateway):
	""" Service Gateway for Twitter. 
	
	This gateway supports reading a user's timeline and publishing tweets on
	their behalf, with support for geo-tagged content.
	"""
	def __init__(self):
		self.service_name = "Twitter"
		self.service_description = "Micro-blogging service"

		self.consumer_key = 'x39RMkComhNOjLgnhUfyXA'
		self.consumer_secret = 'LJ2mas1AgEPkF5Z67cs6BUHcuBh1sNZ9LJtYqPVFqI4'

		self.request_token_url = 'https://api.twitter.com/oauth/request_token'
		self.access_token_url = 'https://api.twitter.com/oauth/access_token'
		self.authorize_url = 'http://twitter.com/oauth/authorize'

		self.consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
		self.client = oauth2.Client(self.consumer)

		self.access_token = None

	
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
		
		return self.access_token
		
	def Timeline(self, operation, payload):
		"""
		Performs operations relating to people's musical tastes.
		Currently only supports GET operations, so we can just get the bands a person / user likes.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of the bands this person likes.
		"""

		url_user = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&user_id="
		tristans_id = "17899123"
		raise Exception("Invalid response %s." % str(payload))
		