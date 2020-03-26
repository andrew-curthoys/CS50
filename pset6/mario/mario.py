from cs50 import get_int


def main():
    height = get_height("Height: ")
    # we need to subtract 1 from height & add 1 to i to account for zero indexing
    for i in range(height):
        blanks = height - i - 1
        blocks = i + 1
        print_blocks(blanks, blocks)
        print()

# makes sure the height is between 1 and 8


def get_height(prompt):
    while True:
        n = get_int("Height: ")
        if n > 0 and n < 9:
            return n

# function to define the printing of the blocks


def print_blocks(blanks, blocks):
    # prints blanks to pad left side blocks
    for blank in range(blanks):
        print(" ", end="")
    # prints left side blocks
    for block in range(blocks):
        print("#", end="")
    # prints space between blocks
    print("  ", end="")
    # prints right side blocks
    for block in range(blocks):
        print("#", end="")


if __name__ == "__main__":
    main()