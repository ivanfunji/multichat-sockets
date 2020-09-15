#!/usr/bin/python3.8

import os
os.system('clear')

import threading
import helpers
import socket
import storage
import sys

class Server():

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('localhost', 5050))
		self.socket.listen()

	def handle_conn(self, io):
		cmd_selector = helpers.ClientCMDSelector(io)
		msg_handler = helpers.MSGHandler(io, cmd_selector)

		try:
			while True:
				message = io.receive()
				msg_handler.treat( message )

		except (Exception, KeyboardInterrupt) as e:
			print(str(e), 'on line %s\n' % sys.exc_info()[-1].tb_lineno)
			io.client.delete()
			io.client.socket.shutdown(socket.SHUT_RDWR)
			io.client.socket.close()

	def start(self):
		try:
			#Individual server storage
			connections_storage = storage.ConnectionsStorage()

			while True:
				#A client make a connection
				clientsocket, addr = self.socket.accept()


				client = storage.ClientConnection(socket=clientsocket, address=addr)
				client.preset(storage=connections_storage)

				print('%s has requested a connection' % str(client))

				io = helpers.IOController(client, connections_storage)

				client_thread = threading.Thread(target=self.handle_conn, args=(io,))
				client_thread.start()

		except (Exception, KeyboardInterrupt) as e:
			print(str(e))
			self.socket.shutdown(socket.SHUT_RDWR)
			self.socket.close()
			print('server.exit')
			sys.exit()

server = Server()
server.start()

