# I- Hash Brute-Force Attack (bruteforce_hash.c)

## Description
This program performs a brute-force attack to find a random string that matches a specified truncated MD5 hash (24-bit). The code generates random strings up to a length of 10 characters using alphanumeric characters, computes their MD5 hash, and compares the first 3 bytes (24 bits) with a target hash value. It prints the matching string and the number of trials required.

## Requirements
- OpenSSL library (`libssl-dev` or equivalent for your platform)
- C Compiler (`gcc` recommended)

## How to Run
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/hash-bruteforce-attack.git
    cd hash-bruteforce-attack
    ```

2. **Compile the Program:**
    Make sure OpenSSL is installed on your system. Compile using `gcc`:
    ```bash
    gcc -o bruteforce_hash bruteforce_hash.c -lssl -lcrypto
    ```

3. **Run the Program:**
    After compiling, run the program using:
    ```bash
    ./bruteforce_hash
    ```

4. **Output:**
    - The program will begin generating random strings and computing their truncated MD5 hashes.
    - It will log each generated string and its hash into a file called `hashes.txt`.
    - When a match is found, the program will display the matching string and the number of trials it took.
    - If no match is found after `NUM_TRIALS` iterations, it will print a message indicating no match was found.

# II- SHA1 Dictionary Attack Script (sha1_dictionary_attack.py)

## Description
This script performs a dictionary attack against SHA1-hashed passwords stored in a password file. It reads a list of user:hash pairs from an `.htpasswd`-formatted file and attempts to crack them by comparing each hash against the SHA1 hashes of words from a given dictionary file.

### Features:
- Reads a password file (`htpasswd-sha1`) that contains user credentials in the format: `username:{SHA}hashed_password`.
- Uses the `rockyou.txt` dictionary to hash each word using SHA1 and compares it to the stored passwords.
- Prints the cracked passwords along with their usernames upon finding a match.
- Displays the time taken and the number of words attempted.

### Prerequisites
- Python 3.x
- A file named `htpasswd-sha1` with hashed user passwords in SHA1 format.
- A dictionary file named `rockyou.txt` for the dictionary attack (can be downloaded from [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/rockyou.txt.tar.gz)).

### How to Run
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/sha1-dictionary-attack.git
    cd sha1-dictionary-attack
    ```

2. **Prepare the Password and Dictionary Files:**
    - Place your password file (`htpasswd-sha1`) in the data directory.
    - Make sure your dictionary file (`rockyou.txt`) is in the data directory.

3. **Run the Script:**
    Execute the script using the command below:
    ```bash
    python3 sha1_dictionary_attack.py
    ```

4. **Output:**
    - The script will display the cracked passwords and the associated usernames for each match found.
    - It will show the total number of words attempted and the time taken for the operation.

# III- Multi-Algorithm Dictionary Attack Script (md5_sha256_dictionary_attack.py)

## Description
This script performs a dictionary attack against passwords stored in multiple files, each using a different hashing algorithm. It supports MD5, SHA-1 (Base64 encoded), and unsalted SHA-256 hashes. The script reads a list of user:hash pairs from separate `.htpasswd`-formatted files and attempts to crack them by comparing each hash against the hashes of words from a given dictionary file.

### Features:
- **Supports multiple hashing algorithms:** MD5, SHA-1 (Base64), and SHA-256.
- **Reads from multiple password files:** Each password file corresponds to a different hashing algorithm.
- **Uses a dictionary file (`rockyou.txt`)** to attempt cracking the passwords.
- **Outputs the cracked passwords** for each algorithm and provides a summary including time taken and number of words attempted.

## Prerequisites
- **Python 3.x**: Make sure Python 3 is installed on your system.
- **Password Files**:
  - `htpasswd-md5`: Contains user credentials hashed using MD5.
  - `htpasswd-sha1`: Contains user credentials hashed using Base64 encoded SHA-1.
  - `htpasswd-sha256`: Contains user credentials hashed using unsalted SHA-256.
- **Dictionary File**: A file named `rockyou.txt` containing potential passwords.

## How to Run
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/multi-algorithm-dictionary-attack.git
    cd multi-algorithm-dictionary-attack
    ```

2. **Prepare the Password and Dictionary Files:**
    - Place your password files (`htpasswd-md5`, `htpasswd-sha1`, `htpasswd-sha256`) in the data directory.
    - Make sure your dictionary file (`rockyou.txt`) is in the data directory.

3. **Run the Script:**
    Execute the script using the command below:
    ```bash
    python3 multi_algorithm_dictionary_attack.py
    ```

4. **Output:**
    - The script will display the cracked passwords and the associated usernames for each hashing algorithm.
    - It will show the total number of words attempted and the time taken for each algorithm.