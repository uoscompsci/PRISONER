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

if __name__ == "__main__":
	"""
	OLD DUMMY CODE	
	session = SocialObjectGateway.SocialObjectsGateway() 
	session.provide_privacy_policy("/home/lhutton/svn/progress2/lhutton/projects/sns_arch/spec/privacy_policy_validation_test.xml")
	session.provide_experimental_design("/home/lhutton/svn/progress2/lhutton/projects/sns_arch/spec/experimental_design_test.xml")

	# acquire auth for service for user (via web)
	authent_url = session.request_authentication("Lastfm")
	print "Get authent by going to %s " % authent_url
	print "When done, press key to confirm auth"
	inp = raw_input()	
	session.complete_authentication("Lastfm",authent_url)
	
	me = SocialObjects.Person()
	me.id = "lukeweb"

	#img = session.GetObject("Lastfm","Image",me)
	#print img
	#print img.fullImage

	tracks = session.GetObject("Lastfm","Track",me)

	response_obj = {}
	response_obj['track'] = tracks.objects[0]
	response_obj['answer'] = "Test answer"
	session.post_response("response",response_obj)

	# Uncomment to test publish
	post_shout = SocialObjects.Comment()
	post_shout.author = me
	post_shout.inReplyTo= me
	post_shout.content = "PRISONER post test"
	session.PostObject("Lastfm","Comment",post_shout)
	"""

	privacy_policy = "/home/lhutton/hg/prisoner/src/lib/privacy_policy_validation_test.xml"
	exp_design = "/home/lhutton/hg/prisoner/src/lib/experimental_design_test.xml"
	
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

	me = SocialObjects.Person()
	me.id = "lukeweb"
	img = expBuilder.sog.GetObject("Lastfm","Image",me)
	print img
	print img.fullImage
	print img.author.displayName

	expBuilder.authenticate_providers(["Lastfm"])
	consent_url = expBuilder.build()	
	print "Visit %s to begin participating in this experiment" % consent_url
	

