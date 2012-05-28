from ServiceGateway import ServiceGateway
import SocialObjects

import md5
import random
import urllib


class FacebookServiceGateway(ServiceGateway):
	"""
	Service gateway for Facebook.
	"""
	
	
	def __init__(self, access_token=None):
		"""
		Initialises itself with PRISONER's App ID and App Secret. (Might be unnecessary?)
		"""
		
		# App details.
		self.app_id = "123177727819065"
		self.app_secret = "ffccbab29c959b17bf53c8d200321c12"
		
		# URI references.
		self.auth_base_uri = "https://www.facebook.com/dialog/oauth?"
		self.request_base_uri = "http://graph.facebook.com"
		
		# Generate a unique state.
		r = random.random()
		self.state = md5.new(str(r)).hexdigest()
		
		# Permissions. (Horribly hacky for now)
		user_permissions = "user_about_me,user_activities,user_birthday,user_checkins,user_education_history,user_events,user_groups,user_hometown,user_interests,user_likes,user_location,user_notes,user_photos,user_questions,user_relationships,user_relationship_details,user_religion_politics,user_status,user_subscriptions,user_videos,user_website,user_work_history,email"
		friend_permissions = "friends_about_me,friends_activities,friends_birthday,friends_checkins,friends_education_history,friends_events,friends_groups,friends_hometown,friends_interests,friends_likes,friends_location,friends_notes,friends_photos,friends_questions,friends_relationships,friends_relationship_details,friends_religion_politics,friends_status,friends_subscriptions,friends_videos,friends_website,friends_work_history"
		extended_permissions = "read_friendlists,read_insights,read_mailbox,read_requests,read_stream,xmpp_login,ads_management,create_event,manage_friendlists,manage_notifications,user_online_presence,friends_online_presence,publish_checkins,publish_stream,rsvp_event"
		
		# Set the scope for our app. (What permissions do we need?)
		self.scope = user_permissions + "," + friend_permissions + "," + extended_permissions
	
	
	def request_authentication(self, callback):
		"""
		Initiates Facebook's authentication process.
		Returns a URI at which the user can confirm access to their profile by the application.
		"""
		
		params = {}
		params["client_id"] = self.app_id
		params["redirect_uri"] = callback
		params["scope"] = self.scope
		params["state"] = self.state
		
		uri = self.auth_base_uri + urllib.urlencode(params)
		return uri
	
	
	
# Testing.
if __name__ == "__main__":
	fb = FacebookServiceGateway()
	print fb.request_authentication("http://www.st-andrews.ac.uk")
		
		
		
