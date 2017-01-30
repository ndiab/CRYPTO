'''
Created on Oct 13, 2016
@author: Nabil Diab
    
'''


from random import *
from copy import *
from Arith import *

class RSA :
	"""
	Object that initializes all the values that RSA needs

	generates keys and can Encrypt, Decrypt integers
	"""	

	# define the bounds of the primary numbers generation  (1024 bits each)
	min_bound = 1 << 1024    #2^1024	 	
	max_bound = (1 << 1025) -1    #2^1025 - 1
	
	def __init__(self):
		self._p = 0
		self._q = 0
		self.e = 0
		self._d = 0
		self._phi = 0
		self.n = 0
		self.generate_keys()
		

	def generate_keys(self):
		"""
		generates keys and set the RSA values
		"""
		# step 1 : chose random primary numbers p and q
		n = generate_prime(self.min_bound,self.max_bound)
		self._p = copy(n)
		n = generate_prime(self.min_bound,self.max_bound)
		while(n == self._p):
			n = generate_prime(self.min_bound,self.max_bound)
		self._q = copy(n)

		#step 2 : compute n = pq
		self.n = self._p * self._q

		#step 3 : compute phi(n)
		self._phi = (self._p - 1) * (self._q - 1)

		#step 4 : chose the exponent
		n = randint(100,self._phi)
		while (gcd(self._phi,n) != 1):
			n = randint(100,self._phi)
		self.e = copy(n)

		#step 5 : compute d (private key)
		self._d = euclide_algorithm(self.e, self._phi)["U"] % self._phi

	def encrypt(self, message : int) -> int:
		"""
		RSA encryption
		Entry : integer message
		Return : message encrypted
		"""
		m = Mint(message,self.n)
		m.fast_exp(self.e)
		return m.value

	def decrypt(self, cipher : int) -> int:
		"""
		RSA decryption
		Entry : cipher	(integer)
		Return : clear message (integer)
		"""
		c = Mint(cipher,self.n)
		c.fast_exp(self._d)
		return c.value

	def force_public_key(self, new_e : int) :
		"""
		modify the public key and adapt the private key to this one
		useful for the broadcast Attack
		Entry : the new public key
		"""
		
		if (gcd(self._phi,new_e) != 1) :
			return False
		
		self.e = copy(new_e)
		self._d = euclide_algorithm(self.e, self._phi)["U"] % self._phi

		return True

	def is_private_key(self, key: int) -> bool:
		return key == self._d






