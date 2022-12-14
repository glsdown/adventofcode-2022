import sys

import aocd

# Set the day and year
DAY = "14"
YEAR = "2022"


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [
                [int(x) for x in i.split(",")]
                for i in line.strip().split(" -> ")
            ]
            for line in f.readlines()
        ]

    return values


def get_rock_coordinates(data):
    """Identify the coordinates of the rocks"""

    rocks = set()

    # Get the coordinates of the rocks
    for rock_path in data:
        for i in range(len(rock_path) - 1):
            x_0, y_0 = rock_path[i]
            x_1, y_1 = rock_path[i + 1]

            # If the rocks are going in the x direction then...
            if x_0 == x_1:
                # Coordinates between the two points
                if y_1 > y_0:
                    new = [(x_0, y) for y in range(y_0, y_1 + 1)]
                else:
                    new = [(x_0, y) for y in range(y_1, y_0 + 1)]

            else:
                # Coordinates between the two points
                if x_1 > x_0:
                    new = [(x, y_0) for x in range(x_0, x_1 + 1)]
                else:
                    new = [(x, y_0) for x in range(x_1, x_0 + 1)]

            rocks = rocks.union(new)

    return rocks


def get_lowest_level(rocks):
    """Find the y coordinate that indicates sand has falledn
    into the abyss"""

    return max(rock[1] for rock in rocks)


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the data
    data = get_input(path)

    # Identify the rock co-ordinates
    rocks = get_rock_coordinates(data)

    # Initialise the sand
    sand_start = (500, 0)
    sand = sand_start

    # Identify at what point the sand has fallen too far
    lowest_level = get_lowest_level(rocks)

    # Keep track of the sand grains
    answer = 0

    # Keep adding sand until it falls below the ground
    while sand[1] < lowest_level:
        x, y = sand

        # A unit of sand always falls down one step if possible.
        if (x, y + 1) not in rocks:
            sand = (x, y + 1)

        # If the tile immediately below is blocked (by rock or sand),
        # the unit of sand attempts to instead move diagonally one
        # step down and to the left.
        elif (x - 1, y + 1) not in rocks:
            sand = (x - 1, y + 1)

        # If that tile is blocked, the unit of sand attempts to instead
        # move diagonally one step down and to the right.
        elif (x + 1, y + 1) not in rocks:
            sand = (x + 1, y + 1)

        # If all three possible destinations are blocked, the unit of
        # sand comes to rest and no longer moves, at which point the
        # next unit of sand is created back at the source.
        else:
            rocks.add(sand)
            answer += 1
            sand = sand_start

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get the data
    data = get_input(path)

    # Identify the rock co-ordinates
    rocks = get_rock_coordinates(data)

    # Initialise the sand
    sand_start = (500, 0)
    sand = sand_start

    # Identify at what point the sand has fallen too far
    floor_level = get_lowest_level(rocks) + 2

    # Keep track of the sand grains
    answer = 0

    # Keep adding sand until it gets blocked
    while sand_start not in rocks:

        x, y = sand

        # Check if it's reached the floor
        if y + 1 >= floor_level:
            rocks.add(sand)
            answer += 1
            sand = sand_start
            continue

        # A unit of sand always falls down one step if possible.
        if (x, y + 1) not in rocks:
            sand = (x, y + 1)

        # If the tile immediately below is blocked (by rock or sand),
        # the unit of sand attempts to instead move diagonally one
        # step down and to the left.
        elif (x - 1, y + 1) not in rocks:
            sand = (x - 1, y + 1)

        # If that tile is blocked, the unit of sand attempts to instead
        # move diagonally one step down and to the right.
        elif (x + 1, y + 1) not in rocks:
            sand = (x + 1, y + 1)

        # If all three possible destinations are blocked, the unit of
        # sand comes to rest and no longer moves, at which point the
        # next unit of sand is created back at the source.
        else:
            rocks.add(sand)
            answer += 1
            sand = sand_start

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-14.py -test`
        `python day-14.py`
        `python day-14.py -test -2`
        `python day-14.py -2`
        `python day-14.py -test -both`
        `python day-14.py -both`
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
