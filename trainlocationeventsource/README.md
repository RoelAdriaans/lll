# TrainLocationEventSource

This project connects to the freely available, best effort ZeroMQ interface of
the NDOV Loket. It subscribes to the topic `RIG/NStreinpositiesInterface5`.

Events on this topic are received in a gzipped format. The event is uncompressed,
expanded and the individual messages are then published again.

This topic is then pushed to a EvenstoreDB.

The goal of this daemon is to be as light and small as possible.

## Docker

Building the project:

```bash
DOCKER_BUILDKIT=1 docker build -t trainlocationeventsource --target=runtime .
```

Run the project:

```bash
docker run -it trainlocationeventsource
```
