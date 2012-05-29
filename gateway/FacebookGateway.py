from ServiceGateway import ServiceGateway
import SocialObjects

import json	# Used for parsing responses from Facebook.
import md5	# Used for generating unique state.
import random	# Used for generating unique state.
import urllib	# Used for formatting URI params, reading web addresses, etc.
import urllib2	# Used for formatting URI params, reading web addresses, etc.
import urlparse	# Used for reading Facebook access token.


class FacebookServiceGateway(ServiceGateway):
	"""
	Service gateway for Facebook.
	This gateway interacts with Facebook directly by making calls via the network's Social Graph API.
	"""
	
	
	def __init__(self, access_token=None):
		"""
		Initialises itself with PRISONER's App ID and App Secret. (Might be unnecessary?)
		"""
		
		# Gateway details.
		self.service_name = "Facebook"
		self.service_description = "Connect and share with people you know."
		
		# App details.
		self.app_id = "123177727819065"
		self.app_secret = "ffccbab29c959b17bf53c8d200321c12"
		
		# URI references.
		self.redirect_uri = None # Placeholder. This will be initialised by request_authorisation()
		self.auth_request_uri = "https://www.facebook.com/dialog/oauth?"
		self.auth_token_uri = "https://graph.facebook.com/oauth/access_token?"
		self.graph_uri = "https://graph.facebook.com"
		
		# Generate a unique state. (Required by Facebook for security)
		r = random.random()
		self.state = md5.new(str(r)).hexdigest()
		
		# Permissions. (Horribly hacky for now)
		user_permissions = "user_about_me,user_activities,user_birthday,user_checkins,user_education_history,user_events,user_groups,user_hometown,user_interests,user_likes,user_location,user_notes,user_photos,user_questions,user_relationships,user_relationship_details,user_religion_politics,user_status,user_subscriptions,user_videos,user_website,user_work_history,email"
		friend_permissions = "friends_about_me,friends_activities,friends_birthday,friends_checkins,friends_education_history,friends_events,friends_groups,friends_hometown,friends_interests,friends_likes,friends_location,friends_notes,friends_photos,friends_questions,friends_relationships,friends_relationship_details,friends_religion_politics,friends_status,friends_subscriptions,friends_videos,friends_website,friends_work_history"
		extended_permissions = "read_friendlists,read_insights,read_mailbox,read_requests,read_stream,xmpp_login,ads_management,create_event,manage_friendlists,manage_notifications,user_online_presence,friends_online_presence,publish_checkins,publish_stream,rsvp_event"
		
		# Set the scope for our app. (What permissions do we need?)
		self.scope = user_permissions + "," + friend_permissions + "," + extended_permissions
		
		# Placeholder for token.
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
		
		# Save the callback URI as our redirect. This is required by Facebook / OAuth.
		# (Redirect URIs for authentication and requesting token must match)
		self.redirect_uri = callback
		
		# Parameters for the authorisation request URI.
		params = {}
		params["client_id"] = self.app_id
		params["redirect_uri"] = self.redirect_uri
		params["scope"] = self.scope
		params["state"] = self.state
		
		uri = self.auth_request_uri + urllib.urlencode(params)
		return uri
	
	
	def complete_authentication(self, request):
		"""
		Completes authentication. Extracts the "code" param that Facebook provided and exchanges it for an
		access token so we can make authenticated calls on behalf of the user.
		
		:param request: Response from the first stage of authentication.
		:type request: HTTPRequest
		:returns: Unique access token that should persist for this user.
		"""
		
		# Before doing this, could check that our state value matches the state returned by Facebook. (Later addition)
		facebook_code = request.arguments['code'][0]
		#facebook_code = request # Uncomment me if testing with a known code.
		
		# Parameters for the token request URI.
		params = {}
		params["code"] = facebook_code
		params["client_secret"] = self.app_secret
		params["redirect_uri"] = self.redirect_uri
		params["client_id"] = self.app_id
		
		# Load the token request URI and get its response parameters.
		token_request_uri = self.auth_token_uri + urllib.urlencode(params)
		response = urlparse.parse_qs(urllib.urlopen(token_request_uri).read())
		
		# Parse response to get access token and expiry date.
		self.access_token = response["access_token"][0]
		expires = response["expires"][0]
		
		print "Access token: " + self.access_token
		print "Token expires in: " + expires + " secs"
		
		return self.access_token
	
	
	def Image(self, operation, payload):
		"""
		Dummy operation (At present) to get a user's Facebook profile picture.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: Provide a Person object, to return that user's profile image.
		:type payload: SocialObject
		:returns: An image object complete with author data and so on.
		"""

		if (operation == "GET"):
			try:
				user_id = payload.id
				#user_id = "me"
				
				# Get information about the image's author.
				author_obj = SocialObjects.Person()
				author_details = self.get_graph("/" + user_id)
				author_obj.id = author_details["id"]
				author_obj.displayName = author_details["name"]
			
				# Get the user's profile picture. (URL)
				img_object = SocialObjects.Image()
				user_image = self.graph_uri + "/" + user_id + "/picture?type=normal" + "&access_token=" + self.access_token
				img_object.fullImage = user_image
				
				# Add any additional information to the image object.
				img_object.author = author_obj
				
				return img_object
			
			except:
				return SocialObjects.Image()
		else:
			raise NotImplementedException("Operation not supported")
	
	
	def get_graph(self, query):
		"""
		Queries Facebook's Graph API and returns the result as a dict.
		
		:param query: The Graph API query to perform. (Eg: /me/picture?access_token=...)
		:type query: str
		:return: A Dict containing the parsed JSON response from Facebook. Attributes are accessed through their name.
		"""
		
		# Compose query to Facebook.
		query = self.graph_uri + query + "?access_token=" + self.access_token
		
		# Retrieve and parse result.
		data = urllib2.urlopen(query).read()
		json_obj = json.loads(data)

		return json_obj
		
	
	
	
# Testing.
if __name__ == "__main__":
	# Create an instance of the service gateway.
	fb = FacebookServiceGateway()
	
	# Request authentication and print the resulting URI.
	# To test, go to the address printed on-screen, sign in, then copy the "Code" param from the URI and paste it 
	# in the complete_authentication() method below.
	response = fb.request_authentication(fb.redirect_uri) # This param would be callback under real usage.
	print "Request authentication URI: " + response
	
	# Complete authentication. (Comment out the parsing of input params in complete_authentication() to use)
	fb.complete_authentication("AQDl1Sveh39IuntpJjJnf0yovWEi1z-c7SRv1vuLk1lqoNne6ncTCzM0zn10WvSwkgFVRcNE1xjqqLNsBI2Ctxf0kO1pTaB1pVHHpogZGg6M1JSuuxh3OYqr3x_qa-1Yk7HAPp7Q5xqG1sVuvqHD8CnmL0gdzQMYkx0e_PzbIh700FQOdt5QMyR_eexZ65sZg48#_=_")
	
	# Set up a person for testing.
	person_1 = SocialObjects.Person()
	person_1.id = "532336768"
	
	# Test "Get Image."
	img_obj = fb.Image("GET", person_1)
	print "Grabbed image from Facebook:"
	print "- Full image: " + img_obj.fullImage
	print "- Author ID: " + img_obj.author.id
	print "- Author name: " + img_obj.author.displayName
	
	
