Best practices for distributing PRISONER experiments
============================================

.. PRISONER is designed to make social network studies more reproducible, by
.. providing formats for encoding key information about the data-handling
.. constraints of your experiment. This guide outlines best
.. practices for sharing your PRISONER experiments with others. Please note, this
.. is a living document which does not cover all scenarios. If you have any
.. feedback or improvements, please raise an issue on GitHub or submit a pull
.. request.

.. Packaging your experiment
.. ---------------------
The reproducibility of your experiments is largely dependent on what you are
willing to share with the community. Placing your code in an archive online or
public version controlled repository, via GitHub for example, is a good way of
letting others examine and run your code.

This approach, however, has some limitations. Distributing software in this way
does not make it easy to resolve package dependencies, and if others are not
running the same operating system as you, or other environmental variables
differ, it may be difficult or impossible to execute your experiment.

Specifically, if you are developing a PRISONER experiment, you will need to
distribute your PRISONER policies, and someone hoping to execute your experiment
needs to be able to understand how to setup and run an instance of PRISONER to
get things working.

In this guide we cover some best practices for distributing PRISONER
experiments. Please note this guidance is not final and may not cover all
scenarios. We welcome
suggestions or improvements as GitHub issues or pull requests.