## PRISONER Version 0.2.2 (May 18, 2015)

### Bug fixes

* Facebook Service Gateway now calls /tagged_places rather than /locations to
 get checkins.


## PRISONER Version 0.2.1 (May 15, 2015)

### New features

* PRISONER can now be deployed as a Docker container. Assuming the image is
available from the Docker registry run the following:
```
docker run -it --rm -P --name prisoner lhutton/prisoner
```

* Experimental designs must now include a "secret" prop for "PRISONER". This
should be a secure passphrase. When making
requests to administrative endpoints, such as /begin, /register, or /schema, an
additional parameter must be provided: secret, which matches this value. If this
does not match the secret in the design, the request will be rejected. This
ensures that such requests are only made by the experiment administrator. For
added security, make sure your experimental design is not in a URL known to
participants.

* Experiment response databases can now be created via the web service. A new
endpoint, /schema, expects a form including a policy, design, secret and db
attributes (as when calling /register). This will build the corresponding
schema, and will delete any data in that database already.

### Bug fixes

* Old hard-coded paths removed
* Experimental design XSD now handles props correctly
* PersistenceManager parses props correctly
* FacebookServiceGateway no longer tries to request deprecated permissions
* request_handler in ServiceGateways now passes through operation and payload



##  PRISONER Version 0.2 (April 30, 2015)

### New features

* Service Gateways can now receive properties (props) from experiments, by
including prop
elements in the experimental design file. These are passed as a dictionary to
the service gateway to provide service-specific metadata to gateways, such as
API keys. Service Gateways should now expect a props dictionary in their
__init__ method (this will be empty if no props were passed).

* Setting a debug==true prop for "PRISONER" in the experimental design enables
the display of developer-friendly error messages. This should not be used in
production, as it may reveal sensitive data or details about your experiment.

* Service gateways must now implement a request_handler() method. This
receives a callable for the request which should be evoked and returned. This
allows service gateways to inject additional data into each response, such as debug headers.

* Facebook service gateway now requires app_id, app_secret and api_version
props. This app will make PRISONER requests for Facebook data, so make sure
login review has been completed before any Facebook experiments go public. Only
api_version==2.0 is supported.

* Facebook service gateway now uses version 2.0 of the Graph API. None of the
new features of this version are incorporated yet, apart from the new Login flow
but all breaking changes in 2.0 have been incorporated without the service
gateway API changing. The /Friends endpoint  now only provides a list of the
participant's friends who also use the experiment app.

* Service gateways are now provided with a PolicyProcessor instance when
initialised, as a policy parameter. This allows the policy of an experiment to
be interrogated by a ServiceGateway. This is NOT necessary for service
gateways to function, but can be used for debugging purposes.

* Facebook service gateway now provides a list of the Facebook permissions an
experiment requires. This is returned as a PRISONER-FB-Permissions header in
each request if a debug==true prop is set in the experimental design (note
this is separate from setting a global debug prop as above).

* HTTPS is now required for the PRISONER web service. Ensure your client is
correctly configured as PRISONER is no longer available over HTTP.
