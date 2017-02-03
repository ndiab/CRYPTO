'''
Created on Oct 13, 2016
@author: Nabil Diab
    
'''

import unittest
from Arith import *
from RSA import *
from random import *
from RSA_CRT import *
from Attacks import *
from User import *



class ArithTest(unittest.TestCase):
	""" Test case used for test the Arithmetics functions """
	
	def test_euclide_algorithm(self):
		""" Test if the euclide_algorithm working """
		print("euclide test ...")
		a = 654987452
		b = 165496
		res = euclide_algorithm(a,b)
		self.assertEqual({ "PGCD":4 , "U":-8109 , "V":32093182 } , res)

	def test_CRT(self):
		"""Test the Chiness Remainder Theorem"""
		print("CRT test ... ")
		a = Mint(3,7)
		b = Mint(5,11)
		x = CRT(a,b)
		self.assertEqual((38,77),(x.value,x.mod))

	def test_CRT_list(self):
		"Test the multi Chiness Remainder Theorem"
		print("CRT list test ... ")
		a = Mint(3,7)
		b = Mint(5,11)
		c = Mint(8,13)
		d = Mint(4,5)
		e = Mint(14,17)
		f = Mint(2,3)
		g = Mint(1,19)
		l = [a,b,c,d,e,f,g]
		x = CRT_list(l)
		self.assertEqual((2140484,4849845),(x.value, x.mod))

	def test_BSGS(self):
		""" test the baby Step Giant Step """
		print("Baby Step Giant Step Test ...")
		i = randint(1,len(prime_tab)-1)
		j = randint(0,i-1)
		N = prime_tab[i] #choose a prime number
		e = prime_tab[j]
		m = randint(0,N-1)
		c = Mint(m,N)
		c.fast_exp(e)
		c.fast_exp(BSGS(c.value,m,N))
		self.assertEqual(c.value,m)
		

class MintTest(unittest.TestCase):
	""" Test case used for test the Mint's functions """

	def test_mint_fast_exp(self):
		""" Test the fast exponentiation of a mint """
		print("Fast exponentiation test ...")
		m = Mint(41,527)
		m.fast_exp(37)
		self.assertEqual( 113, m.value)

class RSATest(unittest.TestCase):
	""" Test case used for test the RSA's functions """
	
	#def test_keys_1(self):
	#	""" Test if e * d = 1 mod phi"""
	#	print("key test 1 ...")
	#	test = RSA()
	#	ed = (test.e * test.d)% test.phi
	#	self.assertEqual( 1, ed)

	def test_encryption(self):
		"""Test if the encryption works correctly"""
		print("test encryption (RSA) ...")
		test = RSA()
		n = randint(1,100000)
		a = test.encrypt(n)
		b = test.decrypt(a)
		self.assertEqual(n,b)

class RSA_CRTTest(unittest.TestCase):
	""" Test case used for test the RSA's functions """

	#def test_keys_1(self):
	#	""" Test if e * d = 1 mod phi"""
	#	print("key test 2 ...")
	#	test = RSA()
	#	ed = (test.e * test.d)% test.phi
	#	self.assertEqual( 1, ed)

	def test_encryption(self):
		"""Test if the encryption works correctly"""
		print("test encryption (RSA-CRT) ...")
		test = RSA_CRT()
		n = randint(1,100000)
		a = test.encrypt(n)
		b = test.decrypt(a)
		self.assertEqual(n,b)

class AttacksTest(unittest.TestCase):
	""" Test case used for test the RSA's functions """
	
	def test_bellcore_attack(self):
		""" Test the Bellcore attack """
		print("test Bellcore attack ...")
		victim = RSA_CRT()
		cipher = victim.encrypt(randint(0,victim.n))
		secret = Bellcore_attack(victim,cipher)
		self.assertEqual(True,victim.is_private_key(secret))

	def test_broadcast_attacks(self):
		""" test the broadcast attack """
		print("test the broadcast attack")
		u = User()
		u.force_public_key(3)
		s1 = copy(u)
		m1 = (u.get_message(),u.rsa.n,u.rsa.e)
		u.change_modulus()
		s2 = copy(u)
		m2 = (u.get_message(),u.rsa.n,u.rsa.e)
		u.change_modulus()
		s3 = copy(u)
		m3 = (u.get_message(),u.rsa.n,u.rsa.e)

		L = [m1,m2,m3]
		m = broadcast_attack(L)
		
		self.assertEqual(True,u.verify_message(m))
		

		
		

class UserTest(unittest.TestCase):
	""" Test case for the User Class """
	
	def test_user_encryption(self):
		""" test the user class """
		print("test the user class : encryption")
		u = User()
		self.assertEqual(u.verify_message(u.rsa.decrypt(u.get_message())),True)
		
	def test_user_new_pk(self):
		""" test the user class """
		print("test the user class : new public key")
		u = User()
		u.force_public_key(3)
		self.assertEqual(u.rsa.e,3)
		self.assertEqual(u.verify_message(u.rsa.decrypt(u.get_message())),True)
		

if __name__ == '__main__' :
		unittest.main()
		
