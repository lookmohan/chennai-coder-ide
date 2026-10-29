"""Batch 4: Searching (first six questions: 2 Easy, 2 Medium, 2 Hard).

Each entry carries its own difficulty, topic and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_4 = [
    {
        "slug": "linear-search-position",
        "title": "Find the Position",
        "topic": "searching",
        "difficulty": "Easy",
        "sort_order": 101,
        "tags": ["Array", "Searching"],
        "description": (
            "A librarian has a row of books, each with a number on its spine. A reader asks where a particular "
            "number is on the shelf. The shelf is numbered from 0 at the left.\n\n"
            "Read the spine numbers and the number the reader wants. Print the position of its first appearance, "
            "or -1 if it is not on the shelf."
        ),
        "input_format": (
            "Line 1: n, the number of books.\n"
            "Line 2: n space-separated integers, the numbers on the spines.\n"
            "Line 3: the number the reader wants."
        ),
        "output_format": "One integer: the position of the first match, or -1 if there is none.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each number <= 10^9",
        "explanation": "Walk through the list from left to right. Stop at the first value that matches the target.",
        "tests": [
            pub("5\n4 7 1 9 2\n7\n", "1", "The first 7 is at position 1, counting from 0."),
            pub("3\n1 2 3\n5\n", "-1", "5 is not on the shelf, so the answer is -1."),
            hid("4\n5 5 5 5\n5\n", "0"),
            hid("2\n3 4\n4\n", "1"),
        ],
    },
    {
        "slug": "is-it-there",
        "title": "Is It There?",
        "topic": "searching",
        "difficulty": "Easy",
        "sort_order": 102,
        "tags": ["Array", "Searching"],
        "description": (
            "A club keeps a list of member numbers. Before letting someone in, the door checker wants to know whether "
            "that number is on the list.\n\n"
            "Read the list and the number to check. Print YES if the number is on the list, otherwise NO."
        ),
        "input_format": (
            "Line 1: n, the number of members on the list.\n"
            "Line 2: n space-separated integers, the member numbers.\n"
            "Line 3: the number to check."
        ),
        "output_format": "Print YES if the number is on the list, otherwise NO.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each number <= 10^9",
        "explanation": "Check each value in the list. As soon as one equals the number you are looking for, the answer is YES.",
        "tests": [
            pub("4\n2 8 6 1\n6\n", "YES", "The list contains 6."),
            pub("3\n1 2 3\n7\n", "NO", "7 is not on the list."),
            hid("1\n5\n5\n", "YES"),
            hid("2\n1 1\n2\n", "NO"),
        ],
    },
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "topic": "searching",
        "difficulty": "Medium",
        "sort_order": 103,
        "tags": ["Array", "Binary Search"],
        "description": (
            "A dictionary is sorted, so you never need to read every page to find a word. You open the middle page, "
            "decide which half the word must be in, and repeat. This is binary search.\n\n"
            "Read a sorted list of different numbers and a target. Print the position of the target, or -1 if it is "
            "not in the list. Positions start at 0."
        ),
        "input_format": (
            "Line 1: n, the number of values.\n"
            "Line 2: n different integers, in increasing order.\n"
            "Line 3: the target."
        ),
        "output_format": "One integer: the position of the target, or -1 if it is not in the list.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each value <= 10^9\nThe values are in increasing order and all different.",
        "explanation": (
            "Keep two positions, low and high, around the part of the list that could still hold the target. "
            "Look at the middle, then throw away the half that cannot contain it."
        ),
        "tests": [
            pub("5\n1 3 5 7 9\n7\n", "3", "7 is the fourth value, at position 3."),
            pub("4\n2 4 6 8\n5\n", "-1", "5 falls between 4 and 6, so it is not in the list."),
            hid("1\n10\n10\n", "0"),
            hid("6\n1 2 3 4 5 6\n1\n", "0"),
        ],
    },
    {
        "slug": "search-insert-position",
        "title": "Where Would It Go?",
        "topic": "searching",
        "difficulty": "Medium",
        "sort_order": 104,
        "tags": ["Array", "Binary Search"],
        "description": (
            "A bookshop keeps its books on a shelf in order of price. A new book arrives. The shopkeeper wants to know "
            "where it belongs, so the shelf stays in order.\n\n"
            "Read the sorted prices and a new price. Print the position where the new price is, or where it would go if "
            "it is not already there."
        ),
        "input_format": (
            "Line 1: n, the number of prices.\n"
            "Line 2: n different integers, in increasing order.\n"
            "Line 3: the new price."
        ),
        "output_format": "One integer: the position of the price, or the position where it would be inserted.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each value <= 10^9\nThe values are in increasing order and all different.",
        "explanation": (
            "Walk along the list until you reach a value that is not smaller than the new one. "
            "That position is the answer, whether or not the values are equal."
        ),
        "tests": [
            pub("4\n1 3 5 6\n5\n", "2", "5 is already at position 2."),
            pub("4\n1 3 5 6\n2\n", "1", "2 is bigger than 1 and smaller than 3, so it goes at position 1."),
            hid("3\n1 3 5\n7\n", "3"),
            hid("3\n1 3 5\n0\n", "0"),
        ],
    },
    {
        "slug": "rotated-search",
        "title": "Find in a Turned Shelf",
        "topic": "searching",
        "difficulty": "Hard",
        "sort_order": 105,
        "tags": ["Array", "Binary Search"],
        "description": (
            "A list of different numbers was sorted in increasing order, and then the whole list was turned, so the "
            "start moved to somewhere in the middle. For example, 4 5 6 7 0 1 2 was made from 0 1 2 4 5 6 7.\n\n"
            "Read the turned list and a target. Print the position of the target, or -1 if it is not in the list."
        ),
        "input_format": (
            "Line 1: n, the number of values.\n"
            "Line 2: n different integers, in the turned order.\n"
            "Line 3: the target."
        ),
        "output_format": "One integer: the position of the target, or -1 if it is not in the list.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each value <= 10^9\nAll values are different.",
        "explanation": (
            "At any middle position, one half of the list is still in order. Check which half that is, and whether the "
            "target lies inside it, then choose the half to keep."
        ),
        "tests": [
            pub("7\n4 5 6 7 0 1 2\n0\n", "4", "The turned list is 4 5 6 7 0 1 2, and 0 sits at position 4."),
            pub("7\n4 5 6 7 0 1 2\n3\n", "-1", "3 is not in this list."),
            hid("1\n1\n1\n", "0"),
            hid("5\n3 4 5 1 2\n1\n", "3"),
        ],
    },
    {
        "slug": "count-peaks",
        "title": "Count the Peaks",
        "topic": "searching",
        "difficulty": "Hard",
        "sort_order": 106,
        "tags": ["Array", "Searching"],
        "description": (
            "On a hill walk, a peak is a point higher than the points on either side of it. A point at the very start "
            "or the very end only has one side, so it is a peak if it is higher than its single neighbour. "
            "A list with one point has that point as a peak.\n\n"
            "Read the heights and print how many peaks there are."
        ),
        "input_format": (
            "Line 1: n, the number of points.\n"
            "Line 2: n integers, the heights, from one end of the walk to the other."
        ),
        "output_format": "One integer: the number of peaks.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each height <= 10^9",
        "explanation": (
            "Check each point against its neighbours. Treat a missing neighbour at either end as one that is always lower."
        ),
        "tests": [
            pub("5\n1 3 2 4 1\n", "2", "3 is higher than 1 and 2, and 4 is higher than 2 and 1. That makes two peaks."),
            pub("3\n1 2 3\n", "1", "Only the last point, 3, is higher than its single neighbour."),
            hid("1\n5\n", "1"),
            hid("6\n1 2 1 2 1 2\n", "3"),
        ],
    },
]
