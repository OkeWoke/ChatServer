from socket import *
from threading import *
import json

class Server():
	def __init__(self):
		self.port = 23013
		self.serverName = "Server: "
		self.motd = [self.serverName,"You have connected to Oke\'s Server\n"]
		self.connections = []

		self.s =socket(AF_INET,SOCK_STREAM) #Create Socket Object
#		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',self.port)) #Bind port to computer
		self.s.listen(25) #Listens for 25 connections
		
		self.acceptConnections()		
			
	def acceptConnections(self):
		while True:
			client,addr = self.s.accept()
			print("Connection made with "+addr[0])
			alias = str(client.recv(1024).decode('utf-8'))
			client.send(json.dumps(self.motd).encode('utf-8'))
			clientDict= {
				"alias": alias,
				"ip": addr,
				"clientOb": client
			}
			self.connections.append(clientDict)
			clientHandler = Thread(target=self.clientReceive,args=(clientDict,))			
			clientHandler.start()
			commandHandler = Thread(target=self.serverCommand)
			commandHandler.start()

	def broadcast(self, data):
		for clientDict in self.connections:
			try:
				clientDict["clientOb"].send(data)
			except:
				print("Unable to send data to: "+ clientDict["alias"] + " " + clientDict["ip"])
				clientDict["clientOb"].close()
				self.connections.remove(clientDict)

	def clientReceive(self,clientDict):
		while True:
			try:
				data = clientDict["clientOb"].recv(1024)
				print(json.loads(data.decode('utf-8')))		
				self.broadcast(data)
			except:
				print("Someone Disconnected or failed to broacast data or failed to receive data from: "+str(clientDict["alias"])+" "+str(clientDict["ip"]))
				self.connections.remove(clientDict)
				clientDict["clientOb"].close()
			try:
				if not data:
					break
			except:
				print("failed, loop exiting")
		clientDict["clientOb"].close()

	def shutDown(self):
		self.broadcast(json.dumps([self.serverName,"Server Shutting Down..."]).encode('utf-8'))
		for clientDict in self.connections:
			clientDict["clientOb"].close()
		quit()

	def serverCommand(self):
		while True:
			command = str(raw_input(">"))
			command = command.split()
			if command[0] =="stop":
				self.shutDown()		
				
server = Server()
