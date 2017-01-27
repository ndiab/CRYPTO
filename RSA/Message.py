'''
Created on Oct 13, 2016
@author: Nabil Diab
    
'''

class Message :
	"""
	Object that Mapping a string and an integer
	not functional yet, not finished

	to use it :
	After initialize the Message object you have to set one of the entity.
	
	the string value can be access by message_str
	the int value can be access by message_int 
	"""
	
	def __init__(self) :
		self.message_str = ""
		self.message_int = 0

	def set_str(self, m : str) :
		"""
		set the string of the message and will transcript it automatically into int
		useful for sending a message
		"""
		self.message_str = m
		self.string_to_int()

	def set_int(self, m : int) :
		"""
		set the int of the message and will transcript it automatically into string
		useful to receive a message
		"""
		self.message_int = m
		self.int_to_string()

	def string_to_int(self):
		"""
		transcript a string to an int
		"""
		m = ''.join(str(ord(c)) for c in self.message_str)
		self.message_int = int(m)

	def int_to_string(self):
		"""
		transcript an int to a string
		"""
		m = str(self.message_int)
		self.message_str = "".join(chr(int(i)) for i in m)

