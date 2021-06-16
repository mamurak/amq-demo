FROM registry.access.redhat.com/ubi8/python-39

RUN pip3 install python-qpid-proton

ENV BROKER_CONNECTION_URL="tcp://localhost:61616"
ENV MESSAGE_ADDRESS="myqueue"
ENV FREQUENCY="2.0"
ENV MESSAGE_COUNT="0"

ADD *.py ./

CMD ["python3", "main.py"]
