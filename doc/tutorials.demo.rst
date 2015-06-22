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
