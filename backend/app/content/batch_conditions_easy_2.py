"""Conditions, Easy (last 7 of 20).

Each entry carries its topic, level and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_CONDITIONS_EASY_2 = [
    {
        "slug": "triangle-check",
        "title": "Triangle Check",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 311,
        "tags": ["Conditions", "Math", "Input"],
        "description": (
            "A carpenter wants to cut three pieces of wood to make a triangle. A triangle can only be formed when every "
            "side is longer than zero, and the two shorter sides together are longer than the longest side.\n\n"
            "Read the three side lengths and print YES if they can form a triangle, otherwise NO."
        ),
        "input_format": "One line containing three integers a, b and c, the side lengths.",
        "output_format": "Print YES or NO.",
        "constraints": "0 <= a, b, c <= 10^6",
        "explanation": "Check that each side is above zero, and that each pair of sides adds up to more than the third side.",
        "tests": [
            pub("3 4 5\n", "YES", "3 + 4 is 7, which is more than 5, and the other pairs also work."),
            pub("1 2 10\n", "NO", "1 + 2 is only 3, which is far less than 10."),
            hid("2 2 2\n", "YES"),
            hid("0 3 3\n", "NO"),
        ],
    },
    {
        "slug": "odd-and-positive",
        "title": "Odd and Positive",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 312,
        "tags": ["Conditions", "Math", "Input"],
        "description": (
            "A raffle only accepts entry numbers that are both positive and odd. The organiser checks each number as "
            "it is written on a ticket.\n\n"
            "Read the number and print YES if it is positive and odd, otherwise NO."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "Print YES or NO.",
        "constraints": "-10^9 <= n <= 10^9",
        "explanation": "Both checks must pass: n is above zero, and n % 2 is 1.",
        "tests": [
            pub("7\n", "YES", "7 is positive and odd."),
            pub("4\n", "NO", "4 is positive but even."),
            hid("-3\n", "NO"),
            hid("1\n", "YES"),
        ],
    },
    {
        "slug": "big-order-discount",
        "title": "Big Order Discount",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 313,
        "tags": ["Conditions", "Math", "Input"],
        "description": (
            "A shop gives 10% off any order of 1000 or more. Smaller orders pay the full price.\n\n"
            "Read the order amount and print the amount to pay. For a discounted order, 10% is removed, rounded down to a "
            "whole number."
        ),
        "input_format": "One line containing one integer a, the order amount.",
        "output_format": "One integer: the amount to pay.",
        "constraints": "0 <= a <= 10^7",
        "explanation": "If the amount is 1000 or more, subtract a // 10 from it. Otherwise pay the full amount.",
        "tests": [
            pub("1500\n", "1350", "10% of 1500 is 150, so 1500 - 150 = 1350."),
            pub("900\n", "900", "900 is under 1000, so there is no discount."),
            hid("1000\n", "900"),
            hid("0\n", "0"),
        ],
    },
    {
        "slug": "divisible-by-both",
        "title": "Divisible by Both",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 314,
        "tags": ["Conditions", "Math", "Input"],
        "description": (
            "A factory packs items into boxes. A box is only full when the number of items divides exactly by both 4 "
            "and 6, with nothing left over.\n\n"
            "Read the number of items and print YES if it divides exactly by both 4 and 6, otherwise NO."
        ),
        "input_format": "One line containing one non-negative integer n.",
        "output_format": "Print YES or NO.",
        "constraints": "0 <= n <= 10^9",
        "explanation": "Check that n % 4 and n % 6 are both 0. Zero divides exactly, so 0 counts.",
        "tests": [
            pub("12\n", "YES", "12 divides exactly by 4 (3 times) and by 6 (2 times)."),
            pub("8\n", "NO", "8 divides by 4, but not by 6."),
            hid("0\n", "YES"),
            hid("18\n", "NO"),
        ],
    },
    {
        "slug": "day-or-night",
        "title": "Day or Night",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 315,
        "tags": ["Conditions", "Input"],
        "description": (
            "A garden lamp switches on at night. It counts the hours from midnight, where 0 is midnight and 23 is the "
            "last hour before midnight again. The hours from 6 up to, but not including, 18 are daytime.\n\n"
            "Read the hour and print Day if it is daytime, otherwise print Night."
        ),
        "input_format": "One line containing one integer h, from 0 to 23.",
        "output_format": "Print Day or Night.",
        "constraints": "0 <= h <= 23",
        "explanation": "Day is from 6 up to 17, so check that h is at least 6 and less than 18.",
        "tests": [
            pub("10\n", "Day", "10 is between 6 and 17."),
            pub("20\n", "Night", "20 is after 18, so it is night."),
            hid("6\n", "Day"),
            hid("18\n", "Night"),
        ],
    },
    {
        "slug": "shirt-size",
        "title": "Shirt Size",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 316,
        "tags": ["Conditions", "Input"],
        "description": (
            "A clothing shop sizes shirts by chest measurement in centimetres. Up to and including 90 is S, up to and "
            "including 100 is M, up to and including 110 is L, and anything bigger is XL.\n\n"
            "Read the chest measurement and print the shirt size."
        ),
        "input_format": "One line containing one integer c, the chest size in centimetres.",
        "output_format": "Print S, M, L or XL.",
        "constraints": "50 <= c <= 200",
        "explanation": "Check the smallest limit first. Each check only needs to compare with its upper limit.",
        "tests": [
            pub("95\n", "M", "95 is above 90 and up to 100."),
            pub("85\n", "S", "85 is up to 90."),
            hid("90\n", "S"),
            hid("111\n", "XL"),
        ],
    },
    {
        "slug": "login-check",
        "title": "Login Check",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 317,
        "tags": ["Conditions", "String", "Input"],
        "description": (
            "A club door checks a username and a PIN before letting someone in. The username and PIN must match exactly, "
            "including upper and lower case letters.\n\n"
            "Read the username and the PIN, separated by a space. Print Welcome if the username is admin and the PIN is "
            "1234, otherwise print Access denied."
        ),
        "input_format": "One line containing a username and a PIN, separated by one space.",
        "output_format": "Print Welcome or Access denied.",
        "constraints": "Each part has 1 to 20 characters with no spaces.",
        "explanation": "Split the line into two parts, then check both parts. Text comparisons are case-sensitive.",
        "tests": [
            pub("admin 1234\n", "Welcome", "Both the username and the PIN match."),
            pub("admin 0000\n", "Access denied", "The PIN is wrong."),
            hid("guest 1234\n", "Access denied"),
            hid("Admin 1234\n", "Access denied"),
        ],
    },
]
