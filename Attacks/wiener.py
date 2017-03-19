def Wiener(N : int, e : int) -> int :
	"""
	Wiener Attack
	return the private key if it's vulnerable
	if not, return 0
	(need cont_frac, fraq_seq, isqrt)
	"""
	
	#1 - initialize the list of partial quotients
	quot = cont_frac(e,N)
	
	#2 - initialize a list of continued fractions
	seq = frac_seq(quot)

	#check if d is actually the key
	for (k,d) in seq :
		# Now we are going to check if the couple (k,d)
		# produce a factorization of N (p * q)
		
		if k == 0:
			continue

		# compute phi
		# phi(N) = (ed - 1)/ k
		phi = (e * d - 1) // k
		
		# Now from phi and N we can deduce the eventual factorization
		# by solving the equation : x^2 - ((N-phi)+1)x + N
		a = 1
		b = (N - phi) + 1
		c = N
		
		discr = b*b - 4 * a * c
	
		# in that case we got solutions to the equation
		if discr > 0 :
			# to works, the solutions must be integers
			# first, the root of the discriminent must be integer 
			rdiscr = isqrt(discr)

			if (rdiscr * rdiscr) == discr :
				#the root of the discr is integer, we compute the solutions 
				p = -((-b - rdiscr) // (2 * a))
				q = -((-b + rdiscr) // (2 * a))
				if N == (p * q) :
					print("Hacked")
					return d

	print("Not vulnerable to Wiener")

	return 0

