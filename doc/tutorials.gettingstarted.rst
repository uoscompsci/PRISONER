Installing PRISONER
===============

This tutorial helps you get up and running with a PRISONER instance.

Installing PRISONER for local development
-------------------

For developing experiments, you will probably want to run a PRISONER server locally on your development machine to quickly iterate. There are two ways to do
this: using our pre-prepared Docker VM image, or cloning the latest release from
GitHub.

Spin-up a Docker VM
`````````````````````````````
If you have familiarity with the Docker environment, using the PRISONER Docker
container is probably the easiest way to get up and running without having to
worry about your environment and resolving dependencies. We have an image in Docker Hub which includes the latest release from our GitHub repository.

This guide assumes you have installed Docker and are familiar with using it.

To spin-up a PRISONER instance, run the following at the command line::

 docker run -p 5000:5000 --name prisoner lhutton/prisoner

This will pull the prisoner image from the DockerHub registry, and its prerequisites, which may take several minutes then start an instance of the container.

Now, PRISONER's development server has started on port 5000. Test that
everything is working, and that Docker has correctly mapped the port by visiting
localhost:<mapped_port>, which should display a "Welcome to PRISONER" message.
Depending on your Docker configuration, you may have to
access the underlying VM via an alternative IP.


Clone from GitHub
`````````````````````````````

Prerequisites
~~~~~~~~~~
PRISONER should work on any platform which supports Python 2.7. PRISONER is not
compatible with Python 3.

Installing PRISONER
~~~~~~~~~~~~~~~~
PRISONER is developed openly, with all active development pushed to `GitHub
<https://github.com/uoscompsci/PRISONER>`_.
We recommend cloning `the latest release
<https://github.com/uoscompsci/PRISONER/releases>`_ rather than pulling from
head for
stability. From the directory where you cloned the repository, run the following
at the command line to install any dependencies::

 pip install -r requirements.txt

We strongly recommend running PRISONER from within a virtualenv to isolate
dependencies and avoid conflicts with your system Python configuration. See
`this guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ for more
information about setting up virtual environments.

From the PRISONER directory, run the following to start the local development server::

 python server/prisoner.wsgi

Make sure everything is working by visiting localhost:5000, where you should see
a "Welcome to PRISONER" message.

In the next tutorial, we cover writing your first PRISONER experiment.
