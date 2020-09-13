import socket
import json
import collections
import storage
import sys

class CommandSelector:

	""" Executes the choosed command """

	def __init__(self, io_manager):
		self.io = io_manager

	def select(self, statement):
		try:
			case = statement[0]

			commands = {
				'/register': self.register,
				'/exit': self.exit
			}
			commands.get(case, self.bad_command)(statement[1:])

		except Exception as e:
			print('Failed to excecute command')
			print(e)

	def bad_command(self, *args, **kargs):
		self.io.send('use /help to show the commands list')

	def exit(self, *args, **kargs):
		if self.io.client.exists():
			self.io.client.delete()
			self.io.send('\n\nsession.exit')
		else:
			self.io.send('No session found')
			print(storage.connections.clients)

	def register(self, *args, **kargs):
		data = args[0]
		if len(data) == 0:
			self.io.send('No nickname has been choosen\nuse: /register [nickname]')

		else:
			if data[0] in storage.connections.clients:
				self.io.send('nickname in use')

			else:
				self.io.client.save(data[0])

				response = '[%s] joined the chat' % self.io.client.nickname
				self.io.broadcast(response)


class MSGHandler:

	""" Determines how the messages will be treated """

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

