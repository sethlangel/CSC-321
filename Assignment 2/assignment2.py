import os
from Crypto.Cipher import AES

def import_bmp():
  with open("mustang.bmp", 'rb') as f:
    return f.read()
  
def write_bmp(data, filename):
  with open(filename, 'wb') as f:
    return f.write(data)

def create_random_key():
  return os.urandom(16)

def create_random_iv():
  return os.urandom(16)

def pkcs7(input):
  padding_len = 128 - (len(input) % 128)
  padding = bytes([padding_len] * padding_len)
  return input + padding

def ecb_encryption(key, iv, data):
  cipher = AES.new(aes_key, AES.MODE_ECB)
  padded_data = pkcs7(data)
  ciphertext = b""

  for i in range(0, len(padded_data), AES.block_size):
    block = padded_data[i:i + AES.block_size]
    encrypted_block = cipher.encrypt(block)
    ciphertext += encrypted_block

  new_bmp = bmp_header + ciphertext

  write_bmp(new_bmp, "ECB_Final.bmp")

def cbc_encryption(key, iv, data):
  cipher = AES.new(aes_key, AES.MODE_ECB)
  
orig_bmp = import_bmp()
bmp_header = orig_bmp[:55]
bmp_body = orig_bmp[55:]

#input = bmp_body.encode()
input = pkcs7(bmp_body)

aes_key = create_random_key()
aes_iv = create_random_iv()

ecb_encryption(aes_key, aes_iv, bmp_body)

#hmac = HMAC.new(hmac_key, digestmod=SHA256)
#tag = hmac.update(cipher.nonce + ciphertext).digest()

#with open("encrypted.bin", "wb") as f:
 #   f.write(tag)
 #   f.write(cipher.nonce)
 #   f.write(ciphertext)