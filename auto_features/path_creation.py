import math
from miscellaneous import important_variables

from miscellaneous.utility_functions import *

from miscellaneous.colors import path_action_point_color


def get_closest_path_point(left_edge, top_edge):
    """
        Returns:
            list[float]: [left_edge, top_edge]; the closest point on the path to the path_action_point. IMPORTANT the unit for the
            left_edge, top_edge, and path_points must all be equal (meters, pixel, etc.)"""

    return points.path_points[get_closest_path_point_index(left_edge, top_edge)]


def get_closest_path_point_index(left_edge, top_edge):
    """
            Returns:
                int: the index of the closest path point"""

    shortest_distance = float('inf')
    closest_point_index = 0

    for i in range(len(points.path_points)):
        current_distance = math.dist(points.path_points[i], (left_edge, top_edge))

        if current_distance < shortest_distance:
            shortest_distance = current_distance
            closest_point_index = i

    return closest_point_index


def draw_path_lines(field_canvas, path_modifying_point_line_width, path_line_width):
    """Draws the path and the path_action_points which are connected to the path"""

    pixel_path_points = get_pixel_path_points()

    for j in range(len(pixel_path_points) - 1):
        start_point = pixel_path_points[j]
        end_point = pixel_path_points[j + 1]
        field_canvas.create_line(start_point, end_point, fill=path_modifying_point_color, width=path_line_width)

    # for path_action_point in points.path_action_points:
    #     closest_point = get_closest_path_point(path_action_point.left_edge, path_action_point.top_edge, pixel_path_points, path_action_point)
    #     field_canvas.create_line((path_action_point.left_edge, path_action_point.top_edge), closest_point, fill=path_action_point_color, width=path_modifying_point_line_width)
    #
    # for required_point in points.required_points:
    #         closest_point = get_closest_path_point(required_point.left_edge, required_point.top_edge, pixel_path_points, required_point)
    #         field_canvas.create_line((required_point.left_edge, required_point.top_edge), closest_point, fill=required_point_color, width=path_modifying_point_line_width)


def get_pixel_location(left_edge, top_edge):
    """
            Returns:
                list[float]: [left_edge, top_edge]; the pixel location that the GUI uses. This converts from the Swerve Code
                locations to the GUI code locations."""

    return [int(meters_to_pixels(left_edge)), int(meters_to_pixels(top_edge))]

# The reason this function has very similar code to get_meter_path_points() is because calling get_meter_path_points()
# And then getting the pixel points requires going through the same points twice, which is too slow
def get_pixel_path_points():
    """
            Returns:
                list[list[float]]: [[x1, y1], [x2, y2]]; the points along the path (in pixels)"""

    pixel_path_points = []
    file = open("swerve_output.txt", "r")

    # The last line has no data as of now, so that line should be ignored (hence list[:-1])
    for line in get_lines(file.read()[:-1]):
        is_path_action_point_line = line.__contains__("Control Point")

        if is_path_action_point_line:
            continue

        point_coordinates = line.split(",")
        left_edge, top_edge = float(point_coordinates[0]), float(point_coordinates[1])
        left_edge, top_edge = get_gui_centric_coordinates(left_edge, top_edge)
        pixel_locations = get_pixel_location(left_edge, top_edge)

        if not pixel_path_points.__contains__(pixel_locations):
            pixel_path_points.append(pixel_locations)

    file.close()
    return pixel_path_points

def update_meter_path_points():
    """Updates 'points.path_points' to reflect what was written to swerve_output.txt"""

    path_points = []
    file = open("swerve_output.txt", "r")

    for line in get_lines(file.read()[:-1]):
        is_path_action_point_line = line.__contains__("Control Point")

        # The lines that does not contain control points then it has the path points
        if not is_path_action_point_line:
            point_coordinates = line.split(",")
            left_edge, top_edge = float(point_coordinates[0]), float(point_coordinates[1])

            # Have to convert from the (0, 0) of the coordinates being the top left edge of the screen to the (0, 0) being the center of the hub
            # left_edge, top_edge = get_hub_centric_coordinates(left_edge, top_edge)

            path_points.append([left_edge, top_edge])

    file.close()

    points.path_points = path_points
    points.path_modifying_point_path_indexes = get_path_modifying_point_path_indexes()

def get_hub_centric_coordinates(left_edge, top_edge):
    """ The meter left_edge and top_edge (location user modifies) has (0, 0) at the center of the hub and the pixel location
        (GUI location) has (0,0) at the top left edge of the screen. When the pixel coordinates are converted to meters by a scalar multiplier,
        therefore, offsets must be subtracted to have (0, 0) once again be the center of the hub

        Args:
            left_edge (float): the left_edge of a point that has (0, 0) at the top left edge of the screen instead of the center of the hub
            top_edge (double): the top_edge of a point that has (0, 0) at the top left edge of the screen instead of the center of the hub

        Returns:
            list[double]: {converted_left_edge, converted_top_edge}; the left_edge and top_edge that has the center of the hub be (0, 0)
    """

    left_edge -= important_variables.CENTER_OF_FIELD_HORIZONTAL_OFFSET
    top_edge -= CENTER_OF_FIELD_VERTICAL_OFFSET

    top_edge *= -1  # Because of how the GUI is set up the number will be the negative version of the correct meter number

    return [left_edge, top_edge]

