## 0.2 (April 20, 2015)

### New features

* Service Gateways can now receive props from experiments, by including prop elements in the experimental design file. These are passed as a dictionary to the service gateway to provide service-specific metadata to gateways, such as API keys. Service Gateways should now expect a props dictionary in their __init__ method (this will be empty if no props were passed).

* Facebook service gateway now requires app_id, app_secret and api_version props. This app will make PRISONER requests for Facebook data, so make sure login review has been completed before any Facebook experiments go public. Only api_version==2.0 is supported.

* Facebook service gateway now uses version 2.0 of the API. None of the new features of this version are incorporated yet, apart from the new Login flow but all breaking changes in 2.0 have been incorporated without the service gateway API changing.

* Service gateways can now request the privacy policy of an experiment from...

* HTTPS is now required for the PRISONER web service. Ensure your client is correctly configured as any insecure requests will now be rejected.