"""Batch 3: problems 13-26, written in full statement style.

Hidden tests are the same as in the seed, so grading does not change. Every expected output was
checked by hand against its explanation.
"""


def pub(stdin: str, out: str, why: str) -> dict:
    """Visible example with an explanation students can read."""
    return {"in": stdin, "out": out, "hidden": False, "why": why}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged on the server, never shown."""
    return {"in": stdin, "out": out, "hidden": True, "why": None}


BATCH_3 = [
    {
        "slug": "second-largest",
        "title": "Second Largest",
        "description": (
            "A school runs a quiz, and the teacher wants to award a prize to the student with the second-best score. "
            "No two students have the same score.\n\n"
            "Read the scores and print the second largest one."
        ),
        "input_format": (
            "Line 1: n, the number of scores (at least 2).\n"
            "Line 2: n distinct integers, the scores."
        ),
        "output_format": "One integer: the second largest score.",
        "constraints": "2 <= n <= 10^5\n-10^9 <= each score <= 10^9\nAll scores are different.",
        "explanation": (
            "You could sort the list, but you can also keep track of the largest and second largest values "
            "as you go through the list once."
        ),
        "tests": [
            pub("4\n3 8 1 5\n", "5", "The largest score is 8, so the second largest is 5."),
            pub("3\n10 20 30\n", "20", "30 is the largest, and 20 comes next."),
            hid("2\n-1 -5\n", "-5"),
            hid("5\n4 9 2 7 6\n", "7"),
        ],
    },
    {
        "slug": "prime-check",
        "title": "Prime Check",
        "description": (
            "A prime number is a whole number greater than 1 that has no divisors other than 1 and itself. "
            "The numbers 2, 3, 5, 7 and 11 are primes. The number 9 is not, because 3 divides it.\n\n"
            "Read one number and decide whether it is prime."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "Print YES if n is prime, otherwise NO.",
        "constraints": "1 <= n <= 10^6",
        "explanation": (
            "You only need to test divisors up to the square root of n. If none of them divides n evenly, n is prime."
        ),
        "tests": [
            pub("7\n", "YES", "7 has no divisors except 1 and 7, so it is prime."),
            pub("9\n", "NO", "3 divides 9 evenly (9 = 3 × 3), so 9 is not prime."),
            hid("1\n", "NO"),
            hid("97\n", "YES"),
        ],
    },
    {
        "slug": "sum-of-digits",
        "title": "Sum of Digits",
        "description": (
            "Every number is made of digits. The digits of 1234 are 1, 2, 3 and 4, and their sum is 10.\n\n"
            "Read one non-negative number and print the sum of its digits."
        ),
        "input_format": "One line containing one non-negative integer n.",
        "output_format": "One integer: the sum of the digits of n.",
        "constraints": "0 <= n <= 10^9",
        "explanation": (
            "Take the last digit with n % 10, add it to a total, then remove that digit with n // 10. Repeat until n is 0."
        ),
        "tests": [
            pub("1234\n", "10", "1 + 2 + 3 + 4 = 10."),
            pub("0\n", "0", "The only digit is 0."),
            hid("99999\n", "45"),
            hid("101\n", "2"),
        ],
    },
    {
        "slug": "count-words",
        "title": "Count the Words",
        "description": (
            "A writing app shows how many words a student has typed. Words are separated by spaces, and extra spaces "
            "at the start, the end or between words do not create empty words.\n\n"
            "Read one line of text and count its words."
        ),
        "input_format": "One line of text. It may start or end with spaces.",
        "output_format": "One integer: the number of words in the line.",
        "constraints": "1 <= length of the line <= 1000",
        "explanation": (
            "Splitting the line on spaces and ignoring the empty pieces gives you the words. In Python, "
            "line.split() does this for you."
        ),
        "tests": [
            pub("hello world\n", "2", "There are two words: hello and world."),
            pub("  one   two three \n", "3", "The extra spaces do not count. The words are one, two and three."),
            hid("single\n", "1"),
            hid("a b c d e\n", "5"),
        ],
    },
    {
        "slug": "two-sum-exists",
        "title": "Two Sum Exists",
        "description": (
            "A shop has a list of prices, and a customer has a budget. The customer wants to know whether any two "
            "different items in the list add up to exactly the budget.\n\n"
            "Two items are different when they come from different positions in the list, even if their prices are the same."
        ),
        "input_format": (
            "Line 1: n, the number of prices.\n"
            "Line 2: n space-separated integers, the prices.\n"
            "Line 3: the budget, one integer."
        ),
        "output_format": "Print YES if two different positions add up to the budget, otherwise NO.",
        "constraints": "1 <= n <= 10^4\n-10^9 <= each price <= 10^9",
        "explanation": (
            "For each number, ask: have I already seen the number that would complete it? If yes, you have a pair."
        ),
        "tests": [
            pub("4\n2 7 11 15\n9\n", "YES", "2 + 7 = 9, and 2 and 7 come from different positions."),
            pub("3\n1 2 3\n10\n", "NO", "No two of 1, 2 and 3 add up to 10."),
            hid("2\n5 5\n10\n", "YES"),
            hid("1\n4\n8\n", "NO"),
        ],
    },
    {
        "slug": "fibonacci",
        "title": "Fibonacci Number",
        "description": (
            "The Fibonacci numbers start with 0 and 1. Each number after that is the sum of the two before it: "
            "0, 1, 1, 2, 3, 5, 8, 13, and so on.\n\n"
            "Count from 0, so the 0th Fibonacci number is 0 and the 1st is 1. Read n and print the n-th number."
        ),
        "input_format": "One line containing one integer n.",
        "output_format": "One integer: the n-th Fibonacci number.",
        "constraints": "0 <= n <= 50",
        "explanation": "Keep the last two numbers, and move them forward one step at a time inside a loop.",
        "tests": [
            pub("0\n", "0", "The 0th Fibonacci number is 0."),
            pub("10\n", "55", "The sequence reaches 55 at position 10."),
            hid("20\n", "6765"),
            hid("50\n", "12586269025"),
        ],
    },
    {
        "slug": "anagram-check",
        "title": "Anagram Check",
        "description": (
            "Two words are anagrams when they use exactly the same letters, the same number of times. "
            "For example, listen and silent are anagrams. Hello and world are not.\n\n"
            "Read two words separated by one space, and print YES if they are anagrams, otherwise NO."
        ),
        "input_format": "One line containing two lower case words, separated by one space.",
        "output_format": "Print YES if the words are anagrams, otherwise NO.",
        "constraints": "Each word has 1 to 100 lower case letters.",
        "explanation": (
            "If you sort the letters of each word, anagrams end up looking exactly the same. Compare the two sorted versions."
        ),
        "tests": [
            pub("listen silent\n", "YES", "Both words use the letters e, i, l, n, s and t, once each."),
            pub("hello world\n", "NO", "The letters do not match, so the words are not anagrams."),
            hid("abc cba\n", "YES"),
            hid("aab abb\n", "NO"),
        ],
    },
    {
        "slug": "longest-run",
        "title": "Longest Run",
        "description": (
            "A sensor records a reading every minute. A run is a block of readings next to each other that are all "
            "the same value. In the readings 1 1 2 2 2 3, the longest run is 2 2 2, which has length 3.\n\n"
            "Read the readings and print the length of the longest run."
        ),
        "input_format": (
            "Line 1: n, the number of readings.\n"
            "Line 2: n space-separated integers, the readings."
        ),
        "output_format": "One integer: the length of the longest run.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each reading <= 10^9",
        "explanation": (
            "Keep two numbers: the length of the run you are in now, and the longest run you have seen so far. "
            "When the value changes, start counting again."
        ),
        "tests": [
            pub("6\n1 1 2 2 2 3\n", "3", "The run 2 2 2 has length 3, which is the longest."),
            pub("4\n5 6 7 8\n", "1", "No two readings are next to each other and equal, so every run has length 1."),
            hid("5\n9 9 9 9 9\n", "5"),
            hid("1\n4\n", "1"),
        ],
    },
    {
        "slug": "binary-representation",
        "title": "Binary Representation",
        "description": (
            "Computers store numbers in binary, which uses only the digits 0 and 1. Each digit is a power of 2. "
            "For example, 5 is written 101, because 4 + 1 = 5.\n\n"
            "Read a non-negative integer and print its binary form, with no leading zeros. Print 0 for the number 0."
        ),
        "input_format": "One line containing one non-negative integer n.",
        "output_format": "One line: the binary form of n.",
        "constraints": "0 <= n <= 10^9",
        "explanation": (
            "Repeatedly divide by 2 and write down the remainders. Read the remainders in reverse order at the end. "
            "In Python, bin(n)[2:] gives the same result."
        ),
        "tests": [
            pub("5\n", "101", "5 = 4 + 1, which is 1 in the 4s place, 0 in the 2s place and 1 in the 1s place."),
            pub("0\n", "0", "Zero is written as 0 in binary."),
            hid("255\n", "11111111"),
            hid("1024\n", "10000000000"),
        ],
    },
    {
        "slug": "balanced-brackets",
        "title": "Balanced Brackets",
        "description": (
            "Brackets come in three kinds: round ( ), square [ ] and curly { }. A string of brackets is balanced when "
            "every opening bracket is closed by the same kind, in the right order. The string ([]{}) is balanced. "
            "The string ([)] is not, because the brackets cross each other.\n\n"
            "Read one string of brackets and print YES if it is balanced, otherwise NO."
        ),
        "input_format": "One line containing only the characters ( ) [ ] { }.",
        "output_format": "Print YES if the brackets are balanced, otherwise NO.",
        "constraints": "1 <= length of the string <= 1000",
        "explanation": (
            "Use a stack. Push each opening bracket. When you see a closing bracket, check that the bracket on top of the "
            "stack is its matching opening bracket, and remove it."
        ),
        "tests": [
            pub("([]{})\n", "YES", "Every bracket is closed by its matching partner, in the right order."),
            pub("([)]\n", "NO", "The square bracket opens after the round one, but the round one closes first."),
            hid("((\n", "NO"),
            hid("{}[]()\n", "YES"),
        ],
    },
    {
        "slug": "move-zeroes",
        "title": "Move the Zeros",
        "description": (
            "A list of numbers has some zeros mixed in. Move all the zeros to the end, while keeping the other numbers "
            "in the same order they were in.\n\n"
            "Read the list and print the new list, separated by spaces."
        ),
        "input_format": (
            "Line 1: n, the number of values.\n"
            "Line 2: n space-separated integers."
        ),
        "output_format": "One line: the new list, with the zeros at the end.",
        "constraints": "1 <= n <= 10^5\n-10^9 <= each value <= 10^9",
        "explanation": (
            "Build a new list. Add the non-zero values in their original order, then add as many zeros as you removed."
        ),
        "tests": [
            pub("5\n0 1 0 3 12\n", "1 3 12 0 0", "The numbers 1, 3 and 12 keep their order, and the two zeros go to the end."),
            pub("3\n1 2 3\n", "1 2 3", "There are no zeros, so the list stays the same."),
            hid("4\n0 0 1 0\n", "1 0 0 0"),
            hid("2\n0 0\n", "0 0"),
        ],
    },
    {
        "slug": "max-profit",
        "title": "Best Day to Sell",
        "description": (
            "A shop owner watches the price of a product each day. She can buy on one day and sell on a later day. "
            "She wants to know the largest profit she could make with one buy and one sell.\n\n"
            "If every later price is lower than the buying price, she cannot make a profit, and the answer is 0."
        ),
        "input_format": (
            "Line 1: n, the number of days.\n"
            "Line 2: n space-separated integers, the price on each day, in order."
        ),
        "output_format": "One integer: the largest profit, or 0 if no profit is possible.",
        "constraints": "1 <= n <= 10^5\n1 <= each price <= 10^9",
        "explanation": (
            "Keep track of the lowest price so far. For each day, ask: if I sold today, what would my profit be?"
        ),
        "tests": [
            pub("6\n7 1 5 3 6 4\n", "5", "Buy at 1 (day 2) and sell at 6 (day 5): 6 - 1 = 5."),
            pub("4\n7 6 4 3 1\n", "0", "The price falls every day, so there is no profit to make."),
            hid("3\n2 4 1\n", "2"),
            hid("5\n1 2 3 4 5\n", "4"),
        ],
    },
    {
        "slug": "longest-unique-substring",
        "title": "Longest Run Without Repeats",
        "description": (
            "A password checker looks for the longest stretch of letters in a word where no letter appears twice. "
            "In abcabcbb, the best stretch is abc, which has length 3.\n\n"
            "Read one word of lower case letters and print the length of the longest stretch with no repeated letters."
        ),
        "input_format": "One line containing lower case letters only.",
        "output_format": "One integer: the length of the longest stretch with no repeated letters.",
        "constraints": "1 <= length of the word <= 10^5",
        "explanation": (
            "Use a window that slides along the word. When a letter repeats inside the window, move the left edge "
            "forward until the repeat is gone."
        ),
        "tests": [
            pub("abcabcbb\n", "3", "The longest stretch without a repeat is abc, which has length 3."),
            pub("bbbbb\n", "1", "Every letter is the same, so the longest stretch is a single letter."),
            hid("pwwkew\n", "3"),
            hid("abcdef\n", "6"),
        ],
    },
    {
        "slug": "coin-change",
        "title": "Fewest Coins",
        "description": (
            "A cashier needs to give exact change using coins. There is an unlimited supply of each coin value. "
            "She wants to use as few coins as possible.\n\n"
            "Read the amount and the coin values, and print the fewest coins that add up to the amount. "
            "If the amount cannot be made, print -1."
        ),
        "input_format": (
            "Line 1: the amount.\n"
            "Line 2: the coin values, separated by spaces."
        ),
        "output_format": "One integer: the fewest coins needed, or -1 if the amount cannot be made.",
        "constraints": (
            "0 <= amount <= 10^4\n"
            "1 to 100 coin values, each between 1 and 10^4"
        ),
        "explanation": (
            "Work out the answer for each amount from 0 up to the target. Each amount can be built from a smaller amount "
            "plus one coin, so reuse the answers you have already found."
        ),
        "tests": [
            pub("11\n1 2 5\n", "3", "Use 5 + 5 + 1 = 11. Three coins is the fewest possible."),
            pub("3\n2\n", "-1", "Only 2-value coins are available, so an odd amount such as 3 can never be made."),
            hid("0\n1 2\n", "0"),
            hid("30\n7 3\n", "6"),
        ],
    },
]
