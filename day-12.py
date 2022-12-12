import networkx as nx
import sys

import aocd

# Set the day and year
DAY = "12"
YEAR = "2022"


def get_input(path):
    """Load the file as a 2d list"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [list(line.strip()) for line in f.readlines()]

    return values


def create_graph(values, multiple_start=False):
    """
    Create the graph and identify the start and end points
    If multiple_start = True, this will return a list of possible
    start points. If False (default) it will return the start point
    denoted by S.
    """

    # Create the graph
    G = nx.DiGraph()

    start = []
    end = None

    # Get the number of rows and columns
    number_rows = len(values)
    number_cols = len(values[0])

    # Loop through each co-ordinate and create the nodes
    for row in range(number_rows):
        for col in range(number_cols):
            # Create the node
            G.add_node((row, col))

            match values[row][col]:
                # Work out what the end point is
                case "E":
                    end = (row, col)
                    values[row][col] = 25
                # Work out what the start point is
                case "S":
                    if multiple_start:
                        start.append((row, col))
                    else:
                        start = (row, col)
                    values[row][col] = 0
                case "a":
                    if multiple_start:
                        start.append((row, col))
                    values[row][col] = 0
                # Work out the value of the letter
                case _:
                    values[row][col] = "abcdefghijklmnopqrstuvwxyz".index(
                        values[row][col]
                    )

    # Loop through each co-ordinate and add the edges
    for row in range(number_rows):
        for col in range(number_cols):

            # Get the current value
            current = values[row][col]

            # Check the value immediately above and below
            for row_adjust in [-1, 1]:

                check_row = row + row_adjust

                # Check that the row to check is on the grid
                if 0 <= check_row < number_rows:
                    # If the new peak is at most 1 more than the current one
                    if values[check_row][col] <= current + 1:
                        # Add a path to it
                        G.add_edge((row, col), (check_row, col))

            # Check the value immediately right and left
            for col_adjust in [-1, 1]:

                check_col = col + col_adjust

                # Check that the col to check is on the grid
                if 0 <= check_col < number_cols:
                    # If the new peak is at most 1 more than the current one
                    if values[row][check_col] <= current + 1:
                        # Add a path to it
                        G.add_edge((row, col), (row, check_col))

    return start, end, G


def part_1(path, submit):
    """Part 1/Star 1"""

    # Get the graph
    start, end, map = create_graph(get_input(path))

    # Find the shortest path
    answer = nx.shortest_path_length(map, start, end)

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get the graph
    possible_starts, end, map = create_graph(
        get_input(path), multiple_start=True
    )

    # Find the shortest path
    answer = float("inf")
    for start in possible_starts:
        try:
            new = nx.shortest_path_length(map, start, end)
            answer = min(new, answer)
        except Exception:
            pass

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-12.py -test`
        `python day-12.py`
        `python day-12.py -test -2`
        `python day-12.py -2`
        `python day-12.py -test -both`
        `python day-12.py -both`
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
