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

def attack_exo_2(N : int, e : int, N_bis : int, e_bis : int) -> int :
	d = Wiener (N,e)
	nblb = int(log2(d)) + 1  # number of least significant bits k known

	offset = 1 << (nblb +1)	 # Offset for each iteration
	max_iter = 1 << (276 - nblb)

	print(max_iter)
	print(offset)


	d_bis = offset

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



N= 0x1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143b7ef096124769b084359a72b000000000000000000000000000000000000000000000000000000000000000000000000000002ab354728c9c9e417c3a3017028b5f14ed6cb2a2abccfe41f4bcf
e= 0x9f4f9e2c3634631d7ce5f6d92316acb180cfed06a759d840735e3f5c230f2f4f1822646d21ea6d523ca1fe48223a74dc2bd8d1b9d722ced486219b3a5f9e1812fc1eeaaa7d11699b576bbf87a2b2684d5555df984e355a4f4a3c392cec236847a2e97d4c6575292744a988f907fec624b9cf1379e145423155c6336992092bf


Nbis= 0x1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143b7ef096124769b084359a72c620000000000000000000000000000000000000000000000000000000000000000000000000002ab354728c9c9e417c3a301a2bfb5958214c121a20a1bc3a60b5d
ebis= 0xcab33aef8b29f93115458e31b7f14ff3efbdf91dfaa4e025dafe66913c8db9ab77e860536b79875327449e2c759a774d91c0f09595589613c804f4565dcb202e78559233b609d0a578e9a8029b255ef11179303c1335af7db80ea574488c4195eb259e9dd1b85a9a45eef8a541e4e03a2a4c6a87af63bfd7fb2fe9cf66060f7

attack_exo_2(N, e , Nbis , ebis)		

