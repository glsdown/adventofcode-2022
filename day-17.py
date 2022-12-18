import sys

import aocd

import numpy as np
import matplotlib.pyplot as plt

# Set the day and year
DAY = "17"
YEAR = "2022"

ROCKS = [
    {"shape": [(0, 0), (1, 0), (2, 0), (3, 0)], "width": 4},
    {"shape": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], "width": 3},
    {"shape": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], "width": 3},
    {"shape": [(0, 0), (0, 1), (0, 2), (0, 3)], "width": 1},
    {"shape": [(0, 0), (1, 0), (0, 1), (1, 1)], "width": 2},
]


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        jets = [1 if j == ">" else -1 for j in f.read().strip()]

    return jets


def part_1(path, submit, debug):
    """Part 1/Star 1"""

    # Get the data
    jets = get_input(path)
    number_jets = len(jets)

    # Initialise variables
    max_width = 7  # Width of the grid
    jet = 0  # Jet number
    occupied = set([(i, 0) for i in range(max_width)])  # The 'occupied' points
    height = 0  # Track the 'top' row
    number_of_shapes = 2022  # How many shapes to track

    # Loop through the number of rows
    for s in range(number_of_shapes):

        # Get the starting point
        x, y = (
            2,
            height + 4,
        )

        # Identify the falling shape
        rock = ROCKS[s % 5]
        shape = rock["shape"]
        shape_width = rock["width"]

        # Move the rock
        for drop in range(height + 5):

            # Work out which direction the jet is going in
            x_adjust = jets[jet]

            # Get the next jet
            jet = (jet + 1) % number_jets

            # Check if that's going to go off the grid or intersect with a rock
            new_x = x + x_adjust
            if (
                new_x >= 0  # Not too far left
                and new_x + shape_width <= max_width  # Not too far right
                and not (
                    occupied
                    & set((new_x + x_i, y + y_i) for (x_i, y_i) in shape)
                )  # Not intersecting with another shape
            ):
                # Move the x-direction
                x = new_x

            # First three moves will always be 'safe'
            if drop > 2:

                # Check if dropping by 1 will intersect another shape
                if y == 1 or (
                    set((x + x_i, y + y_i - 1) for (x_i, y_i) in shape)
                    & occupied
                ):
                    break

            # Move the y down
            y -= 1

        # Add the stopped shape to the occupied positions
        occupied = occupied | set((x + x_i, y + y_i) for (x_i, y_i) in shape)

        # Adjust the height
        height = max(s[1] for s in occupied)

    if debug:
        # Show the points on a graph
        x_plt, y_plt = np.array(list(occupied)).T
        plt.scatter(x_plt, y_plt)
        plt.show()

    # Get how tall the unit will be
    answer = height

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
        `python day-17.py -test`
        `python day-17.py`
        `python day-17.py -test -2`
        `python day-17.py -2`
        `python day-17.py -test -both`
        `python day-17.py -both`
    """
    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"
    # Identify if they need to submit the answer
    submit = "-test" not in sys.argv and "-submit" in sys.argv
    # Check if in debug
    debug = "-debug" in sys.argv
    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path, submit)
    elif "-both" in sys.argv:
        part_1(path, submit, debug)
        part_2(path, submit)
    else:
        part_1(path, submit, debug)
