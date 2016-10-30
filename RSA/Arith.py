from math import *
from random import *
from copy import *
from Mint import *

#Tableau de petits premiers
prime_tab = [2,3,5,7,11,13,17,19,23,29,3137,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223]

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

def CRT(a : Mint, b : Mint) -> Mint :
	"""
	Chiness Remainder Theorem 
	"""
	r = euclide_algorithm(a.mod, b.mod)
	u = r["U"]
	v = r["V"]
	x = (a.value * v * b.mod) + (b.value * u * a.mod)
	m = Mint(x, a.mod * b.mod)
	return m	

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
