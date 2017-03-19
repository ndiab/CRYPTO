'''
Created on Feb 03, 2017
@author: Nabil Diab
    
'''

import unittest
from random import randint
from IDEA import *


class IDEATest(unittest.TestCase):
	""" Test case used for test the Idea cryptographic system """
	
	def test_block_encryption(self):
		I = IDEA()
		m = randint(0,235)
		c = I.encrypt_block(m)
		d = I.decrypt_block(c)
		self.assertEqual(m,d)


if __name__ == '__main__' :
		unittest.main()
