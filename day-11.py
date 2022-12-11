import sys

import aocd
import numpy as np
from tqdm import tqdm

# Set the day and year
DAY = "11"
YEAR = "2022"


def get_input(path):
    """Get the input from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        monkeys = [m.split("\n") for m in f.read().split("\n\n")]

    all_monkeys = []

    # Parse the monkey structure
    for monkey in monkeys:
        new_monkey = {"items_inspected": 0}
        # Get the item list
        new_monkey["items"] = [
            int(i)
            for i in (
                monkey[1].strip().replace("Starting items: ", "").split(", ")
            )
        ]
        # Get the operation
        new_monkey["operation"] = lambda old, monkey=monkey: eval(
            monkey[2].strip().replace("Operation: new = ", "")
        )
        # Get the test
        new_monkey["divisor"] = int(
            monkey[3].strip().replace("Test: divisible by ", "")
        )
        # Get the true monkey
        new_monkey["true"] = int(
            monkey[4].strip().replace("If true: throw to monkey ", "")
        )
        # Get the false monkey
        new_monkey["false"] = int(
            monkey[5].strip().replace("If false: throw to monkey ", "")
        )

        all_monkeys.append(new_monkey)

    return all_monkeys


def part_1(path, submit, debug=False):
    """Part 1/Star 1"""

    monkeys = get_input(path)

    # Number of rounds to complete
    rounds = 20

    for _ in range(rounds):

        # For each round need to work through each monkey in turn
        for number, monkey in enumerate(monkeys):

            if debug:
                print(f"\nMonkey {number}:")

            # Increase the number of items inspected
            monkey["items_inspected"] += len(monkey["items"])

            # Work out where each item goes
            for item in monkey["items"]:

                # Get the worry level
                worry = monkey["operation"](item) // 3

                if debug:
                    print(
                        f"  Monkey inspects an item with a worry level of {item}.\n"
                        f"    Worry level after operation is {monkey['operation'](item)}.\n"
                        f"    Monkey gets bored with item. Worry level is divided by 3 to {worry}."
                    )

                # Check who to throw it to
                if worry % monkey["divisor"] == 0:
                    next = monkey["true"]
                else:
                    next = monkey["false"]
                if debug:
                    print(
                        f"    Current worry level is {'not ' if worry % monkey['divisor'] != 0 else ''}divisible by {monkey['divisor']}.\n"
                        f"    Item with worry level 500 is thrown to monkey {next}."
                    )

                # Throw the item
                monkeys[next]["items"].append(worry)

            # Set the list empty as all items have now been checked
            monkey["items"] = []

    if debug:
        print(monkeys)

    # Look at all checks for all monkeys
    total_checks = sorted(
        [monkey["items_inspected"] for monkey in monkeys], reverse=True
    )

    # Calculate the required answer
    answer = total_checks[0] * total_checks[1]

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit, debug=False):
    """Part 2/Star 2"""

    monkeys = get_input(path)

    # Find the lowest common multiple of all divisors
    # This will allow us to reduce the worry
    total_worry = np.lcm.reduce([m["divisor"] for m in monkeys])

    # Number of rounds to complete
    rounds = 10000

    for _ in tqdm(range(rounds)):

        # For each round need to work through each monkey in turn
        for monkey in monkeys:

            # Increase the number of items inspected
            monkey["items_inspected"] += len(monkey["items"])

            # Work out where each item goes
            for item in monkey["items"]:

                # Get the new worry level
                worry = monkey["operation"](item)

                # Check who to throw it to
                if worry % monkey["divisor"] == 0:
                    next = monkey["true"]

                else:
                    next = monkey["false"]

                # Reduce the worry
                worry = worry % total_worry

                # Throw the item
                monkeys[next]["items"].append(worry)

            # Set the list empty as all items have now been checked
            monkey["items"] = []

    if debug:
        print(monkeys)

    # Look at all checks for all monkeys
    total_checks = sorted(
        [monkey["items_inspected"] for monkey in monkeys], reverse=True
    )

    # Calculate the required answer
    answer = total_checks[0] * total_checks[1]

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-11.py -test`
        `python day-11.py`
        `python day-11.py -test -2`
        `python day-11.py -2`
        `python day-11.py -test -both`
        `python day-11.py -both`
    """
    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"
    # Identify if they need to submit the answer
    submit = "-test" not in sys.argv and "-submit" in sys.argv
    # Identify whether to debug
    debug = "-debug" in sys.argv
    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path, submit, debug)
    elif "-both" in sys.argv:
        part_1(path, submit, debug)
        part_2(path, submit, debug)
    else:
        part_1(path, submit, debug)
