import re
import sys

import aocd

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path, submit=False):
    """Part 1/Star 1"""
    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        # Split the values by elf, and sum the calories
        values = [
            sum([int(cals) for cals in elf.split("\n")])
            for elf in f.read().split("\n\n")
        ]

    answer = max(values)

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=1, year=2022)


def part_2(path, submit=False):
    """Part 2/Star 2"""
    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            sum([int(cals) for cals in elf.split("\n")])
            for elf in f.read().split("\n\n")
        ]

    answer = sum(sorted(values, reverse=True)[:3])

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=1, year=2022)


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-1.py -test`
        `python day-1.py`
        `python day-1.py -submit`
        `python day-1.py -test -2`
        `python day-1.py -2`
        `python day-1.py -2 -submit`
        `python day-1.py -test -both`
        `python day-1.py -both`
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
