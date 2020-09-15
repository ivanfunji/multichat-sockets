
class ConnectionsStorage:

	"""Storage for the active connections"""

	def __init__(self):
		self.clients = {}

	def save(self, client):
		self.clients.update({client.nickname: client})

	def remove(self, client):
		self.clients.pop(client.nickname)

	def exists(self, client):
		return client.nickname in self.clients


class ClientConnection:

	def __init__(self, socket, address):
		self.socket = socket
		self.address = str(address)
		self.nickname = None

	def preset(self, storage):
		"""Set configuration. Instances wich client could interact with."""
		self.storage = storage

	def __str__(self):
		return '[client] %s' % self.address

	def save(self, nickname):
		self.nickname = nickname
		self.storage.save(self)

	def update(self, nickname):
		self.delete()
		self.save(nickname)

	def delete(self):
		self.storage.remove(self)
		self.nickname = None

	def exists(self):
		return self.storage.exists(self)
