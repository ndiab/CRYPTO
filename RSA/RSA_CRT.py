from RSA import *

class RSA_CRT(RSA):
	

	def __init__(self, *args, **kwargs):
		super(CRT_RSA, self).__init__(*args, **kwargs)
		self.test = "tout est ok"

	def decrypt(n : int) -> int :
		
