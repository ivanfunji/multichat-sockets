from . import base

class Broadcast(base.Command):

	def __init__(self, **data):
		self.msg = data['message']

	def execute(self):
		if len(self.msg) > 1:
			self.io.broadcast(self.msg[1])
		else:
			print('use: /broadcast "message"')

class Badcmd(base.Command):
	def execute(self):
		print('use /help to show the commands list')

class Exit(base.Command):
	def execute(self):
		print('exit from server')
