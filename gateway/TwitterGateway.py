from ServiceGateway import ServiceGateway
import SocialObjects
import urlparse
import oauth2
import datetime


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
		
		self.resp, self.content = self.client.request(self.request_token_url, "GET")
		self.timetest = datetime.datetime.now()
		if self.resp['status'] != '200':
		    raise Exception("Invalid response %s." % str(self.timetest))

		self.request_token = dict(urlparse.parse_qsl(self.content))

		print "Request Token:"
		print "    - oauth_token        = %s" % self.request_token['oauth_token']
		print "    - oauth_token_secret = %s" % self.request_token['oauth_token_secret']
		print 


		# Step 2: Redirect to the provider. Since this is a CLI script we do not 
		# redirect. In a web application you would redirect the user to the URL
		# below.

		return "%s?oauth_token=%s" % (self.authorize_url, self.request_token['oauth_token']) 

	
	
	# def complete_authentication(self, request):
	# 	"""
	# 	Completes authentication. Extracts the "code" param that Facebook provided and exchanges it for an
	# 	access token so we can make authenticated calls on behalf of the user.
		
	# 	:param request: Response from the first stage of authentication.
	# 	:type request: HTTPRequest
	# 	:returns: Unique access token that should persist for this user.
	# 	"""
		
	# 	# Before doing this, could check that our state value matches the state returned by Facebook. (Later addition)
	# 	facebook_code = None
	# 	#facebook_code = request # Uncomment me if testing with a known code.
		
	# 	if (request.args.has_key("code")):
	# 		facebook_code = request.args['code']
		
	# 	else:
	# 		return False
		
	# 	# Parameters for the token request URI.
	# 	params = {}
	# 	params["code"] = facebook_code
	# 	params["client_secret"] = self.app_secret
	# 	params["redirect_uri"] = self.redirect_uri
	# 	params["client_id"] = self.app_id
		
	# 	# Load the token request URI and get its response parameters.
	# 	token_request_uri = self.auth_token_uri + urllib.urlencode(params)
	# 	response = urlparse.parse_qs(urllib.urlopen(token_request_uri).read())
	# 	print "Response: " + str(response)
		
	# 	# Parse response to get access token and expiry date.
	# 	access_token = None
	# 	expires = None
		
	# 	self.access_token = response["access_token"][0]
	# 	expires = response["expires"][0]
		
	# 	# Create a User() object for the authenticated user.
	# 	auth_user = User()
		
	# 	# Query Facebook to get the authenticated user's ID and username.
	# 	result_set = self.get_graph_data("/me")
	# 	auth_user.id = self.get_value(result_set, "id")
	# 	auth_user.username = self.get_value(result_set, "username")
		
	# 	# Set up session.
	# 	self.session = auth_user
		
	# 	print "Access token: " + self.access_token
	# 	print "Token expires in: " + expires + " secs"
		
	# 	return self.access_token