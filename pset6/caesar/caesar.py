from sys import argv, exit
from cs50 import get_string


def main():
    # check to make sure user input the command line arguments correctly
    if not len(argv) == 2:
        print("Usage: python caesar.py key")
        exit(1)
    else:
        # initialize empty string
        word = ""
        # get key
        k = int(argv[1])
        # get string from user
        s = get_string("plaintext: ")
        for c in s:
            # get the ASCII number for each character in the string
            # ord() returns the ASCII number for a character
            c_int = ord(c)
            # check if the character is an uppercase letter
            # if so rotate the character by the value of the key
            # use chr() to convert back to character from ASCII number
            if c_int >= 65 and c_int <= 90:
                c_int = 65 + (c_int - 65 + k) % 26
                word = word + chr(c_int)
            # check if the character is a lowercase letter
            # if so rotate the character by the value of the key
            # use chr() to convert back to character from ASCII number
            elif c_int >= 97 and c_int <= 122:
                c_int = 97 + (c_int - 97 + k) % 26
                word = word + chr(c_int)
            else:
                word = word + c
        print(f"ciphertext: {word}")


if __name__ == "__main__":
    main()