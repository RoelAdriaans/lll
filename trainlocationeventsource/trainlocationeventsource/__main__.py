import io
from gzip import GzipFile

import zmq


def main():
    print("Connect to ZeroMQ here")
    context = zmq.Context()

    #  Socket to talk to server
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://pubsub.besteffort.ndovloket.nl:7664")

    topicfilter = b"/RIG/NStreinpositiesInterface5"
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    multipart = socket.recv_multipart()
    address = multipart[0]
    contents = b"".join(multipart[1:])
    contents = GzipFile(fileobj=io.BytesIO(contents)).read()
    print("Address", address)
    print("GZIP", contents[:250])
    socket.close()
    context.term()


if __name__ == "__main__":
    raise SystemExit(main())
