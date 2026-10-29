"""Python Basics, Easy (questions 1-10 of 20).

Each entry carries its topic, level and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_PYTHON_BASICS_EASY_1 = [
    {
        "slug": "add-three-numbers",
        "title": "Add Three Numbers",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 201,
        "tags": ["Math", "Input"],
        "description": (
            "A shopkeeper writes three amounts on a slip of paper: the cash, the card payment and the coupon. "
            "She wants the total.\n\n"
            "Read the three whole numbers from one line and print their sum."
        ),
        "input_format": "One line containing three integers a, b and c, separated by spaces.",
        "output_format": "One integer: a + b + c.",
        "constraints": "-10^9 <= a, b, c <= 10^9",
        "explanation": "Use input().split() to get the three parts, convert each with int(), then add them.",
        "tests": [
            pub("1 2 3\n", "6", "1 + 2 + 3 = 6."),
            pub("10 -5 0\n", "5", "10 + (-5) + 0 = 5."),
            hid("0 0 0\n", "0"),
            hid("1000000 1000000 1000000\n", "3000000"),
        ],
    },
    {
        "slug": "rectangle-area",
        "title": "Rectangle Area",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 202,
        "tags": ["Math", "Input"],
        "description": (
            "A student is painting a rectangular wall. She needs to know how much area it covers, so she can buy "
            "the right amount of paint.\n\n"
            "Read the length and the width, and print the area. The area is length multiplied by width."
        ),
        "input_format": "One line containing two integers: the length and the width, separated by a space.",
        "output_format": "One integer: the area of the rectangle.",
        "constraints": "0 <= length, width <= 10^6",
        "explanation": "Area is length × width. In Python, use the * operator.",
        "tests": [
            pub("4 5\n", "20", "4 × 5 = 20."),
            pub("7 1\n", "7", "7 × 1 = 7. A strip one unit wide still has area."),
            hid("0 9\n", "0"),
            hid("1000 1000\n", "1000000"),
        ],
    },
    {
        "slug": "total-cost",
        "title": "Total Cost",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 203,
        "tags": ["Math", "Input"],
        "description": (
            "A bakery sells every cake for the same price. A customer buys several cakes and wants to know the total "
            "before paying.\n\n"
            "Read the price of one cake and the number of cakes, and print the total cost."
        ),
        "input_format": "One line containing two integers: the price of one cake and the number of cakes.",
        "output_format": "One integer: the total cost.",
        "constraints": "0 <= price <= 10^6\n0 <= number of cakes <= 10^6",
        "explanation": "Multiply the price by the number of cakes.",
        "tests": [
            pub("5 3\n", "15", "3 cakes at 5 each cost 3 × 5 = 15."),
            pub("12 0\n", "0", "No cakes were bought, so the total is 0."),
            hid("7 10\n", "70"),
            hid("100 100\n", "10000"),
        ],
    },
    {
        "slug": "middle-of-two",
        "title": "Middle of Two",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 204,
        "tags": ["Math", "Input"],
        "description": (
            "Two friends each have a number of marbles. They want to share them out as evenly as they can. "
            "Each gets the same whole number of marbles, and any leftover is ignored.\n\n"
            "Read the two numbers and print the whole-number average, rounding down."
        ),
        "input_format": "One line containing two integers a and b.",
        "output_format": "One integer: (a + b) divided by 2, rounded down.",
        "constraints": "-10^9 <= a, b <= 10^9",
        "explanation": "Use the // operator, which divides and rounds down. Negative results round down too.",
        "tests": [
            pub("3 4\n", "3", "(3 + 4) = 7, and 7 // 2 rounds down to 3."),
            pub("10 20\n", "15", "(10 + 20) = 30, and 30 // 2 = 15."),
            hid("-3 -4\n", "-4"),
            hid("0 1\n", "0"),
        ],
    },
    {
        "slug": "remainder-machine",
        "title": "Remainder Machine",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 205,
        "tags": ["Math", "Input"],
        "description": (
            "A machine deals cards into piles. It puts as many cards as it can into full piles of size b, and whatever "
            "is left over goes into one last pile. Your job is to report how many cards are left over.\n\n"
            "Read the number of cards a and the pile size b, and print the number of cards left over."
        ),
        "input_format": "One line containing two integers: a (the cards) and b (the pile size).",
        "output_format": "One integer: a % b, the number of cards left over.",
        "constraints": "0 <= a <= 10^9\n1 <= b <= 10^6",
        "explanation": "The % operator gives the remainder after division.",
        "tests": [
            pub("17 5\n", "2", "Three full piles of 5 use 15 cards, and 17 - 15 = 2 are left."),
            pub("9 3\n", "0", "9 divides exactly into piles of 3, so nothing is left."),
            hid("4 7\n", "4"),
            hid("100 9\n", "1"),
        ],
    },
    {
        "slug": "word-length",
        "title": "Word Length",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 206,
        "tags": ["String", "Input"],
        "description": (
            "A game gives points for the length of the word you type. Before scoring, the game needs to count the "
            "letters.\n\n"
            "Read one word and print how many characters it has."
        ),
        "input_format": "One line containing one word with no spaces.",
        "output_format": "One integer: the number of characters in the word.",
        "constraints": "1 <= length of the word <= 100",
        "explanation": "The built-in len() function counts the characters in a string.",
        "tests": [
            pub("python\n", "6", "p, y, t, h, o, n: six characters."),
            pub("a\n", "1", "A single letter has length 1."),
            hid("chennai\n", "7"),
            hid("coder\n", "5"),
        ],
    },
    {
        "slug": "swap-two-numbers",
        "title": "Swap Two Numbers",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 207,
        "tags": ["Math", "Input"],
        "description": (
            "Two numbers are written on a whiteboard in the order a, then b. The teacher asks the class to swap them, "
            "so b comes first.\n\n"
            "Read the two numbers and print them in swapped order, separated by one space."
        ),
        "input_format": "One line containing two integers a and b, separated by a space.",
        "output_format": "One line: b and a, separated by one space.",
        "constraints": "-10^9 <= a, b <= 10^9",
        "explanation": "Assign the two values to two variables, then print them in the opposite order.",
        "tests": [
            pub("3 8\n", "8 3", "The swapped order is 8 then 3."),
            pub("-1 0\n", "0 -1", "The swapped order is 0 then -1."),
            hid("5 5\n", "5 5"),
            hid("100 -100\n", "-100 100"),
        ],
    },
    {
        "slug": "double-and-add-one",
        "title": "Double and Add One",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 208,
        "tags": ["Math", "Input"],
        "description": (
            "A game gives a score by doubling a number and then adding one. Players want the score for a starting "
            "number.\n\n"
            "Read the starting number n and print 2 × n + 1."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: 2 × n + 1.",
        "constraints": "-10^6 <= n <= 10^6",
        "explanation": "Multiply by 2 first, then add 1.",
        "tests": [
            pub("3\n", "7", "2 × 3 = 6, and 6 + 1 = 7."),
            pub("0\n", "1", "2 × 0 = 0, and 0 + 1 = 1."),
            hid("-4\n", "-7"),
            hid("500\n", "1001"),
        ],
    },
    {
        "slug": "square-of-a-number",
        "title": "Square of a Number",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 209,
        "tags": ["Math", "Input"],
        "description": (
            "A square garden has sides of length n. The gardener wants to know the area of the garden, which is the "
            "side length multiplied by itself.\n\n"
            "Read n and print its square, n × n."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: n × n.",
        "constraints": "-10^4 <= n <= 10^4",
        "explanation": "A square number is the number multiplied by itself. A negative number squared is positive.",
        "tests": [
            pub("4\n", "16", "4 × 4 = 16."),
            pub("-3\n", "9", "(-3) × (-3) = 9, because a negative times a negative is positive."),
            hid("0\n", "0"),
            hid("1000\n", "1000000"),
        ],
    },
    {
        "slug": "minutes-to-seconds",
        "title": "Minutes to Seconds",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 210,
        "tags": ["Math", "Input"],
        "description": (
            "A video editor measures clips in minutes, but the software needs them in seconds. Each minute has 60 "
            "seconds.\n\n"
            "Read a number of minutes and print the same length in seconds."
        ),
        "input_format": "One line containing one non-negative integer m, the number of minutes.",
        "output_format": "One integer: the number of seconds, which is m × 60.",
        "constraints": "0 <= m <= 10^6",
        "explanation": "Multiply the minutes by 60.",
        "tests": [
            pub("2\n", "120", "2 minutes is 2 × 60 = 120 seconds."),
            pub("0\n", "0", "Zero minutes is zero seconds."),
            hid("15\n", "900"),
            hid("1440\n", "86400"),
        ],
    },
]
