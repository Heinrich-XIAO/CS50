#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void) {
    float cash;

    do
    {
        cash = get_float("How much change is owed?\n");
    }
    while(cash < 1);

    int cents = round(cash * 100);
    int coins = 0;
    do
    {
        cents = (cents - 25);
        coins++;
    }
    while (cents > 25);
    do
    {
        cents = (cents - 10);
        coins++;
    }
    while (cents > 10);
    do
    {
        cents = (cents - 5);
        coins++;
    }
    while (cents > 5);
    do
    {
        cents = (cents - 1);
        coins++;
    }
    while (cents > 5);

    printf("%i coins \n", coins);
}