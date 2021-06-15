import os

from receive import consume_messages


def main():
    connection_url = os.environ['BROKER_CONNECTION_URL']
    address = os.environ['MESSAGE_ADDRESS']

    consume_messages(connection_url, address)


if __name__ == '__main__':
    main()
