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
	""" SocialObjects are representations of social data, consumed and
	generated by a range of services and applications. Every SocialObject
	provides a small number of general attributes, with each implementation
	providing additional relevant attributes.
	SocialObjects must also provide transformation logic for each attribute,
	allowing each attribute to be sanitised to an appropriate level. 
	"""
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
		self.prisoner_id = None
	
		self._friendly_names = {
		"author": "author",
		"content": "content",
		"displayName": "full name",
		"id": "unique identifier",
		"published": "time of publication",
		"summary": "brief summary",
		"updated": "last updated time",
		"url": "permanent link online",
		"location": "location of creation",
		"tags": "tags",
		"provider": "service where originally published"}

	def get_friendly_name(self, attribute):
		""" All Social Objects should include a dictionary of friendly
		names - mapping their attributes to human-readable terms. Friendly names may
		consist of several words, and must make sense in the following sentence
		construction:

		"This experiment may retrieve this social object's <friendly
		name>"

		Subclassed objects should provide their own self._friendly_names
		dictionary with mappings for each additional attribute it provides, or where it
		has semantically altered a base attribute. PRISONER will attempt to return a
		friendly name from the most specialised dictionary where possible

		:param attribute: Attribute to get friendly name of
		:type attribute: str
		"""
		return self._friendly_names[attribute]	


	def base_transform_name(self, string, transformation, level):
		""" The Base Social Objects package provides a number of
		standard transformations which are intended for use by any objects providing
		attributes of common types.
		This base transformation is designed to anonymise names of
		people, objects etc. but can be used for any string attribute

		:param string: the string to transform
		:type string: str
		:param transformation:
			"reduce" supported. Coarsens author object depending on
			value for level
		:type transformation: str
		:param level:
			first - reduce author's displayName to first name
			last - reduce author's displayName to last name
			initial - reduce author's displayName to initials of
			current names
		:type level: str
		:raises: InvalidTransformationLevelError
		"""
		levels = ["first","last","initials"]
                if level not in levels:
                        raise InvalidTransformationLevelError(level)

                if level == "first":
                        string = string.split(" ")[0]
                elif level == "last":
                        split_name = string.split(" ")
                        string = split_name[len(split_name)-1]
                elif level == "initials":
                        split_name = string.split(" ")
                        initials = ""
                        for word in split_name:
                                initials = initials + word[0]
                        string = initials

		return string


	def transform_author(self, transformation, level):
		""" Applies sanitising transformations to the author attribute,
		using the base name transformation (see base_transform_name()).
		This assumes the author is an instance of Person.
		"""
		self.author.displayName = self.base_transform_name(self.author.displayName,
		transformation, level)

	@property
	def author(self):
		""" The person responsible for the creation of the object. For
		example, the person who wrote a post, uploaded a photo, etc.
		Should be an instance of Person.
		"""
		return self._author

	@author.setter
	def author(self, value):
		self._author = value

	@property
	def content(self):
		""" The main content of this object. Where possible, this should
		be plain text, or a URI to an external resource. Avoid packing binary data into
		this property as it may be difficult to sanitise and serialize.
		"""
		return self._content
	
	@content.setter
	def content(self, value):
		self._content = value

	@property
	def displayName(self):
		""" A natural language plain-text description of this object,
		without any additional markup. For example, the name of a location, or a
		person's full name. """
		return self._displayName
	
	@displayName.setter
	def displayName(self,value):
		self._displayName = value

	@property
	def id(self):
		""" A unique identifier for this object. Where possible, this
		should allow the service gateway to relate an instance of a SocialObject to its
		counterpart on the service """
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

	@property
	def location(self):
		""" An instance of Place to indicate the location of an object,
		or the location in which it was used. """
		return self._location

	@location.setter
	def location(self, value):
		self._location = value

	@property
	def provider(self):
		""" The name of the ServiceGateway which generated this object,
		or where it is intended to be published to. This must map to an available
		ServiceGateway, or not be set. """
		return self._provider

	@provider.setter
	def provider(self, value):
		self._provider = value

	@property
	def published(self):
		""" A time object indicating when the object was created. """
		return self._published

	@published.setter
	def published(self, value):
		self._published = value
	
	@property
	def tags(self):
		""" A collection of SocialObjects associated with this object.
		This object must not be dependent on the tags to be semantically correct (eg. do
		not embed a collection of authors as tags) """
		return self._tags

	@tags.setter
	def tags(self, value):
		self._tags = value

	@property
	def updated(self):
		""" A time object indicating when the object was last updated. """
		return self._updated

	@updated.setter
	def updated(self, value):
		self._updated = value

	@property
	def url(self):
		""" A permament link to this object's online representation.
		This should be unique to this object and ideally permanent. It is acceptable for
		this link to be inaccessible without authentication. """
		return self._url

	@url.setter
	def url(self, value):
		self._url = value

