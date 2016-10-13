import unittest
from Euclide import *
from Mint import *



class EuclideTest(unittest.TestCase):
	""" Test case used for test the Euclide's functions """
	
	def test_euclide_algorithm(self):
		""" Test if the euclide_algorithm working """
		a = 654987452
		b = 165496
		res = euclide_algorithm(a,b)
		self.assertEqual({ "PGCD":4 , "U":-8109 , "V":32093182 } , res)

	def test_mint_fast_exp(self):
		""" Test the fast exponentiation of a mint """
		m = Mint(41,527)
		m.fast_exp(37)
		self.assertEqual( 113, m.value)
		

if __name__ == '__main__' :
		unittest.main()
		
