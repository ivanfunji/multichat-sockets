import socket
import json
import collections
import storage
import sys
import commands

class CommandSelector:

	"""Determines what command it has to execute"""

	def __init__(self, io_manager):
		self.io = io_manager

	def select(self, statement):
		try:
			case = statement[0]
			options = {
				'/register': commands.CMDRegister(statement[1:]),
				'/exit': commands.CMDExit()
			}
			command = options.get(case, commands.CMDBadcmd())
			command.preset(self.io)
			command.execute()
		except Exception as e:
			print('Failed to excecute command')
			print(str(e), 'on line %s\n' % sys.exc_info()[-1].tb_lineno)


class MSGHandler:

	"""Determines how the messages will be treated"""

	def __init__(self, io_manager, cmd_selector):
		self.io = io_manager
		self.cmd = cmd_selector

	def treat(self, message):
		if len(message) > 0 and message[0] == '/':
			self.cmd.select(message.split(' '))
		else:
			if self.io.client.exists():
				response = '%s: %s' % (self.io.client.nickname, message)
				self.io.broadcast(response)
			else:
				self.io.send('you are not registered \nuse /register [nickname]')


class IOManager:
	""" Controlls incoming and outgoing messages """

	def __init__(self, client):
		self.client = client
		self.msg_handler = MSGHandler(self, CommandSelector(self))

	def send(self, message):
		self.client.socket.send(message.encode())

	def sendto(self, rclient, message):
		rclient.socket.send(message.encode())

	def broadcast(self, message):
		for client in storage.connections.clients.values():
			self.sendto(client, message)

	def handle_client(self):
		try:
			while True:
				message = self.client.socket.recv(4096).decode('utf-8')
				self.msg_handler.treat(message)

		except (Exception, KeyboardInterrupt) as e:
			print('Failed to handle from: %s' % str(self.client))
			print(str(e), 'on line %s\n' % sys.exc_info()[-1].tb_lineno)
			self.client.delete()
			self.client.socket.shutdown(socket.SHUT_RDWR)
			self.client.socket.close()

