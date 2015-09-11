# Dockerfile for PRISONER Demonstration
# http://prisoner.cs.st-andrews.ac.uk

# Version 0.1
# Last updated June 10th 2015

FROM lhutton/prisoner
MAINTAINER Luke Hutton <lh49@st-andrews.ac.uk>
LABEL Description="This image prepares an environment for a trivial demonstration of PRISONER."

COPY ./ /usr/bin/prisoner-demo

EXPOSE 9000

CMD ["bin/bash","/usr/bin/prisoner-demo/start_demo.sh"]
