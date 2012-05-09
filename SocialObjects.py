"""
PRISONER - Core Social Objects
==============================
This package contains abstract implementations of Social Objects. They provide
the common structure that any implementation should be able to handle, and
contain all common processing logic for core types.
"""

class SocialObject(object):
	def __init__(self):
		self._author = None
		self._content = None
		self._displayName = None
		self._id = None
		self._published = None
		self._summary = None
		self._updated = None
		self._url = None
		self.location = None
		self.tags = None

	@property
	def author(self):
		return self._author

	@author.setter
	def author(self, value):
		self._author = value

	@property
	def content(self):
		return self._content
	
	@content.setter
	def content(self, value):
		self._content = value
	
	

			

class Image(SocialObject):
	def __init__(self):
		pass


