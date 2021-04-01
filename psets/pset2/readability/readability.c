// Include librarys
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

// Main code
int main(void)
{
    // Declare variables
    string sentince = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentinces = 0;
    char character = ' ';

    // Loop through sentince
    for (int i = 0; i < strlen(sentince); i++)
    {
        character = sentince[i];

        // Check if it is a letter
        if (isupper(character) || islower(character))
        {
            // If it is a letter add to the letter count
            letters++;
        // Check for spaces
        } else if (character == ' ')
        {
            // If it is a space add to the words count
            words++;
        // Check for punctuation marks
        } else if (character == '!' || character == '?' || character == '.')
        {
            // If it is a punctuation mark add to the sentince count
            sentinces++;
        }
    }
    // Calculate per 100 words
    int l = 100 / words * letters;
    int s = 100 / words * sentinces;

    // Calculate readability
    int index = 0.0588 * l - 0.296 * s - 15.8;

    printf("Grade %i\n", index);

    // // Check for grades bigger than 15
    // if (index > 15)
    // {
    //     printf("Grade 16+");
    // } else {
    //     // Check for before grade 1
    //     if (index < 1) {
    //         printf("Before Grade 1\n");
    //     // Else print grade
    //     } else {

    //     }
    // }
}