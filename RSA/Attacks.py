'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from Arith import *
from Mint import *
from RSA import *
from random import *
from RSA_CRT import *
from math import *


def Bellcore_attack(victim : RSA_CRT, cipher : int) -> int :
	"""
	Bellcore attack
	return the private key of the victim
	"""
	#collect the true clear message
	m = victim.decrypt(cipher)

	#We set the fault attack
	victim.set_bellcore(True)
	
	#Collect the false clear message
	mfault = victim.decrypt(cipher)

	#compute q
	q = gcd(m - mfault, victim.n)

	#compute p
	p = victim.n // q

	#compute phi
	phi = (p-1) * (q-1)

	#compute the private key
	d = euclide_algorithm(victim.e, phi)["U"] % phi

	#now we can decrypt what we want !!!
	return d


def Wiener(N : int, e : int) -> int :
	"""
	Wiener Attack
	return the private key if it's vulnerable
	if not, return 0
	"""
	
	#1 - initiate the list of partial quotients
	quot = cont_frac(e,N)
	
	#2 - initiate a list of continued fractions
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
		


	
	
