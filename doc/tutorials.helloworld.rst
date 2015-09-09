Writing your first experiment
=============================

**Please note, this tutorial is a work-in-progress and not complete. In the
meantime, we recommend reviewing the :doc:`PRISONER demo </tutorials.demo>` for
an understanding of how to build a simple experiment.**

Now that you have a PRISONER development server up and running, we are going to
write a simple experiment which collects some data from a participant's Facebook
account, sanitises it, and displays it in the browser.

Prerequisites
-------------
This tutorial shows an experiment being written in Python, but as this is
to only demonstrate how to use the PRISONER web service, this can be easily
adapted to any other environment. This guide assumes a working understanding of
XML files.

This example requires a Facebook account to test, and assumes you are registered
as a `Facebook developer <https://developers.facebook.com>`_. You will need to
create a Facebook app, and make a note of its App ID and Secret. A short guide
to doing this is available in our :doc:`demo tutorial </tutorials.demo>`.

In this tutorial
----------------
PRISONER experiments consist of three elements, which we will introduce and
develop during this tutorial:

* Your experimental application

* An XML privacy policy

* An XML experimental design

Privacy policies
----------------
Privacy policies are XML documents which outline the types of data your
experiment needs to collect or publish to social network sites. They contain
rules that place constraints on how your experiment handles data.
For a given type of data (for example, a tweet, or a Facebook user profile),
the policy answers the following questions:

* Is my experiment able to handle this data type?

* Can my experiment retrieve, store, or publish this data type, or a combination of these?

* Under which conditions can I retrieve, store, or publish this data type?

* Which attributes of this data type can my experiment retrieve, store, or publish?

* Which attributes need to be sanitised as they are retrieved, stored, or published?

Encoding this information in a policy file yields some advantages from both
ethical and reproducibility perspectives:

*  Policies can be written "offline" before you write any code. This allows you
   to iterate on the appropriate data-handling strategy for your experiment,
   including engagement with IRB or ethics boards, until you arrive at a final
   set of constraints for your experiment.

* PRISONER enforces this policy at runtime, so that if the experimental code you are writing attempts to violate its constraints, you cannot inadvertently collect more data than needed for your experiment.

*  The standardised representation of the policy allows other documents to be
   automatically and consistently generated, such as consent forms for
   participants which reflect the actual data-handling practices of a study, or
   human-readable summaries of the study's design for review by IRB or ethics
   boards.

*  Privacy policies are effectively a workflow standard for social network
   experiments, and allow the protocols for studies to be shared. While ideally
   coupled with the underlying experimental code to support full reproducibility
   of experiments, the platform-agnostic nature of the privacy policy allows
   other researchers to replicate a study under the same constraints, even if
   they are not using PRISONER.

Writing the privacy policy
``````````````````````````
Outside of the PRISONER directory, create a directory to store your experiment
application. In there, create a new file called policy.xml. Populate it with the following:

.. literalinclude:: code/tutorials.helloworld.policy.xml
   :language: xml

So, what does this policy do? Simply, it enumerates the objects we can collect,
and the attributes of those objects we can collect. The policy file includes a
clear hierarchy where we define policy elements for each data type, which
contains a collection of attributes we can process, and an object-policy which
describes the criteria under which we can collect objects of this type. In this
experiment, we want to collect some biographical information about the
participant in this experiment, so our policy is for the User object provided by
Facebook. The Facebook prefix defines the namespace, which means we are
explicitly requesting Facebook's representation of a User, and is not
generalisable to the other social network sites that PRISONER supports. This
means we can access Facebook-specific attributes, but at the cost of making our
experiment harder to adapt for other services. Because we only want to collect
data about the current participant, we provide an object-policy which dictates
that we can only collect a User object if it matches the ID of the participant.
This ensures our experiment can not inadvertently collect more sensitive data
than we need, such as the identitfy of the participant's friends. Although we
now have criteria for collecting the objects themselves, the objects PRISONER
returns will have no attributes. Therefore, we must specifically enumerate the
attributes we need in the attributes collection of this policy. Each policy
element enables us to retrieve that attribute. We could add additional
attribute-policy elements for each attribute to also enable us to store those
attributes if we later wish to persist these data, but this is not necessary for
this experiment.

Later, when we write the experimental application, we will provide PRISONER with this policy to initialise the experiment and allow these constraints to be enforced.

Experimental designs
----------------
Experimental design files provide PRISONER with basic metadata about your
experiment, such as its name, properties for specific services such as API keys, and the structure of any data you wish to store so PRISONER can manage the database appropriately. 

Writing the experimental design
``````````````````````````````
In the same directory where you wrote your privacy policy, add another file
called design.xml, and populate it with the following:

.. literalinclude:: code/tutorials.helloworld.design.xml
   :language: xml

What does this design do? First of all, note that in the tables element, we
specify two tables. The first is marked as a "participant" table, which
indicates to PRISONER that the table stores metadata about individual
participants. This allows PRISONER's internal record of an individual
participant, including their service-specific session identifiers, to be related
to the metadata that is specific to your experiment. In this case, we identify
participants by their email address.

Our second table is marked as a "response" table, which lets PRISONER know that
data collected during the course of an experiment can be stored here. For the
purposes of this tutorial, we will store the participant's Facebook profile
along with our identifier for that participant. 

The schema we have provided here does not directly translate to the underlying
database which PRISONER will instantiate on our behalf. The "mapTo" syntax in
our response table means PRISONER will store the representation of a Facebook
profile in a metatable, which individual response records will be related to.
Rather than directly accessing the database, PRISONER recommends you use its
persistence API to store responses and retrieve them, with fully-formed social
objects returned as part of the response, where appropriate. 

Finally, we provide some properties, or "props", which provide miscellaneous
metadata PRISONER needs to provide your experiment. Because we are using
Facebook, we must provide the App ID and secret for our app which we noted
earlier, so make sure you edit the file with these values as appropriate.
Finally, we provide a PRISONER secret. This is a passphrase which you will
provide to PRISONER whenever you make administrative commands, such as
initialising an experiment, to make sure you are authorised to do this.


