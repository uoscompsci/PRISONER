"""
Last.fm Service Gateway for PRISONER

This is a concrete implementation of the Service Gateway interface, for
reference
"""
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
		return self._track

	@track.setter
	def track(self, value):
		self._track = value

	@property
	def artist(self):
		return self._artist

	@artist.setter
	def artist(self, value):
		self._artist = value

	@property
	def tag(self):
		return self._tag

	@tag.setter
	def tag(self, value):
		self._tag = value

class Playlist(SocialObjects.Collection):
	def __init__(self):
		pass

		

class LastfmServiceGateway(ServiceGateway):

	def __init__(self, access_token=None):
		self.service_name = "Last.fm"
		self.service_description = "Music recommendation service"
		
		API_KEY = "e88606453074ed34ca84904d9ef195d4"	
		API_SECRET = "62ae5491416da384b241bff1a5833873"

		self.network = pylast.LastFMNetwork(api_key = API_KEY,
		api_secret = API_SECRET,
		session_key=access_token)

	""" Last.fm Track interface
	GET:
	Returns a set of Track objects, depending on the payload:
	instance of Person - get Loved Tracks
	"""
	def Track(self, operation, payload):
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

	""" Last.fm Shout interface
	Shouts are an alternative name for Comments
	Shouts are inReplyTo an instance of Person
	
	GET:
	Providing a Person will return the set of shouts for that user
	
	POST:
	Providing a Shout will post the shout to the inReplyTo target

	POST operation requires an access key or it will die of death.
	The content key is only required on a PUT operation
	"""	
	def Comment(self, operation, payload):
		if(operation == "GET"):
			pass
		elif(operation == "POST"):
			target = self.network.get_user(payload.inReplyTo.id)
			target.shout(payload.content)
		else:
			raise OperationNotImplementedError(operation)

	""" Last.fm Image interface
	Read-only interface to images of albums, artists, events, and people
	
	Common interface:
	Providing an Author will return the user's profile photo if possible

	Extended interface:
	Possible payload keys:
		artist - Artist name
		album - Album name
		event - ID of event
		user - username
	Will return an appropriate image for the keys given (album needs album
	and artist).
	"""
	def Image(self, operation, payload):
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

	"""
	Return a URL used for end-users to confirm authentication for this
	provider 
	"""
	def request_authentication(self, callback):
		self.session_manager = pylast.SessionKeyGenerator(self.network)
		return self.session_manager.get_web_flow(callback)

	"""
	Call after user completes authentication - do request to get session
	token
	"""
	def complete_authentication(self, request):
		access_token = request.arguments['token'][0]
		print "Last.fm access token: %s" % access_token
		session_key = self.session_manager.get_web_auth_session_key_verbose(access_token)
		self.session_key = session_key
		self.network.session_key = session_key
		return session_key
	

