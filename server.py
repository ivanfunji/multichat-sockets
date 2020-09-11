
import os
os.system('clear')

import threading
import helpers
import socket

class ConnectionsStorage:

	def __init__(self):
		self.clients = {}

	def save(self, addr, socket):
		self.clients.update({addr: socket})

	def remove(self, addr):
		self.clients.pop(addr)


class Server():

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('localhost', 5050))
		self.socket.listen()

		self.connections = ConnectionsStorage()

	def start(self):
		try:
			while True:
				client, addr = self.socket.accept()
				print('%s has requested a connection' % str(addr))

				io = helpers.IOManager(self.connections, client, addr)

				client_thread = threading.Thread(target=io.handle_client)
				client_thread.start()

		except (Exception, KeyboardInterrupt) as e:
			print(str(e))
			print('server.exit')
			self.socket.shutdown(socket.SHUT_RDWR)
			self.socket.close()

server = Server()
server.start()

