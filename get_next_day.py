import shutil
from pathlib import Path
import re

from aocd import get_data

HERE = Path("__file__").parent

YEAR = 2022

TEMPLATE_PYTHON = """
import sys

import aocd

# Set the day and year
DAY = "{DAY}"
YEAR = "{YEAR}"


def get_input(path):
    \"\"\"Load the data from the file\"\"\"

    # Open the file
    with open(f"{{path}}/day-{{DAY}}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    return values


def part_1(path, submit):
    \"\"\"Part 1/Star 1\"\"\"

    # Get the data
    data = get_input(path)
    
    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 1 Answer: {{answer}}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    \"\"\"Part 2/Star 2\"\"\"

    # Get the data
    data = get_input(path)

    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 2 Answer: {{answer}}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    \"\"\"
    Run using e.g.
        `python day-{DAY}.py -test`
        `python day-{DAY}.py`
        `python day-{DAY}.py -test -2`
        `python day-{DAY}.py -2`
        `python day-{DAY}.py -test -both`
        `python day-{DAY}.py -both`
    \"\"\"
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
"""


def get_next_day():
    """Identify what the next day is to load"""
    pattern = re.compile(r"day\-(\d+)")

    file_list = [0] + [
        int(pattern.match(file.stem).groups()[0])
        for file in Path(HERE).glob("day-*.py")
        if pattern.match(file.stem)
    ]

    return max(file_list) + 1


def prepare_new_day():
    """Create the files for the next available day"""

    # Identify the next day to get
    next_day = get_next_day()
    day_string = f"{next_day:02}"

    # Check the folders exist already
    input_folder = HERE / "inputs"
    input_test_folder = HERE / "input-tests"
    input_folder.mkdir(exist_ok=True)
    input_test_folder.mkdir(exist_ok=True)

    # Check if the files exist already
    python_file = HERE / f"day-{day_string}.py"
    input_file = input_folder / f"day-{day_string}.txt"
    test_input_file = input_test_folder / f"day-{day_string}.txt"
    if python_file.exists():
        raise FileExistsError(f"{input_file} already exists")
    elif test_input_file.exists():
        raise FileExistsError(f"{test_input_file} already exists")
    elif input_file.exists():
        raise FileExistsError(f"{test_input_file} already exists")

    # Get the input data
    # Run this first as if the day isn't yet available we don't want to create
    # the other files
    input_data = get_data(day=next_day, year=YEAR)
    with open(input_file, "w") as f:
        f.write(input_data)

    # Create an (empty) test input file
    with open(test_input_file, "w") as f:
        f.write("")

    # Create the template file
    with open(python_file, "w") as f:
        f.write(TEMPLATE_PYTHON.format(DAY=day_string, YEAR=YEAR))


if __name__ == "__main__":
    prepare_new_day()
