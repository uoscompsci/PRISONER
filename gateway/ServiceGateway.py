"""
PRISONER Service Gateway
========================

Abstract interface for PRISONER Service Gateways. Concrete implementations must
subclass this.
"""

class ServiceGateway(object):

        def __init__(self):
                pass

	""" Common interface for core Image Social Object """
	def Image(self, operation, payload): 
		raise NotImplementedError("Service Gateway does not support \
		Images")
