import unittest
from Arith import *
from Mint import *
from RSA import *



class EuclideTest(unittest.TestCase):
	""" Test case used for test the Euclide's functions """
	
	def test_euclide_algorithm(self):
		""" Test if the euclide_algorithm working """
		print("euclide test ...")
		a = 654987452
		b = 165496
		res = euclide_algorithm(a,b)
		self.assertEqual({ "PGCD":4 , "U":-8109 , "V":32093182 } , res)

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
	
	def test_keys_1(self):
		""" Test if e * d = 1 mod phi"""
		print("key test 1 ...")
		test = RSA()
		ed = (test.e * test.d)% test.phi
		self.assertEqual( 1, ed)
		

if __name__ == '__main__' :
		unittest.main()
		
