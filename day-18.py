import sys

import aocd

# Set the day and year
DAY = "18"
YEAR = "2022"


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = set(
            tuple(int(i) for i in line.strip().split(","))
            for line in f.readlines()
        )

    return values


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the data
    cubes = get_input(path)

    faces = 0

    # Check each cube
    for x, y, z in cubes:
        # Assume 6 faces unless has a neighbouring cube
        cube_faces = 6
        # Check whether it has a neighbour
        for adj in [-1, 1]:
            if (x + adj, y, z) in cubes:
                cube_faces -= 1
            if (x, y + adj, z) in cubes:
                cube_faces -= 1
            if (x, y, z + adj) in cubes:
                cube_faces -= 1
        faces += cube_faces

    # Find the number of faces
    answer = faces

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
        `python day-18.py -test`
        `python day-18.py`
        `python day-18.py -test -2`
        `python day-18.py -2`
        `python day-18.py -test -both`
        `python day-18.py -both`
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
