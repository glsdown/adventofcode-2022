import re
import sys

import aocd

# Set the day and year
DAY = "16"
YEAR = "2022"


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split(";") for line in f.readlines()]

    values = {}

    # Extract the values
    valve_regex = re.compile(r"Valve (\w+) has flow rate=(\d+)")
    tunnel_regex = re.compile(r"tunnel(?:s?) lead(?:s?) to valve(?:s?) ((\w+|\,\ )+)")

    for valve, tunnel in values:
        # Get the values
        valve_name, valve_rate = valve_regex.match(valve).groups()
        tunnels = tunnel_regex.match(tunnel).groups().split(", ")

        values[valve_name] = {"rate": valve_rate, "tunnels": tunnels}

    return values


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the data
    data = get_input(path)

    # Want to minimise 'steps' and maximise 'flow'

    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get the data
    data = get_input(path)

    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-16.py -test`
        `python day-16.py`
        `python day-16.py -test -2`
        `python day-16.py -2`
        `python day-16.py -test -both`
        `python day-16.py -both`
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
