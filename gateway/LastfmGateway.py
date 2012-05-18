"""
Last.fm Service Gateway for PRISONER

This is a concrete implementation of the Service Gateway interface, for
reference
"""
from ServiceGateway import ServiceGateway
import SocialObjects

import pylast # wrapper for last.fm API

class LastfmServiceGateway(ServiceGateway):

	def __init__(self):
		self.service_name = "Last.fm"
		self.service_description = "Music recommendation service"
		
		API_KEY = "e88606453074ed34ca84904d9ef195d4"	
	
		self.network = pylast.LastFMNetwork(api_key = API_KEY)

	""" Last.fm Shout interface
	Shout is  a subclass of base Social Object Comment
	Common interface:
	Providing a Person keyed on user will return the set of shouts for that
	user

	Extended interfaces:
	Possible payload keys:
		user - Who the shout is intended for
		content - The text of the shout
	PUT operation requires an access key or it will die of death.
	The content key is only required on a PUT operation
	"""	
	def Shout(self, operation, payload):
		if(operation == "GET"):
			pass
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
	def request_authentication(self, authent_id=False)
