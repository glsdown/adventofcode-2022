import sys

import aocd

# Set the day and year
DAY = "10"
YEAR = "2022"


def get_input(path):
    """Get the input"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [i for line in f.readlines() for i in line.split()]

    return values


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get input
    instructions = get_input(path)

    # Cycles to get the value from
    required_cycles = [20, 60, 100, 140, 180, 220]

    # Initialise the values
    cycle = 0
    register = 1
    answer = 0

    for instruction in instructions:
        # Increment the cycle number
        cycle += 1

        # If this is a 'stop' point, then add the score
        if cycle in required_cycles:
            answer += cycle * register

        # If reached the target cycles, stop
        if cycle == required_cycles[-1]:
            break

        # Check if it's a number to be added
        if instruction not in ["addx", "noop"]:
            # Change the register value
            register += int(instruction)

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get input
    instructions = get_input(path)

    # Initialise the values
    sprite = 1
    crt = ["" for _ in range(6)]

    for cycle, instruction in enumerate(instructions):

        # Check if the current cycle
        if abs(cycle % 40 - sprite) <= 1:
            pixel = "O"  # "#"
        else:
            pixel = " "  # "."

        # 'Draw' the current pixel
        crt[cycle // 40] += pixel

        # Check if it's a number to be added
        if instruction not in ["addx", "noop"]:
            sprite += int(instruction)

    # Print out the response
    print("Task 2 Answer:")

    # Print the grid
    for line in crt:
        print("".join(line))

    # Manually obtain the answer - need to see the grid
    answer = ""
    while not answer:
        answer = input("What capital letters can you see?\nLetters: ").upper()

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-10.py -test`
        `python day-10.py`
        `python day-10.py -test -2`
        `python day-10.py -2`
        `python day-10.py -test -both`
        `python day-10.py -both`
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
