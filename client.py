#!/usr/bin/python3.8

import os
os.system('clear')

import socket
import threading
import json

class Client:

	"""Client side application class"""

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.socket.connect(('localhost', 5050))

	def send(self, message):
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
				self.send(str(input()))
			except Exception as e:
				print('Error sending the message.')
				print(e)
				self.socket.close()
				break

	def start(self):
		try:
			reception_thread = threading.Thread(target=self.reception)
			sending_thread = threading.Thread(target=self.sending)
			reception_thread.start()
			sending_thread.start()
		except KeyboardInterrupt:
			self.socket.close()
			print('exit')

client = Client()
client.start()
