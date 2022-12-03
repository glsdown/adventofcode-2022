import sys

import aocd

# Set the day and year
DAY = "03"
YEAR = "2022"

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def part_1(path, submit):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    answer = 0
    for value in values:
        n = len(value)
        # Split each line in two and find the common letter
        answer += (
            ALPHABET.index(
                list(set(value[: n // 2]).intersection(set(value[n // 2 :])))[
                    0
                ]
            )
            + 1
        )

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    answer = 0
    for i in range(0, len(values), 3):
        answer += (
            ALPHABET.index(
                list(
                    set(values[i])
                    .intersection(set(values[i + 1]))
                    .intersection(set(values[i + 2]))
                )[0]
            )
            + 1
        )

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-03.py -test`
        `python day-03.py`
        `python day-03.py -test -2`
        `python day-03.py -2`
        `python day-03.py -test -both`
        `python day-03.py -both`
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
