import sys

import aocd
import numpy as np

# Set the day and year
DAY = "08"
YEAR = "2022"


def get_data(path):
    """Extract the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        trees = [[int(i) for i in list(line.strip())] for line in f.readlines()]

    # Print the tree grid
    print("Original Tree Grid")
    print("\n".join(" ".join([str(i) for i in t]) for t in trees))
    print("\n")

    return trees


def part_1(path, submit):
    """Part 1/Star 1"""

    trees = get_data(path)

    # Get the rows and columns
    rows = len(trees)
    cols = len(trees[0])

    # Tree is invisible if there is a tree in every direction that is bigger than it
    # so assume it's visible unless we determine otherwise
    total_trees = rows * cols

    # Create a map (for debugging purposes) of the invisible trees
    invisible_trees = [[i for i in row] for row in trees]

    # No need to check the outside ring - all visible
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            tree_height = trees[row][col]

            # Check if there are any trees in both directions taller than it
            invisible_in_row = (
                max(trees[row][:col]) >= tree_height
                and max(trees[row][col + 1 :]) >= tree_height
            )

            # Check if there are any trees in both directions taller than it
            invisible_in_col = (
                max([r[col] for r in trees[:row]]) >= tree_height
                and max([r[col] for r in trees[row + 1 :]]) >= tree_height
            )

            # If the tree can't be seen in the column and the row
            if invisible_in_row and invisible_in_col:
                total_trees -= 1
                # Mark on the debug map that it's invisible
                invisible_trees[row][col] = "X"

    # Print out a map of the visible trees (debugging purposes)
    print("Visible Tree Grid")
    print("\n".join(" ".join([str(i) for i in t]) for t in invisible_trees))
    print("\n")

    # Print out the response
    print(f"Task 1 Answer: {total_trees}")

    # Submit the answer
    if submit:
        aocd.submit(total_trees, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    trees = get_data(path)

    current_best = 0

    # Get the rows and columns
    rows = len(trees)
    cols = len(trees[0])

    # Loop through each tree in turn
    for row in range(rows):
        for col in range(cols):

            tree_height = trees[row][col]
            viewable_trees = []

            # Check left and right
            adjustments = [-1, 1]
            for adjust in adjustments:
                score = 0

                check_col = col + adjust
                while check_col >= 0 and check_col < cols:
                    # Check if the tree in that direction is smaller than it
                    if trees[row][check_col] < tree_height:
                        score += 1
                        check_col += adjust
                    else:
                        score += 1
                        # Stop when reach a tall tree
                        break

                # Add that direction to your viewable_trees list
                viewable_trees.append(score)

            # Check up and down
            adjustments = [-1, 1]
            for adjust in adjustments:
                score = 0

                check_row = row + adjust
                while check_row >= 0 and check_row < rows:
                    # Check if the tree in that direction is smaller than it
                    if trees[check_row][col] < tree_height:
                        score += 1
                        check_row += adjust
                    else:
                        score += 1
                        # Stop when reach a tall tree
                        break

                # Add that direction to your viewable_trees list
                viewable_trees.append(score)

            # Multiply them together
            tree_score = np.prod(viewable_trees)

            # print(
            #     f"{row}, {col} with height {tree_height} has score {tree_score} from {viewable_trees}"
            # )
            current_best = max(current_best, tree_score)

    # Print out the response
    print(f"Task 2 Answer: {current_best}")

    # Submit the answer
    if submit:
        aocd.submit(current_best, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-08.py -test`
        `python day-08.py`
        `python day-08.py -test -2`
        `python day-08.py -2`
        `python day-08.py -test -both`
        `python day-08.py -both`
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
