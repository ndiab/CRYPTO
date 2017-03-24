'''
Created on Oct 30, 2016
@author: Nabil Diab
    
'''

from Asymetric import RSA
from random import *


class User :
	"""
	Representation of an user
	contain the RSA keys and the private message
	"""

	
	def __init__(self):
		self.rsa = RSA()
		self.__message = randint(1<<900,1<<1000)	
	
	def get_message(self) -> int:
		cipher = self.rsa.encrypt(self.__message)
		return cipher

	def verify_message(self, clear : int) -> int:
		return (clear == self.__message)

	def force_public_key(self, new_e : int) :
		"""
		try to force to get a new couple (public key, private key) with the current RSA
		if it's not possible, it regenerates new a new RSA context untill find a working couple
		"""
		while(not (self.rsa.force_public_key(new_e))):
			self.rsa = RSA()

	
	
	def change_modulus(self):
		"""
		Change all the keys of RSA except the public key
		"""
		e = self.rsa.e
		self.rsa = RSA()
		self.force_public_key(e)
