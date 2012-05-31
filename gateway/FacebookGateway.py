from ServiceGateway import ServiceGateway
import SocialObjects

import datetime	# Used for creating standardised date / time objects from Facebook's attribute values.
import json	# Used for parsing responses from Facebook.
import md5	# Used for generating unique state.
import random	# Used for generating unique state.
import re
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
				
				# Get information about the image's author.
				author_obj = SocialObjects.Person()
				author_details = self.get_graph_data("/" + user_id)
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
	
	
	def User(self, operation, payload):
		"""
		Performs operations on a User object.
		Takes a Person object as a payload and returns a new object populated with that person's profile information.
		Only supports GET operations as you can only get a user's details, not change them.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A person whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A person object.
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
				timestamp = datetime.datetime.strptime(updated_time_str, "%Y-%m-%dT%H:%M:%S+0000")
				user.updatedTime = timestamp
				
				user.bio = self.get_value(user_details, "about")
				
				# Parse the user's birthday.
				birthday_str = self.get_value(user_details, "birthday")
				birthday_timestamp = datetime.datetime.strptime(birthday_str, "%m/%d/%Y")
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
		Takes a Person object and returns a list of bands that that person likes. (In String form)
		Currently only supports GET operations.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A person whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of strings.
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
					bands.append(band["name"])
				
				print "Number of favourite bands for user " + user_id + ": " + str(len(bands))
				return sorted(bands)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Movies(self, operation, payload):
		"""
		Performs operations relating to people's taste in films.
		Takes a Person object and returns a list of movies that that person likes. (In String form)
		Currently only supports GET operations.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A person whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of strings.
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
					movies.append(movie["name"])
				
				print "Number of movies for user " + user_id + ": " + str(len(movies))
				return sorted(movies)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
	def Books(self, operation, payload):
		"""
		Performs operations relating to people's taste in books and literature.
		Takes a Person object and returns a list of books that that person likes. (In String form)
		Currently only supports GET operations.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A person whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A list of strings.
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
					books.append(book["name"])
				
				print "Number of books for user " + user_id + ": " + str(len(books))
				return sorted(books)
				
			
			except:
				return []
		
		else:
			raise NotImplementedException("Operation not supported.")
		
		
	def Statuses(self, operation, payload):
		"""
		Performs operations on a user's status updates.
		Takes a Person object and returns a collection of Status objects. (All of them)
		Currently only supports GET operations.
		
		:param operation: The operation to perform. (GET)
		:type operation: str
		:param payload: A person whose ID is either a Facebook UID or username.
		:type payload: SocialObject
		:returns: A collection of Status objects.
		"""
		
		if (operation == "GET"):
			try:
				# Get user ID and query Facebook for their info.
				user_id = payload.id
				print "GET Statuses: " + user_id
				
				# Get the initial result set.
				result_set = self.get_graph_data("/" + user_id + "/statuses")
				status_obj_list = []
				page_num = 1
				
				# Add all statuses to our list.
				while ((result_set.has_key("paging")) and (result_set["paging"].has_key("next"))):
					# Get status updates.
					this_data = result_set["data"]
					num_updates = len(this_data)
					print "- Page " + str(page_num) + " has " + str(num_updates) + " updates"
					page_num += 1
					
					last_update = this_data[num_updates - 1]
					last_update_stamp = datetime.datetime.strptime(last_update["updated_time"], "%Y-%m-%dT%H:%M:%S+0000").strftime("%s")
					print "- Got last update on page (Posted: " + last_update["updated_time"] + ")"
					print "- Timestamp: " + last_update_stamp
					
					next_address = result_set["paging"]["next"]
					print "- Next address: " + next_address
					match = re.compile("until=..........")
					replace_with = "until=" + last_update_stamp
					new_address = re.sub(match, replace_with, next_address)
					print "\n- New address: " + new_address + "\n"
					
					# Get next result set.
					result_set = self.get_graph_data(new_address)
				
				return None
				
			
			except:
				return None
		
		else:
			raise NotImplementedException("Operation not supported.")
	
	
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
	
	
	def __str__(self):
		"""
		Returns a String representation of this User object.
		Mainly used for testing purposes.
		
		:returns: A String.
		"""
		
		# Start off the string representation...
		str_rep =  "<User>"
		
		# Single value.
		
		str_rep += "- ID: " + check_none(self.id) + "\n"
		str_rep += "- Display Name: " + check_none(self.displayName) + "\n"
		str_rep += "- Profile Picture: " + check_none(self.image.fullImage) + "\n"
		str_rep += "- Username: " + check_none(self.username) + "\n"
		str_rep += "- First Name: " + check_none(self.firstName) + "\n"
		str_rep += "- Middle Name: " + check_none(self.middleName) + "\n"
		str_rep += "- Last Name: " + check_none(self.lastName) + "\n"
		str_rep += "- Gender: " + check_none(self.gender) + "\n"
		str_rep += "- Last Update: " + check_none(self.updatedTime).strftime("%d/%m/%Y @ %H:%M:%S") + "\n"
		str_rep += "- Birthday: " + check_none(self.birthday).strftime("%d/%m/%Y") + "\n"
		
		# Multi value.
		user_langs = check_none(self.languages)
		str_rep += "- Language: " + str(user_langs) + "\n"
		
		# Single value.
		str_rep += "- Timezone: " + check_none(str(self.timezone)) + "\n"
		str_rep += "- Bio: " + check_none(self.bio) + "\n"
		
		# Multi value.
		user_education = check_none(self.education).objects
		
		if (not (user_education == "None")):
			for place in user_education:
				str_rep += "- Education: " + place.displayName + "\n"
		
		else:
			str_rep += "- Education: " + user_education + "\n"
		
		# Single value.
		str_rep += "- Email: " + check_none(self.email) + "\n"
		
		# Single value.
		hometown = check_none(self.hometown)
		
		if (not (hometown == "None")):
			str_rep += "- Hometown: " + hometown.displayName + "\n"
		
		else:
			str_rep += "- Hometown: " + hometown + "\n"
		
		# Single value.
		location = check_none(self.location)
		
		if (not (location == "None")):
			str_rep += "- Location: " + location.displayName + "\n"
		
		else:
			str_rep += "- Hometown: " + location + "\n"
		
		# Single value.
		str_rep += "- Political Views: " + check_none(self.politicalViews) + "\n"
		str_rep += "- Religion: " + check_none(self.religion) + "\n"
		
		# Multi value.
		interested_in = check_none(self.interestedIn)
		str_rep += "- Interested In: " + str(interested_in) + "\n"
		
		# Single value.
		str_rep += "- Relationship Status: " + check_none(self.relationshipStatus) + "\n"
		str_rep += "- Significant Other: " + check_none(self.significantOther).displayName + "\n"
		
		# Multi value.
		user_work = check_none(self.work)
		
		if (not (user_work == "None")):
			for place in user_work.objects:
				str_rep += "- Work: " + place.displayName + "\n"
		
		else:
			str_rep += "- Work: " + user_work + "\n"
		
		# Finish off and return.
		str_rep += "</User>"
		return str_rep
			

class Status(SocialObjects.Note):
	"""
	A Facebook Status object. Contains details such as content, location, number of likes and
	so on.
	"""
	
	def __init__(self):
		super(Status, self).__init__()
		self._provider = "Facebook"	# String
		self._place = None	# Place
		self._likes = None	# Collection of users
		self._comments = None	# Collection of comments.
	
	@property
	def place(self):
		""" The location this status was tagged at. """
		return self._place
	
	
	@property
	def likes(self):
		""" The people who liked this status update. """
		return self._likes
	
	
	@property
	def comments(self):
		""" The comments on this status update. """
		return self._comments
	
	
	@place.setter
	def place(self, value):
		self._place = value
	
	
	@likes.setter
	def likes(self, value):
		self._likes = value
	
	
	@comments.setter
	def comments(self, value):
		self._comments = value


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
	print "<Start tests>"
	
	# Create an instance of the service gateway.
	fb = FacebookServiceGateway()
	
	# Request authentication and print the resulting URI.
	# To test, go to the address printed on-screen, sign in, then copy the "Code" param from the URI and paste it 
	# in the complete_authentication() method below.
	response = fb.request_authentication("http://www.st-andrews.ac.uk/") # This param would be callback under real usage.
	print "Request authentication URI: " + response
	
	# Complete authentication. (Comment out the parsing of input params in complete_authentication() to use)
	fb.complete_authentication("AQClg-2eEzYdYQ_PRlsYOnzmGgSlb7VgAxHSIjGKtOpUmYB-g_zTSjNvhrZD9m7zLqOGyxIVihFQKjwLRcMMZp14NOrl60DQBZvI9nRO0s358YVtnw5tvGoocadR_5NY1tYv9bfuGJUxIT4pt2v-TnAaeJp8X_lN5DG9gYlKTw0Yp3uE3ML2od-_zG8Oh8E88ts#_=_")
	
	# Set up a person for testing.
	person_1 = SocialObjects.Person()
	person_1.id = "532336768"
	
	# Test "Get Image."
	img_obj = fb.Image("GET", person_1)
	print "Grabbed image from Facebook:"
	print "- Full image: " + img_obj.fullImage
	print "- Author ID: " + img_obj.author.id
	print "- Author name: " + img_obj.author.displayName
	
	# Test "Get Person."
	person_obj = fb.User("GET", person_1)
	print "Grabbed user from Facebook:"
	print person_obj
	
	# Test "Get Music."
	#music_obj = fb.Music("GET", person_1)
	#print "Printing list of favourite bands:"
	#for band in music_obj:
		#print "- " + band
	
	# Test "Get Movies."
	#movie_obj = fb.Movies("GET", person_1)
	#print "Printing list of favourite movies:"
	#for movie in movie_obj:
		#print "- " + movie
	
	# Test "Get Books."
	#book_obj = fb.Books("GET", person_1)
	#print "Printing list of favourite books:"
	#for book in book_obj:
		#print "- " + book
	
	# Test "Get Statuses."
	statuses = fb.Statuses("GET", person_1)
	
	# End.
	print "<End tests>"

	
	
