#!/usr/bin/python3.8

import os
os.system('clear')

import threading
import helpers
import socket
import storage
import sys

class ClientConnection:

	def __init__(self, socket, address):
		self.socket = socket
		self.address = str(address)
		self.nickname = None

	def __str__(self):
		return '[client] %s' % self.address

	def save(self, nickname):
		self.nickname = nickname
		storage.connections.save(self)

	def update(self, nickname):
		self.delete()
		self.save(nickname)

	def delete(self):
		storage.connections.remove(self)
		self.nickname = None

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
				client = ClientConnection(socket=clientsocket, address=addr)
				print('%s has requested a connection' % str(client))

				io = helpers.IOManager(client)

				client_thread = threading.Thread(target=io.handle_client)
				client_thread.start()

		except (Exception, KeyboardInterrupt) as e:
			print(str(e))
			self.socket.shutdown(socket.SHUT_RDWR)
			self.socket.close()
			print('server.exit')
			sys.exit()

server = Server()
server.start()

