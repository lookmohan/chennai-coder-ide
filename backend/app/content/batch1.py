"""Batch 1: the first six problems, written in full statement style.

Each entry replaces the statement and examples of an existing sample problem (matched by slug).
Hidden tests are kept exactly as they were, so grading does not change. Expected outputs were
checked by hand against each explanation.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_1 = [
    {
        "slug": "sum-of-two-numbers",
        "title": "Sum of Two Numbers",
        "description": (
            "Two friends each tell you a whole number. Your job is to add them together and report the total.\n\n"
            "Read the two numbers from a single line of input, add them, and print the result. "
            "The numbers can be negative, and the total can be larger than either of them."
        ),
        "input_format": "A single line containing two integers a and b, separated by one space.",
        "output_format": "Print one integer: a + b.",
        "constraints": "-10^9 <= a, b <= 10^9",
        "explanation": "Split the line at the space, turn each part into a number with int(), then add them.",
        "tests": [
            pub("2 3\n", "5", "2 + 3 = 5."),
            pub("10 -4\n", "6", "10 + (-4) = 6. Adding a negative number is the same as subtracting its size."),
            hid("0 0\n", "0"),
            hid("1000000000 1000000000\n", "2000000000"),
        ],
    },
    {
        "slug": "say-hello",
        "title": "Say Hello",
        "description": (
            "Greeting people is one of the first things most programs do. Your program will read a name "
            "from the user and print a friendly greeting.\n\n"
            "The greeting starts with the word Hello, then a comma and a space, then the name, then an "
            "exclamation mark. Print exactly that sentence and nothing else."
        ),
        "input_format": "A single line containing one name. The name has no spaces.",
        "output_format": "One line in the form: Hello, NAME!",
        "constraints": "1 <= length of the name <= 50. The name contains only letters.",
        "explanation": "Read the line, remove the newline with strip(), and build the sentence with an f-string.",
        "tests": [
            pub("Asha\n", "Hello, Asha!", "The name is Asha, so the sentence is Hello, Asha!"),
            pub("Mohanraj\n", "Hello, Mohanraj!", "The same pattern works for any name."),
            hid("Chennai\n", "Hello, Chennai!"),
            hid("Coder\n", "Hello, Coder!"),
        ],
    },
    {
        "slug": "double-it",
        "title": "Double It",
        "description": (
            "Doubling a number means multiplying it by 2. Doubling appears everywhere, from scaling a "
            "recipe to working out how much a savings amount grows.\n\n"
            "Read one integer and print its double."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "Print one integer: 2 × n.",
        "constraints": "-10^6 <= n <= 10^6",
        "explanation": "Read the number with int(), multiply it by 2, and print the result.",
        "tests": [
            pub("4\n", "8", "Doubling 4 gives 8."),
            pub("0\n", "0", "Doubling zero still gives zero."),
            hid("-7\n", "-14"),
            hid("1000000\n", "2000000"),
        ],
    },
    {
        "slug": "is-even",
        "title": "Is It Even?",
        "description": (
            "A whole number is even when it can be split into two equal whole-number halves. For example, "
            "4 is even because it splits into 2 and 2. A number that can't be split this way is odd.\n\n"
            "Read one integer and decide whether it is even or odd."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "Print the word Even if n is even, or Odd if n is odd.",
        "constraints": "-10^9 <= n <= 10^9",
        "explanation": "A number is even when dividing it by 2 leaves no remainder. The % operator gives the remainder.",
        "tests": [
            pub("4\n", "Even", "4 splits into 2 and 2, so it is even."),
            pub("7\n", "Odd", "7 cannot be split into two equal whole numbers, so it is odd."),
            hid("0\n", "Even"),
            hid("-3\n", "Odd"),
        ],
    },
    {
        "slug": "largest-of-three",
        "title": "Largest of Three",
        "description": (
            "Three friends each score a number in a game. You need to find the highest score.\n\n"
            "Read three integers from one line and print the largest. The numbers may repeat, and they may be negative."
        ),
        "input_format": "One line containing three integers a, b and c, separated by spaces.",
        "output_format": "Print the largest of a, b and c.",
        "constraints": "-10^9 <= a, b, c <= 10^9",
        "explanation": "Keep a 'best so far' value. Compare each number with it and keep the bigger one.",
        "tests": [
            pub("3 9 4\n", "9", "9 is the biggest of 3, 9 and 4."),
            pub("-1 -5 -2\n", "-1", "-1 is greater than -2 and -5, so it is the largest."),
            hid("7 7 7\n", "7"),
            hid("0 100 50\n", "100"),
        ],
    },
    {
        "slug": "reverse-a-string",
        "title": "Reverse a String",
        "description": (
            "Reversing text is a common task. For example, a word reads the same backwards if it is a palindrome.\n\n"
            "Read one line of text and print its characters in reverse order. Spaces count as characters, "
            "so they move to their reversed positions too."
        ),
        "input_format": "A single line of text. It may contain spaces.",
        "output_format": "The same characters in reverse order, on one line.",
        "constraints": "1 <= length of the line <= 1000",
        "explanation": "In Python, text[::-1] gives the characters in reverse order. Strip only the newline, not the spaces.",
        "tests": [
            pub("hello world\n", "dlrow olleh", "Read backwards: d, l, r, o, w, space, o, l, l, e, h."),
            pub("a\n", "a", "A single character reversed is still itself."),
            hid("racecar\n", "racecar"),
            hid("Chennai\n", "iannehC"),
        ],
    },
]
