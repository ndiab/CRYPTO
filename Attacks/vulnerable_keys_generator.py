'''
Created on Mar 26, 2017
@author: Nabil Diab
    
'''

from Arithmetic import *
from Asymetric import RSA


class Wiener_vuln(RSA):
	"""
	RSA generator
	Generate vulnerable keys for Wiener
	"""

	#min_bound = 1<<128   ##set here the wanted size of key
	#max_bound = 1<<129

	def __init__(self, *args, **kwargs):
		super(Wiener_vuln, self).__init__(*args, **kwargs)
		self.bellcore = False




	def generate_keys(self):
		"""
		generates keys and set the RSA values
		"""

		condition = False
		
			
		while (not condition) :
			# step 1 : chose random primary numbers p and q
			n = generate_prime(self.min_bound,self.max_bound)
			self._p = n
			n = generate_prime(self.min_bound,self.max_bound)
			while(n == self._p):
				n = generate_prime(self.min_bound,self.max_bound)
			self._q = n

			#step 2 : compute n = pq
			self.n = self._p * self._q
			
			a = find_invpow(self.n,4) // 3
			condition = (self._p > self._q) and (self._p < 2 * self._q)
			if (not condition) :
				continue

			print("step one OK")

			#step 3 : compute phi(n)
			self._phi = (self._p - 1) * (self._q - 1)

			#step 4 : chose the exponent
			n = randint(100,a)
			while (gcd(self._phi,n) != 1):
				n = randint(100,self._phi)
			self._d = n

			#step 5 : compute d (private key)
			self.e = euclide_algorithm(self._d, self._phi)["U"] % self._phi

			condition = (self._d < a)







