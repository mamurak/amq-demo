from __future__ import print_function

from argparse import ArgumentParser
from datetime import datetime
import logging
from time import sleep

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def read_arguments():
    log.debug('Reading arguments.')
    parser = ArgumentParser()
    parser.add_argument('--connection_url')
    parser.add_argument('--message_count', type=int, default=0)
    parser.add_argument('--frequency', type=float, default=2.)
    parser.add_argument('--address', default='myqueue')
    arguments = parser.parse_args()
    return arguments


class SendHandler(MessagingHandler):
    def __init__(self, conn_url, address, frequency, message_count):
        super(SendHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address
        self.frequency = float(frequency)
        self.message_count = int(message_count)

    def __str__(self):
        self_string =(
            f'<SendHandler(connection_url: {self.conn_url}, '
            f'address: {self.address}, frequency: {self.frequency}, '
            f'message_count: {self.message_count})>'
        )
        return self_string

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        # To connect with a user and password:
        # conn = event.container.connect(self.conn_url, user="<user>", password="<password>")

        event.container.create_sender(conn, self.address)

    def on_link_opened(self, event):
        log.info(f"SEND: Opened sender for target address '{event.sender.target.address}'")

    def on_sendable(self, event):
        if self.message_count == 0:
            while True:
                self.send_once(event)
        else:
            for i in range(self.message_count):
                self.send_once(event)

        event.sender.close()
        event.connection.close()

    def send_once(self, event):
        message = Message(generate_message_content())
        event.sender.send(message)
        print(f"SEND: Sent message '{message.body}'")
        event.sender.close()
        sleep(1./self.frequency)



def generate_message_content():
    now = datetime.now()
    return f"It's {now.ctime()}. That's {now.timestamp()} after T0."


def produce_messages(connection_url, address, frequency, message_count):
    handler = SendHandler(
        connection_url,
        address,
        frequency,
        message_count,
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
            arguments.message_count,
        )
    except KeyboardInterrupt:
        pass
