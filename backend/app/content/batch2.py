"""Batch 2: problems 7-12, written in full statement style.

Hidden tests are the same as in the seed, so grading does not change. Every expected output was
checked by hand against its explanation.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_2 = [
    {
        "slug": "count-even-numbers",
        "title": "Count Even Numbers",
        "description": (
            "A shop gives every item a code number. The owner wants to know how many of the codes are even, "
            "because the even codes are kept on one shelf.\n\n"
            "Read the list of codes and count the even ones. Zero counts as even."
        ),
        "input_format": (
            "Line 1: n, the number of codes.\n"
            "Line 2: n space-separated integers, the codes."
        ),
        "output_format": "One integer: how many of the codes are even.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each code <= 10^9",
        "explanation": (
            "A number is even when number % 2 == 0. Keep a count, and add one each time you find an even code."
        ),
        "tests": [
            pub("5\n1 2 3 4 5\n", "2", "The even codes are 2 and 4, so the answer is 2."),
            pub("3\n2 4 6\n", "3", "Every code is even, so all 3 count."),
            hid("4\n1 3 5 7\n", "0"),
            hid("1\n0\n", "1"),
        ],
    },
    {
        "slug": "sum-of-array",
        "title": "Sum of an Array",
        "description": (
            "A teacher has a list of marks, one number per student. She wants the total of all the marks, "
            "so she can work out the class average.\n\n"
            "Read the marks and print their sum. Some values can be negative, for example a mark taken off "
            "as a penalty."
        ),
        "input_format": (
            "Line 1: n, the number of values.\n"
            "Line 2: n space-separated integers."
        ),
        "output_format": "One integer: the sum of all the values.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each value <= 10^9",
        "explanation": "Start with total = 0, then add each value to total inside a loop.",
        "tests": [
            pub("3\n1 2 3\n", "6", "1 + 2 + 3 = 6."),
            pub("4\n-1 -2 10 5\n", "12", "The negative values pull the total down: -1 - 2 + 10 + 5 = 12."),
            hid("1\n100\n", "100"),
            hid("5\n0 0 0 0 0\n", "0"),
        ],
    },
    {
        "slug": "factorial",
        "title": "Factorial",
        "description": (
            "The factorial of a number n, written n!, is the product of all the whole numbers from 1 up to n. "
            "For example, 4! = 1 × 2 × 3 × 4 = 24.\n\n"
            "By definition, 0! = 1. Read n and print n!."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: n!.",
        "constraints": "0 <= n <= 12. The answer fits in a normal integer.",
        "explanation": "Start with result = 1, then multiply result by each number from 1 up to n.",
        "tests": [
            pub("5\n", "120", "1 × 2 × 3 × 4 × 5 = 120."),
            pub("0\n", "1", "By definition, 0! = 1."),
            hid("10\n", "3628800"),
            hid("12\n", "479001600"),
        ],
    },
    {
        "slug": "fizzbuzz",
        "title": "FizzBuzz",
        "description": (
            "FizzBuzz is a classic exercise. You look at one number and decide what to print instead of the number, "
            "depending on what it divides by.\n\n"
            "If n is divisible by both 3 and 5, print FizzBuzz. If it is divisible by 3 only, print Fizz. "
            "If it is divisible by 5 only, print Buzz. Otherwise print n itself."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One line: FizzBuzz, Fizz, Buzz, or the number n.",
        "constraints": "1 <= n <= 10^6",
        "explanation": (
            "Check the 'both 3 and 5' case first. If you check for 3 first, then 15 would print Fizz instead of FizzBuzz."
        ),
        "tests": [
            pub("3\n", "Fizz", "3 is divisible by 3 but not by 5."),
            pub("5\n", "Buzz", "5 is divisible by 5 but not by 3."),
            hid("15\n", "FizzBuzz"),
            hid("7\n", "7"),
        ],
    },
    {
        "slug": "count-vowels",
        "title": "Count the Vowels",
        "description": (
            "Vowels are the letters a, e, i, o and u. They can appear in upper or lower case.\n\n"
            "Read a line of text and count how many vowels it contains. Consonants, digits and spaces are not counted."
        ),
        "input_format": "One line of text, which may contain letters, digits and spaces.",
        "output_format": "One integer: the number of vowels in the line.",
        "constraints": "1 <= length of the line <= 1000",
        "explanation": "Convert each character to lower case, then check whether it is one of a, e, i, o or u.",
        "tests": [
            pub("hello\n", "2", "The vowels in hello are e and o."),
            pub("Chennai\n", "3", "The vowels in Chennai are e, a and i."),
            hid("rhythm\n", "0"),
            hid("AEIOU\n", "5"),
        ],
    },
    {
        "slug": "palindrome-check",
        "title": "Palindrome Check",
        "description": (
            "A palindrome reads the same forwards and backwards. Examples are racecar and level. "
            "A single letter counts as a palindrome too.\n\n"
            "Read one word and print YES if it is a palindrome, or NO if it is not. Upper and lower case letters "
            "are different, so Ab is not a palindrome."
        ),
        "input_format": "One word with no spaces.",
        "output_format": "Print YES if the word is a palindrome, otherwise NO.",
        "constraints": "1 <= length of the word <= 1000",
        "explanation": "Compare the word with its reverse. In Python, word[::-1] gives the reversed word.",
        "tests": [
            pub("racecar\n", "YES", "Read backwards, racecar is still racecar."),
            pub("hello\n", "NO", "Read backwards, hello becomes olleh, which is different."),
            hid("a\n", "YES"),
            hid("Ab\n", "NO"),
        ],
    },
]
