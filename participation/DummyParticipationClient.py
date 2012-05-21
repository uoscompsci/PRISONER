"""
PRISONER Dummy Participation client

This is designed to be evokable from the cmdline etc. as a way of testing
various features of PRISONER.
If its various bits work, it's a good indication you've set it up right.
"""

import SocialObjects
from gateway import LastfmServiceGateway
from workflow import SocialObjectGateway

if __name__ == "__main__":
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

	tracks = session.GetObject("Lastfm","Track",me,allow_many=True)
	print tracks

	response_obj = {}
	response_obj['track'] = tracks[0]
	response_obj['answer'] = "Test answer"
	session.post_response("response",response_obj)

	# Uncomment to test publish
	"""
	post_shout = SocialObjects.Comment()
	post_shout.author = me
	post_shout.inReplyTo= me
	post_shout.content = "PRISONER post test"
	session.PostObject("Lastfm","Comment",post_shout)
	"""
