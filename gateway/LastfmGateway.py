"""
Last.fm Service Gateway for PRISONER

This is a concrete implementation of the Service Gateway interface, for
reference
"""
from ServiceGateway import ServiceGateway
import SocialObjects

class LastfmServiceGateway(ServiceGateway):

	def __init__(self):
		self.service_name = "Last.fm"
		self.service_description = "Music recommendation service"

	def Image(self, operation, payload):
		if (operation == "GET"):
			return "You GOT a Last.fm image!"
		else:
			return "Oops..."
