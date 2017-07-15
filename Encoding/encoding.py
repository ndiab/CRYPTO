#!/usr/bin/python3.5
#-*- coding : utf-8 -*-


'''
Created on July 09, 2017
@author: Nabil Diab

Convertions strings to int blocks
'''


from Encoding.PKCS1 import *
import math
import binascii

def encode(message : str, size_block : int, pad_option : str) -> int:
	"""
	Encoding function
	encode utf-8 strings to an hexadecimal block
	
	Entries : 
		- message	: the string to encode
		- size_block	: the size of the output blocks (in bits)
		- pad_option	: the padding format (for now, only PKCS1 is available)

	For the moment, only one block can be generated from this function. Then only strings who can be 		
	represented by a hex block smaller than the size_block can be represented.
	More padding options will be available in the future.
	"""

	#convert size_block bit to byte
	size_block = size_block//8

	message = bytes(message,'utf-8')

	message = int(binascii.hexlify(message),16)

	message = padding(message, size_block, pad_option)

	return message

def decode(message : int, pad_option : str) -> str :
	
	size_block = math.ceil(math.ceil(math.log2(message))/8)*8
	
	message = unpadding(message, size_block, pad_option)

	message = binascii.unhexlify(hex(message)[2:])

	return str(message)[2:-1]


def padding(message : int, size_block : int, pad_opt : str) -> int :
	"""
	Launch the padding choosen.
	"""
	pad_opt = pad_opt.upper()

	opt_available = {"PKCS1" : PKCS1} #add the new padding options here

	if pad_opt not in opt_available :
		print("CRYPTO Error : ", pad_opt,"is not on the padding options, please choose one of these : ")
		for e in opt_available :
			print("\t\t* ",e)
		return -1

	return opt_available[pad_opt](message, size_block)


def unpadding(message : int, size_block, pad_opt : int) -> int :
	"""
	Launch the unpadding 
	"""
	pad_opt = pad_opt.upper()

	opt_available = {"PKCS1" : unpad_PKCS1} #add the new padding options here

	if pad_opt not in opt_available :
		print("CRYPTO Error : ", pad_opt,"is not on the padding options, please choose one of these : ")
		for e in opt_available :
			print("\t\t* ",e)
		return -1

	return opt_available[pad_opt](message, size_block)




