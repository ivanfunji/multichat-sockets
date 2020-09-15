class Command:

	"""Command base class"""

	def preset(self, io_controller):
		"""Specifies the instances used to work with"""
		self.io = io_controller
