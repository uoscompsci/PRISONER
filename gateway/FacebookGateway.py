from ServiceGateway import ServiceGateway
import SocialObjects

import datetime	# Used for creating standardised date / time objects from Facebook's attribute values.
import json	# Used for parsing responses from Facebook.
import md5	# Used for generating unique state.
import random	# Used for generating unique state.
import sys	# Used for displaying error message names and descriptions.
import traceback
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
		self.facebook_uri = "https://www.facebook.com/";
		
		# Generate a unique state. (Required by Facebook for security)
		r = random.random()
		self.state = md5.new(str(r)).hexdigest()
		
		# Permissions. (We'll ask for them ALL for now)
		user_permissions = "user_about_me,user_activities,user_birthday,user_checkins,user_education_history,user_events," +\
		"user_groups,user_hometown,user_interests,user_likes,user_location,user_notes,user_photos,user_questions,user_relationships," +\
		"user_relationship_details,user_religion_politics,user_status,user_subscriptions,user_videos,user_website,user_work_history,email"
		friend_permissions = "friends_about_me,friends_activities,friends_birthday,friends_checkins,friends_education_history," +\
		"friends_events,friends_groups,friends_hometown,friends_interests,friends_likes,friends_location,friends_notes,friends_photos," +\
		"friends_questions,friends_relationships,friends_relationship_details,friends_religion_politics,friends_status,friends_subscriptions," +\
		"friends_videos,friends_website,friends_work_history"
		extended_permissions = "read_friendlists,read_insights,read_mailbox,read_requests,read_stream,xmpp_login,ads_management,create_event," +\
		"manage_friendlists,manage_notifications,user_online_presence,friends_online_presence,publish_checkins,publish_stream,rsvp_event,user_tagged_places"

		# this is a terrible pattern
		# just do this until individual apps can provide their permissions in bootstrap
		
		#mobiad_permissions = "user_about_me,user_checkins,friends_about_me,read_stream,publish_checkins,publish_stream"
		
		# Set the scope for our app. (What permissions do we need?)
		
		self.scope = user_permissions + "," + friend_permissions + "," + extended_permissions # get all perms

		#self.scope = mobiad_permissions #get mobiad perms
		
		# Placeholders.
		self.access_token = None
		self.session = None

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
		
		# Compose request URI.
		uri = self.auth_request_uri + urllib.urlencode(params)
		print "Request URI: " + uri
		
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
		facebook_code = None
		#facebook_code = request # Uncomment me if testing with a known code.
		
		if (request.args.has_key("code")):
			facebook_code = request.args['code']
		
		else:
			return False
		
		# Parameters for the token request URI.
		params = {}
		params["code"] = facebook_code
		params["client_secret"] = self.app_secret
		params["redirect_uri"] = self.redirect_uri
		params["client_id"] = self.app_id
		
		# Load the token request URI and get its response parameters.
		token_request_uri = self.auth_token_uri + urllib.urlencode(params)
		response = urlparse.parse_qs(urllib.urlopen(token_request_uri).read())
		print "Response: " + str(response)
		
		# Parse response to get access token and expiry date.
		access_token = None
		expires = None
		
		self.access_token = response["access_token"][0]
		expires = response["expires"][0]
		
		# Create a User() object for the authenticated user.
		auth_user = User()
		
		# Query Facebook to get the authenticated user's ID and username.
		result_set = self.get_graph_data("/me")
		auth_user.id = self.get_value(result_set, "id")
		auth_user.username = self.get_value(result_set, "username")
		
		# Set up session.
		self.session = auth_user
		
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
	
	
	def Session(self):
		"""
		The Facebook session exposes the authenticated user as an instance of User().
		Can also be accessed in the same way as Person() as this class simply extends it.
		"""
		
		return self.session
	
	
	def User(self, operation, payload):
		"""
		Performs operations relating to people's profile information.
		Currently only supports GET operations. This allows us to, given a suitable payload such as a Person() or
		User() object, retrieve the information they have added to Facebook. (Eg: Full name, education, religion...)
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A Person() or User() object whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A User() object with all available attributes populated.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload
				user_details = self.get_graph_data("/" + user_id)
				
				# Create user object.
				user = User()
				
				# Create author object for future use.
				author = SocialObjects.Person()
				author.id = user_id
				user.author = author
				
				# Basic information.
				user.id = self.get_value(user_details, "id")
				user.firstName = self.get_value(user_details, "first_name")
				user.middleName = self.get_value(user_details, "middle_name")
				user.lastName = self.get_value(user_details, "last_name")
				user.username = self.get_value(user_details, "username")
				user.displayName = self.get_value(user_details, "name")
				user.gender = self.get_value(user_details, "gender")
				user.email = self.get_value(user_details, "email")
				user.url = "https://www.facebook.com/" + user_id
				
				# Get a list of the user's languages.
				languages = self.get_value(user_details, "languages")
				
				# Language info was supplied.
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
				
				# Timezone.
				user.timezone = self.get_value(user_details, "timezone")
				
				# Parse the user's last update time.
				updated_time_str = self.get_value(user_details, "updated_time")
				timestamp = self.str_to_time(updated_time_str)
				user.updatedTime = timestamp
				
				# About / short biography.
				user.bio = self.get_value(user_details, "bio")
				
				# Parse the user's birthday.
				birthday_str = self.get_value(user_details, "birthday")
				birthday_timestamp = self.str_to_time(birthday_str)
				user.birthday = birthday_timestamp
				
				# Get a list detailing the user's education history.
				education_list = self.get_value(user_details, "education")
				edu_coll = SocialObjects.Collection()
				edu_coll.author = author
				
				# Education information exists.
				if ((education_list) and (len(education_list) > 0)):
					# Create list to hold places.
					edu_list = []
					
					# Loop through places and add to list.
					for place in education_list:
						this_place = SocialObjects.Place()
						this_place.id = place["school"]["id"]
						this_place.displayName = place["school"]["name"]
						edu_list.append(this_place)
					
					edu_coll.objects = edu_list
				
				# Add education info to User object.
				user.education = edu_coll
				
				# Get a list detailing the user's work history.
				work_coll = SocialObjects.Collection()
				work_coll.author = author
				work_history = self.get_value(user_details, "work")
				
				# Info exists.
				if ((work_history) and (len(work_history) > 0)):
					# Create Collection object to hold work history.
					work_list = []
					
					# Loop through places and add to list.
					for place in work_history:
						this_place = SocialObjects.Place()
						this_place.id = place["employer"]["id"]
						this_place.displayName = place["employer"]["name"]
						work_list.append(this_place)
					
					work_coll.objects = work_list
					
				
				# Add work info to User object.
				user.work = work_coll
				
				# Make a Place object for the user's hometown.
				hometown_place = SocialObjects.Place()
				hometown_info = self.get_value(user_details, "hometown")
				
				# Hometown supplied.
				if (hometown_info):
					hometown_place.id = hometown_info["id"]
					hometown_place.displayName = hometown_info["name"]
					user.hometown = hometown_place
				
				# Not supplied, so use an empty Place object.
				else:
					user.hometown = SocialObjects.Place()
				
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
					user.location = SocialObjects.Place()
				
				# Additional info.
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
					user.significantOther = User()
				
				# Get the user's profile picture.
				img = SocialObjects.Image()
				img.fullImage = self.graph_uri + "/me/picture?type=large" + "&access_token=" + self.access_token
				user.image = img
				
				print "User() function returned successfully."
				return user
				
			except:
				print "User() function exception:"
				print sys.exc_info()[0]
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
				user_id = payload
				
				# Create author object.
				author = SocialObjects.Person()
				author.id = user_id
				
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
					# Create an object for this band.
					this_band = Music()
					this_band.displayName = self.get_value(band, "name")
					this_band.id = self.get_value(band, "id")
					this_band.url = "https://www.facebook.com/" + this_band.id
					
					this_band.author = author
					bands.append(this_band)
				
				# Create a collection object to hold the list.
				bands_coll = SocialObjects.Collection()
				bands_coll.author = author
				bands_coll.provider = "Facebook"
				bands_coll.objects = bands
				
				# Return.
				print "Music() function returned successfully."
				return bands_coll

			except:
				print "Music() function exception:"
				print sys.exc_info()[0]
				return SocialObjects.Collection()
		
		else:
			raise NotImplementedException("Operation not supported.")


	def Like(self, operation, payload):
		"""
		Returns a user's liked pages.
		Only supports GET operations.

		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of pages this person likes.
		"""
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload
				
				# Create author object.
				author = SocialObjects.Person()
				author.id = user_id
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/likes")
				like_obj_list = []
				
				# While there are still more likes available, add them to the list.
				while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
					# Get movies.
					like_obj_list.extend(result_set["data"])
					
					# Get next result set.
					result_set = self.get_graph_data(result_set["paging"]["next"])
				
				# Loop through the movie object list and add their names to a separate list.
				likes = []
				
				for like in like_obj_list:
					# Create an object for this movie.
					this_like = Page()
					this_like.displayName = self.get_value(like, "name")
					this_like.id = self.get_value(like, "id")
					this_like.url = "https://www.facebook.com/" + this_like.id
					this_like.author = author
					this_like.category = self.get_value(like,"category")
					likes.append(this_like)
				
				# Create a collection object to hold the list.
				likes_coll = SocialObjects.Collection()
				likes_coll.author = author
				likes_coll.provider = "Facebook"
				likes_coll.objects = likes
				
				# Return.
				print "Like() function returned successfully."
				return likes_coll

			except:
				print "Like() function exception:"
				print sys.exc_info()[0]
				raise
				return SocialObjects.Collection()
		
		else:
			raise NotImplementedException("Operation not supported.")

	
	
	
	
	def Movie(self, operation, payload):
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
				user_id = payload
				
				# Create author object.
				author = SocialObjects.Person()
				author.id = user_id
				
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
					# Create an object for this movie.
					this_movie = Movie()
					this_movie.displayName = self.get_value(movie, "name")
					this_movie.id = self.get_value(movie, "id")
					this_movie.url = "https://www.facebook.com/" + this_movie.id
					this_movie.author = author
					movies.append(this_movie)
				
				# Create a collection object to hold the list.
				movies_coll = SocialObjects.Collection()
				movies_coll.author = author
				movies_coll.provider = "Facebook"
				movies_coll.objects = movies
				
				# Return.
				print "Movie() function returned successfully."
				return movies_coll

			except:
				print "Movie() function exception:"
				print sys.exc_info()[0]
				return SocialObjects.Collection()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Book(self, operation, payload):
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
				user_id = payload
				
				# Create author object.
				author = SocialObjects.Person()
				author.id = user_id
				
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
					# Create an object for this book.
					this_book = Book()
					this_book.displayName = self.get_value(book, "name")
					this_book.id = self.get_value(book, "id")
					this_book.url = "https://www.facebook.com/" + this_book.id
					this_book.author = author
					books.append(this_book)
				
				# Create a collection object to hold the list.
				books_coll = SocialObjects.Collection()
				books_coll.author = author
				books_coll.provider = "Facebook"
				books_coll.objects = books
				
				# Return.
				return books_coll

			except:
				print "Book() function exception:"
				print sys.exc_info()[0]
				return SocialObjects.Collection()
		
		else:
			raise NotImplementedException("Operation not supported.")
		
		
	def Status(self, operation, payload):
		"""
		Performs operations on a user's status updates.
		Currently only supports GET operations. This lets us retrieve a user's entire backlog of status updates.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A User() or Person() whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A collection representing this person's backlog of status updates.

		For POST payloads:
			payload must be a dictionary with all mandatory (and any optional) fields of a Status object}
		"""
		if(operation == "POST"):
			# convert SO dict to fb call	
			call_dict = {
				"message":payload.content,
				"link":payload.link
				}

			if(payload.privacy):
				privacy = "{'value':'CUSTOM', 'allow': '%s'}" % payload.privacy
				call_dict['privacy'] = privacy
			response = self.post_graph_data("/me/feed", call_dict)



		elif (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload
				status_coll = StatusList()
				status_list = []
				
				# Create author object for this collection.
				author = SocialObjects.Person()
				author.id = user_id
				status_coll.author = author
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/feed")
				
				# Page limit for testing.
				page_limit = 50
				page = 0
				
				# So long as there's data, parse it.
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0) and (page < page_limit)):
					# Get status updates in this batch.
					this_data = result_set["data"]
					
					# For each update...
					for status in this_data:
						status_type = self.get_value(status, "type")
						status_author = self.get_value(status["from"], "id")
						
						# Ensure this is a real status update. (Not a story, comment, etc.)
						if (status.has_key("message")):
							# Ensure the current user posted this update and it is a valid status object.
							if (((status_type == "status") or (status_type == "link") or (status_type == "photo")) and (status_author == user_id)):
								# Set basic info.
								this_status = Status()

								author = SocialObjects.Person()
								author.id = user_id
								this_status.author = author
								
								this_status.content = self.get_value(status, "message")
								this_status.id = self.get_value(status, "id")
								this_status.published = self.str_to_time(self.get_value(status, "created_time"))
								id_components = this_status.id.split("_")
								this_status.url = "https://www.facebook.com/" + user_id + "/posts/" + id_components[1]
								
								# Privacy info. (If available)
								if (status.has_key("privacy")):
									this_status.privacy = self.get_value(status["privacy"], "description")
					
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
													
					# Compose next address.
					page += 1
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Add the status list to our collection.
				status_coll.objects = status_list
				
				# Return statuses.
				print "Status() function returned successfully."
				return status_coll
				
			
			except:
				print "Status() function exception:"
				print sys.exc_info()[0]
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
				print "friends payload: %s " % payload
				user_id = payload
				fields = "name,id,hometown,location,education,work"
				result_set = self.get_graph_data("/" + user_id + "/friends?fields=%s" % fields)
				friend_coll = Friends()
				friend_obj_list = []
				
				# Create author object for this collection.
				author = SocialObjects.Person()
				author.id = user_id
				friend_coll.author = author
				
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
						this_friend.url = "https://www.facebook.com/" + this_friend.id

						user_details = friend

						# Get a list detailing the user's education history.
						education_list = self.get_value(user_details, "education")
						edu_coll = SocialObjects.Collection()
						edu_coll.author = author
						
						# Education information exists.
						if ((education_list) and (len(education_list) > 0)):
							# Create list to hold places.
							edu_list = []
							
							# Loop through places and add to list.
							for place in education_list:
								this_place = SocialObjects.Place()
								this_place.id = place["school"]["id"]
								this_place.displayName = place["school"]["name"]
								edu_list.append(this_place)
							
							edu_coll.objects = edu_list
						
						# Add education info to User object.
						this_friend.education = edu_coll
						
						# Get a list detailing the user's work history.
						work_coll = SocialObjects.Collection()
						work_coll.author = author
						work_history = self.get_value(user_details, "work")
						
						# Info exists.
						if ((work_history) and (len(work_history) > 0)):
							# Create Collection object to hold work history.
							work_list = []
							
							# Loop through places and add to list.
							for place in work_history:
								this_place = SocialObjects.Place()
								this_place.id = place["employer"]["id"]
								this_place.displayName = place["employer"]["name"]
								work_list.append(this_place)
							
							work_coll.objects = work_list
							
						
						# Add work info to User object.
						this_friend.work = work_coll
						
						# Make a Place object for the user's hometown.
						hometown_place = SocialObjects.Place()
						hometown_info = self.get_value(user_details, "hometown")
						
						# Hometown supplied.
						if (hometown_info):
							hometown_place.id = hometown_info["id"]
							hometown_place.displayName = hometown_info["name"]
							this_friend.hometown = hometown_place
						
						# Not supplied, so use an empty Place object.
						else:
							this_friend.hometown = SocialObjects.Place()
						
						# Make a Place object for the user's current location.
						location_place = SocialObjects.Place()
						location_info = self.get_value(user_details, "location")
						
						# Location supplied.
						if (location_info):
							location_place.id = location_info["id"]
							location_place.displayName = location_info["name"]
							this_friend.location = location_place
						
						# Location not supplied.
						else:
							this_friend.location = SocialObjects.Place()
						
						# Create author object for this friend. (User "has" their friends)
						author = SocialObjects.Person()
						author.id = user_id
						this_friend.author = author
						
						
						# Compose profile pic address.
						profile_pic = SocialObjects.Image()
						profile_pic.fullImage = self.graph_uri + "/" + this_friend.id + "/picture?type=large" + "&access_token=" + self.access_token
						profile_pic.author = this_friend.id
						this_friend.image = profile_pic
						
						
						# Add friend to list.
						friend_obj_list.append(this_friend)
					
					# Get next set of results.
					next_address = result_set["paging"]["next"]
					result_set = self.get_graph_data(next_address)
				
				# Add friend list to collection and return.
				friend_coll.objects = friend_obj_list
				print "Friends() function returned successfully."
				return friend_coll
				
			except:
				print "Friends() function exception:"
				print traceback.format_exc()
				return FriendsList()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Album(self, operation, payload):
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
				obj_id = payload
				result_set = self.get_graph_data("/" + obj_id + "/albums")
				album_coll = Albums()
				album_obj_list = []
				
				# Create author object for this collection.
				author = SocialObjects.Person()
				author.id = obj_id
				album_coll.author = author
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of albums.
					this_data = result_set["data"]
					
					for album in this_data:
						# Set basic album info.
						this_album = Album()
						this_album.id = self.get_value(album, "id")
						this_album.displayName = self.get_value(album, "name")
						
						# Author info.
						author = SocialObjects.Person()
						author.id = self.get_value(album["from"], "id")
						this_album.author = author
						
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
				print "Album() function returned successfully."
				return album_coll
				
			except:
				print "Album() function exception:"
				print sys.exc_info()[0]
				return Albums()
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Photo(self, operation, payload):
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
				obj_id = payload
				result_set = self.get_graph_data("/" + obj_id + "/photos/uploaded")
				photo_obj_list = []
				
				# Author info for individual photos and the collection.
				author = SocialObjects.Person()
				author.id = obj_id
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of photos.
					this_data = result_set["data"]
					
					# For each photo in this batch...
					for photo in this_data:
						# Create photo object and set basic info.
						this_photo = Photo()
						this_photo.id = self.get_value(photo, "id")
						this_photo.displayName = self.get_value(photo, "name")
						this_photo.published = self.str_to_time(self.get_value(photo, "created_time"))
						this_photo.updated = self.str_to_time(self.get_value(photo, "updated_time"))
						this_photo.url = self.get_value(photo, "link")
						this_photo.position = self.get_value(photo, "position")
						this_photo.author = author
						
						# Get image info.
						img_normal = SocialObjects.Image()
						img_normal.id = this_photo.id
						img_normal.author = author
						img_normal.fullImage = self.get_value(photo["images"][0], "source")
						this_photo.image = img_normal
						
						# Image dimensions.
						this_photo.width = self.get_value(photo["images"][0], "width")
						this_photo.height = self.get_value(photo["images"][0], "height")
						
						# Thumbnail info.
						img_small = SocialObjects.Image()
						img_small.id = this_photo.id
						img_small.author = author
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
				photo_album.author = author
				
				print "Photo() function returned successfully."
				return photo_album
			
			except:
				print "Photo() function exception:"
				#raise
				print sys.exc_info()[0]
				return Photos()
		
		else:
			raise NotImplementedException("Operation not supported")
	
	
	def Checkin(self, operation, payload):
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
				user_id = payload
				result_set = self.get_graph_data("/" + user_id + "/locations")
				checkin_obj_list = []
				
				# Author info.
				author = SocialObjects.Person()
				author.id = user_id
				
				
				# While there is still data available...
				while ((result_set.has_key("data")) and (len(result_set["data"]) > 0)):
					# Grab the current batch of check-ins.
					this_data = result_set["data"]
					
					# Loop through each check-in on this page.
					for checkin in this_data:
						# Get and set basic info.
						this_checkin = Checkin()

						# author posted this
						author = SocialObjects.Person()
						#author.id = checkin["from"]["id"]
						#author.displayName = checkin["from"]["name"]


						this_checkin.id = self.get_value(checkin, "id")
						this_checkin.author = author
						#this_checkin.checkinType = self.get_value(checkin, "type")
						this_checkin.checkinType = "status"
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
				checkins_coll.author = author
				
				print "Checkin() function returned successfully."
				return checkins_coll
			
			except:
				print "Checkin() function exception:"
				#print sys.exc_info()[0]
				print traceback.format_exc()
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
		
		# This object has a "Likes" attribute.
		if (facebook_obj.has_key("likes")):
			# This object has likes.
			if (facebook_obj["likes"].has_key("data")):
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
		
		
		# This object has a "Comments" attribute.
		if (facebook_obj.has_key("comments")):
			# This object has comments.
			if (facebook_obj["comments"].has_key("data")):
				comments = []
				comments_on = facebook_obj["comments"]["data"]
			
				# Loop through comments and add them to our list.
				for comment in comments_on:
					this_comment = Comment()
					this_comment.id = self.get_value(comment, "id")
					
					author = SocialObjects.Person()
					author.id = self.get_value(comment["from"], "id")
					this_comment.author = author
					
					this_comment.content = self.get_value(comment, "message")
					this_comment.published = self.str_to_time(self.get_value(comment, "created_time"))
					this_comment.url = "https://www.facebook.com/me/posts/" + this_comment.id
					
					comments.append(this_comment)
				
				return comments
			
			# No comments, return empty list.
			else:
				return []
		
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
			
			# pull information from the page for this location
			result_set = self.get_graph_data("/" + place.id)
			category = self.get_value(result_set,"category")
			try:
				image = result_set["cover"]["source"]
			except:
				image = None
			place.category = category
			place.image = image


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
				street = self.get_value(facebook_obj["place"]["location"], "street")
				city = self.get_value(facebook_obj["place"]["location"], "city")
				country = self.get_value(facebook_obj["place"]["location"], "country")
				#place.address = street + ", " + city + ", " + country
			else:
				place.address = None	
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
					
					author = SocialObjects.Person()
					author.id = self.get_value(comment["from"], "id")
					this_comment.author = author
					
					this_comment.content = comment["message"]
					this_comment.published = self.str_to_time(comment["created_time"])
					this_comment.url = "https://www.facebook.com/me/posts/" + this_comment.id
					comments.append(this_comment)
				
				# Get the next set of results.
				result_set = self.get_graph_data(result_set["paging"]["next"])
		
		return comments
	
	def post_graph_data(self, query, params):
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
			query = self.graph_uri + query + "?access_token=" + self.access_token
		
		# Retrieve and parse result.
		data_req = urllib2.Request(query,
		data = urllib.urlencode(params))

		data_resp = urllib2.urlopen(data_req)
		data = data_resp.read()
		json_obj = self.parse_json(data)

		return json_obj

	
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
			if "?" not in query:
				token = "?"
			else:
				token = "&"

			query = self.graph_uri + query + token + "access_token=" + self.access_token
		
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
		
		# Check none.
		if (time == None):
			return None
		
		# ISO 8601
		elif (len(time) > 10):
			return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+0000")
		
		# MM/DD/YYYY
		else:
			return datetime.datetime.strptime(time, "%m/%d/%Y")
		

class User(SocialObjects.Person):
	"""
	Representation of a user object on Facebook.
	Users are essentially the backbone of the Facebook service and such objects can contain a great deal of information.
	User objects will not always have values for all their attributes, as Facebook does not require users to provide 
	allthis information.
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


