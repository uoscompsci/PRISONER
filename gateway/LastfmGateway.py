from ServiceGateway import ServiceGateway
import SocialObjects

import pylast # wrapper for last.fm API

class Track(SocialObjects.SocialObject):
	def __init__(self):
		super(Track,self).__init__()
		self._track = None
		self._artist = None	
		self._provider = "Lastfm"
		self._tag = None
	
	@property
	def track(self):
	""" The title of this track. """
		return self._track

	@track.setter
	def track(self, value):
		self._track = value

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

	@tag.setter
	def tag(self, value):
		self._tag = value

class Playlist(SocialObjects.Collection):
	def __init__(self):
		pass

		

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
		
		API_KEY = "e88606453074ed34ca84904d9ef195d4"	
		API_SECRET = "62ae5491416da384b241bff1a5833873"

		self.network = pylast.LastFMNetwork(api_key = API_KEY,
		api_secret = API_SECRET,
		session_key=access_token)

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
			user = self.network.get_user(payload.id)
			tracks = user.get_loved_tracks(limit=10)
			track_coll = SocialObjects.Collection()
			track_coll.author = user

			track_set = []
			for track in tracks:
				this_track = Track()
				this_track.author = user
				this_track.artist = track.track.artist
				this_track.title = track.track.title
				this_track.tag = track.track.get_top_tags(limit=1)[0].item.name
				track_set.append(this_track)
			track_coll.objects = track_set
			return track_coll	

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
		access_token = request.arguments['token'][0]
	#	print "Last.fm access token: %s" % access_token
		session_key = self.session_manager.get_web_auth_session_key_verbose(access_token)
		self.session_key = session_key
		self.network.session_key = session_key
		return session_key
	

