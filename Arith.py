from math import *

def gcd(a, b):
	"""
	fast gcd
	"""
	while b != 0:
		a, b = b, a % b
	return a

def euclide_algorithm (a: int, b: int) -> dict :
	"""
	Extended Euclide's algorithm
	Compute the PGCD from two integers and return the Bezout's relation elements
	
	Entry : two integers A and B
	Return : a dict ( "PGCD" , "U" , "V") 
	where r is the remind and u and v are the the coefficients of the Bezout's relation
	"""
	r1 = a
	r2 = b
	u1 = 1
	u2 = 0
	v1 = 0
	v2 = 1
	
	while (r2 != 0) :
		q = r1 // r2
		rt = r1
		ut = u1
		vt = v1
		r1 = r2
		u1 = u2
		v1 = v2
		r2 = rt - q * r2
		u2 = ut - q * u2
		v2 = vt - q * v2
	
	return { "PGCD":r1 , "U":u1 , "V":v1 }

def is_prime(n : int) -> bool :
		"""
		naive primality test
		"""
		for i in range(2,n-1):
			if  (n%i == 0):
				return False
		return True

def generate_prime(mn : min, mx : int) -> int :
		"""
		randomly generates prime numbers
		in :
			* mn : integer.		lower bound
			* mx : integer.		upper bound

		out :
			n : integer. 		a prime number between mn and mx
		"""
		assert ((2 < mn) and (mn <= mx)) , "The chosen bounds are not valid"
		#except AssertionError:
		#	print("The chosen bounds are not valid")

		#define the max try
		r = 100 * (math.log2(mx)+1) 

		n = randint(mn, mx)

		while (not is_prime(n)) :
			r = r-1
			assert r>0 , "Tno prime number found in the selected interval"
			#except AssertionError:
			#	print("Tno prime number found in the selected interval")
			n = randint(mn, mx)
		return n
