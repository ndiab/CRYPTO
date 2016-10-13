

class Message :
	
	def __init__(self) :
		self.message_str = ""
		self.message_int = 0

	def set_str(self, m : str) :
		self.message_str = m
		self.string_to_int()

	def set_int(self, m : int) :
		self.message_int = m
		self.int_to_string()

	def string_to_int(self):
		m = ''.join(str(ord(c)) for c in self.message_str)
		self.message_int = int(m)

	def int_to_string(self):
		m = str(self.message_int)
		self.message_str = "".join(chr(int(i)) for i in m)

