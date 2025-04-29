from Crypto.Hash import SHA256
import random
import time
import sys

def hash(input):
    sha = SHA256.new()

    # left pad so bits are divisible by 8
    if (len(input) % 8 != 0):
        dif = 8 - (len(input) % 8)
        input = ("0" * dif) + input

    to_int = int(input, 2)
    sha.update(to_int.to_bytes(len(input) // 8, byteorder="big"))

    print(sha.hexdigest())

def modified_hash(input, size):
    sha = SHA256.new()

    # left pad so bits are divisible by 8
    if (len(input) % 8 != 0):
        dif = 8 - (len(input) % 8)
        input = ("0" * dif) + input

    to_int = int(input, 2)
    sha.update(to_int.to_bytes(len(input) // 8, byteorder="big"))

    int_val = int.from_bytes(sha.digest())

    return bin(int_val)[2:2+size]

def find_collision(size):
    table = dict()
    count = 0
    start_time = time.perf_counter()

    while 1:
        rand_int = random.randint(0, sys.maxsize)
        to_binary = bin(rand_int)[2:]
        hash = modified_hash(to_binary, size)

        if hash in table and table[hash] != to_binary:
            execution_time = time.perf_counter() - start_time
            print(f"Collision found in first {size} bits!")
            print(f" - {to_binary} ({int(to_binary, 2)}) and {table[hash]} ({int(table[hash], 2)})")
            print(f" - iterations: {count}")
            print(f" - time: {execution_time:.4f} seconds")
            break
        else:
            table[hash] = to_binary
            count += 1

def main():
    hash("000110101")
    hash("000110100")

    hash("1110110")
    hash("1111110")

    hash("000000")
    hash("000001")

    modified_hash("1100011111", 10)
    modified_hash("1100011111", 9)

    for i in range(8, 52, 2):
        find_collision(i)

main()