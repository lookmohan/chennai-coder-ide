"""Create DEVELOPMENT SAMPLE problems. These are placeholders, not Chennai Coder content.

    python -m app.seed

The list below is the learning path, in order. Problem N is the Nth entry.
Idempotent: existing problems keep their content; only their position is updated.
"""
from sqlalchemy import select

from app.core.database import get_session_factory
from app.models import Problem, ProblemStatus, ProblemTestCase

PY_STUB = "# Write your solution here\n"
JS_STUB = "// Write your solution here\n"
STARTERS = {"python": PY_STUB, "javascript": JS_STUB}


def pub(stdin: str, out: str) -> dict:
    """Example test: visible to the student."""
    return {"in": stdin, "out": out, "hidden": False}


def hid(stdin: str, out: str) -> dict:
    """Hidden test: judged, never shown."""
    return {"in": stdin, "out": out, "hidden": True}


SAMPLES = [
    # ---------- Warm-up (Easy) ----------
    {
        "slug": "sum-of-two-numbers", "title": "Sum of Two Numbers", "difficulty": "Easy", "tags": ["Math"],
        "description": "Read two integers, a and b, from one line and print their sum.",
        "input_format": "A single line with two space-separated integers a and b.",
        "output_format": "Print a + b.",
        "constraints": "-10^9 <= a, b <= 10^9",
        "explanation": "Split the line into two parts, turn each part into a number, then add them.",
        "tests": [pub("2 3\n", "5"), pub("10 -4\n", "6"), hid("0 0\n", "0"), hid("1000000000 1000000000\n", "2000000000")],
    },
    {
        "slug": "say-hello", "title": "Say Hello", "difficulty": "Easy", "tags": ["Strings"],
        "description": "Read a name and greet it. This is your first output, so take your time and enjoy it.",
        "input_format": "A single line with one name.",
        "output_format": 'Print "Hello, " followed by the name and an exclamation mark.',
        "constraints": "1 <= length of the name <= 50",
        "explanation": "Joining pieces of text together is called concatenation or formatting.",
        "tests": [pub("Asha\n", "Hello, Asha!"), pub("Mohanraj\n", "Hello, Mohanraj!"),
                  hid("Chennai\n", "Hello, Chennai!"), hid("Coder\n", "Hello, Coder!")],
    },
    {
        "slug": "double-it", "title": "Double It", "difficulty": "Easy", "tags": ["Math"],
        "description": "Read a whole number and print twice its value.",
        "input_format": "One integer n.",
        "output_format": "Print 2 × n.",
        "constraints": "-10^6 <= n <= 10^6",
        "explanation": "Multiply the number by 2.",
        "tests": [pub("4\n", "8"), pub("0\n", "0"), hid("-7\n", "-14"), hid("1000000\n", "2000000")],
    },
    {
        "slug": "is-even", "title": "Is It Even?", "difficulty": "Easy", "tags": ["Math", "Conditions"],
        "description": "Decide whether a number is even or odd. A number is even when dividing it by 2 leaves no remainder.",
        "input_format": "One integer n.",
        "output_format": "Print Even or Odd.",
        "constraints": "-10^9 <= n <= 10^9",
        "explanation": "The remainder operator (% in most languages) tells you what is left after dividing.",
        "tests": [pub("4\n", "Even"), pub("7\n", "Odd"), hid("0\n", "Even"), hid("-3\n", "Odd")],
    },
    {
        "slug": "largest-of-three", "title": "Largest of Three", "difficulty": "Easy", "tags": ["Math", "Conditions"],
        "description": "Find the largest of three numbers. Compare two numbers first, then compare the winner with the third.",
        "input_format": "One line with three integers a, b and c.",
        "output_format": "Print the largest of them.",
        "constraints": "-10^9 <= a, b, c <= 10^9",
        "explanation": "Keep a 'best so far' value and compare each new number with it.",
        "tests": [pub("3 9 4\n", "9"), pub("-1 -5 -2\n", "-1"), hid("7 7 7\n", "7"), hid("0 100 50\n", "100")],
    },
    {
        "slug": "reverse-a-string", "title": "Reverse a String", "difficulty": "Easy", "tags": ["String"],
        "description": "Read one line of text and print its characters in reverse order.",
        "input_format": "A single line of text.",
        "output_format": "The reversed line.",
        "constraints": "1 <= length <= 1000",
        "explanation": "Many languages can reverse a string with one built-in function or a slice.",
        "tests": [pub("hello world\n", "dlrow olleh"), pub("a\n", "a"),
                  hid("racecar\n", "racecar"), hid("Chennai\n", "iannehC")],
    },
    {
        "slug": "count-even-numbers", "title": "Count Even Numbers", "difficulty": "Easy", "tags": ["Array"],
        "description": "The first line contains n. The second line contains n integers. Print how many of them are even.",
        "input_format": "Line 1: n. Line 2: n space-separated integers.",
        "output_format": "A single integer: the count of even numbers.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Go through the numbers one by one and keep a running count.",
        "tests": [pub("5\n1 2 3 4 5\n", "2"), pub("3\n2 4 6\n", "3"),
                  hid("4\n1 3 5 7\n", "0"), hid("1\n0\n", "1")],
    },
    {
        "slug": "sum-of-array", "title": "Sum of an Array", "difficulty": "Easy", "tags": ["Array"],
        "description": "Add up every number in a list. You will use a loop here, one of the most important ideas in programming.",
        "input_format": "Line 1: n. Line 2: n space-separated integers.",
        "output_format": "The sum of the numbers.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Start with a total of 0 and add each number to it.",
        "tests": [pub("3\n1 2 3\n", "6"), pub("4\n-1 -2 10 5\n", "12"),
                  hid("1\n100\n", "100"), hid("5\n0 0 0 0 0\n", "0")],
    },
    {
        "slug": "factorial", "title": "Factorial", "difficulty": "Easy", "tags": ["Math", "Loops"],
        "description": "Compute n! = 1 × 2 × ... × n. Remember that 0! = 1.",
        "input_format": "One integer n.",
        "output_format": "The value of n!.",
        "constraints": "0 <= n <= 12",
        "explanation": "Multiply up from 1 to n, one number at a time.",
        "tests": [pub("5\n", "120"), pub("0\n", "1"), hid("10\n", "3628800"), hid("12\n", "479001600")],
    },
    {
        "slug": "fizzbuzz", "title": "FizzBuzz", "difficulty": "Easy", "tags": ["Math", "Conditions"],
        "description": "If a number is divisible by 3 print Fizz. If it is divisible by 5 print Buzz. If both, print FizzBuzz. Otherwise print the number.",
        "input_format": "One integer n.",
        "output_format": "Fizz, Buzz, FizzBuzz, or n itself.",
        "constraints": "1 <= n <= 10^6",
        "explanation": "Check the 'divisible by both' case first, then the single cases.",
        "tests": [pub("3\n", "Fizz"), pub("5\n", "Buzz"), hid("15\n", "FizzBuzz"), hid("7\n", "7")],
    },
    {
        "slug": "count-vowels", "title": "Count the Vowels", "difficulty": "Easy", "tags": ["String"],
        "description": "Count the vowels (a, e, i, o, u) in a line of text. Upper and lower case both count.",
        "input_format": "A single line of letters.",
        "output_format": "The number of vowels.",
        "constraints": "1 <= length <= 1000",
        "explanation": "Check each character to see whether it is one of the vowel letters.",
        "tests": [pub("hello\n", "2"), pub("Chennai\n", "3"), hid("rhythm\n", "0"), hid("AEIOU\n", "5")],
    },
    {
        "slug": "palindrome-check", "title": "Palindrome Check", "difficulty": "Easy", "tags": ["String"],
        "description": "A palindrome reads the same forwards and backwards, like 'level'. Decide whether a word is one.",
        "input_format": "A single word with no spaces.",
        "output_format": "Print YES if it is a palindrome, otherwise NO.",
        "constraints": "1 <= length <= 1000. Upper and lower case are different letters.",
        "explanation": "Compare the word with its reverse.",
        "tests": [pub("racecar\n", "YES"), pub("hello\n", "NO"), hid("a\n", "YES"), hid("Ab\n", "NO")],
    },
    # ---------- Building blocks (Medium) ----------
    {
        "slug": "second-largest", "title": "Second Largest", "difficulty": "Medium", "tags": ["Array", "Sorting"],
        "description": "Find the second largest number in a list. All the numbers in the list are different.",
        "input_format": "Line 1: n (at least 2). Line 2: n distinct integers.",
        "output_format": "The second largest number.",
        "constraints": "2 <= n <= 10^5",
        "explanation": "You could sort the list. Can you track the two largest values in one pass instead?",
        "tests": [pub("4\n3 8 1 5\n", "5"), pub("3\n10 20 30\n", "20"),
                  hid("2\n-1 -5\n", "-5"), hid("5\n4 9 2 7 6\n", "7")],
    },
    {
        "slug": "prime-check", "title": "Prime Check", "difficulty": "Medium", "tags": ["Math"],
        "description": "A prime number is greater than 1 and has no divisors other than 1 and itself. Is the number prime?",
        "input_format": "One integer n.",
        "output_format": "Print YES if n is prime, otherwise NO.",
        "constraints": "1 <= n <= 10^6",
        "explanation": "You only need to test divisors up to the square root of n.",
        "tests": [pub("7\n", "YES"), pub("9\n", "NO"), hid("1\n", "NO"), hid("97\n", "YES")],
    },
    {
        "slug": "sum-of-digits", "title": "Sum of Digits", "difficulty": "Medium", "tags": ["Math"],
        "description": "Add together the digits of a number. For example, 1234 gives 1 + 2 + 3 + 4 = 10.",
        "input_format": "One non-negative integer n.",
        "output_format": "The sum of its digits.",
        "constraints": "0 <= n <= 10^9",
        "explanation": "Take the last digit with n % 10, add it, then remove it with n // 10. Repeat.",
        "tests": [pub("1234\n", "10"), pub("0\n", "0"), hid("99999\n", "45"), hid("101\n", "2")],
    },
    {
        "slug": "count-words", "title": "Count the Words", "difficulty": "Medium", "tags": ["String"],
        "description": "Count how many words are in a line. Words are separated by spaces. Extra spaces at the start or end do not count.",
        "input_format": "A single line of text.",
        "output_format": "The number of words.",
        "constraints": "1 <= length <= 1000",
        "explanation": "Splitting on whitespace and ignoring empty pieces does most of the work.",
        "tests": [pub("hello world\n", "2"), pub("  one   two three \n", "3"),
                  hid("single\n", "1"), hid("a b c d e\n", "5")],
    },
    {
        "slug": "two-sum-exists", "title": "Two Sum Exists", "difficulty": "Medium", "tags": ["Array", "Hash Map"],
        "description": "Is there a pair of different positions in the list whose values add up to a target number?",
        "input_format": "Line 1: n. Line 2: n integers. Line 3: the target.",
        "output_format": "YES if such a pair exists, otherwise NO.",
        "constraints": "1 <= n <= 10^4",
        "explanation": "For each number, ask: have I already seen the number that would complete it?",
        "tests": [pub("4\n2 7 11 15\n9\n", "YES"), pub("3\n1 2 3\n10\n", "NO"),
                  hid("2\n5 5\n10\n", "YES"), hid("1\n4\n8\n", "NO")],
    },
    {
        "slug": "fibonacci", "title": "Fibonacci Number", "difficulty": "Medium", "tags": ["Math", "Loops"],
        "description": "The Fibonacci sequence starts 0, 1, and each next number is the sum of the two before it: 0, 1, 1, 2, 3, 5, ... Print the n-th number, counting from 0.",
        "input_format": "One integer n.",
        "output_format": "F(n).",
        "constraints": "0 <= n <= 50",
        "explanation": "Keep track of the last two numbers and move them forward in a loop.",
        "tests": [pub("0\n", "0"), pub("10\n", "55"), hid("20\n", "6765"), hid("50\n", "12586269025")],
    },
    {
        "slug": "anagram-check", "title": "Anagram Check", "difficulty": "Medium", "tags": ["String", "Sorting"],
        "description": "Two words are anagrams if they use exactly the same letters, the same number of times. For example, 'listen' and 'silent'.",
        "input_format": "One line with two words separated by a space.",
        "output_format": "YES if they are anagrams, otherwise NO.",
        "constraints": "Each word has 1 to 100 lower case letters.",
        "explanation": "If you sort the letters of both words, anagrams end up looking identical.",
        "tests": [pub("listen silent\n", "YES"), pub("hello world\n", "NO"),
                  hid("abc cba\n", "YES"), hid("aab abb\n", "NO")],
    },
    {
        "slug": "longest-run", "title": "Longest Run", "difficulty": "Medium", "tags": ["Array"],
        "description": "Find the longest run of equal numbers sitting next to each other. In 1 1 2 2 2 3 the longest run is 2 2 2.",
        "input_format": "Line 1: n. Line 2: n integers.",
        "output_format": "The length of the longest run.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Keep the length of the current run, and the longest run you have seen so far.",
        "tests": [pub("6\n1 1 2 2 2 3\n", "3"), pub("4\n5 6 7 8\n", "1"),
                  hid("5\n9 9 9 9 9\n", "5"), hid("1\n4\n", "1")],
    },
    {
        "slug": "binary-representation", "title": "Binary Representation", "difficulty": "Medium", "tags": ["Math", "Bits"],
        "description": "Write a non-negative integer in binary, using only the digits 0 and 1.",
        "input_format": "One non-negative integer n.",
        "output_format": "The binary form of n with no leading zeros. Print 0 when n is 0.",
        "constraints": "0 <= n <= 10^9",
        "explanation": "Repeatedly divide by 2 and note the remainders. Then read them in reverse order.",
        "tests": [pub("5\n", "101"), pub("0\n", "0"), hid("255\n", "11111111"), hid("1024\n", "10000000000")],
    },
    {
        "slug": "balanced-brackets", "title": "Balanced Brackets", "difficulty": "Medium", "tags": ["Stack", "String"],
        "description": "Given a string of brackets ( ) [ ] { }, decide whether every opening bracket is closed by the right kind of bracket, in the right order.",
        "input_format": "A single line containing only the characters ()[]{}.",
        "output_format": "YES if the brackets are balanced, otherwise NO.",
        "constraints": "1 <= length <= 1000",
        "explanation": "A stack helps. Push opening brackets. When you see a closing bracket, check the one on top.",
        "tests": [pub("([]{})\n", "YES"), pub("([)]\n", "NO"), hid("((\n", "NO"), hid("{}[]()\n", "YES")],
    },
    {
        "slug": "move-zeroes", "title": "Move the Zeros", "difficulty": "Medium", "tags": ["Array", "Two Pointers"],
        "description": "Move all the zeros to the end of the list. The other numbers must keep their original order.",
        "input_format": "Line 1: n. Line 2: n integers.",
        "output_format": "The new list, space-separated.",
        "constraints": "1 <= n <= 10^5",
        "explanation": "Build a new list with the non-zero numbers first, then add the zeros at the end.",
        "tests": [pub("5\n0 1 0 3 12\n", "1 3 12 0 0"), pub("3\n1 2 3\n", "1 2 3"),
                  hid("4\n0 0 1 0\n", "1 0 0 0"), hid("2\n0 0\n", "0 0")],
    },
    # ---------- Level up (Hard) ----------
    {
        "slug": "max-profit", "title": "Best Day to Sell", "difficulty": "Hard", "tags": ["Array", "Greedy"],
        "description": "You may buy a stock on one day and sell it on a later day. Find the biggest profit you could make. If no profit is possible, the answer is 0.",
        "input_format": "Line 1: n. Line 2: n prices, one per day, in order.",
        "output_format": "The maximum profit, or 0.",
        "constraints": "1 <= n <= 10^5. Prices are positive integers.",
        "explanation": "Track the lowest price so far. For each day, ask: what if I sold today?",
        "tests": [pub("6\n7 1 5 3 6 4\n", "5"), pub("4\n7 6 4 3 1\n", "0"),
                  hid("3\n2 4 1\n", "2"), hid("5\n1 2 3 4 5\n", "4")],
    },
    {
        "slug": "longest-unique-substring", "title": "Longest Run Without Repeats", "difficulty": "Hard",
        "tags": ["String", "Sliding Window"],
        "description": "Find the length of the longest stretch of letters in a word where no letter repeats. In 'abcabcbb' the best stretch is 'abc', which has length 3.",
        "input_format": "A single line of lower case letters.",
        "output_format": "The length of the longest stretch with no repeated letters.",
        "constraints": "1 <= length <= 10^5",
        "explanation": "Use a window that slides along the word. Move its left edge forward whenever a letter repeats.",
        "tests": [pub("abcabcbb\n", "3"), pub("bbbbb\n", "1"), hid("pwwkew\n", "3"), hid("abcdef\n", "6")],
    },
    {
        "slug": "coin-change", "title": "Fewest Coins", "difficulty": "Hard", "tags": ["Dynamic Programming"],
        "description": "You have coins of several values, and you may use each value as many times as you like. Find the fewest coins that add up to the amount. If it is impossible, print -1.",
        "input_format": "Line 1: the amount. Line 2: the coin values, space-separated.",
        "output_format": "The minimum number of coins, or -1.",
        "constraints": "0 <= amount <= 10^4. 1 to 100 coins. Each coin value is between 1 and 10^4.",
        "explanation": "Work out the answer for every amount from 0 up to the target, building each one from the smaller amounts.",
        "tests": [pub("11\n1 2 5\n", "3"), pub("3\n2\n", "-1"), hid("0\n1 2\n", "0"), hid("30\n7 3\n", "6")],
    },
]


