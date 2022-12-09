import sys
from operator import add, sub

import aocd
from numpy import sign

# Set the day and year
DAY = "09"
YEAR = "2022"


def get_input(path, debug=False):
    """Read the file"""

    debug_file = "-debug" if debug else ""

    # Open the file
    with open(f"{path}/day-{DAY}{debug_file}.txt", "r") as f:
        values = [(line.split()[0], int(line.split()[1])) for line in f.readlines()]

    return values


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the instructions
    instructions = get_input(path)

    # Keep track of where the tail has been
    visited_coords = {(0, 0)}

    # Initialise the locations
    head = [0, 0]
    tail = [0, 0]

    for direction, distance in instructions:

        # Get the direction
        match direction:
            case "R":
                adjust = 1
                axis = 0
            case "L":
                adjust = -1
                axis = 0
            case "U":
                adjust = 1
                axis = 1
            case "D":
                adjust = -1
                axis = 1
        opposite_axis = (axis + 1) % 2

        # Loop through each distance
        for _ in range(distance):

            # Move the head in that direction
            head[axis] += adjust

            # If the tail is now more than 1 column/row away
            if abs(tail[axis] - head[axis]) > 1:
                # Need to move the tail in that direction
                tail[axis] += adjust
                # If the head is a row/column above the tail
                if head[opposite_axis] > tail[opposite_axis]:
                    # Need to move the tail up/right
                    tail[opposite_axis] += 1
                # If the head is a row/column below the tail
                elif head[opposite_axis] < tail[opposite_axis]:
                    # Need to move the tail down/left
                    tail[opposite_axis] -= 1

            visited_coords.add(tuple(tail))

    # Find the number of places visited by the tail
    answer = len(visited_coords)

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit, debug):
    """Part 2/Star 2"""

    # Get the instructions
    instructions = get_input(path, debug)

    # Keep track of where the tail has been
    visited_coords = {(0, 0)}

    if debug:
        # Grid for debugging purposes - very limited scope
        grid = [["." for _ in range(6)] for _ in range(5)]

        grid[0][0] = "0"

        def print_grid(grid):
            for row in grid[::-1]:
                print(" ".join(row))
            print("\n")

        def update_grid(knots):
            new_grid = [["." for _ in range(6)] for _ in range(5)]
            for i, knot in enumerate(knots[::-1]):
                new_grid[knot[1]][knot[0]] = str(9 - i)

            return new_grid

        print_grid(grid)

    # Initialise the locations
    number_of_knots = 10
    knots = [[0, 0] for i in range(number_of_knots)]

    for direction, distance in instructions:

        # Get the direction
        match direction:
            case "R":
                head_adjustment = [1, 0]
            case "L":
                head_adjustment = [-1, 0]
            case "U":
                head_adjustment = [0, 1]
            case "D":
                head_adjustment = [0, -1]

        # Loop through each distance
        for _ in range(distance):

            # Move the head in that direction
            knots[0] = list(map(add, knots[0], head_adjustment))

            for knot_number in range(1, number_of_knots):
                # Now find out what direction to move the next one in
                head = knots[knot_number - 1]
                next = knots[knot_number]

                if abs(head[0] - next[0]) < 1 and abs(head[1] - next[1]) < 1:
                    # No need to move
                    pass
                else:
                    new_adjustment = [0, 0]
                    # Look in both directions
                    for axis in [0, 1]:
                        # Get the difference in that direction
                        difference = head[axis] - next[axis]
                        # If more than one away move the second counter closer
                        if abs(difference) > 1:
                            new_adjustment[axis] = sign(difference)

                        # If it's one away but the other direction is more than one
                        # Then want to move it diagonally
                        elif (
                            abs(difference) == 1
                            and abs(head[int(not axis)] - next[int(not axis)]) > 1
                        ):
                            new_adjustment[axis] = sign(difference)

                    knots[knot_number] = list(map(add, next, new_adjustment))

            # Display the grid in debug mode
            if debug:
                print(knots)
                grid = update_grid(knots)
                print_grid(grid)

            # Add the 'tail' record to the visited list
            visited_coords.add(tuple(knots[9]))

    # Find the number of places visited by the tail
    answer = len(visited_coords)

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-09.py -test`
        `python day-09.py`
        `python day-09.py -test -2`
        `python day-09.py -2`
        `python day-09.py -test -both`
        `python day-09.py -both`
    """
    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"
    # Identify if they need to submit the answer
    submit = "-test" not in sys.argv and "-submit" in sys.argv

    debug = "-debug" in sys.argv
    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path, submit, debug)
    elif "-both" in sys.argv:
        part_1(path, submit)
        part_2(path, submit, debug)
    else:
        part_1(path, submit, debug)
