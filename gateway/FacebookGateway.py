from ServiceGateway import ServiceGateway
import SocialObjects

import datetime	# Used for creating standardised date / time objects from Facebook's attribute values.
import json	# Used for parsing responses from Facebook.
import md5	# Used for generating unique state.
import random	# Used for generating unique state.
import urllib2	# Used for formatting URI params, reading web addresses, etc.
import urllib	# Used for formatting URI params, reading web addresses, etc.
import urlparse	# Used for reading Facebook access token.


class FacebookServiceGateway(ServiceGateway):
	"""
	Service gateway for Facebook.
	This gateway interacts with Facebook directly by making calls via the network's Social Graph API.
	"""
	
	
	def __init__(self, access_token=None):
		"""
		Initialises itself with PRISONER's App ID and App Secret.
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
		#facebook_code = request.arguments['code'][0]
		facebook_code = request # Uncomment me if testing with a known code.
		
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
	
	
	def restore_authentication(self, access_token):
		"""
		Provides a mechanism to restore a session. (Essentially refresh an access token)
		Facebook does not allow access tokens to be refreshed. However, if the user is forced to go through the
		authentication process again, it will be done transparently so long as the PRISONER app has not requested
		additional permissions.
		
		:param access_token: The current access token held for this user.
		:type access_token: str
		:returns: False, thus forcing the authentication process to take place again. (Transparently)
		"""
		
		return False
	
	
	def User(self, operation, payload):
		"""
		Performs operations on a User object.
		Takes a Person object as a payload and returns a new object populated with that person's profile information.
		Only supports GET operations as you can only get a user's details, not change them.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A Person() or User() object whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A User() object with all available attributes populated.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				user_details = self.get_graph_data("/" + user_id)
				
				# Create and populate person object.
				user = User()
				user.id = self.get_value(user_details, "id")
				user.firstName = self.get_value(user_details, "first_name")
				user.middleName = self.get_value(user_details, "middle_name")
				user.lastName = self.get_value(user_details, "last_name")
				user.username = self.get_value(user_details, "username")
				user.displayName = self.get_value(user_details, "name")
				user.gender = self.get_value(user_details, "gender")
				
				# Get a list of the user's languages.
				languages = self.get_value(user_details, "languages")
				
				# Info exists.
				if ((languages) and (len(languages)) > 0):
					# Create list to hold languages.
					lang_list = []
					
					# Loop through languages and add to list.
					for lang in languages:
						this_lang = lang["name"]
						lang_list.append(this_lang)
					
					user.languages = lang_list
				
				# No info.
				else:
					user.languages = None
				
				user.timezone = self.get_value(user_details, "timezone")
				
				# Parse the user's last update time.
				updated_time_str = self.get_value(user_details, "updated_time")
				timestamp = self.str_to_time(updated_time_str)
				user.updatedTime = timestamp
				
				user.bio = self.get_value(user_details, "about")
				
				# Parse the user's birthday.
				birthday_str = self.get_value(user_details, "birthday")
				birthday_timestamp = self.str_to_time(birthday_str)
				user.birthday = birthday_timestamp
				
				# Get a list detailing the user's education history.
				education_list = self.get_value(user_details, "education")
				
				# Info exists.
				if ((education_list) and (len(education_list) > 0)):
					# Create Collection object to hold education history.
					edu_coll = SocialObjects.Collection()
					edu_coll.author = user.id
					edu_list = []
					
					# Loop through places and add to list.
					for place in education_list:
						this_place = SocialObjects.Place()
						this_place.id = place["school"]["id"]
						this_place.displayName = place["school"]["name"]
						edu_list.append(this_place)
					
					edu_coll.objects = edu_list
					user.education = edu_coll
						
				
				# No info.
				else:
					user.education = None
				
				user.email = self.get_value(user_details, "email")
				
				# Make a Place object for the user's hometown.
				hometown_place = SocialObjects.Place()
				hometown_info = self.get_value(user_details, "hometown")
				
				# Hometown supplied.
				if (hometown_info):
					hometown_place.id = hometown_info["id"]
					hometown_place.displayName = hometown_info["name"]
					user.hometown = hometown_place
				
				# Not supplied.
				else:
					user.hometown = None
				
				# Make a Place object for the user's current location.
				location_place = SocialObjects.Place()
				location_info = self.get_value(user_details, "location")
				
				# Location supplied.
				if (location_info):
					location_place.id = location_info["id"]
					location_place.displayName = location_info["name"]
					user.location = location_place
				
				# Location not supplied.
				else:
					user.location = None
				
				
				user.interestedIn = self.get_value(user_details, "interested_in")
				user.politicalViews = self.get_value(user_details, "political")
				user.religion = self.get_value(user_details, "religion")
				user.relationshipStatus = self.get_value(user_details, "relationship_status")
				
				# Make a User object for the user's significant other.
				sig_other = User()
				sig_other_info = self.get_value(user_details, "significant_other")
				
				# Info exists.
				if (sig_other_info):
					sig_other.id = sig_other_info["id"]
					sig_other.displayName = sig_other_info["name"]
					user.significantOther = sig_other
				
				# No info.
				else:
					user.significantOther = None
				
				# Get a list detailing the user's work history.
				work_history = self.get_value(user_details, "work")
				
				# Info exists.
				if ((work_history) and (len(work_history) > 0)):
					# Create Collection object to hold work history.
					work_coll = SocialObjects.Collection()
					work_coll.author = user.id
					work_list = []
					
					# Loop through places and add to list.
					for place in work_history:
						this_place = SocialObjects.Place()
						this_place.id = place["employer"]["id"]
						this_place.displayName = place["employer"]["name"]
						work_list.append(this_place)
					
					work_coll.objects = work_list
					user.work = work_coll
						
				
				# No info.
				else:
					user.work = None
				
				# Get the user's profile picture.
				img = SocialObjects.Image()
				img.fullImage = self.graph_uri + "/me/picture?type=normal" + "&access_token=" + self.access_token
				user.image = img
				
				return user
				
			except:
				return User()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Music(self, operation, payload):
		"""
		Performs operations relating to people's musical tastes.
		Currently only supports GET operations, so we can just get the bands a person / user likes.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of the bands this person likes.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/music")
				band_obj_list = []
				
				# While there are still more bands, add them to the list.
				while (result_set["paging"].has_key("next")):
					# Get bands.
					band_obj_list.extend(result_set["data"])
					
					# Get next result set.
					result_set = self.get_graph_data(result_set["paging"]["next"])
				
				# Loop through the band object list and add their names to a separate list.
				bands = []
				
				for band in band_obj_list:
					bands.append(self.get_value(band, "name"))
				
				# Return a sorted list.
				return sorted(bands)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Movies(self, operation, payload):
		"""
		Performs operations relating to people's taste in films.
		Currently only supports GET operations. This lets us retrieve the movies / films people like.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of the movies this person likes.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/movies")
				movie_obj_list = []
				
				# While there are still more movies available, add them to the list.
				while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
					# Get movies.
					movie_obj_list.extend(result_set["data"])
					
					# Get next result set.
					result_set = self.get_graph_data(result_set["paging"]["next"])
				
				# Loop through the movie object list and add their names to a separate list.
				movies = []
				
				for movie in movie_obj_list:
					movies.append(self.get_value(movie, "name"))
				
				# Return a sorted list.
				return sorted(movies)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Books(self, operation, payload):
		"""
		Performs operations relating to people's taste in books and literature.
		Currently only supports GET operations. This lets us get the books / authors people are into.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of the books this person likes.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/books")
				book_obj_list = []
				
				# While there are still more books available, add them to the list.
				while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
					# Get books.
					book_obj_list.extend(result_set["data"])
					
					# Get next result set.
					result_set = self.get_graph_data(result_set["paging"]["next"])
				
				# Loop through the book object list and add their names to a separate list.
				books = []
				
				for book in book_obj_list:
					books.append(self.get_value(book, "name"))
				
				# Return a sorted list.
				return sorted(books)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
		
		
	def Statuses(self, operation, payload):
		"""
		Performs operations on a user's status updates.
		Currently only supports GET operations. This lets us retrieve a user's entire backlog of status updates.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A collection representing this person's backlog of status updates.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				
				# Get the initial result set.
				limit = 100
				offset = 0
				status_obj_list = []
				result_set_address = self.graph_uri + "/me/statuses?limit=" + str(limit) + "&offset=" + str(offset) + "&access_token=" + self.access_token
				result_set = self.get_graph_data(result_set_address)
				
				# So long as there's data, parse it.
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Get status updates.
					this_data = result_set["data"]
					
					# Add each update to our list.
					for item in this_data:
						status_obj_list.append(item)
					
					# Compose next address.
					offset = offset + limit
					next_address = self.graph_uri + "/me/statuses?limit=" + str(limit) + "&offset=" + str(offset) + "&access_token=" + self.access_token
					result_set = self.get_graph_data(next_address)
				
				# Create collection object and list to hold status updates.
				status_coll = StatusList()
				status_coll.author = user_id
				status_list = []
				
				# For each status we retrieved...
				for status in status_obj_list:
					# Set basic info.
					this_status = Status()
					this_status.author = user_id
					this_status.content = self.get_value(status, "message")
					this_status.id = self.get_value(status, "id")
					this_status.published = self.str_to_time(self.get_value(status, "updated_time"))
					this_status.url = "https://www.facebook.com/" + user_id + "/posts/" + this_status.id
					
					# Parse likes. (Initial limit of 25 per status)
					likes_coll = Likes()
					likes_coll.objects = self.parse_likes(status)
					this_status.likes = likes_coll
					
					# Parse comments. (Initial limit of 25 per status)
					comments_coll = Comments()
					comments_coll.objects = self.parse_comments(status)
					this_status.comments = comments_coll
					
					# Parse location.
					this_status.location = self.parse_location(status)
					
					# Add status to our list of statuses.
					status_list.append(this_status)
				
				# Add the status list to our collection.
				status_coll.objects = status_list
				
				# Return statuses.
				return status_coll
				
			
			except:
				return StatusList()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Friends(self, operation, payload):
		"""
		Performs operations on a user's friends.
		Only supports GET operations. This lets us retrieve someone's entire friends list.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: Person
		:returns: A collection representing this person's friends list.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their friends.
				user_id = payload.id
				result_set = self.get_graph_data("/" + user_id + "/friends")
				friend_coll = FriendsList()
				friend_obj_list = []
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of friends.
					this_data = result_set["data"]
					
					# For each friend in this batch...
					for friend in this_data:
						# Get basic info for this friend.
						this_friend = User()
						this_friend.id = self.get_value(friend, "id")
						this_friend.displayName = self.get_value(friend, "name") 
						
						# Compose profile pic address.
						profile_pic = SocialObjects.Image()
						profile_pic.fullImage = self.graph_uri + "/" + this_friend.id + "/picture?type=normal" + "&access_token=" + self.access_token
						profile_pic.author = this_friend.id
						this_friend.image = profile_pic
						
						# Add friend to list.
						friend_obj_list.append(this_friend)
					
					# Get next set of results.
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Add friend list to collection and return.
				friend_coll.objects = friend_obj_list
				return friend_coll
				
			except:
				return FriendsList()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Albums(self, operation, payload):
		"""
		Performs operations on a user's photo albums.
		Currently only supports GET operations. This lets us retrieve a list of photo albums associated with the
		supplied payload ID.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: Person
		:returns: A collection representing this person / object's photo albums.
		"""
		
		if (operation == "GET"):
			try:
				# Get the object's ID from the payload and query for albums.
				obj_id = payload.id
				result_set = self.get_graph_data("/" + obj_id + "/albums")
				album_coll = Albums()
				album_obj_list = []
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of albums.
					this_data = result_set["data"]
					
					for album in this_data:
						# Set basic album info.
						this_album = Album()
						this_album.id = self.get_value(album, "id")
						this_album.displayName = self.get_value(album, "name")
						this_album.author = self.get_value(album["from"], "id")
						this_album.published = self.str_to_time(self.get_value(album, "created_time"))
						this_album.summary = self.get_value(album, "description")
						this_album.updated = self.str_to_time(self.get_value(album, "updated_time"))
						this_album.url = self.get_value(album, "link")
						
						# Parse location info.
						this_album.location = self.parse_location(album)
						
						# Cover photo.
						cover_photo = SocialObjects.Image()
						cover_photo.author = this_album.author
						cover_id = self.get_value(album, "cover_photo")
						
						# Only compose a cover photo if one exists.
						if (cover_id):
							cover_photo.fullImage = self.graph_uri + "/" + cover_id + "/picture?type=normal" + "&access_token=" + self.access_token
						
						this_album.coverPhoto = cover_photo
						
						# Set additional info.
						this_album.privacy = self.get_value(album, "privacy")
						this_album.count = self.get_value(album, "count")
						this_album.albumType = self.get_value(album, "type")
						
						# Parse likes.
						likes_list = self.parse_likes(album)
						album_likes = Likes()
						album_likes.objects = likes_list
						this_album.likes = album_likes
						
						# Parse comments.
						comments_list = self.parse_comments(album)
						album_comments = Comments()
						album_comments.objects = comments_list
						this_album.comments = album_comments
						
						# Add this album to our list of albums.
						album_obj_list.append(this_album)
					
					# Get next set of results.
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Populate and return our album collection.
				album_coll.objects = album_obj_list
				return album_coll
				
			except:
				return Albums()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Images(self, operation, payload):
		"""
		Performs operations on images.
		Currently only supports GET operations. This lets us retrieve the photos associated with the supplied 
		payload's ID. This will commonly be an Album() to get the photos in said album, or a User() / Person() 
		to get any photos they're tagged in.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: The Facebook object to retrieve associated photos for.
		:type payload: SocialObject
		:returns: A collection representing photos associated with the supplied object.
		"""

		if (operation == "GET"):
			try:
				# Get the payload object's ID.
				obj_id = str(payload.id)
				result_set = self.get_graph_data("/" + obj_id + "/photos")
				photo_obj_list = []
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of photos.
					this_data = result_set["data"]
					
					# For each photo in this batch...
					for photo in this_data:
						# Create photo object and set basic info.
						this_photo = Photo()
						this_photo.id = self.get_value(photo, "id")
						this_photo.author = self.get_value(photo["from"], "id")
						this_photo.displayName = self.get_value(photo, "name")
						this_photo.published = self.str_to_time(self.get_value(photo, "created_time"))
						this_photo.updated = self.str_to_time(self.get_value(photo, "updated_time"))
						this_photo.url = self.get_value(photo, "link")
						this_photo.position = self.get_value(photo, "position")
						
						# Get image info.
						img_normal = SocialObjects.Image()
						img_normal.id = this_photo.id
						img_normal.author = this_photo.author
						img_normal.fullImage = self.get_value(photo["images"][0], "source")
						this_photo.image = img_normal
						
						# Image dimensions.
						this_photo.width = self.get_value(photo["images"][0], "width")
						this_photo.height = self.get_value(photo["images"][0], "height")
						
						# Thumbnail info.
						img_small = SocialObjects.Image()
						img_small.id = this_photo.id
						img_small.author = this_photo.author
						img_small.fullImage = self.get_value(photo, "picture")
						this_photo.thumbnail = img_small
						
						# Parse location info.
						this_photo.location = self.parse_location(photo)
						
						# Parse likes.
						likes_list = self.parse_likes(photo)
						photo_likes_coll = Likes()
						photo_likes_coll.objects = likes_list
						this_photo.likes = photo_likes_coll
						
						# Parse comments.
						comments_list = self.parse_comments(photo)
						photo_comments_coll = Comments()
						photo_comments_coll.objects = comments_list
						this_photo.comments = photo_comments_coll
						
						# Parse tags.
						tags_list = self.parse_tags(photo)
						photo_tags_coll = Tags()
						photo_tags_coll.objects = tags_list
						this_photo.tags = photo_tags_coll
						
						# Add photo to list.
						photo_obj_list.append(this_photo)
					
					# Get next set of results.
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Create a collection object for the photos.
				photo_album = Photos()
				photo_album.objects = photo_obj_list
				
				# If the payload was a photo album, add the photos into it.
				if (type(payload) is Album):
					payload.photos = photo_album
					return payload
				
				# Otherwise return the collection object.
				else:
					return photo_album
			
			except:
				return Photos()
		
		else:
			raise NotImplementedException("Operation not supported")
	
	
	def Checkins(self, operation, payload):
		"""
		Performs operations on check-ins / objects with location.
		Currently only supports GET operations. This lets us retrieve a list of places the supplied User()
		or Person() has been.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: The User() or Person() object to retrieve check-in information for.
		:type payload: SocialObject
		:returns: A collection of objects representing check-ins.
		"""

		if (operation == "GET"):
			try:
				# Get user ID from payload and query for initial result set.
				user_id = payload.id
				result_set = self.get_graph_data("/" + user_id + "/locations")
				checkin_obj_list = []
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of check-ins.
					this_data = result_set["data"]
					
					# Loop through each check-in on this page.
					for checkin in this_data:
						# Get and set basic info.
						this_checkin = Checkin()
						this_checkin.id = self.get_value(checkin, "id")
						this_checkin.author = self.get_value(checkin["from"], "id")
						this_checkin.checkinType = self.get_value(checkin, "type")
						this_checkin.published = self.str_to_time(self.get_value(checkin, "created_time"))
						
						# Get location info.
						this_checkin.location = self.parse_location(checkin)
						
						# Get tag info. (People that've been tagged in this check-in)
						tags_list = self.parse_tags(checkin)
						tags_coll = Tags()
						tags_coll.objects = tags_list
						this_checkin.tags = tags_coll
						checkin_obj_list.append(this_checkin)
					
					# Get next set of results.
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Compose collection and return it.
				checkins_coll = Checkins()
				checkins_coll.objects = checkin_obj_list
				return checkins_coll
			
			except:
				return Checkins()
		
		else:
			raise NotImplementedException("Operation not supported")
	
	
	def parse_likes(self, facebook_obj):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a list of the people who've liked it.
		Note that this function just PARSES. It does not attempt to retrieve all the likes for the given 
		object. This means it has a limit of around 25 likes.
		
		:param facebook_obj: The Facebook object to get likes for.
		:type facebook_obj: Dict
		:returns: A list representing the people / users that have liked this object.
		"""
		
		# This object has likes.
		if (facebook_obj.has_key("likes")):
			likes = []
			have_liked = facebook_obj["likes"]["data"]
			
			# Loop through likes and add them to our list.
			for person in have_liked:
				this_person = User()
				this_person.id = self.get_value(person, "id")
				this_person.displayName = self.get_value(person, "name")
				likes.append(this_person)
			
			return likes
		
		# No likes, return an empty list.
		else:
			return []
	
	
	def parse_comments(self, facebook_obj):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a list of the comments on it.
		Note that this function just PARSES. It does not attempt to retrieve all the comments on the given 
		object. This means it has a limit of around 25 comments.
		
		:param facebook_obj: The Facebook object to get comments on.
		:type facebook_obj: Dict
		:returns: A list representing the comments on this object.
		"""
		
		# This object has comments.
		if (facebook_obj.has_key("comments")):
			comments = []
			comments_on = facebook_obj["comments"]["data"]
			
			# Loop through comments and add them to our list.
			for comment in comments_on:
				this_comment = Comment()
				this_comment.id = self.get_value(comment, "id")
				this_comment.author = self.get_value(comment["from"], "id")
				this_comment.content = self.get_value(comment, "message")
				this_comment.published = self.str_to_time(self.get_value(comment, "created_time"))
				this_comment.url = "https://www.facebook.com/me/posts/" + this_comment.id
				comments.append(this_comment)
			
			return comments
		
		# No comments, return an empty list.
		else:
			return []
	
	
	def parse_location(self, facebook_obj):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a Place object representing its location.
		
		:param facebook_obj: The Facebook object to get the location of.
		:type facebook_obj: Dict
		:returns: A Place() object representing the location of the supplied object.
		"""
		
		# Get location.
		if (facebook_obj.has_key("place")):
			place = SocialObjects.Place()
			place.id = self.get_value(facebook_obj["place"], "id")
			place.displayName = self.get_value(facebook_obj["place"], "name")
						
			# Get additional location info if it's present.
			if (facebook_obj["place"].has_key("location")):
				latitude = str(self.get_value(facebook_obj["place"]["location"], "latitude"))
				longitude = str(self.get_value(facebook_obj["place"]["location"], "longitude"))
							
				# Format latitude if necessary.
				if (not latitude.startswith("-")):
					latitude = "+" + latitude
							
				# Format longitude if necessary.
				if (not longitude.startswith("-")):
					longitude = "+" + longitude
							
				place.position = latitude + longitude + "/"
						
			# Get address info if available.
			if ((facebook_obj["place"]["location"].has_key("city")) and (facebook_obj["place"]["location"].has_key("country"))):
				city = self.get_value(facebook_obj["place"]["location"], "city")
				country = self.get_value(facebook_obj["place"]["location"], "country")
				place.address = place.displayName + ", " + city + ", " + country
			
			# Return place object.
			return place
		
		# Return empty place.
		else:
			return SocialObjects.Place()
	
	
	def parse_tags(self, facebook_obj):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a list of the objects that have been tagged
		in it. (Usually people)
		
		:param facebook_obj: The Facebook object to get tags for.
		:type facebook_obj: Dict
		:returns: A list representing the people / objects that were tagged in the supplied object.
		"""
		
		# This object has tags.
		if (facebook_obj.has_key("tags")):
			tags = []
			are_tagged = facebook_obj["tags"]["data"]
			
			# Loop through the tags and add them to our list.
			for person in are_tagged:
				this_person = User()
				this_person.id = self.get_value(person, "id")
				this_person.displayName = self.get_value(person, "name")
				tags.append(this_person)
			
			return tags
		
		# No likes, return an empty list.
		else:
			return []
	
	
	def get_likes(self, object_id):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a list of the people who've liked it.
		
		:param facebook_obj: The Facebook object to get likes for.
		:type facebook_obj: Dict
		:returns: A list representing the people / users that have liked this object.
		"""
		
		# Get initial likes.
		likes = []
		result_set = self.get_graph_data("/" + object_id + "/likes")
		
		# Loop through all likes and add them to our list.
		while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
			while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
				have_liked = result_set["data"]
				
				# Create a User object for each like...
				for person in have_liked:
					this_person = User()
					this_person.id = person["id"]
					this_person.displayName = person["name"]
					likes.append(this_person)
				
				# Get the next result set.
				result_set = self.get_graph_data(result_set["paging"]["next"])
		
		return likes
	
	
	def get_comments(self, object_id):
		"""
		Internal function.
		Takes a JSON Facebook object and returns a list of the comments on it.
		
		:param facebook_obj: The Facebook object to get comments on.
		:type facebook_obj: Dict
		:returns: A list representing the comments on this object.
		"""
		
		# Get initial comments.
		comments = []
		result_set = self.get_graph_data("/" + object_id + "/comments")
		
		# Loop through all comments and add them to our list.
		while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
			while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
				comment_list = result_set["data"]
				
				# Make a Comment() object for each comment in the list...
				for comment in comment_list:
					this_comment = Comment()
					this_comment.id = comment["id"]
					this_comment.author = comment["from"]["id"]
					this_comment.content = comment["message"]
					this_comment.published = self.str_to_time(comment["created_time"])
					this_comment.url = "https://www.facebook.com/me/posts/" + this_comment.id
					comments.append(this_comment)
				
				# Get the next set of results.
				result_set = self.get_graph_data(result_set["paging"]["next"])
		
		return comments
	
	
	def get_graph_data(self, query):
		"""
		Internal function.
		Queries Facebook's Graph API and returns the result as a dict.
		
		:param query: The Graph API query to perform. (Eg: /me/picture?access_token=...)
		:type query: str
		:returns: A Dict containing the parsed JSON response from Facebook. Attributes are accessed through their name.
		"""
		
		# If query doesn't start with https://, we assume it is relative.
		if (not query.startswith("https://")):
			query = self.graph_uri + query + "?access_token=" + self.access_token
		
		# Retrieve and parse result.
		data = urllib2.urlopen(query).read()
		json_obj = self.parse_json(data)

		return json_obj
	
	
	def get_value(self, haystack, needle):
		"""
		Internal function.
		Attempts to get the value corresponding to the supplied key.
		If no key exists, None is returned.
		
		:param haystack: The Dictionary object to look at.
		:type query: dict
		:param needle: The key we're looking for.
		:type query: str
		:returns: If the key exists, its corresponding value is returned. Otherwise None is returned.
		"""
		
		# This key exists, so return it.
		if haystack.has_key(needle):
			return haystack[needle]
		
		# Key doesn't exist.
		else:
			return None
	
	
	def parse_json(self, json_obj):
		"""
		Internal function.
		Takes a JSON object as returned by Facebook and returns the Dict representation of it.
		Avoids having to call json.loads(?) everywhere, and allows for potential improvements in the future.
		
		:param json_obj: The JSON object to parse.
		:type json_obj: str, list
		:returns: A Dict object representing the supplied JSON.
		"""
		
		return json.loads(json_obj)
	
	
	def str_to_time(self, time):
		"""
		Internal function.
		Used to convert Facebook's ISO-8601 date/time into a Date/Time object.
		Also converts Facebook's MM/DD/YYYY format used for birthdays.
		
		:param time: The string to parse.
		:type time: str
		:returns: A Date/Time object.
		"""
		
		# ISO 8601
		if (len(time) > 10):
			return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+0000")
		
		# MM/DD/YYYY
		else:
			return datetime.datetime.strptime(time, "%m/%d/%Y")
		
