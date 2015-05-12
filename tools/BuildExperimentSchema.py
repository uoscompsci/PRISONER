"""
Build Experiment Schema
=======================
Use to construct the schema for an experiment. 
Provide an experimental design file, which is validated and used to generate an
empty. Call this script each time your schema changes (existing data will be
lost) to rebuild the database. This script must be called before running your
experiment or registering participants.
"""

import sys
#sys.path.append("/home/lhutton/prisoner/prisoner")
from optparse import OptionParser
from workflow import ExperimentBuilder




parser = OptionParser()
parser.add_option("-d","--design", type="string", dest="design",
help="Path to the experimental design file for this experiment")

parser.add_option("-p","--policy", type="string", dest="policy",
help="Path to the privacy policy file for this experiment")

parser.add_option("-c","--connection", type="string", dest="connection",
help="Database connection string (eg. sqlite:///test.db")

parser.add_option("-s","--server", type="string", dest="server",
help="URL of PRISONER server")



(options, args) = parser.parse_args()

if __name__ == "__main__":
	design = options.design
	policy = options.policy
	connection = options.connection

	expBuilder = ExperimentBuilder.ExperimentBuilder(options.server)
	expBuilder.provide_privacy_policy(policy)
	expBuilder.provide_db_string(connection)
	expBuilder.provide_experimental_design(design)
	expBuilder.build_schema()	
	
	
