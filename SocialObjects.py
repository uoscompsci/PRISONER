"""
PRISONER - Core Social Objects
==============================
This package contains abstract implementations of Social Objects. They provide
the common structure that any implementation should be able to handle, and
contain all common processing logic for core types.
"""

class InvalidTransformationLevelError(Exception):
	def __init__(self, value):
		self.level = value
	def __str__(self):
		return "Object can not be transformed to level: %s" % self.level

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
		self._provider = None

	"""
	Transformations apply privacy-preserving logic to attributes of an
	object. 
	transformation - "reduce" -  coarsen the data to "level". This depends on
				     the semantics of the transformed object
			 "obfuscate"-replace content with a random
				     non-identifying value that is still semantically relevant

	We provide built-in transformations for all base Social Objects.
	Service gateways MUST support all transformation types on all additional
	objects and attributes, or requests may be invalidated.
	"""

	"""
	Transforms the author attribute.
	If Author is not a Person, an exception is raised.

	Possible values of "level" for transformation="reduce":
		first - Only include first name
		last - Only include last name
		initial - Only include initials
	""" 
	def transform_author(self, transformation, level):
		levels = ["first","last","initials"]
		if level not in levels:
			raise InvalidTransformationLevelError(level)

		if level == "first":
			self.author.displayName = self.author.displayName.split(" ")[0]
		elif level == "last":
			split_name = self.author.displayName.split(" ") 
			self.author.displayName = split_name[len(split_name)-1]
		elif level == "initials":
			split_name = self.author.displayName.split(" ")
			initials = ""
			for word in split_name:
				initials = initials + word[0]
			self.author.displayName = initials

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

	@property
	def displayName(self):
		return self._displayName
	
	@displayName.setter
	def displayName(self,value):
		self._displayName = value

	@property
	def provider(self):
		return self._provider

	@provider.setter
	def provider(self, value):
		self._provider = value

"""
Represents a generic collection of Social Objects - can contain any combination
of types.
Use to represent playlists, photo albums etc. and subclass to add
service-specific extensions
"""
class Collection(SocialObject):
	def __init__(self):
		super(Collection,self).__init__()
		self._objects = None

	@property
	def objects(self):
		return self._objects

	@objects.setter
	def objects(self, value):
		self._objects = value

class Comment(SocialObject):
	def __init__(self):
		super(Comment,self).__init__()
		self._inReplyTo = None
	
	@property
	def inReplyTo(self):
		return self._inReplyTo

	@inReplyTo.setter
	def inReplyTo(self, value):
		self._inReplyTo = value

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

