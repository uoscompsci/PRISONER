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
		self._location = None
		self._tags = None

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
		super(Image,self).__init__()
		self._fullImage = None

	@property
	def fullImage(self):
		return self._fullImage
	
	@fullImage.setter
	def fullImage(self, value):
		self._fullImage = value

class Person(SocialObject):
	def __init__(self):
		super(Person,self).__init__()
		self._image = None
	
	@property
	def image(self):
		return self._image
	
	@image.setter
	def image(self,value):
		self._image = value

