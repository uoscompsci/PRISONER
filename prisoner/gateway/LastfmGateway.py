from prisoner.gateway.ServiceGateway import ServiceGateway
from prisoner import SocialObjects

import datetime

import pylast # wrapper for last.fm API

class Track(SocialObjects.SocialObject):
	def __init__(self):
		super(Track,self).__init__()
		self._title = None
		self._artist = None	
		self._provider = "Lastfm"
		self._tag = None
		self._friendly_names = {
		"track": "title",
		"artist": "artist"}
	
	def get_friendly_name(self, attribute):
		# TODO: move method out of class - dynamically attempt requested
		# subclass (use intermediate method with provider, attribte
		# signature and if fail then try on base
		if attribute in self._friendly_names:
			return self._friendly_names[attribute]

		else:
			return None	
	@property
	def title(self):
		""" The title of this track. """
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def artist(self):
		""" String identifying artist of this track. """
		return self._artist

	@artist.setter
	def artist(self, value):
		self._artist = value

	@property
	def tag(self):
		""" Set of tags associated with this track """
		return self._tag
		#return datetime.datetime.now()

	@tag.setter
	def tag(self, value):
		self._tag = value


	def __str__(self):
		return "%s - %s" % (self.artist, self.title)


	def transform_artist(self, transformation, level):
		""" Applies anonymising transformation to the artist attribute.
		Uses the base_transform_name transformation """
		self.artist = self.base_transform_name(self.artist, transformation,
		level)

class Playlist(SocialObjects.Collection):
	def __init__(self):
		super(Playlist, self).__init__()

		

class LastfmServiceGateway(ServiceGateway):
	""" ServiceGateway for Last.fm. This is a concrete implementation to
	demonstrate how to build experimental applications which consume data from, and
	publish data to, Last.fm

	This ServiceGateway supports a number of core Social Objects, and
	introduces a range of its own to represent site-specific constructs such as
	Tracks and Playlists, etc.

	This gateway uses a modified version of pylast to interact with Last.fm
	API
	"""
	def __init__(self, access_token=None):
		""" Initialises pylast session with API_KEY and API_SECRET."""
		self.service_name = "Last.fm"
		self.service_description = "Music recommendation service"
		
		API_KEY = ""	
		API_SECRET = ""

		self.network = pylast.LastFMNetwork(api_key = API_KEY,
		api_secret = API_SECRET,
		session_key=access_token)
		
		self.session = None

	def __get_author_from_username(self, username):
		""" Returns a simple Person object whose ID is the
		given username

		:param username: username to return a Person object for
		:type username: str
		:returns: Person - id is given username """
		auth = SocialObjects.Person()
		auth.id = username
		return auth

	def Session(self):
		""" The Last.fm session exposes the authenticated
		user as a Person instance
		"""
		return self.session	

	def Playlist(self, operation, payload):
		if(operation == "GET"):
			return self.Track(operation, payload)

	def Track(self, operation, payload):	
		""" Performs operations on Track objects. Only supports the GET
		operation (you can get a user's tracks, you can't create them).

		Returns a set of Tracks depending on the payload.

		:param operation: The operation to perform (GET)
		:type operation: str
		:param payload:
			Provide a Person (whose id is username) to return a set
			of that user's Loved Tracks
		:type payload: SocialObject
		:returns: list[track] - set of tracks matching criteria
		"""
		if(operation == "GET"):
			user = self.network.get_user(payload)
			tracks = user.get_loved_tracks(limit=10)
			track_coll = Playlist()
			track_coll.author = self.__get_author_from_username(payload)

			track_set = []
			for track in tracks:
				this_track = Track()
				#this_track.author = payload
				this_track.author = track_coll.author
				this_track.artist = track.track.artist.name
				this_track.title = track.track.title
				#this_track.tag = track.track.get_top_tags(limit=1)[0].item.name
				this_track.tag = "test_tag"
				track_set.append(this_track)
			track_coll.objects = track_set
			return track_coll
		elif(operation == "POST"):
			target = self.network.get_user(payload.addTo.id)
			artist = payload.artist
			song = payload.song
			track = self.network.get_track(song, artist)
			lib = pylast.Library(target, network = "LastFM")
			lib.add_track(track)


	def Comment(self, operation, payload):
		""" Performs operations on Comment objects. Supports GET and
		POST operations.
		
		:param operation: The operation to perform (GET, POST)
		:type operation: str
		:param payload:
			Provide a Comment object. Will be posted as a shout to
			the profile of the inReplyTo attribute.
		:type payload: SocialObject
		"""
		if(operation == "GET"):
			pass
		elif(operation == "POST"):
			target = self.network.get_user(payload.inReplyTo.id)
			target.shout(payload.content)
		else:
			raise OperationNotImplementedError(operation)

	def Image(self, operation, payload):
		""" Performs operations on Image objects. Only supports GET
		operations.

		:param operation: The operation to perform (GET)
		:type operation: str
		:param payload:
			Provide a Person object, to return that user's profile
			image
		:type payload: SocialObject

		:returns Image -- image of requested object
		"""
		if (operation == "GET"):
			try:
				user = self.network.get_user(payload.id)
				user_image = user.get_image()
				img_object = SocialObjects.Image()
				img_object.fullImage = user_image

				author_obj = SocialObjects.Person()
				author_obj.id = user.name
				author_obj.displayName = user.name

				img_object.author = author_obj
				return img_object
			except:
				return SocialObjects.Image()
		else:
			raise NotImplementedException("Operation not supported")

	def request_authentication(self, callback):
		""" Instigates first of Last.fm's two-stage authentication.
		Returns a URL for the participant to confirm access to their profile by this
		application.

		:param callback:
			PRISONER's authentication flow URL. The
			participant must go here after authenticating with Last.fm to continue the flow
		:type callback: str
		"""
		self.session_manager = pylast.SessionKeyGenerator(self.network)
		return self.session_manager.get_web_flow(callback)

	def complete_authentication(self, request):
		"""
		Completes authentication. Request passed via authentication flow
		must contain a token argument as returned by Last.fm. We pass this to Last.fm to
		return a session key (lasts indefinitely) for making authenticated calls on this
		user.	

		:param request: Request from first stage of authentication
		:type request: HTTPRequest
		:returns: Session key to persist for this user
		"""
		access_token = request.args['token']
	#	print "Last.fm access token: %s" % access_token
		session_key = self.session_manager.get_web_auth_session_key_verbose(access_token)
		self.session_key = session_key
		self.network.session_key = session_key

		# place username in session
		user = self.network.get_authenticated_user()
		user_person = SocialObjects.Person()
		user_person.id = user.get_name()
		self.session = user_person
		return session_key
	
	def restore_authentication(self, access_token):
		""" Restores previously authenticated session. Last.fm session
		keys last indefinitely so this just provides pylast with the old session key and
		hope it works

		:param access_token:
			Last.fm session key received from previous
			auth attempt
		:type access_token: str
		:returns: boolean - was auth successful?
		"""
		self.session_key = access_token
		self.network.session_key = access_token

		# place username in session
		user = self.network.get_authenticated_user()
		user_person = SocialObjects.Person()
		user_person.id = user.get_name()
		self.session = user_person
		
		return True
	
		

