def lines(a, b):
    """Return lines in both a and b"""

    # splitting lines of a then making it a set
    a = a.splitlines()
    a = set(a)
    # splitting lines of b then making it a set
    b = b.splitlines()
    b = set(b)

    # comparing lines
    common_lines = a & b

    return list(common_lines)


def sentences(a, b):
    """Return sentences in both a and b"""

    from nltk.tokenize import sent_tokenize

    # splitting lines of a then making it a set
    a = sent_tokenize(a)
    a = set(a)
    # splitting lines of b then making it a set
    b = sent_tokenize(b)
    b = set(b)

    # comparing lines
    common_lines = a & b

    return list(common_lines)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    def substring_parse(string, n):
        length = len(string)
        substrings = set()
        for i in range(length - n + 1):
            substrings.add(string[i:i+n])
        return substrings

    # parsing a into substrings
    a = substring_parse(a, n)
    # parsing b into substrings
    b = substring_parse(b, n)

    common_lines = a & b

    return list(common_lines)
