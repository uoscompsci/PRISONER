Running the PRISONER demo
=========================

This tutorial helps you launch a Docker container with a self-contained instance of PRISONER and a demo web application which demonstrates how to use its basic functionality.

Prerequisites
-------------

Facebook app
````````````
The PRISONER demo uses data from Facebook. To run this demo, you will need to have a Facebook account to test the experiment with, be a registered Facebook developer, and create an app which PRISONER can use to make authenticated requests to the PRISONER API. Please follow these steps:

* Visit https://developers.facebook.com and follow the steps to register as a developer, if you have not done so before.
* From the navigation bar, click "My Apps > Add a new app > Website".
* Provide a name for your experiment, such as "PRISONER Demo". The name you choose here is not significant.
* Click "Skip quick start", then go to the "Settings" page. Enter "localhost" as the Site URL and App Domains.
* At the top of the screen, note the App ID and App Secret for this app. You will need to provide these to PRISONER later.

Docker
``````
You will need to be running `Docker <https://www.docker.com>`_ to run the demo container. The Docker site provides guides to getting started for your platform.

Start the Docker container
--------------------------


From the command line, run the following to download the Docker image for the PRISONER demo and start the container::

  docker run -i -t -p 9000:9000 -p 5000:5000 --name prisoner-demo lhutton/prisoner-demo

If your /etc/resolv.conf points to 127.0.0.1 (default on Ubuntu installs since 12.04) Docker will try to use public DNS to resolve domains. In some configurations, this might not work (if you receive "Name or service not known" errors when trying to use this experiment, this is probably the cause), in which case you will need to manually provide a nameserver by running the container as follows:

 docker run -i -t -p 9000:9000 -p 5000:5000 -dns [YOUR_NAMESERVER_HERE] --name prisoner-demo lhutton/prisoner-demo

Running the demo
----------------
When the container starts, you will be prompted to enter the Facebook App ID and secret you noted earlier. Then, you will be given a URL to visit to start testing the experiment.

This demo shows the workflow of a trivial experiment which collects some data from your Facebook profile, and displays it in the browser. You can run this experiment to make sure that the PRISONER instance is working. You will see how PRISONER provides the bootstrapping interface to the experiment, showing some basic information about how the experiment works, and the process of authenticating with Facebook.

To view and edit the underlying files, you will need to open a shell on the Docker container::

 docker exec -it prisoner-demo /bin/bash

You can look at how the demo is implemented by visiting /usr/bin/prisoner-demo. "demo.py" implements the server for the web experiment, and shows how the PRISONER session is instantiated, and how Facebook data are collected and displayed. In "static/policy/design.xml" you can see the privacy policy which constrains this experiment. If you are not familiar with the role of the policy, consider reviewing the "Writing your first experiment" tutorial. This container includes vim for editing text files (TODO: include a simpler text editor too)

Modifying the demo
------------------
We can see how trivial modifications to the policy affect the execution of the experiment. For example, when you tried this experiment, you will have seen that your name was displayed, but not your politics Moreover, note that few users were associated with Likes ex- plicitly revealing their attributes. For example, less than 5% of users labeled as gay were connected with explicitly gay groups, such as No H8 Campaign, “Being Gay,” “Gay Marriage,” “I love Being
Fig. 4. Accuracy of selected predictions as a function of the number of available Likes. Accuracy is expressed as AUC (gender) and Pearson’s corre- lation coefficient (age and Openness). About 50% of users in this sample had at least 100 Likes and about 20% had at least 250 Likes. Note, that for gender (dichotomous variable) the random guessing baseline corresponds to an AUC = 0.50.
Prediction accuracy of regression for numeric attributes and traits expressed by the Pearson correlation coefficient between predicted and ac- tual attribute values; all correlations are significant at the P < 0.001 level. The transparent bars indicate the questionnaire’s baseline accuracy, expressed in terms of test–retest reliability.
￼5804 | www.pnas.org/cgi/doi/10.1073/pnas.1218772110
Kosinski et al.
￼Gay,” “We Didn’t Choose To Be Gay We Were Chosen.” Con- sequently, predictions rely on less informative but more popular Likes, such as “Britney Spears” or “Desperate Housewives” (both moderately indicative of being gay).and religion, even if you have provided this in your Facebook profile. In demo.py we make a request to the PRISONER API for a "User" object in our on_get() method, which retrieves a user's biographical attributes, so why are these missing? If we turn to policy.xml, we can see why. Note that in the policy element, we enumerate the gender, first name, and last name attributes, which we have "retrieve" policies for. This provides a whitelist of the data we can collect, so let's add the following religion and politics clauses after the "last name" attribute policy:

.. code-block:: xml

   <attribute type="religion">
   <attribute-policy allow="retrieve" />
   </attribute>

   <attribute type="politicalViews">
   <attribute-policy allow="retrieve" />
   </attribute>

If you now revisit the website for the demo experiment, and continue through the PRISONER bootstrap process, you will note that PRISONER automatically detects the changes to the policy and requests the appropriate additional Facebook permissions. Now, the missing attributes will be visible on the experimental results page.

Similarly, you can modify any other aspect of this demo to see how you can request different types of data. To understand the data you can collect from Facebook using PRISONER, consult the documentation for the Facebook Service Gateway.
