import os

from send import produce_messages


def main():
    connection_url = os.environ['BROKER_CONNECTION_URL']
    address = os.environ['MESSAGE_ADDRESS']
    frequency = os.environ['FREQUENCY']

    produce_messages(connection_url, address, frequency)


if __name__ == '__main__':
    main()
