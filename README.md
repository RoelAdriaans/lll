# Lipwig's Locomotion Ledger - LLL

This project is a hobby project to find out if we have traveled in this train beofore. It consists of multiple parts:

- TrainLocationEventSource - A simple daemon that connects to the realtime ZeroMQ interface of ndovloket to get train positions
- EventstoreDB - Stores the realtime information for further processing

To create:

- API and frontend to view train information
- API to register trips
- Workers to fetch information
- Telegram bot to provide user a simple and quick interface without the need for a browser?

## Docker-compose

To run the project locally, a docker-compose file has been created. This will build all
the required projects and database dependencies.

To run:
```bash
docker compose up
```

Access Eventstore via <http://localhost:2113/web/index.html#/dashboard/>
Please note that the database does not use any authentication and authorization 
(including ACLs) when running insecure.