def main() -> None:
    db = get_session_factory()()
    created = 0
    reordered = 0
    try:
        for number, spec in enumerate(SAMPLES, start=1):
            existing = db.scalar(select(Problem).where(Problem.slug == spec["slug"]))
            if existing is not None:
                if existing.sort_order != number:
                    existing.sort_order = number
                    reordered += 1
                continue

            problem = Problem(
                slug=spec["slug"],
                title=spec["title"],
                description=spec["description"],
                difficulty=spec["difficulty"],
                status=ProblemStatus.published.value,
                sort_order=number,
                tags=spec["tags"],
                input_format=spec["input_format"],
                output_format=spec["output_format"],
                constraints=spec["constraints"],
                explanation=spec["explanation"],
                time_limit_ms=2000,
                memory_limit_mb=256,
                starter_code=dict(STARTERS),
            )
            problem.test_cases = [
                ProblemTestCase(position=i, stdin=t["in"], expected_output=t["out"], is_hidden=t["hidden"])
                for i, t in enumerate(spec["tests"], start=1)
            ]
            db.add(problem)
            created += 1
        db.commit()
    finally:
        db.close()

    print(
        f"Created {created} and re-ordered {reordered} development sample problem(s), "
        f"out of {len(SAMPLES)} on the learning path. These are placeholders, not production content."
    )


if __name__ == "__main__":
    main()
