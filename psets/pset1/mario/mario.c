#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do {
       height = get_int("Height: ");
    }
    while (height > 8 || height < 1);
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - (i + 1); j++)
        {
            printf(" ");
        }

        for (int j = 0; j < height - ((height - 1) - i); j++)
        {
            printf("#");
        }

      //  printf("  ");

        for (int j = 0; j < height - ((height - 1) - i); j++)
        {
            printf("#");
        }
        printf("\n");
    }
}