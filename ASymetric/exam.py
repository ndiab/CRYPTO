from random import randint
from math import *

N= 0x1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143b7ef096124769b084359a72b000000000000000000000000000000000000000000000000000000000000000000000000000002ab354728c9c9e417c3a3017028b5f14ed6cb2a2abccfe41f4bcf

e= 0x9f4f9e2c3634631d7ce5f6d92316acb180cfed06a759d840735e3f5c230f2f4f1822646d21ea6d523ca1fe48223a74dc2bd8d1b9d722ced486219b3a5f9e1812fc1eeaaa7d11699b576bbf87a2b2684d5555df984e355a4f4a3c392cec236847a2e97d4c6575292744a988f907fec624b9cf1379e145423155c6336992092bf


class Mint:
	""" 
	Arithmetic object.
	"""
	
	def __init__(self, value : int, mod : int):
		self.value = value
		self.mod = mod
		self.refresh()

	def refresh(self):
		"""
		refresh the current value whith the modulo
		must be called whenever the value has been changed 
		"""
		self.value = self.value % self.mod

	def fast_exp(self,exp : int):
		"""	
		exponentiation of a Mint computing by the fast exponentiation algorithm
		"""
		k = exp
		pointer = 1
		p = Mint(1,self.mod)
		while (k>0):
			if(pointer & exp):
				p.value = (p.value*self.value) 
				p.refresh()
			self.value = self.value * self.value
			self.refresh()
			k = k // 2
			pointer = pointer << 1
		self.value = p.value
		self.refresh

	def inv(self):
		"""
		self.value = self.value^-1
		"""
		self.value = euclide_algorithm(self.value, self.mod)["U"]
		self.refresh()

	def to_string(self):
		return str(self.value) + " mod " + str(self.mod)
def find_invpow(x,n):
	"""Finds the integer component of the n'th root of x,
	an integer such that y ** n <= x < (y + 1) ** n.
	"""
	low = 1
	high = x

	while low < high:
		mid = (low + high) // 2
		if low < mid and mid**n < x:
			low = mid
		elif high > mid and mid**n > x:
			high = mid
		else:
			return mid

	return mid + 1

def Wiener(N : int, e : int) -> int :
	"""
	Wiener Attack
	return the private key if it's vulnerable
	if not, return 0
	(need cont_frac, fraq_seq, isqrt, compute_frac, )
	"""
	
	#1 - initialize the list of partial quotients
	quot = cont_frac(e,N)
	
	#2 - initialize a list of continued fractions
	seq = frac_seq(quot)

	#check if d is actually the key
	for (k,d) in seq :
		# Now we are going to check if the couple (k,d)
		# produce a factorization of N (p * q)
		
		if k == 0:
			continue

		# compute phi
		# phi(N) = (ed - 1)/ k
		phi = (e * d - 1) // k
		
		# Now from phi and N we can deduce the eventual factorization
		# by solving the equation : x^2 - ((N-phi)+1)x + N
		a = 1
		b = (N - phi) + 1
		c = N
		
		discr = b*b - 4 * a * c
	
		# in that case we got solutions to the equation
		if discr > 0 :
			# to works, the solutions must be integers
			# first, the root of the discriminent must be integer 
			rdiscr = isqrt(discr)

			if (rdiscr * rdiscr) == discr :
				#the root of the discr is integer, we compute the solutions 
				p = -((-b - rdiscr) // (2 * a))
				q = -((-b + rdiscr) // (2 * a))
				if N == (p * q) :
					print("Hacked")
					return d

	print("Not vulnerable to Wiener")

	return 0

def cont_frac(x : int, y : int) -> int:
	"""
	Convert a rational x/y fraction into
	a list of partial quotients [a0, ... , an]
	"""

	L = []
	a = x
	b = y
	r = log2(y) #Maximum partial quotients

	while(a%b != 0 and r > 0 ):
		q = a // b
		a_t = a
		a = b
		b = a_t % b
		L.append(q)
		r = r-1

	L.append(a // b)

	return L


def frac_seq(L : list) -> list:
	"""
	Give the fractional sequence from a list of partial quotient
	"""
	
	seq = []

	for i in range(len(L)) :
		l = L[0:i]
		if len(l) == 0 :
			continue
		elif len(l) == 1 :
			seq.insert(i,(L[0],1))
		else :
			seq.insert(i,compute_frac(l))

	return seq


def compute_frac(l : list) -> tuple:
	"""
	compute symbolically a sequence of fractions
	"""	
	i = len(l)-2

	c = 1
	a = l[i]
	b = l[i+1]
	

	while ( i > 0 ) :
		a = l[i]
		a = a * b + c
		c = b
		b = a
		i = i - 1
	
	a = l[0]
	a = a * b + c

	return (a,b)


def isqrt(n):
	'''
	Calculates the integer square root
	for arbitrary large nonnegative integers
	'''
	if n < 0:
		raise ValueError('square root not defined for negative numbers')
    
	if n == 0:
		return 0

	a = int(log2(n)) + 1 // 2
	b = int(log2(n)) + 1 % 2

	x = 2**(a+b)
	while True:
		y = (x + n//x)//2
		if y >= x:
			return x
		x = y

def test_key(e : int, d : int, N : int) -> bool :
	"""
	test if a triplet public key private key and modulus works
	Entry : * e : public key
		* d : private key
		* N : modulus
	"""

	m = randint(2,N)
	M = Mint(m,N)

	M.fast_exp(e)
	M.fast_exp(d)

	_m = M.value

	if m == _m :
		print("SUCCESS")
		return True

	print("FAIL")
	return False


if __name__ == '__main__':
	d = Wiener(N,e)

	if test_key(e,d,N) :
		print ("This is the private key of Alice : ", hex(d))




