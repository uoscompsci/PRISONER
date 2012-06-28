import sys, os
sys.path.append(os.path.dirname(__file__)
sys.path.append('/home/lhutton/prisoner/prisoner')

from server import *

application = create_app()