def get_gui_centric_coordinates(left_edge, top_edge):
    """ The meter left_edge and top_edge (location user modifies) has (0, 0) at the center of the hub and the pixel location
        (GUI location) has (0,0) at the top left edge of the screen. When the pixel coordinates are converted to meters by a scalar multiplier,
        therefore, offsets must be added to have (0, 0) once again be the top left edge of the screen

        Args:
            left_edge (float): the left_edge of a point that has (0, 0) at the center of the hub instead of the top left edge of the screen
            top_edge (float): the top_edge of a point that has (0, 0) at the center of the hub instead of the top left edge of the screen

        Returns:
            list[float]: {converted_left_edge, converted_top_edge}; the left_edge and top_edge that has the top left edge of the screen be (0, 0)
    """

    top_edge *= -1  # The numbers are multiplied by -1 to convert to hub_centric, so it must be multiplied by -1 to convert it to gui
    left_edge += important_variables.CENTER_OF_FIELD_HORIZONTAL_OFFSET
    top_edge += CENTER_OF_FIELD_VERTICAL_OFFSET

    return [left_edge, top_edge]

def get_meter_location(left_edge, top_edge):
    """
            Returns:
                list[float]: [left_edge, top_edge]; the location that the AutoFollower.jar file needs to create the path - converts
                the values into meters and puts all the numbers based off of the base_left_edge and base_top_edge"""

    return [pixels_to_meters(left_edge), pixels_to_meters(top_edge)]


def get_path_modifying_point_path_indexes():
    """
            Returns:
                list[int]: the path indexes of the path modifying points"""

    return_value = []
    file = open("swerve_output.txt", "r")
    path_modifying_point_index = -1  # So the first path modifying point index starts at 0 not 1

    for line in get_lines(file.read()[:-1]):
        is_path_action_point_line = line.__contains__("Control Point")

        # The lines that does not contain control points then it has the path points
        if is_path_action_point_line:
            amount_added = -1 if path_modifying_point_index == -1 else 0  # It starts at -1, which is not a valid index
            return_value.append(path_modifying_point_index + 1)

        else:
            path_modifying_point_index += 1

    file.close()

    return return_value

def update_path_modifying_point_information(path_action_points=None, path_modifying_points=None, required_points=None):
    """Updates the information that the path modifying points need specifically which required point affects the angle of the robot"""

    required_point_path_indexes = []

    # Updating the required point paths
    path_action_points = points.path_action_points if path_action_points is None else path_action_points
    required_points = points.required_points if required_points is None else required_points
    path_modifying_points = points.path_modifying_points if path_modifying_points is None else path_modifying_points

    path_modifying_point_path_indexes = get_path_modifying_point_path_indexes()
    for x in range(len(points.path_modifying_points)):
        path_modifying_points[x].path_index = path_modifying_point_path_indexes[x]

    for required_point in required_points:
        index = get_t_value_path_index(required_point, path_modifying_point_path_indexes)
        required_point_path_indexes.append(index)

    update_path_modifying_point_angle_at_points(path_modifying_points, required_points, required_point_path_indexes)

    return [points.path_points, required_point_path_indexes, path_modifying_point_path_indexes]

def update_path_modifying_point_angle_at_points(path_modifying_points, required_points, required_point_path_indexes):
    """Updates the path_modifying_point's 'angle_at_point' attribute, so the angle of the robot lines can be drawn"""

    # Updating the angles of the path_modifying_points
    for path_modifying_point in path_modifying_points:
        last_angle = required_points[0].get_angle()
        next_angle = required_points[1].get_angle()

        previous_required_point_path_index = float("-inf")
        next_required_point_path_index = float("inf")
        path_modifying_point_path_index = path_modifying_point.path_index

        for i in range(len(required_point_path_indexes)):
            required_point_path_index = required_point_path_indexes[i]

            if (required_point_path_index <= path_modifying_point_path_index and
                    required_point_path_index > previous_required_point_path_index):

                previous_required_point_path_index = required_point_path_index
                last_angle = required_points[i].get_angle()

            if (required_point_path_index >= path_modifying_point_path_index and
                    required_point_path_index < next_required_point_path_index):

                next_required_point_path_index = required_point_path_index
                next_angle = required_points[i].get_angle()

        angle = get_angle_at_point(path_modifying_point_path_index,
                                   previous_required_point_path_index,
                                   next_required_point_path_index, last_angle,
                                   next_angle)

        path_modifying_point.set_angle_at_point(angle)

