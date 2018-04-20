#!/usr/bin/python3.5
#-*- coding : utf-8 -*-


'''
Created on July 09, 2017
@author: Nabil Diab

Convertions of strings format to int blocks
'''


from Encoding.PKCS1 import *
import math
import binascii

opt_available = {"PKCS1" : unpad_PKCS1} #add the new padding options here

def encode(message , size_block=256, pad_option='pkcs1') -> int:
	"""
	Encoding function
	encode utf-8 strings to an hexadecimal blockpython
	
	Entries : 
		- message	: the string to encode
		- size_block	: the size of the output blocks (in bits)
		- pad_option	: the padding format (for now, only PKCS1 is available)
	"""

	if(type(message) == str):
		message = bytes(message,'utf-8')

	#convert size_block bit to byte
	bytes_block = size_block//8

	message = int(binascii.hexlify(message),16)

	# verify that the message length is not too large for the block size
	if ((math.ceil(math.log2(message))) > (size_block - 24)) :
		print("the given message is too large for one block, exited")
		return 1

	message = padding(message, bytes_block, pad_option)

	return message

def decode(message : int, pad_option='pkcs1') -> str :
	
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


def unpadding(message : int, size_block : int, pad_opt : int) -> int :
	"""
	Launch the unpadding 
	"""
	pad_opt = pad_opt.upper()

	if pad_opt not in opt_available :
		print("CRYPTO Error : ", pad_opt,"is not on the padding options, please choose one of these : ")
		for e in opt_available :
			print("\t\t* ",e)
		return -1

	return opt_available[pad_opt](message, size_block)
