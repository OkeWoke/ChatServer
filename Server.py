from socket import *
from threading import *
import json,sys,time

if sys.version_info >=(3,0):
        raw_input = input
        
class Server():
	def __init__(self):
		self.port = 11111
		self.serverName = "Server: "
		self.motd = [1,self.serverName,"You have connected to Oke\'s Server\n"]
		self.connections = []
		self.s =socket(AF_INET,SOCK_STREAM) #Create Socket Object
		self.s.bind(('',self.port)) #Bind port to computer
		self.s.listen(25) #Listens for 25 connections
		self.userList = []
		commandHandler = Thread(target=self.serverCommand)
		commandHandler.start()
		
		self.acceptConnections()		
		
	def acceptConnections(self):
		while True:
			client,addr = self.s.accept()
			alias = str(client.recv(1024).decode('utf-8'))#This does not use serverDecode because the server is receiving data that is not in the regular format that is a list.
			self.userList.append(alias)
			print("Connection made with "+addr[0]+"\n"+alias+" has connected.")
			
			client.send(self.serverEncode(self.motd))
			clientDict= {
				"alias": alias,
				"ip": addr,
				"clientOb": client
			}
			self.connections.append(clientDict)
			clientHandler = Thread(target=self.clientReceive,args=(clientDict,))			
			clientHandler.start()
			time.sleep(1)
			self.broadcast([0, self.userList])
			self.broadcast([1,"", alias + "  has connected"])

	def broadcast(self, data):
		data = self.serverEncode(data)
		for clientDict in self.connections:
			try:
				clientDict["clientOb"].send(data)
			except:
				print("Unable to send data to: "+ clientDict["alias"] + " " + str(clientDict["ip"]))
				#clientDict["clientOb"].close()
				#self.connections.remove(clientDict)

	def serverEncode(self, data):
		data = json.dumps(data).encode('utf-8')
		return data

	def serverDecode(self, data):
		data = json.loads(data.decode('utf-8'))
		return data

	def clientReceive(self,clientDict):
		while True:
			try:
				data = clientDict["clientOb"].recv(1024)
				data= self.serverDecode(data)
				print(data)		

			except:
				print(clientDict["alias"] + " has disconnected")
				self.broadcast([1,"", clientDict["alias"] +" has disconnected"])
				for i in self.userList:
					if i == clientDict["alias"]:
						self.userList.remove(i)
				self.broadcast([0, self.userList])
				break
			try:
				if data[0] ==1:
					self.broadcast(data)
			except:
				print("Failed to broacast data to everyone?!?")
				break
			try:
				if not data:
					break
			except:
				print("failed, loop exiting")
				break
		try:
			self.connections.remove(clientDict)
			clientDict["clientOb"].close()
		except: 
			print("Unable to remove clientData, possibly removed elsewhere")

	def shutDown(self):
		self.broadcast([1,self.serverName,"Server Shutting Down..."])
		for clientDict in self.connections:
			clientDict["clientOb"].close()
		print("shutting down server...")
		sys.exit()

	def serverCommand(self):
		while True:
			command = str(raw_input(">"))
			command = command.split()
			if command[0] =="stop":
				self.shutDown()		
			elif command[0] =="say":
				msg = command[1:]
				self.broadcast([1,self.serverName," ".join(msg)])
						
server = Server()
# 1 = string message
# 0 = update userList
