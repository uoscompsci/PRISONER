"""
PRISONER Dummy Participation client
===================================

This is designed to be evokable from the cmdline etc. as a way of testing
various features of PRISONER.
If its various bits work, it's a good indication you've set it up right.
"""

import SocialObjects
from gateway import LastfmServiceGateway
from workflow import ExperimentBuilder, SocialObjectGateway


def do_experiment():
	""" Call this after consent completed to do object calls """

	print "Consent complete. Now start experiment"
	me = SocialObjects.Person()
	me.id = "532336768"
	img = expBuilder.sog.GetObject("Facebook","Image",me)
	print img
	print img.fullImage
	print img.author.displayName


if __name__ == "__main__":
	privacy_policy = "../lib/fb_privacy_policy_test.xml"
	exp_design = "../lib/fb_exp_design_test.xml"
	
	expBuilder = ExperimentBuilder.ExperimentBuilder()
	
	expBuilder.provide_privacy_policy(privacy_policy)
	expBuilder.provide_experimental_design(exp_design)
	
	# uncomment to register new participant
#	new_participant = {"name": "Bob", "gender": "male", "serviceGroup": "Lastfm"}
#	my_id =	expBuilder.sog.register_participant("participant",new_participant)
#	participant = expBuilder.authenticate_participant("participant",my_id[0])

	# TODO: user-facing authentication

	# uncomment to login as participant 1
	participant = expBuilder.authenticate_participant("participant",1)

	print participant


	expBuilder.authenticate_providers(["Facebook"])
	consent_url = expBuilder.build(do_experiment)	
	print "Visit %s to begin participating in this experiment" % consent_url

