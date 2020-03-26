from cs50 import get_int, get_string


def main():
    # get a cc number using get_int to make sure the input is in an integer format
    # then convert it to a string for easier manipulation
    cc_num = get_int("Number: ")
    cc_num = str(cc_num)

    # check validity of cc number
    valid = check_cc_num_validity(cc_num)

    # print validity of credit card
    print(f"{valid}")


# function to check the that the initial number check passes
def check_cc_num_validity(cc_num):
    # gets length, first digit, and first two digits of the cc number
    length = len(cc_num)
    first_digi = cc_num[0]
    first_two = cc_num[0:2]

    # checks if the card is an AMEX
    if first_two == '34' or first_two == '37':
        if not length == 15:
            return "INVALID"
        else:
            cc_type = "AMEX"
            valid = check_validity_math(cc_num, length, cc_type)
    # checks if the card is a Visa
    elif first_digi == '4':
        if not length == 13 and not length == 16:
            return "INVALID"
        else:
            cc_type = "VISA"
            valid = check_validity_math(cc_num, length, cc_type)
    # checks if the card is a Mastercard
    elif int(first_two) >= 51 and int(first_two) <= 55:
        if not length == 16:
            return "INVALID"
        else:
            cc_type = "MASTERCARD"
            valid = check_validity_math(cc_num, length, cc_type)
    # returns INVALID after initial digit checks
    else:
        return "INVALID"
    return valid


# function to check the credit card number according to Luhn's Algorithm
def check_validity_math(cc_num, length, cc_type):
    # gets the sum of the even digits in the cc number multiplied by 2
    even_digi_sum = even_digis(cc_num, length)
    # gets the sum of the odd digits in the cc number
    odd_digi_sum = odd_digis(cc_num, length)

    # totals the even digit sum and the odd digit sum
    # then checks if the last digit of the total sum is zero
    # in which case the cc number could plausibly be valid
    total_sum = even_digi_sum + odd_digi_sum
    last_digi = str(total_sum)[-1]

    if last_digi == '0':
        return cc_type
    else:
        return "INVALID"


# function to sum up the even digits
def even_digis(cc_num, length):
    # initialize sum & iterator
    even_digi_sum = 0
    i = -2
    # while loop to run through the cc number
    # this loop runs through the number backwards as the digits start counting from the right
    while i >= -length:
        digi = int(cc_num[i])
        if digi < 5:
            digi = digi * 2
            even_digi_sum = even_digi_sum + digi
        else:
            digi = (digi - 5) * 2 + 1
            even_digi_sum = even_digi_sum + digi
        i = i - 2
    return even_digi_sum


# function to sum up the odd digits
def odd_digis(cc_num, length):
    # initialize sum and iterator
    odd_digi_sum = 0
    i = -1
    # while loop to run through the cc number
    # this loop runs through the number backwards as the digits start counting from the right
    while i >= -length:
        digi = int(cc_num[i])
        odd_digi_sum = odd_digi_sum + digi
        i = i - 2
    return odd_digi_sum


if __name__ == "__main__":
    main()