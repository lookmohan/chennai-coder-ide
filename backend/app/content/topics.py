"""The Python concepts students choose from, in learning order.

Each concept has three levels. Each level has a target number of questions:
Easy 20, Medium 15, Hard 10. The platform shows progress against these targets, so
students see what is ready and what is still being written.
"""

LEVEL_TARGETS = {"Easy": 20, "Medium": 15, "Hard": 10}

TOPICS = [
    {"slug": "python-basics", "name": "Python Basics", "description": "Variables, printing, input and simple arithmetic."},
    {"slug": "conditions", "name": "Conditions", "description": "Making decisions with if, elif and else."},
    {"slug": "loops", "name": "Loops", "description": "Repeating work with for and while loops."},
    {"slug": "numbers", "name": "Number Problems", "description": "Digits, primes, remainders and number patterns."},
    {"slug": "lists", "name": "Lists and Arrays", "description": "Reading, changing and scanning lists of values."},
    {"slug": "strings", "name": "Strings", "description": "Working with text: characters, words and patterns."},
    {"slug": "searching", "name": "Searching", "description": "Finding values quickly in ordered and unordered data."},
    {"slug": "sorting", "name": "Sorting", "description": "Putting data in order, and using order to solve problems."},
    {"slug": "recursion", "name": "Recursion", "description": "Solving a problem by solving a smaller copy of it."},
    {"slug": "hashing", "name": "Hashing", "description": "Dictionaries and sets for fast lookups and counting."},
    {"slug": "stacks-queues", "name": "Stacks and Queues", "description": "Last-in-first-out and first-in-first-out data."},
    {"slug": "linked-lists", "name": "Linked Lists", "description": "Chains of nodes, and moving through them."},
    {"slug": "trees", "name": "Trees", "description": "Branching structures, traversal and search."},
    {"slug": "graphs", "name": "Graphs", "description": "Nodes and connections: paths, neighbours and groups."},
    {"slug": "dynamic-programming", "name": "Dynamic Programming", "description": "Solving big problems by reusing answers to smaller ones."},
]

TOPIC_SLUGS = {t["slug"] for t in TOPICS}

# Which topic each of the first 26 problems belongs to. Future batches set "topic" on each problem.
SLUG_TOPIC = {
    "sum-of-two-numbers": "python-basics",
    "say-hello": "python-basics",
    "double-it": "python-basics",
    "is-even": "conditions",
    "largest-of-three": "conditions",
    "reverse-a-string": "strings",
    "count-even-numbers": "lists",
    "sum-of-array": "lists",
    "factorial": "loops",
    "fizzbuzz": "conditions",
    "count-vowels": "strings",
    "palindrome-check": "strings",
    "second-largest": "lists",
    "prime-check": "numbers",
    "sum-of-digits": "numbers",
    "count-words": "strings",
    "two-sum-exists": "hashing",
    "fibonacci": "recursion",
    "anagram-check": "hashing",
    "longest-run": "lists",
    "binary-representation": "numbers",
    "balanced-brackets": "stacks-queues",
    "move-zeroes": "lists",
    "max-profit": "lists",
    "longest-unique-substring": "strings",
    "coin-change": "dynamic-programming",
}
