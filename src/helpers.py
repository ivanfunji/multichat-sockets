import socket
import json
import collections
import sys
import shlex
from commands import client_commands
from commands import server_commands

class CMDSelector(object):

	def __init__(self, io_controller):
		self.io = io_controller


class ServerCMDSelector(CMDSelector):

	"""Determines instructions to execute for the server"""

	def __init__(self, io_controller):
		self.io = io_controller

	def select(self, statement):
		statement = shlex.split(statement)

		if len(statement) > 0:
			case = statement[0]
			options = {
				'/broadcast': server_commands.Broadcast(message=statement),
				'/exit': server_commands.Exit()
			}
			command = options.get(case, server_commands.Badcmd())
			command.preset(self.io)
			command.execute()

class ClientCMDSelector(CMDSelector):

	"""Determines what command it has to execute for a client"""

	def select(self, statement, storage):
		case = statement[0]
		options = {
			'/register': client_commands.Register(data=statement[1:]),
			'/exit': client_commands.Exit()
		}
		command = options.get(case, client_commands.Badcmd())
		command.preset(self.io)
		command.execute()

class MSGHandler:

	"""Determines how the messages will be treated"""

	def __init__(self, io_controller, cmd_selector):
		self.io = io_controller
		self.cmd = cmd_selector

	def treat(self, message):
		if len(message) > 0 and message[0] == '/':
			#Specifies that message is a command

			self.cmd.select(shlex.split(message), storage=self.io.storage)
		else:
			if self.io.client.exists():
				response = '%s: %s' % (self.io.client.nickname, message)
				self.io.broadcast(response)
			else:
				self.io.send('you are not registered \nuse /register [nickname]')


class IOController:

	"""Controlls incoming and outgoing messages"""

	def __init__(self, client, storage):
		self.client = client
		self.storage = storage

	def send(self, message):
		self.client.socket.send(message.encode())

	def sendto(self, rclient, message):
		rclient.socket.send(message.encode())

	def broadcast(self, message):
		for client in self.storage.clients.values():
			self.sendto(client, message)

	def receive(self):
		return self.client.socket.recv(4096).decode('utf-8')

