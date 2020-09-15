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

	def __handle_conn(self, io, msg_handler):
		try:
			while True:
				message = io.receive()
				msg_handler.treat( message )

		except (Exception, KeyboardInterrupt) as e:
			print(str(e), 'on line %s\n' % sys.exc_info()[-1].tb_lineno)
			io.client.delete()
			io.client.socket.shutdown(socket.SHUT_RDWR)
			io.client.socket.close()

	def __get_instruction(self):
		io = helpers.IOController(None, self.connections_storage)
		cmd_selector = helpers.ServerCMDSelector(io)
		while True:
			instruction = str(input('>'))
			cmd_selector.select(instruction)

	def __listen_connections(self):
		while True:
			#A client make a connection
			clientsocket, addr = self.socket.accept()

			client = storage.ClientConnection(socket=clientsocket, address=addr)
			client.preset(storage=self.connections_storage)

			io = helpers.IOController(client, self.connections_storage)
			cmd_selector = helpers.ClientCMDSelector(io)
			msg_handler = helpers.MSGHandler(io, cmd_selector)

			print('%s has requested a connection' % str(client))
			client_thread = threading.Thread(
				target=self.__handle_conn, args=(io, msg_handler))
			client_thread.start()

	def start(self):
		#Individual server storage
		self.connections_storage = storage.ConnectionsStorage()

		inner_instructions = threading.Thread(target=self.__get_instruction)
		inner_instructions.start()

		listen_connections = threading.Thread(target=self.__listen_connections)
		listen_connections.start()

server = Server()
server.start()

