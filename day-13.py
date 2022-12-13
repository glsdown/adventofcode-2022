import sys
from functools import total_ordering

import aocd

# Set the day and year
DAY = "13"
YEAR = "2022"


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [eval(i) for i in line.splitlines()] for line in f.read().split("\n\n")
        ]

    return values


def get_input_part_2(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [eval(i) for line in f.read().split("\n\n") for i in line.splitlines()]

    return values + [[[2]], [[6]]]  # Add the divider packets


def compare_values(value_1, value_2):
    """Identify if value_1 and value_2 are in the correct order"""

    # If exactly one value is an integer, convert the integer to a list which contains that integer
    # as its only value, then retry the comparison.
    if isinstance(value_1, int) and isinstance(value_2, list):
        value_1 = [value_1]
    if isinstance(value_1, list) and isinstance(value_2, int):
        value_2 = [value_2]

    # The inputs are the same continue checking the next part of the input.
    if value_1 == value_2:
        return None

    # If both values are integers, the lower integer should come first.
    if isinstance(value_1, int) and isinstance(value_2, int):
        # If the left integer is lower
        # than the right integer, the inputs are in the right order. If the left integer is higher than
        #  he right integer, the inputs are not in the right order.
        return value_1 < value_2

    # If both values are lists, compare the first value of each list, then the second value, and so on.
    if isinstance(value_1, list) and isinstance(value_2, list):
        for index, item in enumerate(value_1):
            if index >= len(value_2):
                # The first list has more items, so in the wrong order
                return False

            # Compare each item in the list
            check = compare_values(item, value_2[index])

            # If a decision is made, then return that
            if check is not None:
                return check

        # The left list is shorter
        return len(value_1) < len(value_2)


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the data
    data = get_input(path)

    # Track the answer
    answer = 0

    # Check each pair
    for index, pair in enumerate(data):

        # If they are in the right order
        if compare_values(*pair):
            answer += index + 1

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get the data
    data = get_input_part_2(path)

    # Create a simple class with less than function for ordering
    @total_ordering
    class Packet(list):
        def __lt__(self, other):
            return compare_values(self, other)

        def __eq__(self, other):
            return super().__eq__(other)

    # Get the sorted list
    data = sorted([Packet(d) for d in data])

    # get the decoder key
    answer = (data.index(Packet([[2]])) + 1) * (data.index(Packet([[6]])) + 1)

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-13.py -test`
        `python day-13.py`
        `python day-13.py -test -2`
        `python day-13.py -2`
        `python day-13.py -test -both`
        `python day-13.py -both`
    """
    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"
    # Identify if they need to submit the answer
    submit = "-test" not in sys.argv and "-submit" in sys.argv
    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path, submit)
    elif "-both" in sys.argv:
        part_1(path, submit)
        part_2(path, submit)
    else:
        part_1(path, submit)
