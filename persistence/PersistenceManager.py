""" PRISONER Persistence Manager

Responsible for writing Social Objects and experimental responses to database,
managing and validating schema changes, and ensuring all writes respect relevant
privacy policies
"""
import lxml.etree as etree
from sqlalchemy import *

from gateway.ServiceGateway import *
EXPERIMENTAL_DESIGN_XSD = "/home/lhutton/svn/progress2/lhutton/projects/sns_arch/src/xsd/experimental_design.xsd"

class PersistenceManager(object):
	def __init__(self, exp_design = None, policy_processor=None):

		self.response_tables = {}
		self.object_tables = {}
		self.participant_tables = {}

		#self.engine = create_engine("sqlite:///prisoner.db")
		self.engine = None
		self.metadata = None
		#self.metadata = MetaData(self.engine)

		self.policy_processor = policy_processor

		self._experimental_design = None
		if exp_design:	
			self.experimental_design = exp_design
			self.__build_schema()
		
	@property
	def experimental_design(self):
		return self._experimental_design

	@experimental_design.setter
	def experimental_design(self, value):
		self._experimental_design = self.validate_design(value)
		# instance DB
		exp_element = self._experimental_design.xpath("//experiment")[0]
		exp_name = exp_element.get("name")
		self.engine = create_engine("sqlite:///%s.db"%exp_name)
		self.metadata = MetaData(self.engine)

	def validate_design(self, design):
		if not design:
			raise IOError("Experimental design not found at path")
		print "Validating experimental design at %s" % design
		xsd_file = open(EXPERIMENTAL_DESIGN_XSD)
		schema = etree.XMLSchema(etree.parse(xsd_file))

		design_file = open(design)
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
		table = self.get_table("participant",schema)
		print table.c
		result = table.select(table.c.id==participant_id).execute().fetchone()
		return result

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
		return result.lastrowid

		
		
	
	"""
	Writes response to the given schema
	"""
	def post_response(self, schema, response):
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
		table = self.response_tables[schema]
		insert = table.insert()
		insert.execute(response_out)

		"""
		select = table.select()
		res = select.execute()
		for row in res:
			print row
		
		trackselect = self.object_tables["track"].select()
		res = trackselect.execute()
		for row in res:
			print row
		"""

	"""
	Parses the experimental design and constructs relevant tables, classes,
	and meta_tables (for relating tables to objects).

	if drop_first is True, tables will be rebuilt on the DB, all data lost.
	THIS IS A BAD THING TO DO ACCIDENTALLY.

	This uses SQLAlchemy to generate classes bound to an engine of whatever
	database (by default, SQLite for testing) - this should support just
	about any DB-API friendly database, but no guarantees. And if you want
	to use any DB-specific features, you'll want to roll your own DB layer.
	"""
	def __build_schema(self, drop_first=False):
		tables = self.experimental_design.xpath("//tables")[0]
		
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
			elif table.get("type") == "response":
				self.response_tables[table.get("name")] = new_table
			elif table.get("mapTo") != None:
				self.object_tables[table.get("name")] = new_table
		
		if drop_first:
			self.metadata.create_all()
					
