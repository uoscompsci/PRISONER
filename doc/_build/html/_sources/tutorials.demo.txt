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

If you are using boot2docker, for example if you are running OS X, you should run the following commands to correctly map the ports to the VirtualBox VM. If you are running Docker natively on Linux, you do not need to do this::

 VBoxManage controlvm boot2docker-vm natpf1 "prisoner,tcp,127.0.0.1,5000,,5000"
 VBoxManage controlvm boot2docker-vm natpf1 "demo,tcp,127.0.0.1,9000,,9000"

To avoid port conflicts after using the Docker container, you should run the following when you're done::

 VBoxManage controlvm boot2docker-vm natpf1 delete prisoner
 VBoxManage controlvm boot2docker-vm natpf1 delete demo

From the command line, run the following to download the Docker image for the PRISONER demo and start the container::

  docker run -i -t -p 9000:9000 -p 5000:5000 --name prisoner-demo lhutton/prisoner-demo

If your /etc/resolv.conf points to 127.0.0.1 (default on Ubuntu installs since 12.04) Docker will try to use public DNS to resolve domains. In some configurations, this might not work (if you receive "Name or service not known" errors when trying to use this experiment, this is probably the cause), in which case you will need to manually provide a nameserver by running the container as follows::

 docker run -i -t -p 9000:9000 -p 5000:5000 --dns=[YOUR_NAMESERVER_HERE] --name prisoner-demo lhutton/prisoner-demo

Running the demo
----------------
When the container starts, you will be prompted to enter the Facebook App ID and secret you noted earlier. Then, you will be given a URL to visit to start testing the experiment.

This demo shows the workflow of a trivial experiment which collects some data from your Facebook profile, and displays it in the browser. You can run this experiment to make sure that the PRISONER instance is working. You will see how PRISONER provides the bootstrapping interface to the experiment, showing some basic information about how the experiment works, and the process of authenticating with Facebook.

To view and edit the underlying files, you will need to open a shell on the Docker container::

 docker exec -it prisoner-demo /bin/bash

You can look at how the demo is implemented by visiting /usr/bin/prisoner-demo. "demo.py" implements the server for the web experiment, and shows how the PRISONER session is instantiated, and how Facebook data are collected and displayed. In "static/policy/design.xml" you can see the privacy policy which constrains this experiment. If you are not familiar with the role of the policy, consider reviewing the "Writing your first experiment" tutorial. This container includes vim for editing text files (TODO: include a simpler text editor too)

Modifying the demo
------------------
We can see how trivial modifications to the policy affect the execution of the experiment. For example, when you tried this experiment, you will have seen that your name was displayed, but not your politics and religion, even if you have provided this in your Facebook profile. In demo.py we make a request to the PRISONER API for a "User" object in our on_get() method, which retrieves a user's biographical attributes, so why are these missing? If we turn to policy.xml, we can see why. Note that in the policy element, we enumerate the gender, first name, and last name attributes, which we have "retrieve" policies for. This provides a whitelist of the data we can collect, so let's add the following religion and politics clauses after the "last name" attribute policy:

.. code-block:: xml

   <attribute type="religion">
   <attribute-policy allow="retrieve" />
   </attribute>

   <attribute type="politicalViews">
   <attribute-policy allow="retrieve" />
   </attribute>

If you now revisit the website for the demo experiment, and continue through the PRISONER bootstrap process, you will note that PRISONER automatically detects the changes to the policy and requests the appropriate additional Facebook permissions. Now, the missing attributes will be visible on the experimental results page.

Similarly, you can modify any other aspect of this demo to see how you can request different types of data. To understand the data you can collect from Facebook using PRISONER, consult the documentation for the Facebook Service Gateway.

Saving data
-----------
When running an experiment, we usually want to save some data, which might take the form of some data we collected from a social network site, coupled with data provided by a participant, such as questionnaire responses. PRISONER provides a mechanism for saving data that works similarly to retrieving data from services. It ensures we can only store the data that we absolutely need for our experiment, and can help us apply any sanitisations to remove unnecessarily sensitive data before they are stored, while maintaining as association with additional data provided by participants during the course of an experiment.

We can test this by clicking the "Store this user profile" button, which will save the user profile object we summarise at the top of the screen to the database which PRISONER initialised when we started the experiment.

However, when we click this, we get an error. Why? Just like retrieving data, our policy needs to enable storing social objects on a per-object, and per-attribute basis. Let's quickly amend our policy.xml file to let us save the name attributes of our user object, but not religion and politics. Within both the firstName and lastName elements, where we already have a "retrieve" attribute-policy, add the following:

.. code-block:: xml

 			<attribute-policy allow="store" />

Then, after the "retrieve" object-policy, add the following:

.. code-block:: xml

   <object-policy allow="store">
   <object-criteria>
    <attribute-match match="author.id" on_object="session:Facebook.id" />
   </object-criteria>
  </object-policy>

What did this do? The "store" object-policy tells PRISONER we can now store objects of the type Facebook:User, so long as it matches the current participant, while the two "store" attribute-policies only allow us to store these attributes.

Let's reload the experiment, and try to save the object again. This time, you should be told this was successful. But what can we do with these data? Let's go back to our shell on the Docker container and run the following::

 sqlite3
 .open /tmp/prisoner_demo.db
 SELECT * from response;

Here you will see a JSON representation of the User object we just saved. Note that the attributes, such as religion and gender, have been nullified, while the name is still visible. From here, we can run our own analyses on these results, or share the SQLite database with others.



Packaging the modified demo
---------------------------
Now that we've made these changes, perhaps we want to package up the changes we've made, including our now-populated database, so others can reproduce our version of the experiment or run analyses with our results. Docker allows us to commit the changes we've made within a container and build a new image from that, which we can use to restore the state of this container at any time, or share with others. To do this, run the following::

 docker commit prisoner-demo [YOUR_NAME]/prisoner-demo-mod

Now, if you run::

 docker images

You will see prisoner-demo-mod among your cached images. From here, you could publish this to Docker Hub to make it publicly visible::

  docker push [YOUR_NAME]/prisoner-demo-mod

Then, anyone else can pull and run your image, or you can simply run this container later as above, by running::

   docker run -i -t -p 9000:9000 -p 5000:5000 --name prisoner-demo-mod lhutton/prisoner-demo-mod
