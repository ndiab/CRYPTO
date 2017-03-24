'''
Created on Mar 24, 2017
@author: Nabil Diab
    
'''

from Asymetric import RSA, RSA_CRT, User
from Arithmetic.arith import *


def broadcast_attack(L : list) -> int :
	"""
	Perform the broadcast attack from a list of message
	each message is represented as a tuple (c, N, e)
	with : * c = cipher
	       * N = modulus
	       * e = public key
	"""	

	# 1 - Verify the broadcast attack conditions
	pk = L[1][2]
	S = []
	assert  pk <= len(L), "Can't perform the broadcast attack with these conditions : too few ciphers"
	for (c,N,e) in L :
		assert pk == e, "Can't perform the broadcast attack with these conditions : the public keys are not the same"
		S.append(Mint(c,N))
	

	# 2 - CRT between the messages
	C = CRT_list(S)
	x = C.value

	
	m = find_invpow(x,3)


	return m
