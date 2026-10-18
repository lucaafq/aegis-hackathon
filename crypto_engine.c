#include <stdio.h>
#include <string.h>

void encrypt_data(const char *input, char *output, const char *key) {
    int key_len = strlen(key);
    int input_len = strlen(input);
    
    for(int i = 0; i < input_len; i++) {
        output[i] = input[i] ^ key[i % key_len];
    }
    output[input_len] = '\0';
}