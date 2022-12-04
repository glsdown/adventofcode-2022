import sys

import aocd

# Set the day and year
DAY = "04"
YEAR = "2022"


def part_1(path, submit):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split(",") for line in f.readlines()]

    answer = 0

    # Loop through each one
    for value in values:
        # Identify the two shifts and order by which starts first
        shifts = sorted(
            sorted(
                [[int(i.split("-")[0]), int(i.split("-")[1])] for i in value],
                key=lambda x: -x[1],  # Need the 'larger' one first
            ),
            key=lambda x: x[0],
        )

        # Work out if the first contains the second
        # (min of the second shift is always >= min of first)
        answer += int(shifts[0][1] >= shifts[1][1])

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split(",") for line in f.readlines()]

    answer = 0

    # Loop through each one
    for value in values:
        # Identify the two shifts and order by which starts first
        shifts = sorted(
            sorted(
                [[int(i.split("-")[0]), int(i.split("-")[1])] for i in value],
                key=lambda x: -x[1],  # Need the 'larger' one first
            ),
            key=lambda x: x[0],
        )

        # Work out if there is an overlap contained in the other
        answer += int(
            # Max of first shift is greater than min of second
            # (min of second is always >= min of first)
            shifts[0][1]
            >= shifts[1][0]
        )

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-04.py -test`
        `python day-04.py`
        `python day-04.py -test -2`
        `python day-04.py -2`
        `python day-04.py -test -both`
        `python day-04.py -both`
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
