import re
import sys

import aocd
import portion as P
from tqdm import tqdm

# Set the day and year
DAY = "15"
YEAR = "2022"


def get_manhattan_distance(point_1, point_2):
    """
    Return the manhattan distance between 2 points
    """
    # sum of absolute difference between coordinates
    return sum(abs(p_1 - p_2) for p_1, p_2 in zip(point_1, point_2))


def get_input(path):
    """Load the data from the file"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip().split(":") for line in f.readlines()]

    sensor_regex = re.compile(r"Sensor at x=(\-?\d+), y=(\-?\d+)")
    beacon_regex = re.compile(r"closest beacon is at x=(\-?\d+), y=(\-?\d+)")

    sensors = {}

    for sensor, beacon in values:
        # Extract the x, y values for the sensor and nearest beacon
        sensor_location = tuple(
            [int(i) for i in sensor_regex.match(sensor.strip()).groups()]
        )
        beacon_location = tuple(
            [int(i) for i in beacon_regex.match(beacon.strip()).groups()]
        )

        # Store the nearest beacon
        sensors[sensor_location] = beacon_location

    return sensors


def get_distances(sensors):
    """Create a dictionary to say the maximum possible distances from the sensor"""

    distances = {}

    # Get the minimum distance for a different beacon
    for sensor, beacon in sensors.items():
        distances[sensor] = get_manhattan_distance(sensor, beacon)

    return distances


def filter_sensor_distances(distances, row_to_check):
    """Remove sensors that are too far away"""

    filtered_distances = {}

    for sensor, distance in distances.items():
        # Check if the straight line distance is too far
        if abs(sensor[1] - row_to_check) <= distance:
            filtered_distances[sensor] = distance

    return filtered_distances


def get_beacon_bounds(distances):
    """Identify the edges of the possible beacons"""

    # for each sensor, look at the minus manhattan from the x co-ord to the plus

    left_most_sensor = min([s[0] - d for s, d in distances.items()])

    right_most_sensor = max([s[0] + d for s, d in distances.items()])

    return left_most_sensor, right_most_sensor


def check_point(distances, point, beacons):
    """Identify if the point is in a 'no-beacon' zone"""

    # Check if it's a known beacon
    if point in beacons:
        return 0

    for sensor, distance in distances.items():
        if get_manhattan_distance(sensor, point) <= distance:
            # Can't be a beacon
            return 1

    # If it's not inside the 'no-go' zone, then it could contain a beacon
    return 0


def part_1_original(path, submit, test):
    """Part 1/Star 1"""

    # Get the data
    sensors = get_input(path)

    # Get all known beacons
    beacons = set(sensors.values())

    # Get the minimum distance
    distances = get_distances(sensors)

    # Get the row that we are checking
    row_to_check = 10 if test else 2000000

    # Remove any sensors that have no impact on the row
    distances = filter_sensor_distances(distances, row_to_check)

    # Get the minimum and maximum it could be
    min_check, max_check = get_beacon_bounds(distances)

    answer = 0

    # Check each point in the line
    for x in tqdm(range(min_check, max_check + 1)):
        valid = check_point(distances, (x, row_to_check), beacons)
        answer += valid

    # Print out the response
    print(f"Task 1 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="a", day=int(DAY), year=int(YEAR))


def part_1(path, submit, test):
    """Part 1/Star 1 (Optimised)"""

    # Get the data
    sensors = get_input(path)

    # Get the minimum distance
    distances = get_distances(sensors)

    # Get the row that we are checking
    row_to_check = 10 if test else 2000000

    # Remove any sensors that have no impact on the row
    distances = filter_sensor_distances(distances, row_to_check)

    # For the sensor, need to get the intervals that don't have sensors
    intervals = P.empty()
    for (x, y), distance in distances.items():
        intervals = intervals | P.closed(
            x - (distance - abs((row_to_check - y))),
            x + (distance - abs((row_to_check - y))),
        )

    # Remove any beacons in the row
    beacon_count = len(set([b for b in sensors.values() if b[1] == row_to_check]))

    # Interval count
    answer = 0
    if intervals.atomic:
        answer += intervals.upper - intervals.lower
    else:
        raise Exception("Not Atomic - need to deal with this")

    # Remove the beacon count from the answer
    answer -= beacon_count

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


def part_2(path, submit):
    """Part 2/Star 2"""

    # Get the data
    sensors = get_input(path)

    # Get the minimum distance
    distances = get_distances(sensors)

    # Check each row
    for row_to_check in tqdm(range(0, 4000001)):

        # For the sensor, need to get the intervals that don't have sensors
        intervals = P.empty()
        for (x, y), distance in distances.items():
            intervals = intervals | P.closed(
                x - (distance - abs((row_to_check - y))),
                x + (distance - abs((row_to_check - y))),
            )

        # Stop if there is a space in the line
        if not intervals.atomic:
            break

    # Get the x, y co-ordinate
    x = (P.closed(0, 4000001) - intervals).lower + 1
    y = row_to_check

    # Remove the beacon count from the answer
    answer = x * 4000000 + y

    # Print out the response
    print(f"Task 2 Answer: {answer}")

    # Submit the answer
    if submit:
        aocd.submit(answer, part="b", day=int(DAY), year=int(YEAR))


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-15.py -test`
        `python day-15.py`
        `python day-15.py -test -2`
        `python day-15.py -2`
        `python day-15.py -test -both`
        `python day-15.py -both`
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
        part_1(path, submit, test)
        part_2(path, submit)
    else:
        part_1(path, submit, test)
