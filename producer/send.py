from __future__ import print_function

from argparse import ArgumentParser
from datetime import datetime, fromtimestamp
import logging

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def read_arguments():
    log.debug('Reading arguments.')
    parser = ArgumentParser()
    parser.add_argument('--connection_url')
    parser.add_argument('--frequency', type=float, default=2.)
    parser.add_argument('--address', default='myqueue')
    arguments = parser.parse_args()
    return arguments


class SendHandler(MessagingHandler):
    def __init__(self, conn_url, address, frequency):
        super(SendHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address
        self.period = 1./float(frequency)
        self.sender = None

    def __str__(self):
        self_string =(
            f'<SendHandler(connection_url: {self.conn_url}, '
            f'address: {self.address}, period: {self.period}>'
        )
        return self_string

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        # To connect with a user and password:
        # conn = event.container.connect(self.conn_url, user="<user>", password="<password>")

        self.sender = event.container.create_sender(conn, self.address)
        self.container = event.reactor
        self.container.schedule(self.period, self)

    def on_link_opened(self, event):
        log.info(f"SEND: Opened sender for target address '{event.sender.target.address}'")

    def on_timer_task(self, event):
        if self.sender.credit:
            message = Message(generate_message_content())
            self.sender.send(message)
            print(f"SEND: Sent message '{message.body}'")

        self.container.schedule(self.period, self)


def generate_message_content():
    now = datetime.now()
    message_string = (
        f"It's {now.ctime()}. That's {now.timestamp()} "
        f"seconds after {fromtimestamp(0).date().isoformat()}."
    )
    return message_string


def produce_messages(connection_url, address, frequency):
    handler = SendHandler(
        connection_url,
        address,
        frequency,
    )
    log.info(f'Created {handler}.')
    container = Container(handler)
    container.run()


if __name__ == "__main__":
    try:
        arguments = read_arguments()
        produce_messages(
            arguments.connection_url,
            arguments.address,
            arguments.frequency,
        )
    except KeyboardInterrupt:
        pass
