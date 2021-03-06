import json
import jsonpickle
import lxml.etree as etree
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import urllib2

from prisoner.gateway.ServiceGateway import *
#EXPERIMENTAL_DESIGN_XSD = "../xsd/experimental_design.xsd"

dir = os.path.dirname(__file__)

EXPERIMENTAL_DESIGN_XSD =  os.path.join(dir, "../xsd/experimental_design.xsd")

class PersistenceManager(object):
	""" The PersistenceManager manages the storage of all data, including
	participant metadata, experimental responses, and persistence of Social Objects.
	Storage of data is subject to the privacy policy for the experiment.
	Generally, participation clients do not directly instantiate a
	PersistenceManager, and where possible, friendlier interfaces are available
	through the ExperimentBuilder and SocialObjectsGateway.
	"""

	def __init__(self, exp_design = None, policy_processor=None,
	connection_string=None):
		""" Instantiate a PersistenceManager by supplying an experimental
		design and instance of PolicyProcessor (assumed to already be bound to a valid
		privacy policy).

		:param exp_design: Path to experimental design file
		:type exp_design: str.
		:param policy_processor: Instance of PolicyProcessor used to
		validate and sanitise requests to store data
		:type policy_processor: PolicyProcessor
		:param connection_string: The connection string for the underlying database
		:type connection_string: str
		"""

		self.response_tables = {}
		self.object_tables = {}
		self.participant_tables = {}
		self.participant_table = None
		self.meta_participant_table = None
		self._props = None

		self.engine = None
		self.metadata = None

		self.policy_processor = policy_processor
		self.connection_string = connection_string

		self._experimental_design = None
		if exp_design:
			self.experimental_design = exp_design
			self.__build_schema()

	@property
	def props(self):
		return self.get_props()


	@props.setter
	def props(self, value):
		self._props = value


	@property
	def experimental_design(self):
		return self._experimental_design

	@experimental_design.setter
	def experimental_design(self, value):
		""" Set the experimental design. This is immediately validated
		and used to construct a schema for experimental responses and participant
		metadata.
		:param value: Path to experimental design file
		:type value: str
		"""

		self._experimental_design = self.validate_design(value)
		# instance DB
		exp_element = self._experimental_design.xpath("//experiment")[0]
		exp_name = exp_element.get("name")
		self.engine = create_engine(self.connection_string,
		poolclass=NullPool)
		self.metadata = MetaData(self.engine)


	def rebuild_engine(self, connection_string):
		self.engine = create_engine(connection_string,
		poolclass=NullPool)
		self.metadata = MetaData(self.engine)

	def validate_design(self, design):
		"""
		Tests that the given experimental design validates against the
		XML schema

		:param design: Path to experimental design
		:type design: str
		:raises: IOError
		:returns: ElementTree - parsed experimental design object
		"""

		if not design:
			raise IOError("Experimental design not found at path")
		xsd_file = open(EXPERIMENTAL_DESIGN_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		try:
			design_file = open(design)
		except IOError:
			design_file = urllib2.urlopen(design)
		design = etree.parse(design_file)

		validation = schema.assertValid(design)


		return design

	def get_table(self, table_type, table_name):
		""" Returns an active connection to the requested table. Used
		internally for data access. Do not use this from participation
		clients. Instead, use managed data access interfaces where possible to
		ensure data are sanitised appropriately.

		:param table_type: Type of table [response, participant, object]
		:type table_type: str
		:param table_name: Name of table to return
		:returns: Table - requested table
		"""

		table_dict = getattr(self, "%s_tables" % table_type)
		return table_dict[table_name]

	def get_participant(self, schema, participant_id):
		""" Retrieve the participant with the given ID from the given
		schema.

		:param schema: name of scema to get participant from
		:type schema: str
		:param participant_id: ID of participant to return
		:type participant_id: int
		:returns: tuple - participant data from database
		"""

		table = self.get_table("participant",schema)
		result = table.select(table.c.id==participant_id).execute().fetchone()
		return result

	def get_props(self):
		""" Parses the props collection in the experimental design and makes these
		available as a dict of dicts

		:returns: dict of dicts of props
		"""

		if self._props:
			return self._props

		props = self.experimental_design.xpath("//prop")
		out_props = {}
		for prop in props:
			if prop.get('for') not in out_props:
				out_props[prop.get('for')] = {}
			out_props[prop.get('for')][prop.get('key')] = prop.get('value')

		self._props = out_props
		return out_props



	def register_participant(self, schema, participant):
		""" Add the participant data in given dictionary to the
		participant table in this database and return the ID

		:param schema: name of participant table (must be of type
		'participant')
		:type schema: str.
		:param participant: dictionary of data about participant
		:type participant: dict
		:returns: int -- inserted row ID
		"""

		response = participant
		if schema not in self.participant_tables:
			raise Exception("Participant schema not found")
		# walk the response schema for each column
		xpath = "//table[@name='%s']" % schema
		columns = self.experimental_design.xpath(xpath)
		response_out = {}
		# is column present in response?
		for column in columns[0]:
			if column.get("name") not in response:
				raise Exception("Response object missing value "+\
				"for %s" % column.get("name"))
		# if column has a mapTo attribute, sanitise object
			mapTo = column.get("mapTo")
			if mapTo:
				headers = SARHeaders("PUT",
				None,
				type(response[column.get("name")]).__name__, None)
				response = SocialActivityResponse(response[column.get("name")], headers)

				san_obj = self.policy_processor._sanitise_object_request(response)
				# insert object to corresponding table
				mapTable = self.object_tables[mapTo.split(":")[1]]
				obj_to_insert = {}
				for mapCol in mapTable.columns:
					mapCol = mapCol.name
					obj_to_insert[mapCol] = getattr(san_obj, mapCol)
				# place id of inserted object in map column
				mapInsert = mapTable.insert()
				mapId = mapInsert.execute(obj_to_insert).lastrowid
				response_out[column.get("name")]  = mapId
			else:
				response_out[column.get("name")] = response[column.get("name")]
		# insert response
		table = self.participant_tables[schema]
		insert = table.insert()
		result = insert.execute(response_out)
		return self.get_participant(schema, result.lastrowid)

	def register_participant_with_provider(self, participant_id, provider, token):
		""" Store access credentials with this provider for the given
		participant. Access token can be any object, so long as the
		relevant service gateway is able to interpet it.

		:param participant_id: Participant to register access token with
		:type participant_id: int
		:param provider: Name of provider to register access token with
		:type provider: str
		:param token: Access token used in authenticated calls
		:type token: object
		:returns: row as inserted in meta_table
		"""

		table = self.meta_participant_table
		insert = table.insert()
		response = {"participant_id": participant_id, "provider": provider,
		"access_token": token}
		insert.execute(response)

		res = table.select().execute()

	def get_existing_provider_auth(self, participant_id, provider):
		""" Checks if the given participant has been
		previously authenticated with the named provider. If so, returns the credentials
		stored. Otherwise, returns None, so participant should continue with consent
		flow.
		If credentials are found, a ServiceGateway should be provided with them. It
		should signal whether it is able to successfully authenticate with them. If not,
		it should attempt to reauthenticate server-side if possible (eg. request new
		session from API). If clientside intervention is required, it should signal
		this.

		:param participant_id: ID of participant to authenticate
		:type participant_id: int
		:param provider: Name of provider to return authentication for
		:type provider: str
		:returns: Stored credentials or None
		"""

		table = self.meta_participant_table
		result = table.select(and_(table.c.participant_id==participant_id,
		table.c.provider == provider)).execute().fetchone()
		if result:
			return result.access_token
		else:
			return None


	def post_response_json(self, sog, schema, response):
		""" Wrapper to post_response for use by web services.

		:param sog: Current instance of SocialObjectsGateway
		:type sog: SocialObjectsGateway
		:param schema: Name of response schema to write to
		:type schema: str
		:param response:
			JSON object corresponding to the response schema.
			References to SocialObjects must consist of its prisoner_id (as originally
			received)
		:type response: JSON object as str.
		"""

		if schema not in self.response_tables:
			raise Exception("Schema not found")

		xpath = "//table[@name='%s']" % schema
		columns = self.experimental_design.xpath(xpath)
		response_out = {}

		json_obj = json.loads(response)

		for column in columns[0]:
			mapTo = column.get("mapTo")
			if mapTo:
				obj_id = json_obj[column.get("name")]
				mapped_obj = sog.cached_objects[obj_id]
				json_obj[column.get("name")] = mapped_obj

		return self.post_response(schema, json_obj)

	def post_response(self, schema, response):
		""" Writes response to given schema.

		:param schema: Schema to write to
		:type schema: str
		:param response: Response data to write
		:type response: dict
		"""

		if not self.experimental_design:
			raise Exception("No experimental design")

		# does response data correspond to the given schema?
		if schema not in self.response_tables:
			raise Exception("Schema not found")

		# walk the response schema for each column
		xpath = "//table[@name='%s']" % schema
		columns = self.experimental_design.xpath(xpath)
		response_out = {}
		# is column present in response?
		for column in columns[0]:
			if column.get("name") not in response:
				raise Exception("Response object missing value "+\
				"for %s" % column.get("name"))
		# if column has a mapTo attribute, sanitise object
			mapTo = column.get("mapTo")
			if mapTo:
				headers = SARHeaders("PUT",
				response[column.get("name")].provider,
				type(response[column.get("name")]).__name__, None)
				response = SocialActivityResponse(response[column.get("name")], headers)

				san_obj = self.policy_processor._sanitise_object_request(response)

				if not san_obj:
					raise Exception("Could not write to database. %s failed validation" % column.get("mapTo"))


				san_obj_json = jsonpickle.encode(san_obj)
				response_out[column.get("name")]  = san_obj_json
			else:
				response_out[column.get("name")] = response[column.get("name")]
		# insert response
		table = self.response_tables[schema]
		insert = table.insert()
		result = insert.execute(response_out)


	def do_build_schema(self, drop_first=False):
		return self.__build_schema(drop_first)

	def close_connection(self):
		self.engine.dispose()


	def __build_schema(self, drop_first=False):
		"""
		Parses the experimental design and constructs relevant tables, classes,
		and meta_tables (for relating tables to objects).

		if drop_first is True, tables will be rebuilt on the DB, all data lost.
		THIS IS A BAD THING TO DO ACCIDENTALLY.

		This uses SQLAlchemy to generate classes bound to an engine of whatever
		database (by default, SQLite for testing) - this should support just
		about any DB-API friendly database, but no guarantees. And if you want
		to use any DB-specific features, you'll want to roll your own DB layer.

		:param drop_first: Should database be trashed first?
		:type drop_first: boolean
		"""
		
		tables = self.experimental_design.xpath("//tables")[0]

		if drop_first:
			self.metadata = MetaData(self.engine)
			self.participant_tables = {}
			self.response_tables = {}
			self.object_tables = {}

		for table in tables:
			cols = []
			cols.append(Column("id", Integer, primary_key=True))
			for column in table:
				cols.append(Column(column.get("name"),
				String(100)))
			new_table = Table(table.get("name"),self.metadata,
			*cols)
			if table.get("type") == "participant":
				if len(self.participant_tables.keys()) != 0:
					exp = "Only one participant table can be"+\
					" defined per experiment"
					raise Exception(exp)
				self.participant_tables[table.get("name")] = new_table
				self.participant_table = new_table
				# make a metaparticipant table for storing
				# access keys
				meta_table = Table("meta_%s" %
				table.get("name"), self.metadata,
				Column("id",Integer,primary_key=True),
				Column("participant_id",Integer),
				Column("provider",String(255)),
				Column("access_token",String(255)))
				self.meta_participant_table = meta_table
			elif table.get("type") == "response":
				self.response_tables[table.get("name")] = new_table
			elif table.get("mapTo") != None:
				self.object_tables[table.get("name")] = new_table

		if drop_first:
			self.metadata.create_all()
