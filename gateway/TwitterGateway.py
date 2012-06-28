from ServiceGateway import ServiceGateway
import SocialObjects



class TwitterServiceGateway(ServiceGateway):
	""" Service Gateway for Twitter. 
	
	This gateway supports reading a user's timeline and publishing tweets on
	their behalf, with support for geo-tagged content.
	"""
	def __init__(self):
		self.service_name = "Twitter"
		self.service_description = "Micro-blogging service"