class User(SocialObjects.Person):
	"""
	A Facebook user object. Contains details such as name, email address and other personal information.
	Could probably be used in place of a Person object in some cases, as a User object has an id which can 
	be used to query Facebook.
	"""
	
	def __init__(self):
		super(User, self).__init__()
		self._provider = "Facebook"	# String
		self._username = None	# String
		self._firstName = None	# String
		self._middleName = None	# String
		self._lastName = None	# String
		self._gender = None	# String
		self._languages = None	# List of strings
		self._timezone = None	# String
		self._updatedTime = None	# Date / Time
		self._bio = None	# String
		self._birthday = None	# Date / Time
		self._education = None	# Collection of places
		self._email = None	# String
		self._hometown = None	# Place
		self._interestedIn = None	# List of strings
		self._location = None	# Place
		self._politicalViews = None	# String
		self._religion = None	# String
		self._relationshipStatus = None	# String
		self._significantOther = None	# User or Person object
		self._work = None	# Collection of places
	
	
	@property
	def username(self):
		""" This person's Facebook username. """
		return self._username
	
	
	@property
	def firstName(self):
		""" This person's first name. """
		return self._firstName
	
	
	@property
	def middleName(self):
		""" This person's middle name. """
		return self._middleName
	
	
	@property
	def lastName(self):
		""" This person's last name. """
		return self._lastName
	
	
	@property
	def gender(self):
		""" This person's gender. """
		return self._gender
	
	
	@property
	def languages(self):
		""" Languages this person can speak. """
		return self._languages
	
	
	@property
	def timezone(self):
		""" This person's timezone. (Offset from UTC) """
		return self._timezone
	
	
	@property
	def updatedTime(self):
		""" When this person last updated their Facebook profile. """
		return self._updatedTime
	
	
	@property
	def bio(self):
		""" This person's short biography. """
		return self._bio
	
	
	@property
	def birthday(self):
		""" This person's birthday. """
		return self._birthday
	
	
	@property
	def education(self):
		""" This person's education history. """
		return self._education
	
	
	@property
	def email(self):
		""" This person's email address. """
		return self._email
	
	
	@property
	def hometown(self):
		""" This person's hometown. """
		return self._hometown
	
	
	@property
	def location(self):
		""" This person's current location. """
		return self._location
	
	
	@property
	def interestedIn(self):
		""" This person's sexual orientation. """
		return self._interestedIn
	
	
	@property
	def politicalViews(self):
		""" This person's political preferences. """
		return self._politicalViews
	
	
	@property
	def religion(self):
		""" This person's religion. """
		return self._religion
	
	
	@property
	def relationshipStatus(self):
		""" This person's relationship status. """
		return self._relationshipStatus
	
	
	@property
	def significantOther(self):
		""" This person's significant other. """
		return self._significantOther
	
	
	@property
	def work(self):
		""" This person's work history. """
		return self._work
	
	
	@username.setter
	def username(self, value):
		self._username = value
	
	
	@firstName.setter
	def firstName(self, value):
		self._firstName = value
	
	
	@middleName.setter
	def middleName(self, value):
		self._middleName = value
	
	
	@lastName.setter
	def lastName(self, value):
		self._lastName = value
	
	
	@gender.setter
	def gender(self, value):
		self._gender = value
	
	
	@languages.setter
	def languages(self, value):
		self._languages = value
	
	
	@timezone.setter
	def timezone(self, value):
		self._timezone = value
	
	
	@updatedTime.setter
	def updatedTime(self, value):
		self._updatedTime = value
	
	
	@bio.setter
	def bio(self, value):
		self._bio = value
	
	
	@birthday.setter
	def birthday(self, value):
		self._birthday = value
	
	
	@education.setter
	def education(self, value):
		self._education = value
	
	
	@email.setter
	def email(self, value):
		self._email = value
	
	
	@hometown.setter
	def hometown(self, value):
		self._hometown = value
	
	
	@location.setter
	def location(self, value):
		self._location = value
	
	
	@interestedIn.setter
	def interestedIn(self, value):
		self._interestedIn = value
	
	
	@politicalViews.setter
	def politicalViews(self, value):
		self._politicalViews = value
	
	
	@religion.setter
	def religion(self, value):
		self._religion = value
	
	
	@relationshipStatus.setter
	def relationshipStatus(self, value):
		self._relationshipStatus = value
	
	
	@significantOther.setter
	def significantOther(self, value):
		self._significantOther = value
	
	
	@work.setter
	def work(self, value):
		self._work = value
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off the string representation...
		str_rep =  "<User>" + "\n"
		
		# Single value.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Display Name: " + unicode((check_none(self.displayName))) + "\n"
		str_rep += "- Profile Picture: " + check_none(self.image.fullImage) + "\n"
		str_rep += "- Username: " + check_none(self.username) + "\n"
		str_rep += "- First Name: " + unicode(check_none(self.firstName)) + "\n"
		str_rep += "- Middle Name: " + unicode(check_none(self.middleName)) + "\n"
		str_rep += "- Last Name: " + unicode(check_none(self.lastName)) + "\n"
		str_rep += "- Gender: " + check_none(self.gender) + "\n"
		str_rep += "- Last Update: " + str(check_none(self.updatedTime)) + "\n"
		str_rep += "- Birthday: " + str(check_none(self.birthday)) + "\n"
		
		# Multi value.
		user_langs = check_none(self.languages)
		str_rep += "- Language: " + str(user_langs) + "\n"
		
		# Single value.
		str_rep += "- Timezone: " + check_none(str(self.timezone)) + "\n"
		str_rep += "- Bio: " + unicode(check_none(self.bio)) + "\n"
		
		# Multi value.
		user_education = check_none(self.education)
		
		if (not (user_education == "None")):
			for place in user_education.objects:
				str_rep += "- Education: " + unicode(place.displayName) + "\n"
		
		else:
			str_rep += "- Education: " + user_education + "\n"
		
		# Single value.
		str_rep += "- Email: " + check_none(self.email) + "\n"
		
		# Single value.
		hometown = check_none(self.hometown)
		
		if (not (hometown == "None")):
			str_rep += "- Hometown: " + unicode(hometown.displayName) + "\n"
		
		else:
			str_rep += "- Hometown: " + hometown + "\n"
		
		# Single value.
		location = check_none(self.location)
		
		if (not (location == "None")):
			str_rep += "- Location: " + unicode(location.displayName) + "\n"
		
		else:
			str_rep += "- Hometown: " + location + "\n"
		
		# Single value.
		str_rep += "- Political Views: " + unicode(check_none(self.politicalViews)) + "\n"
		str_rep += "- Religion: " + unicode(check_none(self.religion)) + "\n"
		
		# Multi value.
		interested_in = check_none(self.interestedIn)
		str_rep += "- Interested In: " + str(interested_in) + "\n"
		
		# Single value.
		str_rep += "- Relationship Status: " + check_none(self.relationshipStatus) + "\n"
		
		# Single value.
		significant_other = check_none(self.significantOther)
		
		if (not (significant_other == "None")):
			str_rep += "- Significant Other: " + unicode(significant_other.displayName) + "\n"
		
		else:
			str_rep += "- Significant Other: " + significant_other + "\n"
		
		# Multi value.
		user_work = check_none(self.work)
		
		if (not (user_work == "None")):
			for place in user_work.objects:
				str_rep += "- Work: " + unicode(place.displayName) + "\n"
		
		else:
			str_rep += "- Work: " + user_work + "\n"
		
		# Finish off and return.
		str_rep += "</User>"
		return str_rep


