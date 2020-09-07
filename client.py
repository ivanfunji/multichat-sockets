
import os
os.system('clear')

import socket
import threading
import json

class Client:

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.connect(('localhost', 5050))

	def send(self, type, message):
		message = json.dumps(dict(type=type, data=message))
		self.socket.send(message.encode())

	def reception(self):
		while True:
			try:
				message = self.socket.recv(4096).decode('utf-8')
				print(message)
			except Exception as e:
				print('Error receiving the message.')
				print(e)
				self.socket.close()
				break

	def sending(self):
		while True:
			try:
				message = str(input())
				message = '%s: %s' % (self.nickname, message)
				self.send(type='msg:basic', message=message)

			except Exception as e:
				print('Error sending the message.')
				print(e)
				self.socket.close()
				break

	def start(self):
		self.nickname = str(input('nickname: '))
		self.send(type='nick:create', message=self.nickname)

		try:
			reception_thread = threading.Thread(target=self.reception)
			sending_thread = threading.Thread(target=self.sending)

			reception_thread.start()
			sending_thread.start()

		except KeyboardInterrupt:
			print('exit')
			self.socket.close()

client = Client()
client.start()
