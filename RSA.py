import gmpy2
import rsa

p =
q =
n =
e =
d = int(gmpy2.invert(e, (p - 1) * (q - 1)))

private_key = rsa.PrivateKey(n, e, d, p, q)

with open("encrypted.message", "rb") as f:
    print(rsa.decrypt(f.read(), private_key).decode())
