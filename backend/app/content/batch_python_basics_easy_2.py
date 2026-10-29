"""Python Basics, Easy (questions 11-17, completing the 20 Easy questions).

Each entry carries its topic, level and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_PYTHON_BASICS_EASY_2 = [
    {
        "slug": "perimeter-of-a-square",
        "title": "Perimeter of a Square",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 211,
        "tags": ["Math", "Input"],
        "description": (
            "A gardener wants to put a fence around a square flower bed. Each side of the bed is the same length, "
            "so the fence needs four equal parts.\n\n"
            "Read the length of one side and print the total length of fence needed."
        ),
        "input_format": "One line containing one integer s, the length of one side.",
        "output_format": "One integer: the perimeter, which is 4 × s.",
        "constraints": "0 <= s <= 10^6",
        "explanation": "A square has four sides of equal length, so the perimeter is four times one side.",
        "tests": [
            pub("3\n", "12", "Four sides of 3 make 4 × 3 = 12."),
            pub("0\n", "0", "A bed with no size needs no fence."),
            hid("10\n", "40"),
            hid("1000000\n", "4000000"),
        ],
    },
    {
        "slug": "tip-amount",
        "title": "Tip Amount",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 212,
        "tags": ["Math", "Input"],
        "description": (
            "A customer leaves a tip of a certain percentage of the bill. The waiter wants to know the tip amount in "
            "whole money units, rounded down.\n\n"
            "Read the bill and the tip percentage, and print the tip, rounded down to a whole number."
        ),
        "input_format": "One line containing two integers: the bill and the tip percentage.",
        "output_format": "One integer: the tip, which is bill × percent divided by 100, rounded down.",
        "constraints": "0 <= bill <= 10^6\n0 <= percent <= 100",
        "explanation": "Multiply the bill by the percentage, then divide by 100 using // so the result rounds down.",
        "tests": [
            pub("200 15\n", "30", "15% of 200 is 200 × 15 ÷ 100 = 30."),
            pub("45 0\n", "0", "A 0% tip is nothing."),
            hid("99 10\n", "9"),
            hid("1000 100\n", "1000"),
        ],
    },
    {
        "slug": "last-digit",
        "title": "Last Digit",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 213,
        "tags": ["Math", "Input"],
        "description": (
            "A bus ticket number ends with a digit that tells the seat row. The conductor wants to find that last digit "
            "quickly, without counting.\n\n"
            "Read a non-negative number and print its last digit."
        ),
        "input_format": "One line containing one non-negative integer n.",
        "output_format": "One integer: the last digit of n.",
        "constraints": "0 <= n <= 10^9",
        "explanation": "The remainder after dividing by 10 is always the last digit. Use n % 10.",
        "tests": [
            pub("1234\n", "4", "The remainder when 1234 is divided by 10 is 4."),
            pub("7\n", "7", "A single digit is its own last digit."),
            hid("0\n", "0"),
            hid("1000\n", "0"),
        ],
    },
    {
        "slug": "time-left",
        "title": "Time Left",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 214,
        "tags": ["Math", "Input"],
        "description": (
            "A student has a timed quiz of a certain number of minutes. She has already used some of the time, and wants "
            "to know how many minutes remain.\n\n"
            "Read the total minutes and the minutes already used, and print the minutes left."
        ),
        "input_format": "One line containing two integers: the total minutes and the minutes already used.",
        "output_format": "One integer: the minutes left, which is total minus used.",
        "constraints": "0 <= used <= total <= 10^6",
        "explanation": "Subtract the minutes used from the total minutes.",
        "tests": [
            pub("90 25\n", "65", "90 - 25 = 65 minutes remain."),
            pub("10 10\n", "0", "All the time has been used, so none is left."),
            hid("60 0\n", "60"),
            hid("120 45\n", "75"),
        ],
    },
    {
        "slug": "change-given",
        "title": "Change Given",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 215,
        "tags": ["Math", "Input"],
        "description": (
            "A customer pays for an item with a note. The shopkeeper has to give back the difference, which is the "
            "change.\n\n"
            "Read the amount paid and the price of the item, and print the change to give back."
        ),
        "input_format": "One line containing two integers: the amount paid and the price.",
        "output_format": "One integer: the amount paid minus the price.",
        "constraints": "0 <= price <= amount paid <= 10^6",
        "explanation": "The change is the amount paid minus the price.",
        "tests": [
            pub("10 7\n", "3", "10 - 7 = 3 is the change."),
            pub("5 5\n", "0", "The exact amount was paid, so no change is due."),
            hid("100 1\n", "99"),
            hid("20 0\n", "20"),
        ],
    },
    {
        "slug": "full-dozens",
        "title": "Full Dozens",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 216,
        "tags": ["Math", "Input"],
        "description": (
            "A farm sells eggs in boxes of twelve. A customer buys a number of eggs, and the farmer counts only the full "
            "boxes he can pack.\n\n"
            "Read the number of eggs and print how many full boxes of twelve can be packed."
        ),
        "input_format": "One line containing one non-negative integer n, the number of eggs.",
        "output_format": "One integer: the number of full boxes of 12.",
        "constraints": "0 <= n <= 10^6",
        "explanation": "Divide by 12 using //, which keeps only the whole boxes.",
        "tests": [
            pub("30\n", "2", "Two full boxes use 24 eggs, with 6 left over, so the answer is 2."),
            pub("11\n", "0", "Eleven eggs are not enough for a full box."),
            hid("12\n", "1"),
            hid("1000\n", "83"),
        ],
    },
    {
        "slug": "speed-per-hour",
        "title": "Speed Per Hour",
        "topic": "python-basics",
        "difficulty": "Easy",
        "sort_order": 217,
        "tags": ["Math", "Input"],
        "description": (
            "A cyclist covered a distance in a number of hours. The club wants her average speed for each whole hour, "
            "rounded down.\n\n"
            "Read the distance in kilometres and the number of hours, and print the speed in whole kilometres per hour."
        ),
        "input_format": "One line containing two integers: the distance in kilometres and the number of hours.",
        "output_format": "One integer: the distance divided by the hours, rounded down.",
        "constraints": "0 <= distance <= 10^6\n1 <= hours <= 1000",
        "explanation": "Divide the distance by the hours using //, which rounds the answer down.",
        "tests": [
            pub("120 2\n", "60", "120 km in 2 hours is 60 km per hour."),
            pub("100 3\n", "33", "100 ÷ 3 is 33.33, which rounds down to 33."),
            hid("7 2\n", "3"),
            hid("0 5\n", "0"),
        ],
    },
]
