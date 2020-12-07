# netDiag
Network diagnostic collection system for helpdesk and network operators - Better info creates better results...hopefully

To just use reporting function, you only need flask container and mongo.  If you want to be able to run remote commands and the report remotely, you will need RabbitMQ and the webscoket server container.

To build the clients wsClient and client, go into client dir and tyoe:

pyinstaller client.py --clean -F

pyinstaller wsClient.py --clean -F

This will build binaries for whatever system you are on at build time.
