""" PRISONER Persistence Manager

Responsible for writing Social Objects and experimental responses to database,
managing and validating schema changes, and ensuring all writes respect relevant
privacy policies
"""
import lxml.etree as etree
from sqlalchemy import *

EXPERIMENTAL_DESIGN_XSD = "/home/lhutton/svn/progress2/lhutton/projects/sns_arch/src/xsd/experimental_design.xsd"

class PersistenceManager(object):
	def __init__(self, exp_design = None):

		self.response_tables = {}
		self.object_tables = {}
		self.participant_tables = {}

		self.engine = create_engine("sqlite:///:memory:")
		self.metadata = MetaData()

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
	
	"""
	Writes response to the given schema
	"""
	def post_response(self, schema, response):
		if not self.experimental_design:
			raise Exception("No experimental design")
		
		if schema not in self.response_tables:
			raise Exception("Schema not found")

		table = self.response_tables[schema]
		insert = table.insert()
		insert.execute(response)

		print table.select()
		

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
			for column in table[0]:
				print table
				cols.append(Column(column.get("name"),
				String(100)))
			new_table = Table(table.get("name"),self.metadata,
			*cols)
			if table.get("type") == "participant":
				self.participant_tables[table.get("name")] = new_table
			elif table.get("type") == "response":
				self.response_tables[table.get("name")] = new_table
			elif table.get("mapTo") != None:
				self.object_tables[table.get("name")] = new_table
					
