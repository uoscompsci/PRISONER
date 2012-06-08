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
import random


def do_experiment():
	""" Call this after consent completed to do object calls """

	print "\n-----"
	print "Start experiment"
	print "-----"
	
	# Create user for experimemt.
	# Me: 532336768
	# Ben: 100001427539048
	me = SocialObjects.Person()
	me.id = "532336768"
	print "\n" + "Experiment user: " + me.id
	
	# Grab data.
	print "Retrieving profile information..."
	person_obj = expBuilder.sog.GetObject("Facebook","User", me)
	print "- Done!"
	
	print "Retrieving friends list..."
	friends_list = expBuilder.sog.GetObject("Facebook","Friends", me)
	print "- Done!"
	
	print "Retrieving favourite bands..."
	fav_music = expBuilder.sog.GetObject("Facebook","Music", me)
	print "- Done!"
	
	print "Retrieving favourite movies..."
	fav_movies = expBuilder.sog.GetObject("Facebook","Movie", me)
	print "- Done!"
	
	print "Retrieving favourite books and authors..."
	fav_books = expBuilder.sog.GetObject("Facebook","Book", me)
	print "- Done!"
	
	print "Retrieving a list of your status updates..."
	statuses = expBuilder.sog.GetObject("Facebook","Status", me)
	print "- Done!"
	
	print "Retrieving your photo albums..."
	albums = expBuilder.sog.GetObject("Facebook","Album", me)
	print "- Done!"
	
	print "Populating photo albums..."
	for album in albums.objects:
		album = expBuilder.sog.GetObject("Facebook","Photo", album)
	print "- Done!"
	
	print "Retrieving photos of you..."
	photos_of = expBuilder.sog.GetObject("Facebook","Photo", me)
	print "- Done!"
	
	print "Retrieving your check-ins..."
	checkins = expBuilder.sog.GetObject("Facebook","Checkin", me)
	print "- Done!"
	
	print "Finished retrieving data from Facebook. \n"
	
	# Pick some information to display.
	first_name = unicode(person_obj.firstName)
	last_name = unicode(person_obj.lastName)
	profile_pic = unicode(person_obj.image.fullImage)
	rand_photo = unicode(random.choice(photos_of.objects).image.fullImage)
	rand_band = unicode(random.choice(fav_music.objects).displayName)
	rand_place = random.choice(checkins.objects)
	print checkins.objects
	print "*****"
	print unicode(rand_place)
	rand_album = random.choice(albums.objects)
	rand_upload = unicode(random.choice(rand_album.photos.objects).image.fullImage)
	
	print "Your name: " + first_name + " " + last_name
	print "Your current profile picture: " + profile_pic
	print "Random photo of you: " + rand_photo
	print "You like: " + rand_band
	print "You've been at " + str(rand_place.location.displayName) + " recently with around " + str(len(rand_place.tags.objects)) + " people"
	print "Random album you've uploaded: " + rand_album.displayName
	print "Random image from that album: " + rand_upload
	
	print "\n-----"
	print "End experiment"
	print "-----"
	

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

