
import os
os.system('clear')

import socket
import threading
import json

class ConnectionsStorage:

	def __init__(self):
		self.clients = {}

	def save(self, addr, socket):
		self.clients.update({addr: socket})

	def remove(self, addr):
		self.clients.pop(addr)


class Server:

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('localhost', 5050))
		self.socket.listen()
		self.connections = ConnectionsStorage()

	def send(self, client, message):
		client.send(message.encode())

	def broadcast(self, message):
		for client in self.connections.clients.values():
			self.send(client, message)

	def handleMessage(self, addr, client, message):
		type = message['type']
		data = message['data']

		if type == 'nick:create':
			self.connections.save(addr, client)
			self.broadcast('%s is now connected!' % data)
		elif type == 'msg:basic':
			self.broadcast(data)


	def handleClient(self, addr, client):
		while True:
			try:
				message = client.recv(4096).decode('utf-8')
				message = json.loads(message)
				self.handleMessage(addr, client, message)

			except:
				print('Reception error from: %s' % str(addr))
				client.shutdown(socket.SHUT_RDWR)
				client.close()

	def start(self):
		print('Listening...')

		try:
			while True:
				client, addr = self.socket.accept()

				client_thread = threading.Thread(target=self.handleClient, args=(addr, client))
				client_thread.start()

			client.close()
		except KeyboardInterrupt:
			print('exit')
			self.socket.close()

server = Server()
server.start()
