# Lipwig's Locomotion Ledger - LLL

This project is a hobby project to find out if we have traveled in this train beofore. It consists of multiple parts:

- TreinLocationEventSource - A simple daemon that connects to the realtime ZeroMQ interface of ndovloket to get train positions
- EventstoreDB - Stores the realtime information for further processing

To create:

- API and frontend to view train information
- API to register trips
- Workers to fetch information
- Telegram bot to provide user a simple and quick interface without the need for a browser?
