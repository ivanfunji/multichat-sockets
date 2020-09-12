import socket
import json
import collections
import storage

class CommandSelector:
	def __init__(self, io_manager):
		self.io = io_manager

	def select(self, statement):
		case = statement[0]
		messages = {
			'/register': self.register(statement[1:])
		}
		return messages[case]

	def register(self, data):
		if len(data) == 0:
			return 'No nickname has been choosen\nuse: /register nickname'
		else:
			if self.io.client.exists():
				return 'You are already registered'
			else:
				self.io.client.save()
			return 'Registration successfull'


class MSGHandler:

	""" Determines how the messages will be treated """

	def __init__(self, io_manager, cmd_selector):
		self.io = io_manager
		self.cmd = cmd_selector

	def treat(self, message):
		splited = message.split(' ')
		if splited[0][0] == '/':
			response = self.cmd.select(splited)
			self.io.send(response)
			print(storage.connections.clients)
		else:
			self.io.broadcast(message)

class IOManager:
	""" Controlls incoming and outgoing messages """

	def __init__(self, client):
		self.client = client
		self.msg_handler = MSGHandler(self, CommandSelector(self))

	def send(self, message):
		self.client.socket.send(message.encode())

	def sendto(self, client, message):
		client.socket.send(message.encode())

	def broadcast(self, message):
		for client in storage.connections.clients.values():
			self.sendto(client, message)

	def handle_client(self):
		try:
			while True:
				message = self.client.socket.recv(4096).decode('utf-8')
				self.msg_handler.treat(message)

		except (Exception, KeyboardInterrupt) as e:
			print('Failed to handle from: %s' % str(self.client.address))
			print(str(e))
		finally:
			self.client.socket.shutdown(socket.SHUT_RDWR)
			self.client.socket.close()
