############################
#         ecdsa.py         #
############################

# Source : https://github.com/Y0a0bon/crypto/blob/dev/ecdsa.py

import os, sys
import math, random
from Asymetric.Arith import *
import hashlib


class ECDSA_key:
    """ ECDSA_key class
    """

    def __init__(self, p, a, b, h, n, G):
        """ Constructor """
        if(is_prime(p) ==  False):
            print("Error : You have chosen a non prime number for p")
        if(is_prime(n) ==  False):
            print("Error : You have chosen a non prime number for n")
        if(n < (1<<160)):
            print("Warning : n should be greater than 2^160")
        # Initialize variables #
        self.G = [] # (coordinates (g_x, g_y)) #
        self.G = G
        self.n = n
        self.p = p
        self.a = a
        self.b = b
        self.h = h        

    """ Methods """
    def get_pkey(self):
        return self.Q

    def get_gen(self):
        return self.G

    def get_n(self):
        return n

    def _get_skey(self):
        return self._s

    def _set_skey(self, s):
        self._s = s

    def set_pkey(self, Q):
        self.Q = Q

    s = property(_get_skey)
    s = property(_set_skey)

    #
    # Return if the point lies on the elliptic curve
    #
    def is_on_curve(self, point):
        if point is None:
            # None represents the point at infinity.
            return True
        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    #
    # Return neg point
    #
    def neg_point(self, point):
        assert self.is_on_curve(point)
        if point is None:
            # -0 = 0
            return None
        x, y = point
        result = (x, -y % curve.p)
        assert self.is_on_curve(result)
        return result

    #
    # Add 2 points according to the group
    #
    def point_add(self, point1, point2):
        
        assert self.is_on_curve(point1)
        assert self.is_on_curve(point2)

        if point1 is None:
            # 0 + point2 = point2
            return point2
        if point2 is None:
            # point1 + 0 = point1
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            # point1 + (-point1) = 0
            return None
        if x1 == x2:
            # This is the case point1 == point2.
            m = (3 * x1 * x1 + self.a) * self.mod_inv_ecdsa(2 * y1, self.p)
        else:
            m = (y1 - y2) * self.mod_inv_ecdsa(x1 - x2, self.p)
        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % self.p,
                  -y3 % self.p)
        assert self.is_on_curve(result)
        return result

    #
    # Return k * point
    #
    def scalar_mult(self, k, point):
        assert self.is_on_curve(point)
        if k % self.get_n() == 0 or point is None:
            return None
        if k < 0:
            # k * point = -k * (-point)
            return self.scalar_mult(-k, self.point_neg(point))
        result = None
        addend = point
        while k:
            if k & 1:
                # Add.
                result = self.point_add(result, addend)
            # Double.
            addend = self.point_add(addend, addend)
            k >>= 1
        assert self.is_on_curve(result)
        return result


    #
    # Generate key
    #
    def generate_key(self):
        random.seed()
        self._set_skey(random.randrange(1, self.get_n()-1))
        self.set_pkey(self.scalar_mult(self._get_skey(), self.get_gen()))

    #
    # Sign m with ECDSA
    #
    def sign(self,m):
        r , t = 0 , 0 # t is s in the paper #
        # calculated truncated hash of m #
        z = self.hashed(m)
        # r != 0 #
        while(not r or not t):
            # Take random int between 1 and n-1 #
            k = random.randrange(1, self.get_n()-1)
            # P = k*G #
            x, y = self.scalar_mult(k, self.get_gen())
            # r = x_P mod n  #
            r = x % self.get_n()
            # t = k^-1(z+r*d_A) mod n #
            t = self.mod_inv_ecdsa(k, self.get_n())*(z+r*self._get_skey()) % self.get_n()
        return (r, t)
            
    #
    # Verify signature Sgn
    #
    def verify(self, Sgn, m):
        # u1 = t^-1*z mod n #
        # u2 = t^-1*r mod n #
        z = self.hashed(m)
        r,s = Sgn
        t_inv = self.mod_inv_ecdsa(s, self.get_n())
        u1 = t_inv * z % self.get_n()
        u2 = t_inv * r % self.get_n()
        # P = u1 * G + u2 * Q
        x, y = self.point_add(self.scalar_mult(u1, self.get_gen()),
                     self.scalar_mult(u2, self.get_pkey()))
        if (r % self.get_n()) == (x % self.get_n()):
            return 'signature matches'
        else:
            return 'invalid signature'

    #
    # Hash function
    #
    def hashed(self, m):
        message_hash = hashlib.sha512(m).digest()
        e = int.from_bytes(message_hash, 'big')

        # FIPS 180 says that when a hash needs to be truncated, the rightmost bits
        # should be discarded.
        z = e >> (e.bit_length() - self.get_n().bit_length())

        assert z.bit_length() <= self.get_n().bit_length()

        return z

    #
    # Mod_inv for ECDSA
    #
    def mod_inv_ecdsa(self, k, p):
        if k == 0:
            raise ZeroDivisionError('division by zero')
        if k < 0:
            # k ** -1 = p - (-k) ** -1  (mod p)
            return p - self.mod_inv_ecdsa(-k, p)

        # Extended Euclidean algorithm.
        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = p, k

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        gcd, x, y = old_r, old_s, old_t

        assert gcd == 1
        assert (k * x) % p == 1

        return x % p


"""
def verify(c, sig):
        if(self.Q == O): # /!\ verify that it's not the infinite point (not 0...)
            print("Doesn't match")
            return False
        if(self.n*self.Q != O): # /!\ Same
            print("Dosen't match")
            return False
        if(sig[1] == 0 or y == 0 or sig[1]>n-1 or sig[2]>n-1):
            print("Dosen't match")
            return False
        (i,j)=(hashed(c)/sig[2] % self.n)*self.G + (sig[1]/sig[2] % self.n)*self.Q
        if(sig[1] != i % self.n):
            print("Doesn't match")
            return False
        print("OK")
        return True
"""

# Parameters
p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a=0
b=7
x_G=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
y_G=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
h=1
G=[x_G, y_G]


E = ECDSA_key(p,a,b,h,n,G)
E.sign(17)
