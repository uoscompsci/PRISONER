Writing your first experiment
=============================

Now that you have a PRISONER development server up and running, we are going to
write a simple experiment which collects some data from a participant's Facebook
account, sanitises it, and displays it in the browser.

Prerequisites
-------------
This tutorial shows an experiment being written in Python, but as this is
to only demonstrate how to use the PRISONER web service, this can be easily
adapted to any other environment.

This example requires a Facebook account to test, and assumes you are registered
as a `Facebook developer <https://developers.facebook.com>`_.

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
   
So, what does this policy do?
