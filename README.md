#Chat Server
This is server software written in python, using threading and socket modules to achieve communication.
See Chat Client Repo, OkeWoke/ChatClient.

Currently GUI less, and probably will remain so.
##How to use
Written in Python2, should run on python3, however change raw_input() to input() in the serverCommand function.


1. Set the port number in the program file. self.port=someninthere, note there's a limited amount of ports.
2. Exceute the program, you will then have a window with '>'. This means you can enter a server command. (Currently only stop and say.) i.e. say Hello. This broadcasts to all connected users "Server: Hello", and stop simply stops the server.
3. Other than that just let it run, you will see output appear when users connect, say stuff and disconnect.

##Features
- Server Commands, stop, say (more to come)

##Features to come/To do list
- Account system, so no name spoofing or multiple people with same alias. Possibly some data base n encryption required for this.
- Force Disconnect particular users (kicking)
- Multiple chat rooms?
- Better formatted output