def update_path_action_and_required_point_location(path_action_points, required_points, path_modifying_point_path_indexes, path_modifying_points):
    """Updates the t values of all the path_action_points. The t values allow the robot to know what to execute along the path"""

    for point in path_action_points + required_points:
        path_index = get_t_value_path_index(point, path_modifying_point_path_indexes)
        path_point = points.path_points[path_index]

        # Path point(s) are in this format: [left_edge, top_edge]
        point.set_field_left_edge(path_point[0], want_rounding=True)
        point.set_field_top_edge(path_point[1], want_rounding=True)

def get_path_index_t_value(left_edge, top_edge):
    """
            Returns:
                float: the t_value at that path_index"""

    # Finding the values for the math below
    path_index = points.path_points.index([left_edge, top_edge])

    previous_path_modifying_point_index = float("-inf")
    next_path_modifying_point_index = float("inf")

    previous_path_modifying_point_number = 0

    path_modifying_point_path_indexes = get_path_modifying_point_path_indexes()

    for x in range(len(path_modifying_point_path_indexes)):
        index = path_modifying_point_path_indexes[x]

        if index <= path_index and index > previous_path_modifying_point_index:
            previous_path_modifying_point_index = index
            previous_path_modifying_point_number = x

        if index >= path_index and index < next_path_modifying_point_index:
            next_path_modifying_point_index = index

    # Doing the math
    arc_distance = get_distance(previous_path_modifying_point_index, next_path_modifying_point_index)
    distance_to_path_point = get_distance(previous_path_modifying_point_index, path_index)

    t_value = previous_path_modifying_point_number

    # T values can have a value that is part of the way to another one like 1.5 would be halfway between path modifying
    # point 1 and path modifying point 2
    if arc_distance != 0:
        t_value += distance_to_path_point / arc_distance

    return truncate(t_value, INPUT_FIELD_DECIMAL_ACCURACY)

def get_t_value_path_index(point, path_modifying_point_path_indexes):
    """
            Returns:
                int: the path_index that the t value represents"""

    # T values and indexes are the same except t values need the decimal 'chopped off'
    path_modifying_point_index = int(point.get_t_value())

    return_value = path_modifying_point_path_indexes[path_modifying_point_index]

    # If the t value is not a plain number, then we need to calculate the top edge (2 would be plain while 2.1 would not be plain)
    if path_modifying_point_index != point.get_t_value():
        path_indexes = [path_modifying_point_path_indexes[path_modifying_point_index],
                        path_modifying_point_path_indexes[path_modifying_point_index + 1]]

        # Only keeping the decimal part of the t value
        t_value_proportion = point.get_t_value() - int(point.get_t_value())

        arc_distance = get_distance(*path_indexes)
        return_value = get_point_index_at_closest_distance(path_indexes[0], arc_distance * t_value_proportion)

    return return_value


def get_point_index_at_closest_distance(start_index, distance):
    """
            Returns:
                list[float]: {left_edge, top_edge}; the closest point that is the 'distance' from 'start_index'"""

    end_index = len(points.path_points) - 1
    current_distance = 0
    last_distance = 0
    return_value = end_index

    # You have to add 1 to 'end_index' to get the for loop to go to that value
    for x in range(start_index, end_index):

        last_point_index = x
        current_point_index = x + 1

        last_point = points.path_points[last_point_index]
        current_point = points.path_points[current_point_index]
        
        current_distance += math.dist(last_point, current_point)
        
        last_distance_delta = abs(distance - last_distance)
        current_distance_delta = abs(distance - current_distance)

        if current_distance >= distance and last_distance_delta < current_distance_delta:
            return_value = last_point_index
            break
        
        elif current_distance >= distance and current_distance_delta < last_distance_delta:
            return_value = last_point_index
            break
            
    return return_value
            

def get_angle_at_point(path_modifying_point_path_index, previous_required_point_path_index,
                        next_required_point_path_index, last_angle, next_angle):

    """ 
            Returns:
                float: the angle at the path modifying point (gotten from figuring out how much each required point
                angle affects the path modifying point"""

    return_value = None

    # No proportion calculations need to be done because the required point is on the path modifying point
    if previous_required_point_path_index == next_required_point_path_index:
        return_value = last_angle

    else:
        last_required_point_distance_from_path_modifying_point = get_distance(previous_required_point_path_index, path_modifying_point_path_index)
        next_required_point_distance_from_path_modifying_point = get_distance(path_modifying_point_path_index, next_required_point_path_index)

        total_distance = last_required_point_distance_from_path_modifying_point + next_required_point_distance_from_path_modifying_point
        last_required_point_proportion = 1 - (last_required_point_distance_from_path_modifying_point / total_distance)
        next_required_point_proportion = 1 - (next_required_point_distance_from_path_modifying_point / total_distance)

        last_angle = math.radians(last_angle)
        next_angle = math.radians(next_angle)

        return_value = last_required_point_proportion * last_angle + next_required_point_proportion * next_angle

    return return_value

def get_distance(first_index, last_index):
    """Gets the distance from all the lines of the path points"""

    current_distance = 0
    for x in range(first_index, last_index):
        point1 = points.path_points[x]
        point2 = points.path_points[x + 1]

        current_distance += math.dist(point1, point2)

    return current_distance
