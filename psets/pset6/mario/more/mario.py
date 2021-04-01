from cs50 import get_int

def main():
    height = get_int("Height: ")

    while(height > 8 or height < 1):
        height = get_int("Height: ")

    for i in range(height):
        for j in range(height - i - 1):
            print(" ", end="")

        for j in range(height - ((height - 1) - i)):
            print("#", end="")

        print()

main()