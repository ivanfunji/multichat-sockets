
class ConnectionsStorage:

	def __init__(self):
		self.clients = {}

	def save(self, client):
		self.clients.update({client.address: client})

	def remove(self, client):
		self.clients.pop(client.address)

	def exists(self, client):
		return client.address in self.clients

connections = ConnectionsStorage()
