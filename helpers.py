import dataclasses
import socket
import json

@dataclasses.dataclass
class Scope:
	all : object = None
	client : object = None
	address : str = None


class MSGHandler:

	""" Determines how the messages will be treated """

	def __init__(self, io_manager):
		self.io = io_manager

	def treat(self, message):
		if message.split(' ')[0] == '/':
			self.io.send('you has sent a command')
		else:
			self.io.send(message)
			#self.io.broadcast(message)


class IOManager:
	""" Controlls incoming and outgoing messages """

	def __init__(self, connections, client, address):
		self.scope = Scope(connections, client, address)
		self.msg_handler = MSGHandler(self)

	def send(self, message):
		self.scope.client.send(message.encode())

	def sendto(self, client, message):
		client.send(message.encode())

	def broadcast(self, message):
		for client in self.scope.all.clients.values():
			self.sendto(client, message)

	def handle_client(self):
		try:
			while True:
				message = self.scope.client.recv(4096).decode('utf-8')
				self.msg_handler.treat(message)

		except (Exception, KeyboardInterrupt) as e:
			print('Failed to handle from: %s' % str(self.scope.address))
			print(str(e))
			self.scope.client.shutdown(socket.SHUT_RDWR)
			self.scope.client.close()
