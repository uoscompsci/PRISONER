"""
PRISONER Dummy Participation client
===================================

This is designed to be evokable from the cmdline etc. as a way of testing
various features of PRISONER.
If its various bits work, it's a good indication you've set it up right.
"""


import SocialObjects
from gateway import FacebookGateway
from workflow import ExperimentBuilder, SocialObjectGateway


def do_experiment():
	""" Call this after consent completed to do object calls """

	print "\n-----"
	print "Start experiment..."
	
	# Create user for experimemt.
	print "- Creating person object with ID..."
	me = SocialObjects.Person()
	me.id = "532336768"
	print "- Done!"
	
	# Get user's profile info.
	print "- GetObject() :: User"
	person_obj = expBuilder.sog.GetObject("Facebook","User", me)
	print "- Done!"
	
	# Print profile info.
	print "- ID: " + str(person_obj.id)
	print "- First Name: " + str(person_obj.firstName)
	print "- Middle Name: " + str(person_obj.middleName)
	print "- Last Name: " + str(person_obj.lastName)
	print "- Display Name: " + str(person_obj.displayName)
	print "- Username: " + str(person_obj.username)
	print "- Gender: " + str(person_obj.gender)
	print "- Birthday: " + str(person_obj.birthday)
	print "- Profile Pic: " + str(person_obj.image.fullImage)
	print "- Email Address: " + str(person_obj.email)
	print "- Bio: " + str(person_obj.bio)
	print "- Languages: " + str(person_obj.languages)
	print "- Last Update: " + str(person_obj.updatedTime)
	print "- Timezone: " + str(person_obj.timezone)
	print "- Location: " + str(person_obj.location.displayName)
	print "- Hometown: " + str(person_obj.hometown.displayName)
	print "- Education: " + str(person_obj.education)
	print "- Work: " + str(person_obj.work)
	print "- Politcs: " + str(person_obj.politicalViews)
	print "- Religion: " + str(person_obj.religion)
	print "- Relationship Status: " + str(person_obj.relationshipStatus)
	print "- Significant Other: " + str(person_obj.significantOther)
	
	# Get user's friends list.
	#print "- GetObject() :: FriendsList"
	#friends_list = expBuilder.sog.GetObject("Facebook","Friends", me)
	#print "- Done!"
	
	# Print friends list.
	#print "- Friends List: " + str(friends_list)
	#print "- Number of friends: " + str(len(friends_list.objects))
	
	#for friend in friends_list.objects:
		#print "- Friend object type: " + str(type(friend))
	
	# Get user's music interests.
	print "- GetObject() :: Music"
	music = expBuilder.sog.GetObject("Facebook","Music", me)
	print "- Done!"


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

