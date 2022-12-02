import re
import sys

import aocd

# Set the day and year
DAY = "02"
YEAR = "2022"


def part_1(path, submit):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    scores = {
        # Shapes
        "X": 1,  # Rock
        "Y": 2,  # Paper
        "Z": 3,  # Scissors
        # Outcomes
        "D": 3,  # Draw
        "W": 6,  # Win
        "L": 0,  # Lose
    }

    # Winning scenarios
    wins = [
        "A Y",  # Paper (Y) defeats Rock (A)
        "B Z",  # Scissors (Z) defeats Paper (B)
        "C X",  # Rock (X) defeats Scissors (C)
    ]

    # Get the pairs
    draws = [
        "A X",  # Rock
        "B Y",  # Paper
        "C Z",  # Scissors
    ]

    # Get the scores for the shapes thrown
    shape_scores = [scores[i[-1]] for i in values]

    # Get the scores for the outcomes
    outcome_scores = [
        scores["D"] if i in draws else scores["W"] if i in wins else 0 for i in values
    ]

    answer = sum(shape_scores) + sum(outcome_scores)

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

    scores = {
        # Outcomes
        "Y": 3,  # Draw
        "Z": 6,  # Win
        "X": 0,  # Lose
    }

    # Get the score for the outcome
    outcome_scores = [scores[i[-1]] for i in values]

    # Defeat order
    order = "ABC"  # Rock, Paper, Scissor

    adjustments = {
        "Z": 1,  # For a win need to +1
        "Y": 0,  # For a draw need to +0
        "X": -1,  # For a loss need to -1
    }

    # Get the score for the shape thrown
    shape_scores = [(order.index(i[0]) + adjustments[i[-1]]) % 3 + 1 for i in values]

    # Add the scores
    answer = sum(shape_scores) + sum(outcome_scores)

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-02.py -test`
        `python day-02.py`
        `python day-02.py -test -2`
        `python day-02.py -2`
        `python day-02.py -test -both`
        `python day-02.py -both`
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
