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
	
	me = SocialObjects.Person()
	me.id = "lukeweb"
	session.GetObject("Lastfm","Image",me)
