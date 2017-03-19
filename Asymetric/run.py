from ECC import *
from IDEA import *

#E = ECC(2,3,97)
#P = Point(3,6)

#E.mul(P,0)
#print("----------- 1 ")
#E.mul(P,1)
#print("----------- 2 ")
#E.mul(P,2)
#print("----------- 3 ")
#E.mul(P,3)
#print("----------- 4 ")
#E.mul(P,4)
#print("----------- 5 ")
#E.mul(P,5)
#print("----------- 6 ")
#E.mul(P,6)
#print("----------- 7 ")
#E.mul(P,7)
#print("----------- 8 ")
#E.mul(P,8)


#print("external tests")
#print(E.add(Point(3,91),Point(3,6)).to_string())

I = IDEA()
n = 0xf46e54231965a45c
print("clear : ", hex(n))
c = I.encrypt_block(n)
print("crypted : ", hex(c))
d = I.decrypt_block(c)
print("decrypted : ", hex(d))


