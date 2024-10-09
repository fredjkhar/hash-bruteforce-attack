/*
 * This program performs a brute-force attack to find a random string
 * that matches a specified truncated MD5 hash (24-bit). The code generates
 * random strings up to a length of 10 characters using alphanumeric characters,
 * computes their MD5 hash, and compares the first 3 bytes (24 bits) with a target
 * hash value. It prints the matching string and the number of trials required.
 */

#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define HASH_SIZE 3           // 3 bytes = 24 bits
#define MAX_STRING_LEN 10     // Maximum length for the random string
#define NUM_TRIALS 10000000   // Maximum number of trials before stopping

// Generate random strings of up to length 10 using numbers and alphabet letters
void generate_random_string(char *str, size_t length)
{
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (size_t i = 0; i < length - 1; i++) {
        str[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    str[length - 1] = '\0';  // Null-terminate the generated string
}

// Calculate the MD5 hash and truncate to 24 bits
void calculate_hash(const unsigned char *message, size_t message_len, unsigned char *digest)
{
    EVP_MD_CTX *mdctx;
    unsigned char full_hash[EVP_MAX_MD_SIZE];
    unsigned int hash_len;

    // Initialize the context for MD5 hashing
    mdctx = EVP_MD_CTX_new();
    if (mdctx == NULL) {
        fprintf(stderr, "Error: Failed to create MD context.\n");
        exit(EXIT_FAILURE);
    }

    // Perform MD5 hashing on the input message
    EVP_DigestInit_ex(mdctx, EVP_md5(), NULL);
    EVP_DigestUpdate(mdctx, message, message_len);
    EVP_DigestFinal_ex(mdctx, full_hash, &hash_len);
    EVP_MD_CTX_free(mdctx);

    // Copy only the first 3 bytes of the full hash into the digest buffer
    memcpy(digest, full_hash, HASH_SIZE);
}

int main(void)
{
    unsigned char digest[HASH_SIZE];  
    const unsigned char target_digest[HASH_SIZE] = {0x00, 0x0e, 0x25};  // Target hash "e25" in hexadecimal
    char random_string[MAX_STRING_LEN]; 
    unsigned long long trial_count = 0;  

    srand((unsigned)time(NULL));  // Seed the random number generator with the current time

    printf("Brute force begins...\n");

    // Measure start time
    clock_t start_time = clock();

    // Start the brute-force search
    do {
        generate_random_string(random_string, MAX_STRING_LEN);  // Generate a random string
        calculate_hash((unsigned char *)random_string, strlen(random_string), digest);  // Calculate its hash
        trial_count++;  // Increment the trial counter

    } while (memcmp(digest, target_digest, HASH_SIZE) != 0 && trial_count < NUM_TRIALS);

    // Measure end time
    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    // Check if a match was found
    if (memcmp(digest, target_digest, HASH_SIZE) == 0) {
        printf("Match was found! String: %s after %llu trials\n", random_string, trial_count);
    } else {
        printf("No match found after %llu trials\n", trial_count);
    }

    // Print the elapsed time
    printf("Elapsed time: %.2f seconds\n", elapsed_time);

    return 0;
}