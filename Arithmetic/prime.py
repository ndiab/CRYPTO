'''
Created on Mar 26, 2017
@author: Nabil Diab
    

This Document contains functions to generate large prime numbers
'''

from random import randint
from Arithmetic.arith import *
from math import *


def Rabin_Miller(n : int) -> bool :
	"""
	Rabin Miller primality test
	Entry : integer n
	Return : boolean. True if n is prime.
	"""
	assert (n>=3) and (n%2 != 0), "Rabin Miller : Tested Value not correct"
	#first, compute s and t such as s in odd and (2^t)*s = n-1
	s = n-1
	t = 0 
	while (s%2 == 0) :
		s = s//2
		t = t+1
	#we keep the probability of a false result in k. The max bound of this probability is 2^-k
	k = 0
	while (k < 128) :
		a = randint(2, n-1)
		v = Mint(a,n) 
		v.fast_exp(s)
		if (v.value!= 1):
			i = 0
			while (v.value != n-1):
				if (i == t-1):
					return False
				else:
					v.fast_exp(2)
					i = i+1
		k = k+2
	return True

def is_prime(n : int) -> bool :
	"""
	Primality test
	Entry : integer n
	Return : boolean. True if n is prime.
	"""
	#first we look if it has trivial divisor.
	for i in prime_tab:
		if (n%i == 0):
			return False
	#Once we have eliminated the majority of solutions, we run the Rabin-Miller test to determinate if this integer is prime
	return Rabin_Miller(n)

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
	r = 100 * (log2(mx)+1) 

	n = randint(mn, mx)

	while (not is_prime(n)) :
		r = r-1
		assert r>0 , "no prime number found in the selected interval"
		#except AssertionError:
		#	print("no prime number found in the selected interval")
		n = randint(mn, mx)
	return n

