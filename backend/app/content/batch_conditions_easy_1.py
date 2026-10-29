"""Conditions, Easy (first 10 of the 17 still needed).

Each entry carries its topic, level and sort order. Expected outputs were checked by hand.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_CONDITIONS_EASY_1 = [
    {
        "slug": "number-sign",
        "title": "Number Sign",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 301,
        "tags": ["Conditions", "Input"],
        "description": (
            "A weather station records a temperature change each hour. Some changes are rises, some are falls, and some "
            "are no change at all. The station wants a single word for each reading.\n\n"
            "Read one whole number and print Positive if it is above zero, Negative if it is below zero, or Zero if it is zero."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "Print Positive, Negative or Zero.",
        "constraints": "-10^9 <= n <= 10^9",
        "explanation": "Check for zero first. Then check whether the number is greater than zero, and if not, it must be negative.",
        "tests": [
            pub("5\n", "Positive", "5 is above zero."),
            pub("-2\n", "Negative", "-2 is below zero."),
            hid("0\n", "Zero"),
            hid("-1000000\n", "Negative"),
        ],
    },
    {
        "slug": "adult-or-child",
        "title": "Adult or Child",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 302,
        "tags": ["Conditions", "Input"],
        "description": (
            "A cinema shows a film rated for adults only. The ticket desk needs to check each customer's age, and "
            "anyone aged 18 or over counts as an adult.\n\n"
            "Read the age and print Adult if the person is 18 or older, otherwise print Child."
        ),
        "input_format": "One line containing one integer, the age.",
        "output_format": "Print Adult or Child.",
        "constraints": "0 <= age <= 150",
        "explanation": "Use one if statement that compares the age with 18. Remember that 18 itself counts as an adult.",
        "tests": [
            pub("18\n", "Adult", "18 is the cut-off, so 18 counts as an adult."),
            pub("9\n", "Child", "9 is below 18."),
            hid("17\n", "Child"),
            hid("45\n", "Adult"),
        ],
    },
    {
        "slug": "pass-or-fail",
        "title": "Pass or Fail",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 303,
        "tags": ["Conditions", "Input"],
        "description": (
            "A school marks each test out of 100. A student passes when the score is 40 or more.\n\n"
            "Read the score and print PASS if the student passed, otherwise FAIL."
        ),
        "input_format": "One line containing one integer score, from 0 to 100.",
        "output_format": "Print PASS or FAIL.",
        "constraints": "0 <= score <= 100",
        "explanation": "Compare the score with 40. A score of exactly 40 is a pass.",
        "tests": [
            pub("40\n", "PASS", "40 is the pass mark, so it counts as a pass."),
            pub("39\n", "FAIL", "39 is one below the pass mark."),
            hid("0\n", "FAIL"),
            hid("100\n", "PASS"),
        ],
    },
    {
        "slug": "compare-two",
        "title": "Compare Two",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 304,
        "tags": ["Conditions", "Input"],
        "description": (
            "Two runners finish a race, and the judge records each runner's time as a whole number of seconds. "
            "The judge wants to say who was faster, or whether they tied.\n\n"
            "Read two numbers a and b. Print Greater if a is bigger than b, Less if a is smaller, or Equal if they are the same."
        ),
        "input_format": "One line containing two integers a and b, separated by a space.",
        "output_format": "Print Greater, Less or Equal.",
        "constraints": "-10^9 <= a, b <= 10^9",
        "explanation": "Compare a with b using > and <. If neither is true, the two numbers are equal.",
        "tests": [
            pub("7 3\n", "Greater", "7 is bigger than 3."),
            pub("2 9\n", "Less", "2 is smaller than 9."),
            hid("5 5\n", "Equal"),
            hid("-4 -10\n", "Greater"),
        ],
    },
    {
        "slug": "ticket-price",
        "title": "Ticket Price",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 305,
        "tags": ["Conditions", "Input"],
        "description": (
            "A museum charges by age. Children under 5 enter free. Children from 5 to 12 pay 5, and everyone aged 13 or "
            "over pays 10.\n\n"
            "Read the visitor's age and print the ticket price."
        ),
        "input_format": "One line containing one integer, the age of the visitor.",
        "output_format": "One integer: the ticket price (0, 5 or 10).",
        "constraints": "0 <= age <= 120",
        "explanation": "Check the youngest group first, then the middle group, and treat everyone else as the adult price.",
        "tests": [
            pub("3\n", "0", "Visitors under 5 enter free."),
            pub("10\n", "5", "10 is in the 5 to 12 group."),
            hid("12\n", "5"),
            hid("13\n", "10"),
        ],
    },
    {
        "slug": "weekend-check",
        "title": "Weekend Check",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 306,
        "tags": ["Conditions", "Input"],
        "description": (
            "A gym is open every day of the week, but its classes run only on weekdays. The receptionist types a day "
            "as a number, where 1 is Monday and 7 is Sunday.\n\n"
            "Read the day number and print Weekend for Saturday or Sunday (6 or 7), otherwise print Weekday."
        ),
        "input_format": "One line containing one integer d, from 1 (Monday) to 7 (Sunday).",
        "output_format": "Print Weekend or Weekday.",
        "constraints": "1 <= d <= 7",
        "explanation": "Check whether the day is 6 or 7. Everything else is a weekday.",
        "tests": [
            pub("3\n", "Weekday", "Day 3 is Wednesday."),
            pub("7\n", "Weekend", "Day 7 is Sunday."),
            hid("6\n", "Weekend"),
            hid("1\n", "Weekday"),
        ],
    },
    {
        "slug": "grade-letter",
        "title": "Grade Letter",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 307,
        "tags": ["Conditions", "Input"],
        "description": (
            "A college turns marks into letter grades. 90 and above is an A, 75 to 89 is a B, 60 to 74 is a C, and "
            "anything below 60 is a D.\n\n"
            "Read the marks and print the letter grade."
        ),
        "input_format": "One line containing one integer m, the marks, from 0 to 100.",
        "output_format": "Print A, B, C or D.",
        "constraints": "0 <= m <= 100",
        "explanation": "Check the highest band first, then move down. Each check only needs the lower limit of its band.",
        "tests": [
            pub("95\n", "A", "95 is 90 or more, so it is an A."),
            pub("62\n", "C", "62 is from 60 to 74, so it is a C."),
            hid("75\n", "B"),
            hid("59\n", "D"),
        ],
    },
    {
        "slug": "speed-limit",
        "title": "Speed Limit",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 308,
        "tags": ["Conditions", "Input"],
        "description": (
            "A road has a speed limit of 60 km/h. A camera records the speed of each car that passes it. A car is over "
            "the limit only if it goes faster than 60.\n\n"
            "Read the speed and print Over the limit if it is faster than 60, otherwise print Within the limit."
        ),
        "input_format": "One line containing one integer s, the speed in km/h.",
        "output_format": "Print Over the limit or Within the limit.",
        "constraints": "0 <= s <= 300",
        "explanation": "A speed of exactly 60 is within the limit, so the check is for speeds greater than 60.",
        "tests": [
            pub("60\n", "Within the limit", "60 is the limit itself, so it is within it."),
            pub("75\n", "Over the limit", "75 is faster than 60."),
            hid("0\n", "Within the limit"),
            hid("61\n", "Over the limit"),
        ],
    },
    {
        "slug": "vote-eligible",
        "title": "Vote Eligible",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 309,
        "tags": ["Conditions", "Input"],
        "description": (
            "To vote in a class election, a person must be at least 18 years old and a citizen. The election officer "
            "enters the age and citizenship for each person, with 1 for yes and 0 for no.\n\n"
            "Read the age and the citizenship flag, and print ELIGIBLE only if both conditions are met, otherwise NOT ELIGIBLE."
        ),
        "input_format": "One line containing two integers: the age, then the citizenship flag (1 or 0).",
        "output_format": "Print ELIGIBLE or NOT ELIGIBLE.",
        "constraints": "0 <= age <= 150\ncitizenship flag is 0 or 1",
        "explanation": "Both conditions must be true, so join them with the word and.",
        "tests": [
            pub("20 1\n", "ELIGIBLE", "20 is 18 or older, and the flag is 1, so both conditions are met."),
            pub("17 1\n", "NOT ELIGIBLE", "17 is too young, even though the flag is 1."),
            hid("30 0\n", "NOT ELIGIBLE"),
            hid("18 1\n", "ELIGIBLE"),
        ],
    },
    {
        "slug": "room-temperature",
        "title": "Room Temperature",
        "topic": "conditions",
        "difficulty": "Easy",
        "sort_order": 310,
        "tags": ["Conditions", "Input"],
        "description": (
            "A thermostat describes the room in one word. Below 15 degrees it says Cold. From 15 to 25 degrees, "
            "inclusive, it says Comfortable. Above 25 degrees it says Hot.\n\n"
            "Read the temperature in whole degrees Celsius and print the word."
        ),
        "input_format": "One line containing one integer t, the temperature in degrees Celsius.",
        "output_format": "Print Cold, Comfortable or Hot.",
        "constraints": "-50 <= t <= 60",
        "explanation": "Check for cold first, then for comfortable. Anything left over is hot.",
        "tests": [
            pub("20\n", "Comfortable", "20 is between 15 and 25."),
            pub("10\n", "Cold", "10 is below 15."),
            hid("15\n", "Comfortable"),
            hid("26\n", "Hot"),
        ],
    },
]
