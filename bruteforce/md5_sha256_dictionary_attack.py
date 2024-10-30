"""
This script performs a dictionary attack against passwords stored in multiple files, each using a different hashing algorithm.
It supports MD5, SHA-1 (Base64 encoded), and unsalted SHA-256 hashes. The script reads a list of user:hash pairs from separate
`.htpasswd`-formatted files and attempts to crack them by comparing each hash against the hashes of words from a given dictionary file.

- It reads the password files (`htpasswd-md5`, `htpasswd-sha1`, `htpasswd-sha256`) and identifies the hashing algorithm used.
- The script computes the MD5, SHA1, or SHA256 hash of each word from the dictionary and checks if it matches the stored hash.
- It outputs the cracked passwords for each hashing algorithm and provides a summary of the time taken and the number of words attempted.
"""

import hashlib
import base64
import time

# Function to hash the dictionary word using different algorithms
def hash_word(word, algorithm, salt=None):
    if algorithm == 'md5':
        # Standard MD5 (hexadecimal format)
        return hashlib.md5(word.encode('utf-8')).hexdigest()
    elif algorithm == 'sha1':
        # SHA-1 with Base64 encoding
        return base64.b64encode(hashlib.sha1(word.encode('utf-8')).digest()).decode('utf-8')
    elif algorithm == 'sha256':
        # Unsalted SHA-256
        return hashlib.sha256(word.encode('utf-8')).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

# Function to read the password file and store user:hash pairs along with the algorithm and salt used
def read_password_file(filename):
    passwords = {}
    with open(filename, 'r') as file:
        for line in file:
            user, hashed_password = line.strip().split(':')
            if hashed_password.startswith("{SHA256}"):
                passwords[user] = (hashed_password.replace("{SHA256}", ""), 'sha256', None)
            elif hashed_password.startswith("{MD5}"):  # Hex MD5 hash
                passwords[user] = (hashed_password.replace("{MD5}", ""), 'md5', None)
            else:  # Assume SHA1 if not specified
                passwords[user] = (hashed_password.replace("{SHA}", ""), 'sha1', None)
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
            
            # Try cracking each password in the list
            for user in list(passwords.keys()):
                hashed_password, algorithm, salt = passwords[user]
                hashed_word = hash_word(word, algorithm, salt)
                
                if hashed_word == hashed_password:
                    cracked[user] = word
                    print(f"Password for {user} is {word}")
                    del passwords[user]  # Remove the user after cracking their password
            
                if len(passwords) == 0:
                    return cracked, word_count
    return cracked, word_count

# Main
if __name__ == "__main__":
    password_files = {
        'MD5': './data/htpasswd-md5',
        'SHA1': './data/htpasswd-sha1',
        'SHA256': './data//htpasswd-sha256'  # This file contains unsalted SHA-256 hashes
    }
    dictionary_file = './data/rockyou.txt'

    for algorithm, password_file in password_files.items():
        print(f"Running dictionary attack using {algorithm}...")

        # Measure the time for the attack
        start_time = time.time()
        cracked_passwords, words_attempted = dictionary_attack(password_file, dictionary_file)
        end_time = time.time()

        if cracked_passwords:
            print(f"Cracked passwords using {algorithm}: {cracked_passwords}")
        else:
            print(f"No passwords were cracked using {algorithm}.")

        print(f"Time taken for {algorithm}: {end_time - start_time} seconds")
        print(f"Words attempted for {algorithm}: {words_attempted}\n")