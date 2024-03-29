"""Connect to the ndovloket ZeroMQ interface and listen to the
topic `RIG/NStreinpositiesInterface5`. This will then use the ServiceLayer to store
the events into a repository."""

import io
import json
import logging
import time
from collections.abc import Callable
from gzip import GzipFile

import xmltodict
import zmq

from trainlocationeventsource.service_layer import services, unit_of_work

logger = logging.getLogger(__name__)


class ZMQSubscriber:
    def __init__(self, connection_string: str):
        """Create a new ZMQSubscriber"""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.connection_string = connection_string

    def subscribe(self, topic: str):
        """Subscribe to a topic"""
        self.socket.connect(self.connection_string)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode())

    def handle_message(self, handler: Callable[[bytes], None]):
        try:
            while True:
                # Receive message from publisher
                address, content = self.socket.recv_multipart()
                handler(content)

        except zmq.ZMQError as e:
            logger.error("ZeroMQ error occurred: %s", e)
        finally:
            # Close the socket and terminate the ZeroMQ context
            self.socket.close()
            self.context.term()


def message_handler(content: bytes):
    contents = GzipFile(fileobj=io.BytesIO(content)).read()
    parsed = xmltodict.parse(contents.decode())
    json_data = json.dumps(parsed, indent=4)
    logger.info("Received json data: %s", json_data[:100])
    services.handle_nstreinpositie(parsed, unit_of_work.EventstoreDBUnitOfWork())


def main():
    # @TODO Get the URL from an env variable or config
    zmqsub = ZMQSubscriber("tcp://pubsub.besteffort.ndovloket.nl:7664")
    zmqsub.subscribe("/RIG/NStreinpositiesInterface5")

    while True:
        zmqsub.handle_message(message_handler)
        logger.info("Disconnected from ZeroMQ")
        time.sleep(3)
        logger.info("Retrying to connect")


if __name__ == "__main__":
    print("Starting ndovloket...")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    logger.info("Starting ndovloket entrypoint")
    raise SystemExit(main())
