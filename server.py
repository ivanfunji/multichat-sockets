
import os
os.system('clear')

import threading
import helpers
import socket
import storage

class Client:

	def __init__(self, socket, address):
		self.socket = socket
		self.address = str(address)
		self.nickname = None

	def __str__(self):
		return '[client] %s' % str(self.address)

	def save(self):
		storage.connections.save(self)

	def delete(self):
		storage.connections.remove(self.address)

	def exists(self):
		return storage.connections.exists(self)

class Server():

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('localhost', 5050))
		self.socket.listen()

	def start(self):
		try:
			while True:
				clientsocket, addr = self.socket.accept()
				client = Client(socket=clientsocket, address=addr)
				print('%s has requested a connection' % str(client))

				io = helpers.IOManager(client)

				client_thread = threading.Thread(target=io.handle_client)
				client_thread.start()

		except (Exception, KeyboardInterrupt) as e:
			print(str(e))
			self.socket.shutdown(socket.SHUT_RDWR)
			self.socket.close()
			print('server.exit')
			exit()

server = Server()
server.start()

