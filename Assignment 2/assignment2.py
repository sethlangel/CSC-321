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
  ciphertext = cipher.encrypt(input)

  new_bmp = bmp_header + ciphertext

  write_bmp(new_bmp, "ECB_Final.bmp")

  reg_section1 = data[128:257]
  enc_section1 = ciphertext[128:257]
  print(reg_section1 == enc_section1)

orig_bmp = import_bmp()
bmp_header = orig_bmp[:55]
bmp_body = orig_bmp[55:]

#input = bmp_body.encode()
input = pkcs7(bmp_body)

aes_key = create_random_key()
aes_iv = create_random_iv()



#hmac = HMAC.new(hmac_key, digestmod=SHA256)
#tag = hmac.update(cipher.nonce + ciphertext).digest()

#with open("encrypted.bin", "wb") as f:
 #   f.write(tag)
 #   f.write(cipher.nonce)
 #   f.write(ciphertext)