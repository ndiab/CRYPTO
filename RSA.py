from random import *
from copy import *
from Euclide import *
from Message import *

class RSA :
	"""
	Object that initializes all the values that RSA needs

	generates keys and can Encrypt, Decrypt integers
	"""	
	
	def __init__(self):
		self.p = 0
		self.q = 0
		self.e = 0
		self.d = 0
		self.phi = 0
		self.n = 0
		self.generate_keys()
		
		

	def is_prime(self, n : int) -> bool :
		"""
		naive primality test
		"""
		for i in range(2,n-1):
			if  (n%i == 0):
				return False
		return True

	def generate_prime(self, mn : min, mx : int) -> int :
		"""
		randomly generates prime numbers
		in :
			* mn : integer.		there are the bounds of our
			* mx : integer.		interval

		out :
			n : integer. 		a prime number between mn and mx
		"""
		n = randint(mn, mx)
		while (not self.is_prime(n)) :
			n = randint(mn, mx)
		return n
		

	def generate_keys(self):
		"""
		generates keys and set the RSA values
		"""
		# step 1 : chose random primary numbers p and q
		n = self.generate_prime(100000,1000000000)# we chose only integers between 10e5 to 10e9	
		self.p = copy(n)
		n = self.generate_prime(100000,1000000000)
		while(n == self.p):
			n = self.generate_prime(100000,1000000000)
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
		

