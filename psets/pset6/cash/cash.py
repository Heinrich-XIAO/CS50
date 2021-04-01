from cs50 import get_float

# Get user input
while True:
    try:
        change = get_float("Change Owed: ")
        if change > 0:
            break
    except:
        print("", end="")

# Set the starting value of the coins
coins = 0

# Set the change in dollars into cents
change = change * 100

# Checking if it still can use more 25c
while change >= 25:
    change = change - 25
    coins = coins + 1

# Checking if it still can use more 10c
while change >= 10:
    change = change - 10
    coins = coins + 1

# Checking if it still can use more 5c
while change >= 5:
    change = change - 5
    coins = coins + 1

# Checking if it still can use more 1c
while change >= 1:
    change = change - 1
    coins = coins + 1

print(coins)