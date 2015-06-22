Running the PRISONER demo
========================

This tutorial helps you launch a Docker container with a self-contained instance of PRISONER and a demo web application which demonstrates how to use its basic functionality.

Pre-requisites
----------------

The PRISONER demo uses data from Facebook. To run this demo, you will need to have a Facebook account to test the experiment with, and you will need to be a registered Facebook developer, and create an app which PRISONER can use to make authenticated requests to the PRISONER API.

If you are already familiar with the Facebook Developers interface, please create a new application, and note its App ID and App Secret, as you will need to provide PRISONER with these details when you start the demo application. In addition, please add "localhost" as an App Domain and Site URL under the app's settings.

If you are not familiar with creating Facebook apps, please follow these steps:

* Visit <https://developers.facebook.com> and follow the steps to register as a developer, if you are not already registered.
* From the navigation bar, click "My Apps > Add a new app > Website".
* Provide a name for your experiment, such as "PRISONER Demo". The name you choose here is not significant.
* Click "Skip quick start", then go to the "Settings" page. Enter "localhost" as the Site URL and App Domains.
* At the top of the screen, note the App ID and App Secret for this app. You will need to provide these to PRISONER later.


Start the Docker container
------------------------
