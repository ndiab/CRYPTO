'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from RSA import *
from random import randint

class RSA_CRT(RSA):
	"""
	Object that initializes all the values that RSA needs

	generates keys and can Encrypt, Decrypt integers using CRT
	"""	

	def __init__(self, *args, **kwargs):
		super(RSA_CRT, self).__init__(*args, **kwargs)
		self.bellcore = False

	def set_bellcore(self, b : bool):
		self.bellcore = b

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
		cq.fast_exp(dq)
		# Fault attack !
		if(self.bellcore):
			#We change the value of mp
			n = randint(0,self.p)
			cp.value = n
		m = CRT(cp,cq)
		return m.value
		
