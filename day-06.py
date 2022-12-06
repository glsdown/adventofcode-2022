import sys

import aocd

# Set the day and year
DAY = "06"
YEAR = "2022"


def load_data(path):
    """Load the data in the right format"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        buffer = [line.strip() for line in f.readlines()][0]

    return buffer


def find_marker(buffer, marker_length):
    """Find the first unique marker"""

    for i in range(len(buffer) - marker_length):
        if len(set(buffer[i : i + marker_length])) == marker_length:
            print(buffer[i : i + marker_length])
            return i + marker_length

    return 0


def part_1(path, submit):
    """Part 1/Star 1"""

    # Open the file
    buffer = load_data(path)

    # Find the marker
    answer = find_marker(buffer, 4)

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Open the file
    buffer = load_data(path)

    # Find the marker
    answer = find_marker(buffer, 14)

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-06.py -test`
        `python day-06.py`
        `python day-06.py -test -2`
        `python day-06.py -2`
        `python day-06.py -test -both`
        `python day-06.py -both`
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
