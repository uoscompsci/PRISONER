Running the PRISONER demo
=========================

This tutorial helps you launch a Docker container with a self-contained instance
of PRISONER and a demo web application which demonstrates how to use its basic
functionality, connecting to Facebook and Twitter.

Prerequisites
-------------
The PRISONER demo uses data from Facebook and Twitter. To run this demo, you
will need to have Facebook and Twitter accounts to test the experiment with, be a
registered Facebook and Twitter developer, and create an app for both services
which PRISONER can use to make authenticated requests to the appropriate API.

Facebook app
````````````
Please follow these steps to create a Facebook app:

* Visit https://developers.facebook.com and follow the steps to register as a developer, if you have not done so before.
* From the navigation bar, click "My Apps > Add a new app > Website".
* Provide a name for your experiment, such as "PRISONER Demo". The name you choose here is not significant.
* Click "Skip quick start", then go to the "Settings" page. Enter "localhost" as the Site URL and App Domains.
* At the top of the screen, note the App ID and App Secret for this app. You will need to provide these to PRISONER later.

Twitter app
```````````
Please follow these steps to create a Twitter app:

* Visit https://dev.twitter.com and click "Manage Your Apps" in the footer.
* Click "Create new app" and provide the required details.
* The "Callback URL" most be a non-empty value. As PRISONER dynamically provides
a callback, the callback given here is irrelevant. For example, you can supply
your homepage or http://prisoner.cs.st-andrews.ac.uk
* Click "Create your Twitter application".
* Go to the "Keys and access tokens" tab and make a note of the API key and
secret, which you will need later.

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
When the container starts, you will be prompted to enter the Facebook and
Twitter App IDs and secrets you noted earlier. Then, you will be given a URL to visit to start testing the experiment.

This demo initially shows the workflow of a trivial experiment which collects
some data from your Facebook profile, and displays it in the browser. You can run this experiment to make sure that the PRISONER instance is working. You will see how PRISONER provides the bootstrapping interface to the experiment, showing some basic information about how the experiment works, and the process of authenticating with Facebook.

To view and edit the underlying files, you will need to open a shell on the Docker container::

 docker exec -it prisoner-demo /bin/bash

You can look at how the demo is implemented by visiting /usr/bin/prisoner-demo. "demo.py" implements the server for the web experiment, and shows how the PRISONER session is instantiated, and how Facebook data are collected and displayed. In "static/policy/design.xml" you can see the privacy policy which constrains this experiment. If you are not familiar with the role of the policy, consider reviewing the "Writing your first experiment" tutorial. This container includes vim for editing text files (TODO: include a simpler text editor too)

Modifying the demo
------------------
We can see how trivial modifications to the policy affect the execution of the
experiment. For example, when you tried this experiment, you will have seen that
your name was displayed, but not your politics and religion, even if you have
provided this in your Facebook profile. In demo.py we make a request to the PRISONER API for a "Person" object in our on_get() method, which retrieves a user's biographical attributes, so why are these missing? If we turn to policy.xml, we can see why. Note that in the policy element, we enumerate the gender, first name, and last name attributes, which we have "retrieve" policies for. This provides a whitelist of the data we can collect, so let's add the following religion and politics clauses after the "last name" attribute policy:

.. code-block:: xml

   <attribute type="religion">
   <attribute-policy allow="retrieve" />
   </attribute>

   <attribute type="politicalViews">
   <attribute-policy allow="retrieve" />
   </attribute>

If you now revisit the website for the demo experiment, and continue through the PRISONER bootstrap process, you will note that PRISONER automatically detects the changes to the policy and requests the appropriate additional Facebook permissions. Now, the missing attributes will be visible on the experimental results page.

Similarly, you can modify any other aspect of this demo to see how you can request different types of data. To understand the data you can collect from Facebook using PRISONER, consult the documentation for the Facebook Service Gateway.

So far, we have shown we can collect different types of data from Facebook. Now,
let's change the experiment completely to collect data from Twitter instead.
This might sound like an arduous task, but we can do this by changing a single
line of code. Return to /usr/bin/prisoner-demo/demo.py and find line 28, which
currently indicates Facebook is our social network of choice. Change this to
read "Twitter" and save the file. Return to the URL for the experiment and run
through it one more time. Note that PRISONER now authenticates you with Twitter
instead, and instead of seeing Facebook's status updates, you see a list of your
recent tweets. How is this possible? PRISONER provides a consistent API for
requesting equivalent types of data from different services. Therefore, just by
changing the name of the provider, we can collect data from a completely
different service, while maintaining all other parameters of the experiment. 

If you return to the policy.xml we've edited already, you might notice we don't
even have a policy for Twitter. While we have explicit Facebook policies to
collect attributes such as "gender" or "likes" which are Facebook-specific, we
have "base" policies which only refer to the common attributes in all base
social objects. Instead of matching the author on the Facebook session ID, we
use a special object, "session:Service.id" which allows us to authenticate with
whatever the current data provider is, allowing us to re-use a policy for any
service, including ones which don't exist yet. Only if we required
Twitter-specific attributes would we need to write an explicit Twitter policy.

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

What did this do? The "store" object-policy tells PRISONER we can now store
objects of the type Facebook:Person, so long as it matches the current
participant, while the two "store" attribute-policies only allow us to store these attributes.

Let's reload the experiment, and try to save the object again. This time, you should be told this was successful. But what can we do with these data? Let's go back to our shell on the Docker container and run the following::

 sqlite3
 .open /tmp/prisoner_demo.db
 SELECT * from response;

Here you will see a JSON representation of the Person object we just saved. Note
that the attributes, such as religion and gender, have been nullified, while the name is still visible. From here, we can run our own analyses on these results, or share the SQLite database with others.



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
