import os
import time
from nltk.corpus import words
import multiprocessing
import bcrypt
import ssl

# import nltk
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('words')

def crack_chunk(word_chunk, full_hash, result_queue):
    for index, word in enumerate(word_chunk):
        if bcrypt.checkpw(word.encode(), full_hash.encode()):
            result_queue.put(word)
            break

def main():
    words_list = [w.lower() for w in words.words()]
    filtered_words = [word for word in words_list if 6 <= len(word) <= 10]

    num_cores = multiprocessing.cpu_count()
    chunk_size = len(filtered_words) // num_cores
    chunks = [filtered_words[i:i + chunk_size] for i in range(0, len(filtered_words), chunk_size)]

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'shadow.txt')

    with open(file_path, 'r') as f:
        while (file := f.readline().strip()):
            user = file.split(":")[0]
            algorithm = file.split("$")[1]
            workfactor = file.split("$")[2]
            salt = file.split("$")[3][:22]
            hash = file.split("$")[3][22:]

            complete_hash = file.split(":")[1]
            print(f"Cracking password for {user} with {num_cores} processes. Hash: {hash}")

            start = time.time()

            manager = multiprocessing.Manager()
            result_queue = manager.Queue()
            processes = []

            for chunk in chunks:
                p = multiprocessing.Process(target=crack_chunk, args=(chunk, complete_hash, result_queue))
                processes.append(p)
                p.start()

            found_password = None
            while True:
                if not result_queue.empty():
                    found_password = result_queue.get()
                    break
                if all(not p.is_alive() for p in processes):
                    break

            for p in processes:
                p.terminate()
                p.join()

            end = time.time()
            total_time = end - start

            if found_password:
                print(f"Password found for {user}: \"{found_password}\". Total time to crack password: {total_time:.2f} seconds.")
            else:
                print(f"Password not found for {user}. Total time: {total_time:.2f} seconds.")

if __name__ == '__main__':
    main()
