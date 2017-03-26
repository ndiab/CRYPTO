'''
Created on Mar 26, 2017
@author: Nabil Diab
    
'''

from Arithmetic.arith import *

def bsgs(c : int, m : int, N : int) -> int :
	"""
	Baby Step Giant Step
	Compute the discrete logarithm
	return d such that c^d mod N = m mod N
	Entry :
		* c : cipher
		* m : clear message
		* N : modulus
	"""

	a = find_invpow(N,2) + 1 

	C = Mint(c,N)

	BS = {}
	
	#Baby Step
	for i in range (a):
		C.value = c
		C.fast_exp(i)
		BS[C.value] = i

	# c ^-a
	step = Mint(c, N)
	step.fast_exp(a)
	step.inv()

	g = m

	#Giant step
	for i in range (a):
		if g in BS.keys() :
			return i * a + BS[g]
		else :
			g = (g * step.value) % N

	print("BSGS doesn't work")

	return -1
