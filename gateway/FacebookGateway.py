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
		self.auth_request_uri = "https://www.facebook.com/dialog/oauth?"
		self.auth_token_uri = "https://graph.facebook.com/oauth/access_token?"
		self.graph_uri = "https://graph.facebook.com"
		
		# Generate a unique state.
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
		"""
		
		# Parameters for the authorisation request URI.
		params = {}
		params["client_id"] = self.app_id
		params["redirect_uri"] = callback
		params["scope"] = self.scope
		params["state"] = self.state
		
		uri = self.auth_request_uri + urllib.urlencode(params)
		return uri
	
	
	def complete_authentication(self, request):
		"""
		Completes authentication. Extracts the "code" param that Facebook provided and exchanges it for an
		access token so we can make authenticated calls on behalf of the user.
		"""
		
		# Before doing this, could check that our state value matches the state returned by Facebook. (Later addition)
		facebook_code = request.arguments['code'][0]
		#facebook_code = request # Uncomment me if testing with a known code.
		
		# Parameters for the token request URI.
		params = {}
		params["code"] = facebook_code
		params["client_secret"] = self.app_secret
		params["redirect_uri"] = "http://localhost:8888/"
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
				user_image = self.graph_uri + "/" + user_id + "/picture/" + "?access_token=" + self.access_token
				img_object.fullImage = user_image
				
				# Add any additional information to the image object.
				img_object.author = author_obj
				
				print "Image() details below:"
				print "Author ID: " + author_obj.id + ", Author Name: " + author_obj.displayName + ", Full Image: " + img_object.fullImage
				
				return img_object
			
			except:
				return SocialObjects.Image()
		else:
			raise NotImplementedException("Operation not supported")
	
	
	def get_graph(self, query):
		"""
		Queries Facebook's Graph API and returns the result as a dict.
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
	response = fb.request_authentication("http://www.st-andrews.ac.uk/")
	print "Request authentication URI: " + response
	
	# Complete authentication. (Comment out the parsing of input params in complete_authentication() to use)
	fb.complete_authentication("AQBhC4ulE3Mv_TLJHgnfXAZj5DU1_XM132ISR8z3c3J4M1pYIy-UVrAPahsb1NG_p1yudjqKob0qLJgXNslkW3cgpmr-kjqOZAgxmzRyJWtHYqA_U0Yi7IhL8kVvj3UdO4irNC-nJHvyUB0u7mJH2RzzlbGdTkq__vWcPmnMg_tjNM7aq6pXi8Soknpx_kE1qvI#_=_")
	
	fb.Image("GET", "")
	
	
