
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

connections = ConnectionsStorage()
