'''
Created on Jan 30, 2017
@author: Nabil Diab
    
'''

from Arith import *


class Point:
	
	def __init__(self, a : int, b : int):
		self.x = a
		self.y = b

	def to_string(self) -> str:
		return "(" + str(self.x) + "," + str(self.y) + ")"

class ECC:
	"""
	ECC object
	"""

	def __init__(self, a, b, p):
		self.a = a
		self.b = b
		self.p = p


	def add(self, P : Point, Q : Point) -> Point :
		"""
		Elliptic curve addition
		Entry : two Point P and Q
		Return : P+Q
		"""
	
		#m <- slope of the line through P and Q
		if P.x == Q.x :
			m = mod_division(3 * (P.x**2) + self.a , 2 * P.y, self.p)
		else :
			m = mod_division(P.y - Q.y, P.x- Q.x, self.p)

		print(m)
	
		r_x = m * m - P.x - Q.x
		r_y = P.y + m * (r_x - P.x)

		R = Point(r_x % self.p, -r_y % self.p)

		return R


	def mul(self, P : Point, n : int) -> Point :
		"""
		Elliptic curve scalar multiplication
		Entry : * a point P
			* a scalar n
		Return : nP
		"""
		
		first = True
		tmp = Point(P.x, P.y)

		while n!= 0 :
			if n & 1 :
				if first :
					R = Point(tmp.x, tmp.y)
					first = False
				else :
					R = self.add(R,tmp)
			tmp = self.add(P,tmp)
			n = n>>1
			print("tmp : ", tmp.to_string())
			if not first:
				print(R.to_string())


		if first :
			return Point(0,0)

		return R
		



