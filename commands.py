import storage

class Command:

	"""Command base class"""

	def preset(self, io_manager):
		"""Determines the input/output manager to send or receive messages"""
		self.io = io_manager

class CMDRegister(Command):

	"""Command used to register a nickname on the server connections storage"""

	def __init__(self, *data):
		self.data = data

	def execute(self):

		def __create(nickname):
			self.io.client.save(nickname)
			response = '[%s] joined the chat' % self.io.client.nickname
			self.io.broadcast(response)

		def __update(nickname):
			response = '%s (y/n)\n%s -> %s' % (
				'Do you want to change your current nickname?',
				self.io.client.nickname,
				nickname
			)
			self.io.send(response)

			option = self.io.client.socket.recv(3).decode('utf-8')
			if option == 'yes' or option == 'y':
				response = '[%s] changed to -> [%s]' % (
					self.io.client.nickname,
					nickname
				)
				self.io.client.update(nickname)
				self.io.broadcast(response)


		data = self.data[0]
		if len(data) == 0:
			self.io.send('No nickname has been choosen\nuse: /register [nickname]')

		else:
			if data[0] in storage.connections.clients:
				self.io.send('nickname in use')
			elif self.io.client.exists():
				__update(data[0])
			else:
				__create(data[0])


class CMDBadcmd(Command):
	def execute(self):
		self.io.send('use /help to show the commands list')


class CMDExit(Command):
	"""Exits from the session"""
	def execute(self):
		if self.io.client.exists():
			self.io.client.delete()
			self.io.send('\n\nsession.exit')
		else:
			self.io.send('No session found')
