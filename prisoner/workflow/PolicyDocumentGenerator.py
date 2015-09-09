import lxml.etree as etree

from workflow import SocialObjectGateway

class PolicyDocumentGenerator(object):
	""" The PolicyDocumentGenerator generates human-readable versions of
	PRISONER policy documents - the privacy policy and experimental design. It
	returns natural language documents so that participants and other stakeholders
	know exactly how an experimental application will collect, store, and generate
	data about them. This exposes generators for HTML, LaTeX, among others, with the
	ability to define your own generators for specific output formats.

	This is in-development, concept stuff. Do not use in production!
	"""

	def __init__(self, policy, design, format):
		""" Initialises a generator for the given files, to generate a
		document in the requested format.

		:param policy: path to privacy policy XML file
		:type policy: str
		:param design: path to experimental design XML file
		:type design: str
		:param format:
			what type of document to generate - can be "html"
			or "latex"
		:type format: str
		"""
		self.sog = SocialObjectGateway.SocialObjectsGateway()
		self.sog.provide_privacy_policy(policy)
		self.sog.provide_experimental_design(design)
		self.format = format
		call_format = getattr(self,format)
		call_format()

	def html(self):
		self.do_print_policy()

	def latex(self):
		pass

	def do_print_policy(self):
		priv = self.sog.policy_processor.privacy_policy
		query_path = "//policy"
		tree = priv.xpath(query_path)	

		policy_out = {}
		for policy in tree:
			out = self.print_policy(policy)
			policy_out[policy.get("for")] = out

		print policy_out	

	def print_policy(self, tree):
		policy_out = {}
		logical_elements = ["and-match","or-match"]
		comparison_elements = ["attribute-match"]

		
		criteria_walk = etree.iterwalk(tree,
		events=("start","end"))
		criteria_walk.next()

		logic_stack = []
		obj_policy_set = []
		policy_set = []

		top = "and"
		for action, element in criteria_walk:
			if action == "start":
				if element.tag == "object-policy":
					policy_clause = "This experiment may %s a %s if" % (element.get("allow"), tree.get("for"))
					sub_count = 0
				elif element.tag == "attribute-policy":
					policy_clause = "This experiment may %s a %s of a %s if" % (element.get("allow"),
					element.getparent().get("type"), tree.get("for"))
					sub_count = 0
				elif element.tag in logical_elements:
					if "and" in element.tag:
						top = "and"
					elif "or" in element.tag:
						top = "or"
					logic_stack.push(top)
				elif element.tag in comparison_elements:
					policy_clause = "%s its %s matches %s %s" % (policy_clause, element.get("match"),
					element.get("on_object"), top)
					sub_count += 1

			elif action == "end":
				if  element.tag == "object-criteria":
					policy_clause = policy_clause.rsplit(" ",1)[0]
					obj_policy_set.append(policy_clause)
				elif element.tag == "attribute-criteria":
					policy_clause = policy_clause.rsplit(" ",1)[0]
					obj_policy_set.append(policy_clause)
				elif (element.tag == "object-policy" and
				sub_count == 0):
					policy_clause = policy_clause.rsplit(" ",1)[0]
					obj_policy_set.append(policy_clause)
				elif(element.tag == "attribute-policy" and
				sub_count == 0):
					policy_clause = policy_clause.rsplit(" ",1)[0]
					obj_policy_set.append(policy_clause)
				elif element.tag in logical_elements:
					logic_stack.pop()
		return obj_policy_set

if __name__ == "__main__":
	priv_path = "/home/lhutton/hg/prisoner/src/lib/lastfm_privacy_policy_test.xml"
	exp_design = "/home/lhutton/hg/prisoner/src/lib/lastfm_exp_design_test.xml"
	pdg = PolicyDocumentGenerator(priv_path, exp_design, "html")


