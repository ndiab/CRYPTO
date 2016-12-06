from random import *
from copy import *
from Arith import *
from Message import *

class RSA :
	"""
	Object that initializes all the values that RSA needs

	generates keys and can Encrypt, Decrypt integers
	"""	

	# define the bounds of the primary numbers generation  (1024 bits each)
	min_bound = 1 << 1024    #2^1024	 	
	max_bound = (1 << 1025) -1    #2^1025 - 1
	
	def __init__(self):
		self.p = 0
		self.q = 0
		self.e = 0
		self.d = 0
		self.phi = 0
		self.n = 0
		self.generate_keys()
		

	def generate_keys(self):
		"""
		generates keys and set the RSA values
		"""
		# step 1 : chose random primary numbers p and q
		n = generate_prime(self.min_bound,self.max_bound)
		self.p = copy(n)
		n = generate_prime(self.min_bound,self.max_bound)
		while(n == self.p):
			n = generate_prime(self.min_bound,self.max_bound)
		self.q = copy(n)

		#step 2 : compute n = pq
		self.n = self.p * self.q

		#step 3 : compute phi(n)
		self.phi = (self.p - 1) * (self.q - 1)

		#step 4 : chose the exponent
		n = randint(100,self.phi)
		while (gcd(self.phi,n) != 1):
			n = randint(100,self.phi)
		self.e = copy(n)

		#step 5 : compute d (private key)
		self.d = euclide_algorithm(self.e, self.phi)["U"] % self.phi

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
		c.fast_exp(self.d)
		return c.value
		






