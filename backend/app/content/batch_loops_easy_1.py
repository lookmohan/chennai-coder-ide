"""Loops, Easy (first 10 of the 19 still needed).

Each entry carries its topic, level and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_LOOPS_EASY_1 = [
    {
        "slug": "sum-to-n",
        "title": "Sum to N",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 401,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A teacher gives a class this challenge: add up every whole number from 1 up to n. For example, "
            "for n = 4 the answer is 1 + 2 + 3 + 4 = 10.\n\n"
            "Read n and print the sum of all the whole numbers from 1 to n. If n is 0, the sum is 0."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: the sum 1 + 2 + ... + n.",
        "constraints": "0 <= n <= 10^5",
        "explanation": "Start with total = 0, then use a for loop over range(1, n + 1) and add each number to total.",
        "tests": [
            pub("5\n", "15", "1 + 2 + 3 + 4 + 5 = 15."),
            pub("1\n", "1", "Only the number 1 is added."),
            hid("0\n", "0"),
            hid("100\n", "5050"),
        ],
    },
    {
        "slug": "count-down",
        "title": "Count Down",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 402,
        "tags": ["Loops", "Input"],
        "description": (
            "A rocket launch counts down from a starting number to 1. The control room wants the whole countdown on "
            "one line, with the numbers separated by single spaces.\n\n"
            "Read n and print the numbers from n down to 1."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One line: the numbers n, n-1, ..., 1, separated by single spaces.",
        "constraints": "1 <= n <= 100",
        "explanation": "A loop can count downwards with range(n, 0, -1). Collect the numbers, then join them with spaces.",
        "tests": [
            pub("5\n", "5 4 3 2 1", "The countdown starts at 5 and stops at 1."),
            pub("1\n", "1", "A countdown from 1 is just 1."),
            hid("3\n", "3 2 1"),
            hid("10\n", "10 9 8 7 6 5 4 3 2 1"),
        ],
    },
    {
        "slug": "multiplication-table",
        "title": "Multiplication Table",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 403,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A student is learning times tables. She wants to see a number multiplied by 1, then 2, then 3, all the "
            "way up to 10.\n\n"
            "Read n and print n × 1, n × 2, ... n × 10 on one line, separated by single spaces."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One line: the ten products, separated by single spaces.",
        "constraints": "0 <= n <= 1000",
        "explanation": "Loop with i from 1 to 10, compute n * i each time, and join the results with spaces.",
        "tests": [
            pub("3\n", "3 6 9 12 15 18 21 24 27 30", "3 × 1 = 3, 3 × 2 = 6, and so on up to 3 × 10 = 30."),
            pub("1\n", "1 2 3 4 5 6 7 8 9 10", "Multiplying by 1 leaves each number unchanged."),
            hid("0\n", "0 0 0 0 0 0 0 0 0 0"),
            hid("12\n", "12 24 36 48 60 72 84 96 108 120"),
        ],
    },
    {
        "slug": "sum-of-evens-to-n",
        "title": "Sum of Evens",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 404,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A game gives points only for even numbers. For a round that goes from 1 up to n, the score is the sum of "
            "all the even numbers in that range.\n\n"
            "Read n and print the sum of all the even numbers from 1 to n."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: the sum of the even numbers from 1 to n.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Loop over 1 to n, and only add a number to the total when number % 2 == 0.",
        "tests": [
            pub("10\n", "30", "2 + 4 + 6 + 8 + 10 = 30."),
            pub("7\n", "12", "The even numbers up to 7 are 2, 4 and 6, which add up to 12."),
            hid("1\n", "0"),
            hid("100\n", "2550"),
        ],
    },
    {
        "slug": "count-digits",
        "title": "Count the Digits",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 405,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A form asks for a membership number, and the clerk wants to know how many digits it has. The number 0 "
            "counts as having one digit.\n\n"
            "Read a non-negative whole number and print how many digits it has."
        ),
        "input_format": "One line containing one non-negative integer n.",
        "output_format": "One integer: the number of digits in n.",
        "constraints": "0 <= n <= 10^9",
        "explanation": (
            "Count how many times you can divide by 10 before reaching 0, using a while loop. Treat 0 as a special case "
            "with one digit."
        ),
        "tests": [
            pub("12345\n", "5", "12345 has the digits 1, 2, 3, 4 and 5."),
            pub("0\n", "1", "Zero is written with one digit."),
            hid("7\n", "1"),
            hid("1000000\n", "7"),
        ],
    },
    {
        "slug": "power-by-loop",
        "title": "Power by Loop",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 406,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "Raising a number a to the power b means multiplying a by itself b times. For example, 2 to the power 5 is "
            "2 × 2 × 2 × 2 × 2 = 32. Any number to the power 0 is 1.\n\n"
            "Read a and b, and work out a to the power b using a loop."
        ),
        "input_format": "One line containing two integers a and b, separated by a space.",
        "output_format": "One integer: a raised to the power b.",
        "constraints": "0 <= a <= 10\n0 <= b <= 10",
        "explanation": "Start with result = 1, then multiply result by a, b times, inside a for loop.",
        "tests": [
            pub("2 5\n", "32", "2 × 2 × 2 × 2 × 2 = 32."),
            pub("3 0\n", "1", "Any number to the power 0 is 1."),
            hid("5 3\n", "125"),
            hid("10 6\n", "1000000"),
        ],
    },
    {
        "slug": "star-line",
        "title": "Star Line",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 407,
        "tags": ["Loops", "Input"],
        "description": (
            "A teacher draws a row of stars on the board to show a number. Three stars show 3, five stars show 5, and "
            "so on.\n\n"
            "Read n and print n stars on one line, with no spaces between them."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One line made of n star characters (*).",
        "constraints": "1 <= n <= 100",
        "explanation": "Repeat the star character n times. A loop can add one star each time, or you can use \"*\" * n.",
        "tests": [
            pub("3\n", "***", "Three stars for the number 3."),
            pub("1\n", "*", "One star for the number 1."),
            hid("5\n", "*****"),
            hid("10\n", "**********"),
        ],
    },
    {
        "slug": "sum-of-odds-to-n",
        "title": "Sum of Odds",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 408,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "Another game gives points for odd numbers only. For a round that goes from 1 up to n, the score is the sum "
            "of all the odd numbers in that range.\n\n"
            "Read n and print the sum of all the odd numbers from 1 to n."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: the sum of the odd numbers from 1 to n.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Loop over 1 to n, and only add a number to the total when number % 2 == 1.",
        "tests": [
            pub("5\n", "9", "1 + 3 + 5 = 9."),
            pub("10\n", "25", "1 + 3 + 5 + 7 + 9 = 25."),
            hid("1\n", "1"),
            hid("100\n", "2500"),
        ],
    },
    {
        "slug": "count-multiples",
        "title": "Count the Multiples",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 409,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A teacher is handing out sweets to every k-th student in a line of n students, starting from the k-th. "
            "She wants to know how many students will receive a sweet.\n\n"
            "Read n and k, and print how many multiples of k there are from 1 to n."
        ),
        "input_format": "One line containing two integers n and k, separated by a space.",
        "output_format": "One integer: how many multiples of k there are from 1 to n.",
        "constraints": "1 <= n <= 10^5\n1 <= k <= 10^5",
        "explanation": "Loop over 1 to n and count each number that divides evenly by k, which means number % k == 0.",
        "tests": [
            pub("10 3\n", "3", "The multiples of 3 up to 10 are 3, 6 and 9."),
            pub("5 7\n", "0", "The first multiple of 7 is 7, which is more than 5."),
            hid("100 10\n", "10"),
            hid("15 1\n", "15"),
        ],
    },
    {
        "slug": "average-rounded-down",
        "title": "Average, Rounded Down",
        "topic": "loops",
        "difficulty": "Easy",
        "sort_order": 410,
        "tags": ["Loops", "Math", "Input"],
        "description": (
            "A teacher has a list of test marks and wants the class average as a whole number. If the average is not "
            "exact, she rounds it down.\n\n"
            "Read the marks and print the average, rounded down."
        ),
        "input_format": (
            "Line 1: n, the number of marks.\n"
            "Line 2: n space-separated non-negative integers, the marks."
        ),
        "output_format": "One integer: the sum of the marks divided by n, rounded down.",
        "constraints": "1 <= n <= 10^5\n0 <= each mark <= 10^9",
        "explanation": "Add all the marks in a loop, then divide the total by n using //, which rounds down.",
        "tests": [
            pub("4\n2 4 6 8\n", "5", "The total is 20, and 20 ÷ 4 = 5."),
            pub("3\n1 2 2\n", "1", "The total is 5, and 5 ÷ 3 is 1.67, which rounds down to 1."),
            hid("1\n7\n", "7"),
            hid("3\n10 20 30\n", "20"),
        ],
    },
]
