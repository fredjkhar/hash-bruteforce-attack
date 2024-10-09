"""
This script performs a dictionary attack against SHA1-hashed passwords stored in a password file.
It reads a list of user:hash pairs from an `.htpasswd`-formatted file and attempts to crack them
by comparing each hash against the SHA1 hashes of words from a given dictionary file.

- The script utilizes the `hashlib` library to compute SHA1 hashes.
- It encodes the resulting hashes in Base64 to match the format used in the password file.
- For each match, it prints out the cracked password along with the associated username.
- The script provides a summary at the end, including the number of words attempted and the total time taken.

Make sure to have both a password file (`htpasswd-sha1-task2`) and a dictionary file (`rockyou.txt`) in the same data directory.
"""
import hashlib
import base64
import time

# Function to hash the dictionary word using SHA1 and encode in base64
def hash_sha1(word):
    return base64.b64encode(hashlib.sha1(word.encode('utf-8')).digest()).decode('utf-8')

# Function to read the password file and store user:hash pairs
def read_password_file(filename):
    passwords = {}
    with open(filename, 'r') as file:
        for line in file:
            user, hashed_password = line.strip().split(':')
            passwords[user] = hashed_password.replace("{SHA}", "")
    return passwords

# Function to attempt cracking the passwords using a dictionary file
def dictionary_attack(password_file, dictionary_file):
    passwords = read_password_file(password_file)
    cracked = {}
    word_count = 0

    with open(dictionary_file, 'r', encoding='utf-8', errors='ignore') as dict_file:
        for word in dict_file:
            word = word.strip()
            word_count += 1
            hashed_word = hash_sha1(word)
            
            # Check if hashed word matches any stored hashed password
            for user in list(passwords.keys()):  
                if hashed_word == passwords[user]:
                    cracked[user] = word
                    print(f"Password for {user} is {word}")
                    del passwords[user]
            
                if len(passwords) == 0:
                    return cracked, word_count
    return cracked, word_count

# Main
if __name__ == "__main__":
    password_file = './data/htpasswd-sha1'
    dictionary_file = './data/rockyou.txt'

    start_time = time.time()
    cracked_passwords, words_attempted = dictionary_attack(password_file, dictionary_file)
    end_time = time.time()
    
    if cracked_passwords:
        print("Cracked passwords:", cracked_passwords)
    else:
        print("No passwords were cracked.")
    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Words attempted: {words_attempted}")