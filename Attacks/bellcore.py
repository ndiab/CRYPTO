'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from Asymetric import RSA, RSA_CRT, User
from Arithmetic.arith import *
from random import *
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
	


	

