

from IDEA import *



I = IDEA()

n = 0x0001000055555555



c = I.encrypt_block(n)
d = I.decrypt_block(c)

print("cipher : ", hex(c))
print("clear : ", hex(d))
