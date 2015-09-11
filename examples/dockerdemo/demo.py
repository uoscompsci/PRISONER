import json
import os
import requests
import urllib
import urllib2
import urlparse

from jinja2 import Environment, FileSystemLoader
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
#from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request, Response, BaseRequest
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
#from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.urls import url_fix
from werkzeug.utils import redirect, cached_property

dir = os.path.dirname(os.path.abspath(__file__))
SERVER_URL = "http://0.0.0.0:9000"
TEMPLATE_URL = os.path.join(dir,"static")
PRISONER_INSTANCE = "http://0.0.0.0:5000"

CONNECTION_STRING = "sqlite:////tmp/prisoner_demo.db"

PUBLIC_URL = "http://localhost:9000" # URL to reach this from client

SOCIAL_NETWORK = "Facebook"

IS_DOCKER = False



class Demo(object):
	def __init__(self):
		self.url_map = Map([
			Rule('/', endpoint="entry"),
			Rule('/start', endpoint="start"),
			Rule('/get', endpoint="get"),
			Rule('/createDatabase',endpoint="db"),
			Rule('/store',endpoint="store_data"),
			])
		self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_URL),autoescape=True)

		self.POLICY_PATH = "policy.xml"
		self.DESIGN_PATH = "design.xml"

	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype="text/html")

	def __append_session_to_url(self, url, session):
		if urlparse.urlparse(url)[4]:
			return "%s&PRISession=%s" % (url, session)
		else:
			return "%s?PRISession=%s" % (url, session)

	def on_db(self, request):
		""" This builds the database for this experiment. Only call this once!
		It will delete our participant database each time we call it!
		"""

		# build schema
		register_data = {"email":"", "schema":"participant",
		"secret":"prisonerdemosecret",
		"policy":"%s/static/policy/%s" % (SERVER_URL,self.POLICY_PATH),
		"design":"%s/static/policy/%s" % (SERVER_URL,self.DESIGN_PATH),
		"db": CONNECTION_STRING}

		session = request.sessionid

		reg_url = "%s/schema" % (PRISONER_INSTANCE)
		pri_dict = {"PRISession":session}

		reg_req = requests.post(reg_url, data=register_data, cookies=pri_dict)
		print reg_req

		return redirect("/")

 	def on_entry(self,request):
			""" Handshakes with PRISONER to start a session, registers this
			participant, hands over to PRISONER for authentication, then redirects
			to begin data collection
			"""

			handshake = requests.get(PRISONER_INSTANCE)
			prisession = handshake.cookies["PRISession"]


			response = redirect("/start")
			response.set_cookie("expSession",prisession)
			response.set_cookie("PRISession",prisession)

			return response


	def on_start(self, request):
		prisession = request.cookies["expSession"]
		pri_dict = {'PRISession':prisession}
		print "start session: %s" % prisession

		# register participant
		register_data = {"email":"", "schema":"participant",
		"secret":"prisonerdemosecret",
		"policy":"%s/static/policy/%s" % (SERVER_URL, self.POLICY_PATH),
		"design":"%s/static/policy/%s" % (SERVER_URL, self.DESIGN_PATH),
		"db": CONNECTION_STRING}

		reg_url = "%s/register" % PRISONER_INSTANCE
		reg_req = requests.post(reg_url, data=register_data, cookies=pri_dict)

		redirect_url = "%s/get?PRISession=%s" % (PUBLIC_URL, prisession)
		start_url = "%s/begin?callback=%s" % (PRISONER_INSTANCE,	redirect_url)
		start_data = {"policy":"%s/static/policy/%s" % (SERVER_URL, self.POLICY_PATH),
			"design":"%s/static/policy/%s" % (SERVER_URL, self.DESIGN_PATH),
		"participant":1,
		"providers":SOCIAL_NETWORK,
		"title":"PRISONER Demonstration",
		"contact":"lh49@st-andrews.ac.uk",
		"secret":"prisonerdemosecret",
		"db":CONNECTION_STRING}

		start_req = requests.post(start_url, data=start_data, cookies=pri_dict)

		re = redirect(start_req.text)
		re.content_type = "text/html"
		return re

	def on_store_data(self, request):
		""" Store the User object we retrieved in the database.
		The prisoner_id of the User object is used to make sure we
		save the correct object.
		"""

		prisession = request.sessionid
		prisoner_id = request.args['prisoner_id']

		post_url = "%s/post" % PRISONER_INSTANCE
		resp = {'participant_id': prisession,
				'user': prisoner_id}

		post_data = {'schema': "response",
					'response': json.dumps(resp)}

		store_req = requests.post(post_url, data=post_data,
		cookies={'PRISession':prisession})

		if store_req.status_code == 200:
			return Response("Save success!")
		else:
			raise Exception("Database write fail")

	def on_get(self, request):
		""" Get status updates and bio attributes.
		Display what we got.
		Attempt to display some attributes not in our policy.
		"""
		prisession = request.sessionid

		# status updates
		get_url = "%s/get/%s/Note/session:%s.id?limit=10" % (PRISONER_INSTANCE,
		SOCIAL_NETWORK, SOCIAL_NETWORK)

		get_response = requests.get(get_url,cookies={'PRISession':prisession})

		statuses = json.loads(get_response.text)

		# attributes
		get_url = "%s/get/%s/Person/session:%s.id" % (PRISONER_INSTANCE,
			SOCIAL_NETWORK,
			SOCIAL_NETWORK)


		get_response = requests.get(get_url,cookies={'PRISession':prisession})
		print "json: %s" % get_response.text
		me = json.loads(get_response.text)


		return self.render_template("out.html", status=statuses, me=me,
			provider=SOCIAL_NETWORK)



	# boilerplate stuff for wsgi apps to work, and handle URL-routing

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

	def dispatch_request(self, request,session=None):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, "on_" + endpoint)(request,
			**values)
		except HTTPException, e:
			return e
		except KeyError, e:
			raise
			return self.on_session_timeout(request)

	def on_session_timeout(self, request):
		return self.render_template("session.html")

	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		sid = request.cookies.get("expSession")

		request.sessionid = sid

		response = self.dispatch_request(request)
		return response(environ, start_response)

def create_app():
	app = Demo()
	return app

if __name__ == "__main__":
	from werkzeug.serving import run_simple
	app = create_app()
	#print "Started PRISONER demo..."
	#print "Static resources at %s" % TEMPLATE_URL
	run_simple("0.0.0.0", 9000, app, use_debugger=True, threaded=True,
	use_reloader=True, static_files={"/static": TEMPLATE_URL})
