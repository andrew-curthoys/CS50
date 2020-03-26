#include <stdio.h>
#include <cs50.h>
#include <math.h>

long get_cc_number(string prompt);
string check_cc_num_validity(long);
int even_digis(long, int);
int odd_digis(long, int);
string check_validity_math(long, int, string);

int main(void)
{
// Get credit card number from user
    long cc_num = get_cc_number("Please enter a credit card number\n");

// Test cc number for validity
    string valid = check_cc_num_validity(cc_num);
    printf("%s\n", valid);
}


// Prompt user for credit card number
long get_cc_number(string prompt)
{
    long cc_num;
    do
    {
        cc_num = get_long("%s", prompt);
    }
    while (cc_num < 1);
    return cc_num;
}

// Test credit card number for validity based on
// first two numbers and length of credit card number
string check_cc_num_validity(long cc_num)
{
    // Get length of the cc # and the first & first two digits
    int len = log10(cc_num) + 1;
    int first_digi = cc_num / pow(10, len - 1);
    int first_two = cc_num / pow(10, len - 2);

    // initialize valid variable
    string valid = "";

    // first check validity of cc # based on the
    // first 1-2 digits & cc # length.
    // then check math based on Luhn's Algorithm
    if ((first_two == 34) || (first_two == 37))
    {
        if (len != 15)
        {
            valid = "INVALID";
        }
        else
        {
            string cc_type = "AMEX";
            valid = check_validity_math(cc_num, len, cc_type);
        }
    }
    else if (first_digi == 4)
    {
        if ((len != 13) && (len != 16))
        {
            valid = "INVALID";
        }
        else
        {
            string cc_type = "VISA";
            valid = check_validity_math(cc_num, len, cc_type);
        }
    }
    else if ((first_two >= 51) && (first_two <= 55))
    {
        if (len != 16)
        {
            valid = "INVALID";
        }
        else
        {
            string cc_type = "MASTERCARD";
            valid = check_validity_math(cc_num, len, cc_type);
        }
    }
    else
    {
        valid = "INVALID";
    }
    return valid;
}

string check_validity_math(long cc_num, int len, string cc_type)
{
    int even_digi_sum = even_digis(cc_num, len);
    int odd_digi_sum = odd_digis(cc_num, len);

    int total_sum = even_digi_sum + odd_digi_sum;
    int last_digi = total_sum % 10;
    string validity = "";

    if (last_digi == 0)
    {
        validity = cc_type;
    }
    else
    {
        validity = "INVALID";
    }
    return validity;
}

int even_digis(long cc_num, int len)
{
    // initialize the digit sum
    int even_digi_sum = 0;

    // set up loop to run through every other digit,
    // starting with the penultimate
    for (int i = 1; i < len; i = i + 2)
    {
        // get the desired digit to the "ones" position
        // by dividing by the power of 10 for the desired digit
        long digi = (cc_num / pow(10, i));

        // get the desired digit by returning the mod
        // of the transformed number divided by 10
        digi = digi % 10;

        // special case for digits over 5 since their value * 2
        // will be two digits long
        if (digi < 5)
        {
            digi = digi * 2;
            even_digi_sum = even_digi_sum + digi;
        }
        else
        {
            digi = (digi - 5) * 2 + 1;
            even_digi_sum = even_digi_sum + digi;
        }
    }
    return even_digi_sum;
}

int odd_digis(long cc_num, int len)
{
    // initialize the digit sum
    int odd_digi_sum = 0;

    // set up loop to run through every other digit,
    // starting with the last
    for (int i = 0; i < len; i = i + 2)
    {
        // get the desired digit to the "ones" position
        // by dividing by the power of 10 for the desired digit
        long digi = (cc_num / pow(10, i));

        // get the desired digit by returning the mod
        // of the transformed number divided by 10
        digi = digi % 10;

        odd_digi_sum = odd_digi_sum + digi;
    }
    return odd_digi_sum;
}
