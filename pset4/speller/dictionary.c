// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
struct node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Initialize counter for word count
    unsigned int word_count = 0;

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Increment word count
        word_count ++;

        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy "word" to the word section of new_node
        strcpy(new_node -> word, word);

        // Get index for hashtable with hash function
        unsigned int j = hash(new_node -> word);
        new_node -> next = hashtable[j];
        hashtable[j] = new_node;

        // fseek(file, sizeof(node) - );
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // initialize word count
    unsigned int word_count = 0;

    for (int i = 0; i < N; i++)
        if (hashtable[i] != NULL)
        {
            node *cursor = hashtable[i];
            while (cursor != NULL)
            {
                word_count ++;
                cursor = cursor -> next;
            }

        }
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // hash word into hashtable node
    unsigned int i = hash(word);
    node *cursor = hashtable[i];

    // check word for spelling
    while (cursor != NULL)
    {
        char *dict_word = cursor -> word;
        if (strcasecmp(word, dict_word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // free linked list dictionary from memory
    for (int i = 0; i < N; i++)
    {
        if (hashtable[i] != NULL)
        {
            node *cursor = hashtable[i];
            while (cursor != NULL)
            {
                node *temp = cursor;
                cursor = cursor -> next;
                free(temp);
            }
        }
    }
    return true;
}
