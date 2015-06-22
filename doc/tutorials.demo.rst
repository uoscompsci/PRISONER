Running the PRISONER demo
========================

This tutorial helps you launch a Docker container with a self-contained instance of PRISONER and a demo web application which demonstrates how to use its basic functionality.

Prerequisites
----------------

Facebook app
````````````
The PRISONER demo uses data from Facebook. To run this demo, you will need to have a Facebook account to test the experiment with, and you will need to be a registered Facebook developer, and create an app which PRISONER can use to make authenticated requests to the PRISONER API.

If you are already familiar with the Facebook Developers interface, please create a new application, and note its App ID and App Secret, as you will need to provide PRISONER with these details when you start the demo application. In addition, please add "localhost" as an App Domain and Site URL under the app's settings.

If you are not familiar with creating Facebook apps, please follow these steps:

* Visit https://developers.facebook.com and follow the steps to register as a developer, if you are not already registered.
* From the navigation bar, click "My Apps > Add a new app > Website".
* Provide a name for your experiment, such as "PRISONER Demo". The name you choose here is not significant.
* Click "Skip quick start", then go to the "Settings" page. Enter "localhost" as the Site URL and App Domains.
* At the top of the screen, note the App ID and App Secret for this app. You will need to provide these to PRISONER later.

Docker
``````
You will need to be running `Docker<https://www.docker.com>`_ to run the demo container. The Docker site provides guides to getting started for your platform.

Start the Docker container
------------------------

From the command-line, run the following to download the Docker image for the PRISONER demo and start the container:

  docker run -p 9000:9000 -p 5000:5000 --name prisoner-demo lhutton/prisoner-demo

You will be prompted to enter the Facebook App ID and secret from the previous step. Then, you will be given a URL to visit to start testing the experiment.

Running the demo
----------------
This demo shows the workflow of a trivial experiment which collects some data from your Facebook profile, and displays it in the browser. You can run this experiment to make sure that the PRISONER instance is working. You will see how PRISONER provides the bootstrapping interface to the experiment, showing some basic information about how the experiment works, and the process of authenticating with Facebook. You can look at how the demo is implemented by visiting /usr/bin/prisoner-demo. "demo.py" implements the server for the web experiment, and shows how the PRISONER session is instantiated, and how Facebook data are collected and displayed. In "static/policy/design.xml" you can see the privacy policy which constrains this experiment. If you are not familiar with the role of the policy, consider reviewing the "Writing your first experiment" tutorial.

Modifying the demo
-----------------
We can see how trivial modifications to the policy affect the execution of the experiment. For example, when you tried this experiment, you will have seen that your name was displayed, but not your politics and religion, even if you have provided this in your Facebook profile. In demo.py we make a request to the PRISONER API for a "User" object in our on_get() method, which retrieves a user's biographical attributes, so why are these missing? If we turn to policy.xml, we can see why. Note that in the policy element, we enumerate the gender, first name, and last name attributes, which we have "retrieve" policies for. This provides a whitelist of the data we can collect, so let's add the following religion and politics clauses after the "last name" attribute policy:

 <attribute type="religion">
 <attribute-policy allow="retrieve" />
 </attribute>

 <attribute type="politicalViews">
 <attribute-policy allow="retrieve" />
 </attribute>
 </attributes>

If you now revisit the website for the demo experiment, and continue through the PRISONER bootstrap process, you will note that PRISONER automatically detects the changes to the policy and requests the appropriate additional Facebook permissions. Now, the missing attributes will be visible on the experimental results page.