class Friends(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of users / friends.
	"""
	
	def __init__(self):
		super(Friends, self).__init__()



class Status(SocialObjects.Note):
	"""
	Representation of a status object on Facebook.
	Status updates are short posts by Facebook users. They can either be entirely textual or contain a link or a photo.
	As well as the basic attributes, status updates also contain a privacy setting as well as a collection of likes and 
	comments.
	"""
	
	def __init__(self):
		super(Status, self).__init__()
		self._provider = "Facebook"	# String
		self._privacy = None	# String
		self._likes = None	# Collection of users
		self._comments = None	# Collection of comments
		self._link = None

	@property
	def link(self):
		""" A link to an external resource embedded in this status update """
		return self._link

	@link.setter
	def link(self, value):
		self._link = value
	
	@property
	def privacy(self):
		""" The privacy setting for this status update. (Eg: Friends) """
		return self._privacy
	
	
	@property
	def likes(self):
		""" The people who liked this status update. """
		return self._likes
	
	
	@property
	def comments(self):
		""" The comments on this status update. """
		return self._comments
	
	
	@privacy.setter
	def privacy(self, value):
		self._privacy = value
	
	
	@likes.setter
	def likes(self, value):
		self._likes = value
	
	
	@comments.setter
	def comments(self, value):
		self._comments = value


class StatusList(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of statuses.
	"""
	
	def __init__(self):
		super(StatusList, self).__init__()


class Likes(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of likes.
	"""
	
	def __init__(self):
		super(Likes, self).__init__()


class Comment(SocialObjects.Note):
	"""
	Representation of a comment object on Facebook.
	Comments are typically short replies / notes on objects such as statuses, photos, check-ins or just about any 
	other Facebook object. Comments consist of their content, an author a published date and a permalink.
	"""
	
	def __init__(self):
		super(Comment, self).__init__()
		self._provider = "Facebook"	# String


class Comments(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of comments.
	"""
	
	def __init__(self):
		super(Comments, self).__init__()


class Album(SocialObjects.SocialObject):
	"""
	Representation of an album object on Facebook.
	Albums are created by users or apps and have a number of key attributes such as privacy and count.
	Albums also have a cover photo and a type. Once you have an album's ID, you can then use Photo() to retreive
	the photos it contains.
	"""
	
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


class Albums(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of albums.
	"""
	
	def __init__(self):
		super(Albums, self).__init__()


class Photo(SocialObjects.Image):
	"""
	Representation of a photo object on Facebook.
	Photos are images uploaded by users or applications. As well as the standard attributes inherited from SocialObject,
	a photo also has additional specialised attributes such as position, width and height.
	A photo also contains Image() objects to represent both the full-size image as well as thumbnails.
	"""
	
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


class Photos(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of photos.
	"""
	
	def __init__(self):
		super(Photos, self).__init__()


class Tags(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of tags.
	Tags are simply User() objects that have been tagged in a photo or status.
	"""
	
	def __init__(self):
		super(Tags, self).__init__()


class Checkin(SocialObjects.SocialObject):
	"""
	Representation of a check-in.
	A Facebook user can be determined to have been somewhere if they explicitly said they were there in a status, 
	or have been tagged in a photo that is also tagged with that location.
	As well as containing basic information such as where the check-in is for and who the user was with, a check-in object
	also contains a "Type" attribute that specifies how the check-in was determined. (Eg: Status, Photo...)
	"""
	
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


class Checkins(SocialObjects.Collection):
	"""
	Lightweight collection class for representing collections of check-ins.
	"""
	
	def __init__(self):
		super(Checkins, self).__init__()


class Page(SocialObjects.SocialObject):
	"""
	Representation of a generic Facebook page / object.
	Pages are used to represent entities like bands, books, films and so on.
	"""
	
	def __init__(self):
		super(Page, self).__init__()
		self._provider = "Facebook"
		self._category = None

	@property
	def category(self):
	    return self._category
	@category.setter
	def category(self, value):
	    self._category = value


class Like(Page):
	"""
	A Like is just a representation of a Page
	"""
	
	def __init__(self):
		super(Page, self).__init__()	

class Music(Page):
	"""
	Stub for representing music.
	"""
	
	def __init__(self):
		super(Music, self).__init__()


class Movie(Page):
	"""
	Stub for representing music.
	"""
	
	def __init__(self):
		super(Movie, self).__init__()


class Book(Page):
	"""
	Stub for representing music.
	"""
	
	def __init__(self):
		super(Book, self).__init__()


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

