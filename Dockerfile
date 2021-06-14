FROM registry.access.redhat.com/ubi8/python-39

RUN pip3 install python-qpid-proton
ADD scripts/ scripts/

CMD sleep 10000000
