"""
PRISONER Dummy Participation client

This is designed to be evokable from the cmdline etc. as a way of testing
various features of PRISONER.
If its various bits work, it's a good indication you've set it up right.
"""

import SocialObjects
from gateway import LastfmServiceGateway


if __name__ == "__main__":
	lfm = LastfmServiceGateway()
	img = SocialObjects.Image()
	img.author = "Me"
	print img.author
