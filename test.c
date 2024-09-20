#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define HASH_SIZE 3  // 3 bytes = 24 bits 
#define MAX_STRING_LEN 10  
#define NUM_TRIALS 10000000

// Generate strings up to length 10 from numbers and alphabet letters
void generate_random_string(char *str, size_t length)
{
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (size_t i = 0; i < length - 1; i++) {
        str[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    str[length - 1] = '\0'; 
}

// Calculate the hash and truncate to 24 bits
void calculate_hash(const unsigned char *message, size_t message_len, unsigned char *digest)
{
    EVP_MD_CTX *mdctx;
    unsigned char full_hash[EVP_MAX_MD_SIZE];
    unsigned int hash_len;

    // Initialize the context for MD5 hashing
    mdctx = EVP_MD_CTX_new();
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
    unsigned char target_digest[HASH_SIZE] = {0x00, 0x0e, 0x25};  // Target hash "e25" in hexadecimal form
    char random_string[MAX_STRING_LEN]; 
    unsigned long long trial_count = 0;  

    srand(time(NULL));  // Seed the random number generator

    printf("brute force begins...\n");

    do {
        generate_random_string(random_string, MAX_STRING_LEN);
        calculate_hash((unsigned char *)random_string, strlen(random_string), digest);
        trial_count++;

    } while (memcmp(digest, target_digest, HASH_SIZE) != 0 && trial_count < NUM_TRIALS);

    if (memcmp(digest, target_digest, HASH_SIZE) == 0) {
        printf("Match was found! String: %s after %llu trials\n", random_string, trial_count);
    } else {
        printf("No match found after %llu trials\n", trial_count);
    }

    return 0;
}