class FriendsList(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a unicode representation of this object.
		Mainly used for testing purposes.
		
		:returns: A unicode representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Friends>" + "\n"
		
		# Loop through the objects attribute. (Should be a list of User() objects)
		for user in self.objects:
			str_rep += unicode(user) + "\n"
		
		# Finish off and return.
		str_rep += "</Friends>"
		return str_rep
			

class Status(SocialObjects.Note):
	"""
	A Facebook Status object. Contains details such as content, location, number of likes and
	so on.
	"""
	
	def __init__(self):
		super(Status, self).__init__()
		self._provider = "Facebook"	# String
		self._likes = None	# Collection of users
		self._comments = None	# Collection of comments
	
	
	@property
	def likes(self):
		""" The people who liked this status update. """
		return self._likes
	
	
	@property
	def comments(self):
		""" The comments on this status update. """
		return self._comments
	
	
	@likes.setter
	def likes(self, value):
		self._likes = value
	
	
	@comments.setter
	def comments(self, value):
		self._comments = value
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Status>" + "\n"
		
		# Basic info.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Author: " + unicode(check_none(self.author)) + "\n"
		str_rep += "- Content: " + unicode(check_none(self.content)) + "\n"
		str_rep += "- Published: " + str(check_none(self.published)) + "\n"
		str_rep += "- URL: " + check_none(self.url) + "\n"
		
		# Location.
		location = check_none(self.location.displayName)
		str_rep += "- Location: " + unicode(location) + "\n"
		
		# Likes
		str_rep += unicode(self.likes)
		
		# Comments
		str_rep += unicode(self.comments)
		
		# Finish up and return.
		str_rep +=  "</Status>" + "\n"
		return str_rep


class StatusList(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Statuses>" + "\n"
		
		# Loop through the objects attribute. (Should be a list of Status() objects)
		for status in self.objects:
			str_rep += unicode(status)
		
		# Finish up and return.
		str_rep += "</Statuses>"
		return str_rep


class Likes(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Likes: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of User() objects)
		for user in self.objects:
			str_rep += "- " + unicode(user.displayName) + "\n"
		
		# Finish up and return.
		str_rep += "</Likes>" + "\n"
		return str_rep


class Comment(SocialObjects.Note):
	def __init__(self):
		super(Comment, self).__init__()
		self._provider = "Facebook"	# String
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Comment>" + "\n"
		
		# Basic info.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += unicode("- Author: " + check_none(self.author) + "\n")
		str_rep += unicode("- Content: " + check_none(self.content) + "\n")
		str_rep += "- Published: " + str(check_none(self.published)) + "\n"
		str_rep += "- URL: " + check_none(self.url) + "\n"
		
		# Finish up and return.
		str_rep += "</Comment>" + "\n"
		return str_rep


class Comments(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Comments: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of Comment() objects)
		for comment in self.objects:
			str_rep += unicode(comment)
		
		# Finish up and return.
		str_rep += "</Comments>" + "\n"
		return str_rep


class Album(SocialObjects.SocialObject):
	def __init__(self):
		super(Album, self).__init__()
		self._provider = "Facebook"	# String
		self._coverPhoto = None	# Image
		self._privacy = None	# String
		self._count = None	# Integer
		self._albumType = None	# String
		self._photos = None	# Collection of photos
		self._likes = None	# Collection of users
		self._comments = None	# Collection of comments
		
		
	@property
	def coverPhoto(self):
		""" This album's cover photo. """
		return self._coverPhoto
	
	
	@property
	def privacy(self):
		""" The privacy setting for this album. """
		return self._privacy
	
	
	@property
	def count(self):
		""" The number of photos in this album. """
		return self._count
	
	
	@property
	def albumType(self):
		""" The album's type. (Eg: Wall, Mobile) """
		return self._albumType
	
	
	@property
	def photos(self):
		""" The images in the album. """
		return self._photos
	
	
	@property
	def likes(self):
		""" The people who've liked this album. """
		return self._likes
	
	
	@property
	def comments(self):
		""" The comments on this photo album. """
		return self._comments
	
	
	@coverPhoto.setter
	def coverPhoto(self, value):
		self._coverPhoto = value
	
	
	@privacy.setter
	def privacy(self, value):
		self._privacy = value
	
	
	@count.setter
	def count(self, value):
		self._count = value
	
	
	@albumType.setter
	def albumType(self, value):
		self._albumType = value
	
	
	@photos.setter
	def photos(self, value):
		self._photos = value
	
	
	@likes.setter
	def likes(self, value):
		self._likes = value
	
	
	@comments.setter
	def comments(self, value):
		self._comments = value
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Album>" + "\n"
		
		# Basic info.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Author: " + unicode(check_none(self.author)) + "\n"
		str_rep += "- Name: " + unicode(check_none(self.displayName)) + "\n"
		str_rep += "- Summary: " + unicode(check_none(self.summary)) + "\n"
		str_rep += "- Published: " + str(check_none(self.published)) + "\n"
		str_rep += "- Updated: " + str(check_none(self.updated)) + "\n"
		str_rep += "- URL: " + check_none(self.url) + "\n"
		str_rep += "- Location: " + unicode(check_none(self.location.displayName)) + "\n"
		str_rep += "- Cover Photo: " + check_none(self.coverPhoto.fullImage) + "\n"
		str_rep += "- Privacy: " + check_none(self.privacy) + "\n"
		str_rep += "- Number Of Photos: " + str(check_none(self.count)) + "\n"
		str_rep += "- Type: " + check_none(self.albumType) + "\n"
		
		# Likes
		str_rep += unicode(self.likes)
		
		# Comments
		str_rep += unicode(self.comments)
		
		# Photos
		str_rep += unicode(self.photos) + "\n"
		
		# Finish up and return.
		str_rep += "</Album>"
		return str_rep


class Albums(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Albums: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of Album objects)
		for album in self.objects:
			str_rep += unicode(album) + "\n"
		
		# Finish up and return.
		str_rep += "</Albums>"
		return str_rep


class Photo(SocialObjects.Image):
	def __init__(self):
		super(Photo, self).__init__()
		self._provider = "Facebook"	# String
		self._position = None	# Integer
		self._image = None	# Image
		self._thumbnail = None	# Image
		self._width = None	# Integer
		self._height = None	# Integer
		self._tags = None	# Collection of users
		self._likes = None	# Collection of users
		self._comments = None	# Collection of comments
		
		
	@property
	def position(self):
		""" Position of this photo in its album. """
		return self._position
	
	
	@property
	def image(self):
		""" The full size version of this photo. """
		return self._image
	
	
	@property
	def thumbnail(self):
		""" The thumbnail image for this photo. """
		return self._thumbnail
	
	
	@property
	def width(self):
		""" The width of this photo. (Pixels) """
		return self._width
	
	
	@property
	def height(self):
		""" The height of this photo. (Pixels) """
		return self._height
	
	
	@property
	def tags(self):
		""" The people who are tagged in this photo. """
		return self._tags
	
	
	@property
	def likes(self):
		""" The people who've liked this photo. """
		return self._likes
	
	
	@property
	def comments(self):
		""" The comments on this photo. """
		return self._comments
	
	
	@position.setter
	def position(self, value):
		self._position = value
	
	
	@image.setter
	def image(self, value):
		self._image = value
	
	
	@thumbnail.setter
	def thumbnail(self, value):
		self._thumbnail = value
	
	
	@width.setter
	def width(self, value):
		self._width = value
	
	
	@height.setter
	def height(self, value):
		self._height = value
	
	
	@tags.setter
	def tags(self, value):
		self._tags = value
	
	
	@likes.setter
	def likes(self, value):
		self._likes = value
	
	
	@comments.setter
	def comments(self, value):
		self._comments = value
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Photo>" + "\n"
		
		# Basic info.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Author: " + unicode(check_none(self.author)) + "\n"
		str_rep += "- Name: " + unicode(check_none(self.displayName)) + "\n"
		str_rep += "- Published: " + str(check_none(self.published)) + "\n"
		str_rep += "- Updated: " + str(check_none(self.updated)) + "\n"
		str_rep += "- URL: " + check_none(self.url) + "\n"
		str_rep += "- Position: " + str(check_none(self.position)) + "\n"
		str_rep += "- Image: " + check_none(self.image.fullImage) + "\n"
		str_rep += "- Thumbnail: " + check_none(self.thumbnail.fullImage) + "\n"
		str_rep += "- Location: " + unicode(check_none(self.location.displayName)) + "\n"
		
		# Tags
		str_rep += unicode(self.tags)
		
		# Likes
		str_rep += unicode(self.likes)
		
		# Comments
		str_rep += unicode(self.comments)
		
		# Finish up and return.
		str_rep += "</Photo>" + "\n"
		return str_rep


class Photos(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Photos: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of Album objects)
		for photo in self.objects:
			str_rep += unicode(photo)
		
		# Finish up and return.
		str_rep += "</Photos>"
		return str_rep


class Tags(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Tags: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of User objects)
		for user in self.objects:
			str_rep += "- " + unicode(user.displayName) + "\n"
		
		# Finish up and return.
		str_rep += "</Tags>" + "\n"
		return str_rep


class Checkin(SocialObjects.SocialObject):
	def __init__(self):
		super(Checkin, self).__init__()
		self._provider = "Facebook"	# String
		self._checkinType = None	# String
	
	
	@property
	def checkinType(self):
		""" This check-in's type. (Eg: Status, Photo) """
		return self._checkinType
	
	
	@checkinType.setter
	def checkinType(self, value):
		self._checkinType = value
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Check-in>" + "\n"
		
		# Basic info.
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Author: " + unicode(check_none(self.author)) + "\n"
		str_rep += "- Published: " + str(check_none(self.published)) + "\n"
		str_rep += "- Location: " + unicode(check_none(self.location.displayName)) + "\n"
		
		# Tags
		str_rep += unicode(self.tags)
		
		# Finish up and return.
		str_rep += "</Check-in>" + "\n"
		return str_rep


class Checkins(SocialObjects.Collection):
	def __init__(self):
		pass
	
	
	def __unicode__(self):
		"""
		Returns a string representation of this object.
		Mainly used for testing purposes.
		
		:returns: A string representation of this object.
		"""
		
		# Start off string representation.
		str_rep =  "<Check-ins>: " + str(len(self.objects)) + ">" + "\n"
		
		# Loop through the objects attribute. (Should be a list of Checkin objects)
		for checkin in self.objects:
			str_rep += unicode(checkin)
		
		# Finish up and return.
		str_rep += "</Check-ins>"
		return str_rep


def check_none(value):
	"""
	Internal function.
	Used to check to see whether or not a value is None. If so, it replaces it with N/A.
	Mainly used for testing and creating string representations.
	"""
		
	if (value == None):
		return "None"
		
	else:
		return value		
	
	
# Testing.
if __name__ == "__main__":
	# Start tests.
	print "<Tests>"
	
	# Create an instance of the service gateway.
	fb = FacebookServiceGateway()
	
	# Request authentication and print the resulting URI.
	# To test, go to the address printed on-screen, sign in, then copy the "Code" param from the URI and paste it 
	# in the complete_authentication() method below.
	response = fb.request_authentication("http://www.st-andrews.ac.uk/") # This param would be callback under real usage.
	print "Request authentication URI: " + response
	
	# Complete authentication. (Comment out the parsing of input params in complete_authentication() to use)
	fb.complete_authentication("AQARnoOJST6jPEpYu4Lduyx4soRV6e6mVXozt4Pn-zr9nhZVp0ifzYPZxkQtXaRiXZtwBoWJZo9uiR7StQM3V_vFvm7kHaW3Av6Zk7Wrjh7nY_OZmNtAbhyzdw-MmUnFTgMRUgdep3cduUHDDn5sAj46pzz4HNR6UG8gFrpluC1i7dq5evh9j5yn3bmp4pcGilA#_=_")
	
	# Set up a person for testing.
	# Me: 532336768
	# Alex: 
	# Ben: 100001427539048
	person_1 = SocialObjects.Person()
	person_1.id = "532336768"
	
	# Test "Get Person."
	person_obj = fb.User("GET", person_1)
	print "Grabbed user from Facebook:"
	print unicode(person_obj)
	
	# Test "Get Music."
	music_list = fb.Music("GET", person_1)
	print "<Music>"
	for band in music_list:
		print "- " + band
	print "</Music>"
	
	# Test "Get Movies."
	movie_list = fb.Movies("GET", person_1)
	print "<Movies>"
	for movie in movie_list:
		print "- " + movie
	print "</Movies>"
	
	# Test "Get Books."
	book_list = fb.Books("GET", person_1)
	print "<Books>"
	for book in book_list:
		print "- " + book
	print "</Books>"
	
	# Test "Get Statuses."
	statuses = fb.Statuses("GET", person_1)
	print unicode(statuses)
	
	# Test "Get Friends."
	friends = fb.Friends("GET", person_1)
	print unicode(friends)
	
	# Test "Get Albums."
	albums = fb.Albums("GET", person_1)
	print unicode(albums)
	
	# Test "Get Images."
	for album in albums.objects:
		tmp_album = fb.Images("GET", album)
		print unicode(tmp_album)
	
	# Test "Get Check-ins."
	checkins = fb.Checkins("GET", person_1)
	print unicode(checkins)
	
	# End.
	print "</Tests>"


# Ignore me! I'm just for testing.	
class NotImplementedException(Exception):
	pass