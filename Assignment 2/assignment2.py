import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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
  padding_len = AES.block_size - (len(input) % AES.block_size)
  padding = bytes([padding_len] * padding_len)
  return input + padding

def xor(input1, input2):
  return bytes(a ^ b for a, b in zip(input1, input2))

def ecb_encryption(key, data):
  cipher = AES.new(key, AES.MODE_ECB)
  padded_data = pkcs7(data)
  ciphertext = b""

  for i in range(0, len(padded_data), AES.block_size):
    block = padded_data[i:i + AES.block_size]
    encrypted_block = cipher.encrypt(block)
    ciphertext += encrypted_block

  return ciphertext

def cbc_encryption(key, iv, data):
  cipher = AES.new(key, AES.MODE_ECB)
  padded_data = pkcs7(data)
  ciphertext = b""

  for i in range(0, len(padded_data), AES.block_size):
    block = padded_data[i:i + AES.block_size]

    if i == 0:
      prev_block = iv
    else:
      prev_block = ciphertext[i - AES.block_size:i]
      
    block = xor(block, prev_block)

    encrypted_block = cipher.encrypt(block)
    ciphertext += encrypted_block

  return ciphertext

def submit(key, iv, input):
  encoded = input.replace(";", "%3D").replace("=", "%2B")
  whatever = "userid=456;userdata=" + encoded + ";session-id=31337"
  whatever = pkcs7(whatever.encode("utf-8"))
  return cbc_encryption(key, iv, whatever)
  
orig_bmp = import_bmp()
bmp_header = orig_bmp[:55]
bmp_body = orig_bmp[55:]

input = pkcs7(bmp_body)

aes_key = create_random_key()
aes_iv = create_random_iv()
# aes_key = b'1234567899999999'
# aes_iv = b'6969696969696969'

ecb_bmp = bmp_header + ecb_encryption(aes_key, bmp_body)
write_bmp(ecb_bmp, "ECB_Final.bmp")

cbc_bmp = bmp_header + cbc_encryption(aes_key, aes_iv, bmp_body)
write_bmp(cbc_bmp, "CBC_Final.bmp")

encrypted = submit(aes_key, aes_iv, "woohoo")
#print(encrypted)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
decrypted = cipher.decrypt(encrypted)
# for some reason, cipher.decrypt pads it again. so must unpad twice?
decrypted = unpad(unpad(decrypted, AES.block_size), AES.block_size)
print(decrypted)