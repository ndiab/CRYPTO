'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from Asymetric.RSA import *
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
		cp = Mint(cipher, self._p)
		cq = Mint(cipher, self._q)
		dp = self._d % (self._p - 1)
		dq = self._d % (self._q - 1)
		cp.fast_exp(dp)
		cq.fast_exp(dq)
		# Fault attack !
		if(self.bellcore):
			#We change the value of mp
			n = randint(0,self._p)
			cp.value = n
		m = CRT(cp,cq)
		return m.value
		
