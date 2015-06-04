.. PRISONER documentation master file, created by
   sphinx-quickstart on Thu Jun  4 11:17:31 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PRISONER
====================================

PRISONER is a framework for running ethical and reproducible social network
experiments.

PRISONER is actively under development, and has been released to help steer
its design, and to improve the consideration of these concerns in the community.

Features
--------
* A single consistent API to collect and publish data from supported social network sites

* Built-in support for Facebook, Twitter, and Last.fm with simple interfaces to add support for additional services

* Simplified API for sensitively storing data collected from social network sites along with responses to experimental interventions, with support for any database engine with `SQLAlchemy bindings <http://docs.sqlalchemy.org/en/rel_1_0/dialects/index.html>`_

* Declarative syntax for expressing the data collection requirements of an experiment to ensure only the data needed for an experiment can be collected.

* Built-in support for common sanitisations of sensitive data which can be invoked declaratively

* Includes tools to simplify the creation of Docker containers wrapping experiments along with an instance of PRISONER to support reproducibility of experiments


Currently in development
-------------------------
The following features are not yet ready for distribution, but will be
available in future releases. Please track progress on GitHub if you are
interested in contributing to these features.

* Automatic generation of consent forms based on the data-handling requirements of an experiment

* Improve the longevity of code by automatically mapping older API calls to newer API versions, gracefully degrading where individual calls can no longer be satisfied.

* Support the archiving of social network data and PRISONER workflows by generating metadata designed for ingest by research information systems.


What PRISONER is not
---------------------
PRISONER is not:

* a crawler. PRISONER is designed to support the execution of user studies which handle social network data, and is not designed for crawling or scraping data from these services where there is no direct intervention from a participant. As a rule of thumb, if your experiment would not require individual participants to authenticate your experiment to access data via their social network account, it is probably not the kind of experiment PRISONER can support.

* a tool for "anonymising" social network data. Guaranteeing the anonymity of identifiable data while maintaining utility is not a trivial problem. PRISONER's support for sanitisations is to coarsen sensitive data as they are collected, and is not intended for anonymising data before release.


If you have any issues deploying or using PRISONER, or have suggestions for how
to improve the framework, please raise an issue on GitHub. We would be delighted
if you would like to contribute code or improved documentation to PRISONER, and we will accept pull requests with test coverage.

This documentation includes tutorials to help you run a PRISONER instance,
build experiments which use social network data, and to package your
experiments such that others can reproduce them. A full API reference is
available, but familiarity with this is not required to use PRISONER.



Contents:

.. toctree::
   :maxdepth: 2

   tutorials
   prisoner



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
