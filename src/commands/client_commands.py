
class Command:

	"""Command base class"""

	def preset(self, io_controller):
		"""Specifies the instances used to work with"""
		self.io = io_controller

class Register(Command):

	"""Command used to register a nickname on the client connections storage"""

	def __init__(self, **data):
		self.data = data['data']
		self.storage = data['storage']

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

		if len( self.data ) == 0:
			self.io.send('No nickname has been choosen\nuse: /register [nickname]')

		else:
			nickname = self.data[0]
			if nickname in self.storage.clients:
				self.io.send('nickname in use')
			elif self.io.client.exists():
				__update(nickname)
			else:
				__create(nickname)


class Badcmd(Command):
	def execute(self):
		self.io.send('use /help to show the commands list')


class Exit(Command):
	"""Client exits from its session"""
	def execute(self):
		if self.io.client.exists():
			self.io.client.delete()
			self.io.send('\n\nsession.exit')
		else:
			self.io.send('No session found')
