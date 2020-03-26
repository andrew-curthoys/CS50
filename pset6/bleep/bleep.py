from cs50 import get_string
from sys import argv

# initialize a set for the words in the dictionary
words = set()


def main():
    # check to make sure the user supplied a dictionary & exit with code of 1 if not
    if not len(argv) == 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
    else:
        # load dictionary
        load(argv[1])
        # get a phrase from the user
        phrase = get_string("What message would you like to censor?\n")
        # parse the phrase into its individual words
        phrase_list = phrase.split(" ")
        # initialize censored phrase
        censored_phrase = ""
        # loop through each word in the list & censor it if necessary
        for word in phrase_list:
            censored_word = censor(word)
            censored_phrase = censored_phrase + " " + censored_word
    # finally print the phrase with all appropriate words censored
    print(censored_phrase[1:len(censored_phrase)])


def load(dictionary):
    # load in user supplied dictionary
    file = open(dictionary, "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True


def censor(word):
    # censor a word if it's in the user supplied dictionary
    if word.lower() in words:
        censored_word = ""
        for i in word:
            censored_word = censored_word + "*"
        return censored_word
    else:
        return word


if __name__ == "__main__":
    main()
