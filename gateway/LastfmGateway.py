"""
Last.fm Service Gateway for PRISONER

This is a concrete implementation of the Service Gateway interface, for
reference
"""
from ServiceGateway import ServiceGateway
import SocialObjects

import pylast # wrapper for last.fm API

class LastfmTrack(SocialObjects.SocialObject):
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
			tracks = user.get_loved_tracks()
			track_set = []
			for track in tracks:
				this_track = LastfmTrack()
				this_track.author = track.artist
				this_track.displayName = track.title
				track_set.append(this_Track)
			return track_set	

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
	def request_authentication(self, authent_id=False):
		self.session_manager = pylast.SessionKeyGenerator(self.network)
		return self.session_manager.get_web_auth_url()

	"""
	Call after user completes authentication - do request to get session
	token
	"""
	def complete_authentication(self, access_token=None):
		print access_token
		session_key = self.session_manager.get_web_auth_session_key(access_token)
		self.session_key = session_key
		self.network.session_key = session_key
		return session_key
	

