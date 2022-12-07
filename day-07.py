import sys

import aocd
import shutup

# Remove deprecation warning - .bpointer is deprecated but nothing in docs about how
# to replace it - all examples still use it.
shutup.please()
from treelib import Tree

# Set the day and year
DAY = "07"
YEAR = "2022"


def get_file_system(path):
    """Create a tree of the file system"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Initialise the values
    structure = Tree()
    current_path = "/"
    structure.create_node(current_path, current_path, data=0)

    for line in values[1:]:  # Skip the first cd / line
        # Split on whitespace
        instruction = line.split()

        # Deal with the 'command' case first
        if instruction[0] == "$":
            # Command to run
            command = instruction[1]

            match command:
                case "cd":
                    new_directory = instruction[2]
                    # Change directory
                    if new_directory == "..":
                        # Go back to the previous dir
                        current_path = structure.get_node(current_path).bpointer
                    else:
                        new_node = f"{current_path}{new_directory}/"
                        # Go into the listed directory
                        # See if it exists
                        if not structure.get_node(new_node):
                            # If it doesn't exist, create it
                            structure.create_node(
                                new_node,
                                new_node,
                                parent=current_path,
                                data=0,
                            )
                        # Go into the new directory
                        current_path = new_node
                case "ls":
                    # Do nothing
                    pass

        # Deal with the list of files and directories
        else:
            # This is a list of files and directories
            if instruction[0] == "dir":
                # This is a directory so want to add it to the tree (if it doesn't already exist)
                weight, new_directory = (0, instruction[1])
                new_node = f"{current_path}{new_directory}/"  # Trailing / to indicate a directory
            else:
                # This is a file, need to add it to the tree (if it doesn't already exist)
                weight, new_directory = instruction
                weight = int(weight)
                new_node = (
                    f"{current_path}{new_directory}"  # No trailing / to indicate a file
                )

            # Add a node
            if not structure.get_node(new_node):
                structure.create_node(
                    new_node,
                    new_node,
                    parent=current_path,
                    data=weight,  # Make sure to add the file size
                )

                if weight > 0:
                    # Add the weight to the parent nodes above
                    parent = structure.get_node(current_path)
                    while parent:
                        parent.data += weight
                        parent = structure.get_node(parent.bpointer)

    return structure


def part_1(path, submit):
    """Part 1/Star 1"""

    # Generate the file structure
    structure = get_file_system(path)

    # Calculate the sum of repositories
    answer = 0
    for node in structure.all_nodes():
        if node.identifier[-1] == "/" and node.data <= 100000:
            answer += node.data

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Generate the file structure
    structure = get_file_system(path)

    # Initialise the values from the problem
    total_space_used = int(structure.get_node("/").data)
    total_space = 70000000
    unused_space = total_space - total_space_used
    required_space = 30000000 - unused_space

    # Find the space used in each directory
    data_points = []
    for node in structure.all_nodes():
        if node.identifier[-1] == "/":
            data_points.append(node.data)

    # Need to find the smallest number larger than required_space
    answer = sorted([i for i in data_points if i >= required_space])[0]

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-07.py -test`
        `python day-07.py`
        `python day-07.py -test -2`
        `python day-07.py -2`
        `python day-07.py -test -both`
        `python day-07.py -both`
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
