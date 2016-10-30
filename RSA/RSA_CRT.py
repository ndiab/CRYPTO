from RSA import *

class RSA_CRT(RSA):
	"""
	Object that initializes all the values that RSA needs

	generates keys and can Encrypt, Decrypt integers using CRT
	"""	

	def __init__(self, *args, **kwargs):
		super(RSA_CRT, self).__init__(*args, **kwargs)
		self.test = "tout est ok"

	def decrypt(self, cipher : int) -> int :
		"""
		RSA-CRT decryption
		Entry : cipher	(integer)
		Return : clear message (integer)
		"""
		cp = Mint(cipher, self.p)
		cq = Mint(cipher, self.q)
		dp = self.d % (self.p - 1)
		dq = self.d % (self.q - 1)
		cp.fast_exp(dp)
		cq.fast_exp(dq	)
		m = CRT(cp,cq)
		return m.value
		