class Address(SocialObject):
	""" Generally used as an attribute of Place, encodes a textual
	description of a physical address on Earth """
	
	def __init__(self):
		super(Address, self).__init__()
		self._formatted = None
		self._streetAddress = None
		self._locality = None
		self._region = None
		self._postalCode = None
		self._country = None

	@property
	def formatted(self):
		""" A full textual representation of the address, formatted as
		for printing a mailing label """
		return self._formatted

	@formatted.setter
	def formatted(self, value):
		self._formatted = value

	@property
	def streetAddress(self):
		""" The street address including house number, street name, PO
		Box """
		return self._streetAddress

	@streetAddress.setter
	def streetAddress(self, value):
		self._streetAddress = value

	@property
	def locality(self):
		""" The city, town, village, etc. """
		return self._locality

	@locality.setter
	def locality(self, value):
		self._locality = value

	@property
	def region(self):
		""" The state or region """
		return self._region

	@region.setter
	def region(self, value):
		self._region = value

	@property
	def postalCode(self):
		""" The zip or postal code """
		return self._postalCode

	@postalCode.setter
	def postalCode(self, value):
		self._postalCode = value

	@property
	def country(self):
		""" The country name """
		return self._country

	@country.setter
	def country(self, value):
		self._country = value

class Collection(SocialObject):
	""" Represents a generic collection of SocialObjects. It may contain any
	number and any combination of SocialObjects.
	"""
	def __init__(self):
		super(Collection,self).__init__()
		self._objects = None

	@property
	def objects(self):
		""" The collection of objects. Should be a list or SocialObjects
		instances. """
		return self._objects

	@objects.setter
	def objects(self, value):
		self._objects = value

class Comment(SocialObject):
	""" A textual response to another SocialObject. The base type should not
	be used for replying with rich content - video or images, etc. """
	def __init__(self):
		super(Comment,self).__init__()
		self._inReplyTo = None
	
	@property
	def inReplyTo(self):
		""" The SocialObject (or set of objects) this comment is in
		response to. """
		return self._inReplyTo

	@inReplyTo.setter
	def inReplyTo(self, value):
		self._inReplyTo = value

class Event(SocialObject):
	""" An event occuring in a place during a time interval. """
	def __init__(self):
		super(Event, self).__init__()
		self._attending = None
		self._endTime = None
		self._maybeAttending = None
		self._notAttending = None
		self._startTime = None
	
	@property
	def attending(self):
		""" A collection of People who have RSVP'd to an event """
		return self._attending

	@attending.setter
	def attending(self, value):
		self._attending = value

	@property
	def endTime(self):
		""" A time object representing when the event ends """
		return self._endTime

	@endTime.setter
	def endTime(self, value):
		self._endTime = value

	@property
	def maybeAttending(self):
		""" A collection of People who have responded to say they may
		attend the event """
		return self._maybeAttending

	@maybeAttending.setter
	def maybeAttending(self, value):
		self._maybeAttending = value

	@property
	def notAttending(self):
		""" A collection of People who have responded to say they are
		not attending the event """
		return self._notAttending

	@notAttending.setter
	def notAttending(self, value):
		self._notAttending = value

	@property
	def startTime(self):
		""" A time object representing when the event starts """
		return self._startTime

	@startTime.setter
	def startTime(self, value):
		self._startTime = value

class Image(SocialObject):
	""" A graphical image, such as a photo. """
	def __init__(self):
		super(Image,self).__init__()
		self._fullImage = None

	@property
	def fullImage(self):
		""" A URI for a full-size version of this image. """
		return self._fullImage
	
	@fullImage.setter
	def fullImage(self, value):
		self._fullImage = value

class Note(SocialObject):
	""" A short text message, often used in a microblogging context, or to
	share short status updates. Shorter than blog posts, Notes are expected
	to have a shorter life and might not even expose a permalink """

	def __init__(self):
		super(Note, self).__init__()

class Person(SocialObject):
	""" A human actor involved in the exchange of SocialObjects. """
	def __init__(self):
		super(Person,self).__init__()
		self._image = None
	
	@property
	def image(self):
		""" An instance of Image used to visually represent this
		Person."""
		return self._image
	
	@image.setter
	def image(self,value):
		self._image = value

class Place(SocialObject):
	""" A location on Earth. For maximum flexibility, use geographic
	coordinates. Alternatively, a physical address or free-form location name may be
	provided, so long as the applications which consume Place objects can
	understand its semantics. A combination of location identifiers may be
	used. """

	def __init__(self):
		super(Place, self).__init__()
		self._position = None
		self._address = None

	@property
	def position(self):
		""" Latitude, longitude and altitude of point on Earth. This
		must be an ISO 6709 string (eg. "+27.5916+086.5640+8850/") """
		return self._position

	@position.setter
	def position(self, value):
		self._position = value

	@property
	def address(self):
		""" An instance of Address, for encoding a textual addresss """
		return self._address

	@address.setter
	def address(self, value):
		self._address = value
