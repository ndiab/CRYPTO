#!/usr/bin/python3.5
#-*- coding : utf-8 -*-


'''
Created on July 13, 2017
@author: Nabil Diab

PKCS1 padding
'''

import math
import binascii

def PKCS1(message : int, size_block : int) -> int:
	"""
	PKCS1 padding function
	the format of this padding is :
	
	0x02 | 0x00 | [0xFF...0xFF] | 0x00 | [message]
	"""
	# compute the length in bytes of the message
	length = math.ceil(math.ceil(math.log2(message-1)) / 8)

	template = "0200"
	
	# generate a template 0xFFFFF.....FF of size_block bytes
	for i in range(size_block-2):
		template = template + 'FF'
	template = int(template,16)

	# Add the 00 of the end of the padding to the template
	for i in range(length+1) :
		template = template ^ (0xFF << i*8)

	# add the padding to the original message
	message = message | template
	
	return message
	

def unpad_PKCS1(message : int, size_block : int) -> int:
	"""
	PKCS1 unpadding function
	"""

	pts = 0xff << (size_block - 24)

	while (pts & message != 0):
		pts = pts >> 8
	
	a = ~pts & ((1 << size_block) - 1)

	message = message & (~pts & ((1 << math.ceil(math.log2(pts))) - 1) )

	return message



