# prisoner.wsgi
#
# This spawns a PRISONER web server within a WSGI container
# It can be run directly for testing.



import sys, os
dir = os.path.dirname(os.path.abspath(__file__))
print "dir: %s" % dir


sys.path.append("/usr/bin")
sys.path.append("/usr/bin/prisoner")

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(dir, "../../"))

print sys.path
#import prisoner
from prisoner import server
from werkzeug.debug import DebuggedApplication

#application = DebuggedApplication(server.webservice.create_app(), evalex=True)

from werkzeug.serving import run_simple
app = server.webservice.create_app()
print "Starting PRISONER Web Service..."
TEMPLATE_URL = "/usr/bin/prisoner/static"

run_simple("localhost", 5000, app, use_debugger=True, use_reloader=True,
static_files={"/static": TEMPLATE_URL})