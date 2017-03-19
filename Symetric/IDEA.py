#!/usr/bin/python3.5
#-*- coding : utf-8 -*-

'''
Created on Feb 03, 2017
@author: Nabil Diab

International Data Encryption Algorithm
'''

from random import randint
from operator import xor

class IDEA:
	
	modulo = 0xffff


	def __init__(self):
		# 1 - generate a key of 128 bits
		self.master_key = randint(1<<127,(1<<128)-1)
		# 2 - Compute all the 52 subkeys
		self.subkeys = self.__generate_subkeys()
		# 3 - generate the decryption keys
		self.decrypt_keys = self.__generate_decrypt_keys()


	def __generate_subkeys(self) -> list:
		"""
		Compute all the 52 subkeys of the system
		"""
		key = self.master_key
		L = []
		filt = 0xffff0000000000000000000000000000
		offset = 112
		
		
		for i in range (52) :
			L.append((key & filt) >> offset)
			filt = filt // 0x10000
			offset = offset - 16
			if offset < 0 :
				# 25 bits left rotation
				msb = (key & (0xffffff80000000000000000000000000)) >> 103 # msb = the 25 most significant bit
				key = ((key << 25)  | msb) & 0xffffffffffffffffffffffffffffffff
				filt = 0xffff0000000000000000000000000000
				offset = 112
		return L

	def __generate_decrypt_keys(self) -> list :
		K = []

		K.append(self.multinv(self.subkeys[48]))
		K.append((-(self.subkeys[49]))%(1<<16))
		K.append((-(self.subkeys[50]))%(1<<16))
		K.append(self.multinv(self.subkeys[51]))

		i = 7
		while i>= 1 :
			K.append(self.subkeys[i*6 + 4]) 	
			K.append(self.subkeys[i*6 + 5])
			
			K.append(self.multinv(self.subkeys[i*6]))
			K.append((-(self.subkeys[i*6 + 2]))%(1<<16))
			K.append((-(self.subkeys[i*6 + 1]))%(1<<16))
			K.append(self.multinv(self.subkeys[i*6 + 3]))

			i = i-1

		K.append(self.subkeys[i*6 + 4]) 	
		K.append(self.subkeys[i*6 + 5])
		
		K.append(self.multinv(self.subkeys[i*6]))
		K.append((-(self.subkeys[i*6 + 1]))%(1<<16))
		K.append((-(self.subkeys[i*6 + 2]))%(1<<16))
		K.append(self.multinv(self.subkeys[i*6 + 3]))

		return K
		

	def encrypt_block(self, message : int) -> int :
		"""
		encrypt one bloc of 64 bits
		"""

		if (message >= 1<<64):
			print("WARNING : the message is too large for a bloc, it has been truncated ")
			message = message & 0xffffffffffffffff

		X = self.__split_block(message)


		for i in range (8):
			X = self.__round(X,i, self.subkeys)

		X1,X3,X2,X4 = X
		
		X1 = self.mul(X1,self.subkeys[48]) #& self.modulo
		X2 = X2 + self.subkeys[49] & self.modulo
		X3 = X3 + self.subkeys[50] & self.modulo
		X4 = self.mul(X4,self.subkeys[51]) # & self.modulo

		res = self.join_subblocks((X1,X2,X3,X4))

		return res

	def decrypt_block(self, cipher : int) -> int :
		"""
		decrypt one bloc of 64 bits
		"""
		if (cipher >= 1<<64):
			print("ERROR : not valid cipher ")
			return -1

		X = self.__split_block(cipher)

		for i in range (8):
			X = self.__round(X,i, self.decrypt_keys)

		X1,X3,X2,X4 = X
		
		X1 = self.mul(X1,self.decrypt_keys[48])# & self.modulo
		X2 = X2 + self.decrypt_keys[49] & self.modulo
		X3 = X3 + self.decrypt_keys[50] & self.modulo
		X4 = self.mul(X4,self.decrypt_keys[51])# & self.modulo
		
		res = self.join_subblocks((X1,X2,X3,X4))

		return res

		

	def __round(self, X : tuple, n : int, key : list ) -> tuple :
		"""
		A round of IDEA
		Entry : * n : the round number (0 to 7)
			* X : the 4 quarter of the message
		Return : the 4 quarter of the message after the round
		"""
	
		X1,X2,X3,X4 = X
		
		X1 = self.mul(X1,key[n*6])   #  & self.modulo #1
		X2 = X2 + key[n*6 + 1] & self.modulo #2
		X3 = X3 + key[n*6 + 2] & self.modulo #3
		X4 = self.mul(X4,key[n*6 + 3])# & self.modulo #4

		
		A = xor(X1,X3)			     #5
		B = xor(X2,X4)			     #6


		A = self.mul(A,key[n*6 + 4]) #& self.modulo #7
		B = A + B 	       & self.modulo #8

		
		B = self.mul(B,key[n*6 + 5])# & self.modulo #9
		A = A + B	       & self.modulo #10

		
		X1 = xor(X1,B)			     #11
		X3 = xor(X3,B)			     #12
		X2 = xor(X2,A)			     #13
		X4 = xor(X4,A)			     #14

		return (X1,X3,X2,X4)		     #15 swap
		
		
	

	def __split_block(self, message : int) -> tuple :
		X4 = message & 0xffff
		X3 = (message & 0xffff0000) >> 16
		X2 = (message & 0xffff00000000) >> 32
		X1 = (message & 0xffff000000000000) >> 48
		return (X1,X2,X3,X4)

	def join_subblocks(self, X : tuple) -> int :
		"""
		gathers all the 4 subblocks of 16 bits to one of 64bits
		"""
		X1,X2,X3,X4 = X
		res = X4 | (X3 << 16) | (X2 << 32) | (X1 << 48)

		return res

	def print_keys(self):
		print("master key : ", hex(self.master_key))
		
		print("ENCRYPT KEYS")
		for i in range(len(self.subkeys)):
			print("key ",i, " : ",hex(self.subkeys[i]))

		print("DECRYPT KEYS")
		for i in range(len(self.decrypt_keys)):
			print("dec key ",i, " : ",hex(self.decrypt_keys[i]))
		
	def mul(self, a : int, b : int) -> int :
		a = a & self.modulo
		b = b & self.modulo
		p = a * b
		if p != 0 :
			b = p & self.modulo
			a = p >> 16
			res = b - a
			if b < a :
				res = res+ 1
			return res & self.modulo
		elif a != 0 :
			return 1 - b & self.modulo
		else :
			return 1 - a & self.modulo

	def multinv(self, x : int) -> int :
		
		if x <= 1 :
			return x

		t1 = 0x10001 // x
		y  = 0x10001 %  x

		if y == 1 :
			return (1 - t1) & self.modulo

		t0 = 1

		# extended euclide
		while y != 1 :
			q = x // y
			x = x %  y
			t0 = t0 + (q * t1)
			if x == 1 :
				return t0
			q = y // x
			y = y % x
			t1 = t1 + q * t0

		return (1 - t1) & self.modulo

