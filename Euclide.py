def gcd(a, b):
	"""
	fast gcd
	"""
	while b != 0:
		a, b = b, a % b
	return a

def euclide_algorithm (a: int, b: int) -> dict :
	"""
	Extended Euclide's algorithm
	Compute the PGCD from two integers and return the Bezout's relation elements
	
	Entry : two integers A and B
	Return : a dict ( "PGCD" , "U" , "V") 
	where r is the remind and u and v are the the coefficients of the Bezout's relation
	"""
	r1 = a
	r2 = b
	u1 = 1
	u2 = 0
	v1 = 0
	v2 = 1
	
	while (r2 != 0) :
		q = r1 // r2
		rt = r1
		ut = u1
		vt = v1
		r1 = r2
		u1 = u2
		v1 = v2
		r2 = rt - q * r2
		u2 = ut - q * u2
		v2 = vt - q * v2
	
	return { "PGCD":r1 , "U":u1 , "V":v1 }
