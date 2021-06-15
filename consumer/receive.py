from __future__ import print_function

from argparse import ArgumentParser
import logging

from proton.handlers import MessagingHandler
from proton.reactor import Container


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def read_arguments():
    log.debug('Reading arguments.')
    parser = ArgumentParser()
    parser.add_argument('--connection_url')
    parser.add_argument('--address', default='myqueue')
    arguments = parser.parse_args()
    return arguments


class ReceiveHandler(MessagingHandler):
    def __init__(self, conn_url, address):
        super(ReceiveHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address

    def __str__(self):
        self_string =(
            f'<ReceiveHandler(connection_url: {self.conn_url}, '
            f'address: {self.address})>'
        )
        return self_string

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        # To connect with a user and password:
        # conn = event.container.connect(self.conn_url, user="<user>", password="<password>")

        event.container.create_receiver(conn, self.address)

    def on_link_opened(self, event):
        print(f"RECEIVE: Created receiver for source address '{self.address}'")

    def on_message(self, event):
        message = event.message

        print(f"RECEIVE: Received message '{message.body}'")


def consume_messages(connection_url, address):
    handler = ReceiveHandler(connection_url, address)
    log.info(f'Created {handler}.')
    container = Container(handler)
    container.run()


if __name__ == "__main__":
    try:
        arguments = read_arguments()        
        consume_messages(arguments.connection_url, arguments.address)
    except KeyboardInterrupt:
        pass
