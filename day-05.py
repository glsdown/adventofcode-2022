import re
import sys

import aocd

# Set the day and year
DAY = "05"
YEAR = "2022"


def get_input(path):
    """Get the input and convert to a usable format"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        stacks, instructions = f.read().split("\n\n")

    # Split up the stacks
    stacks = {
        i[-1]: [z for z in i if len(z.strip()) > 0][::-1][1:]  # Remove blank values
        for i in list(map(list, zip(*stacks.splitlines())))  # transpose them
        if len(i[-1].strip()) > 0  # remove blank columns
    }

    # Get the instruction pattern
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

    # Get the details
    instructions = [
        pattern.match(instruction).groups() for instruction in instructions.splitlines()
    ]

    return stacks, instructions


def part_1(path, submit):
    """Part 1/Star 1"""

    # Parse the input
    stacks, instructions = get_input(path)

    # Follow each instruction
    for number, first_stack, second_stack in instructions:
        # Add the letters to the second stack in reverse order (LIFO)
        stacks[second_stack] += stacks[first_stack][-int(number) :][::-1]
        # Remove the letters from the first stack
        stacks[first_stack] = stacks[first_stack][: -int(number)]

    # Work out the answer
    answer = ""
    for i in range(len(stacks.keys())):
        answer += stacks[str(i + 1)][-1]

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Parse the input
    stacks, instructions = get_input(path)

    # Follow each instruction
    for number, first_stack, second_stack in instructions:
        # Add the letters to the second stack
        stacks[second_stack] += stacks[first_stack][-int(number) :]
        # Remove the letters from the first stack
        stacks[first_stack] = stacks[first_stack][: -int(number)]

    # Work out the answer
    answer = ""
    for i in range(len(stacks.keys())):
        answer += stacks[str(i + 1)][-1]

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-05.py -test`
        `python day-05.py`
        `python day-05.py -test -2`
        `python day-05.py -2`
        `python day-05.py -test -both`
        `python day-05.py -both`
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
