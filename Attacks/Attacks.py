'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from Asymetric import Arith, RSA, RSA_CRT, User
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



def attack_exo_2(N : int, e : int, N_bis : int, e_bis : int) -> int :
	d = Wiener (N,e)
	nblb = int(log2(d))  # number of least significant bits k known

	offset = 1 << (nblb +1)	 # Offset for each iteration
	max_iter = 1 << (276 - nblb)

	print(max_iter)
	print(offset)

	d_bis = d + offset

	m_ref = randint(10,1000)

	m = Mint(m_ref,N_bis)
	
	# brute force the high order bits
	for i in range (max_iter):
		# to check if the key works, we compare the encryption and the decryption	
		
		if i%100000 == 0 :
			print (i)
	 
		m.fast_exp(e_bis)
		m.fast_exp(d_bis)
		
		if (m.value == m_ref) :
			print("Hacked")
			print(d_bis)
			return d_bis


		d_bis = d_bis + offset
		m.value = m_ref


	print("doesn't work")
	return 0



	


	

