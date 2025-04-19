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

def verify(key, iv, cyphertext) -> bool:
  cipher = AES.new(key, AES.MODE_CBC, iv)
  decrypted = cipher.decrypt(cyphertext)
  return decrypted.find(b";admin=true;") != -1

def bit_flipping_attack(key, iv):
  user_input = "X" * 32
  cyphertext = submit(key, iv, user_input)

  blocks = []
  for i in range(0, len(cyphertext), AES.block_size):
    blocks.append(cyphertext[i:i + AES.block_size])

  cipher = AES.new(key, AES.MODE_CBC, iv)
  decrypted = cipher.decrypt(cyphertext)
  decrypted = unpad(decrypted, AES.block_size)
  
  decrypted_blocks = []
  for i in range(0, len(decrypted), AES.block_size):
    decrypted_blocks.append(decrypted[i:i + AES.block_size])

  target_block_index = 1
  block_to_modify = target_block_index - 1
  original_plaintext_block = decrypted_blocks[target_block_index]

  target_text = ";admin=true;"
  padded_target = pkcs7(target_text.encode("utf-8"))

  xor_mask = xor(original_plaintext_block, padded_target)

  modified_block = xor(blocks[block_to_modify], xor_mask)

  modified_cyphertext = b"".join(blocks[:block_to_modify]) + modified_block + b"".join(blocks[target_block_index:])

  return modified_cyphertext


def main():
  # AES key & IV
  key = create_random_key()
  iv = create_random_iv()

  # Import the image
  orig_bmp = import_bmp()
  bmp_header = orig_bmp[:55]
  bmp_body = orig_bmp[55:]

  # ECB decryption
  ecb_bmp = bmp_header + ecb_encryption(key, bmp_body)
  write_bmp(ecb_bmp, "ECB_Final.bmp")

  # CBC decryption
  cbc_bmp = bmp_header + cbc_encryption(key, iv, bmp_body)
  write_bmp(cbc_bmp, "CBC_Final.bmp")

  # Bitflip attack
  modified_cyphertext = bit_flipping_attack(key, iv)
  success = verify(key, iv, modified_cyphertext)
  
  # Decrypt bitflip
  cipher = AES.new(key, AES.MODE_CBC, iv)
  decrypted = cipher.decrypt(modified_cyphertext)
  decrypted = unpad(unpad(decrypted, AES.block_size), AES.block_size)
  print(decrypted)
  print("Bitflip attack successful:", success)
  
main()