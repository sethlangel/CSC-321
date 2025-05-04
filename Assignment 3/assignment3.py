from hashlib import sha256
import os
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
import math

def pkcs7(input):
  padding_len = AES.block_size - (len(input) % AES.block_size)
  padding = bytes([padding_len] * padding_len)
  return input + padding

def dh_key_exhange_alice_and_bob(q, a):
    alice_int = 5
    bob_int = 4

    alice_key = pow(a, alice_int) % q
    bob_key = pow(a, alice_int) % q

    alice_s = pow(bob_key, alice_int) % q
    bob_s = pow(alice_key, bob_int) % q

    alice_k = sha256(str(alice_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]

    bob_k = sha256(str(bob_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]
    
    alice_message = "Hi Bob!"
    alice_message = pkcs7(alice_message.encode('utf-8'))
    bob_message = "Hi Alice!"
    bob_message = pkcs7(bob_message.encode('utf-8'))

    iv = os.urandom(16)
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)

    alice_cipher_text = alice_cipher.encrypt(alice_message)
    bob_cipher_text = bob_cipher.encrypt(bob_message)
    print("----Bob and Alice----\n")
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)

    print(alice_cipher.decrypt(alice_cipher_text))
    print(bob_cipher.decrypt(bob_cipher_text), '\n')

def dh_key_exchange_alice_bob_and_mallory_key_tamper(q, a):
    alice_int = 5
    bob_int = 4

    alice_s = pow(q, alice_int) % q
    bob_s = pow(q, bob_int) % q

    alice_k = sha256(str(alice_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]

    bob_k = sha256(str(bob_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]
    
    alice_message = "Hi Bob!"
    alice_message = pkcs7(alice_message.encode('utf-8'))
    bob_message = "Hi Alice!"
    bob_message = pkcs7(bob_message.encode('utf-8'))

    iv = os.urandom(16)
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)

    alice_cipher_text = alice_cipher.encrypt(alice_message)
    bob_cipher_text = bob_cipher.encrypt(bob_message)
    print("----Bob, Alice and Mallory | Key Tamper----\n")
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)
    mallory_alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    mallory_bob_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    print("---Alice---")
    print(alice_cipher.decrypt(alice_cipher_text))
    print("---Bob---")
    print(bob_cipher.decrypt(bob_cipher_text))
    print("---Mallory---")
    print(mallory_alice_cipher.decrypt(alice_cipher_text))
    print(mallory_bob_cipher.decrypt(bob_cipher_text))

def dh_key_exchange_alice_bob_and_mallory_a_tamper(q, a):
    alice_int = 5
    bob_int = 4

    alice_key = pow(0, alice_int) % q
    bob_key = pow(0, alice_int) % q


    alice_s = pow(alice_key, alice_int) % q
    bob_s = pow(bob_key, bob_int) % q

    alice_k = sha256(str(alice_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]

    bob_k = sha256(str(bob_s).encode('utf-8')).hexdigest().encode('utf-8')[:16]
    
    alice_message = "Hi Bob!"
    alice_message = pkcs7(alice_message.encode('utf-8'))
    bob_message = "Hi Alice!"
    bob_message = pkcs7(bob_message.encode('utf-8'))

    iv = os.urandom(16)
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)

    alice_cipher_text = alice_cipher.encrypt(alice_message)
    bob_cipher_text = bob_cipher.encrypt(bob_message)
    print("----Bob, Alice and Mallory | Alpha Tamper----\n")
    alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    bob_cipher = AES.new(bob_k, AES.MODE_CBC, iv=iv)
    mallory_alice_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    mallory_bob_cipher = AES.new(alice_k, AES.MODE_CBC, iv=iv)
    print("---Alice---")
    print(alice_cipher.decrypt(alice_cipher_text))
    print("---Bob---")
    print(bob_cipher.decrypt(bob_cipher_text))
    print("---Mallory---")
    print(mallory_alice_cipher.decrypt(alice_cipher_text))
    print(mallory_bob_cipher.decrypt(bob_cipher_text))

def rsa(message):
    p = getPrime(2048)
    q = getPrime(2048)

    n = p * q
    phi = math.lcm(p - 1, q - 1)
    e = 65537

    d = pow(e, -1, phi)

    m = int(message.encode('utf-8').hex(), 16)

    c = pow(m, e, n)
    decrypt = pow(c, d, n)
    decrypted_message = bytes.fromhex(hex(decrypt)[2:]).decode('utf-8')

    # print("m", m)
    # print("c", c)
    # print("decrypt", decrypt)
    print(decrypt)

    c_prime = c * pow(2, e, n) % n
    decrypt2 = pow(c_prime, d, n)
    #decrypted2_message = bytes.fromhex(hex(decrypt2)[2:]).decode('utf-8')

    print(decrypt2)



def main():
    # q = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
    # a = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)

    # dh_key_exhange_alice_and_bob(q, a)
    # dh_key_exchange_alice_bob_and_mallory_key_tamper(q, a)
    # dh_key_exchange_alice_bob_and_mallory_a_tamper(q,a)

    rsa("message")

if __name__ == "__main__":
    main()
