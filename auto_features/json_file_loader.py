import math

from auto_components.path_modifying_point import PathModifyingPoint
from auto_components.path_action_point import PathActionPoint
from auto_components.required_points import RequiredPoint
from miscellaneous.important_variables import *
from auto_features.commands_retriever import commands_retriever
from miscellaneous.utility_functions import *


class JSONFileLoader:
    """Loads the JSON files the JSONFileWriter writes, so the Auto GUI application can save progress"""

    path_modifying_points_json = None
    required_points_json = None
    path_action_points_json = None
    point_click_function = None

    def set_all_points_to_reflect_json_file(self, path_modifying_points, path_action_points, required_points, json_contents, point_click_function):
        """Updates all points on the screen (path_modifying_points, required_points, and path_action_points) to reflect what is in the JSON file"""

        # How the GUI and Auto Follower name points is different, which is why these names are different
        self.path_modifying_points_json = json_contents["ControlPoints"]
        self.required_points_json = json_contents["RequiredPoints"]
        self.path_action_points_json = json_contents["WayPoints"]

        self.point_click_function = point_click_function

        self.set_path_modifying_points_to_reflect_json_file(path_modifying_points)
        self.set_path_action_points_to_reflect_json_file(path_action_points)
        self.set_required_points_to_reflect_json_file(required_points)

    def set_path_modifying_points_to_reflect_json_file(self, path_modifying_points):
        """Updates the control points list to reflect what is in the JSON file"""

        for x in range(len(self.path_modifying_points_json)):
            # Adding the control point to control points
            current_path_modifying_point = PathModifyingPoint(self.point_click_function, x)
            path_modifying_points.append(current_path_modifying_point)

            # Updating the control point's attributes, so it reflects the JSON file
            current_path_modifying_point_json = self.path_modifying_points_json[x]
            self.set_point_position(current_path_modifying_point, current_path_modifying_point_json)
            current_path_modifying_point.set_vertical_velocity(float(current_path_modifying_point_json["Vy"]))
            current_path_modifying_point.set_horizontal_velocity(float(current_path_modifying_point_json["Vx"]))
            current_path_modifying_point.set_spline_order(current_path_modifying_point_json["order"])

    def set_point_position(self, point, point_json):
        """Sets the point's position to reflect the JSON for the point"""

        point.set_field_left_edge(float(point_json["X"]))
        point.set_field_top_edge(float(point_json["Y"]))

    def set_path_action_points_to_reflect_json_file(self, path_action_points):
        """Updates the control points list to reflect what is in the JSON file"""

        current_path_action_point_number = 0
        path_action_point_number = 0

        while path_action_point_number < len(self.path_action_points_json):
            current_path_action_point_json = self.path_action_points_json[current_path_action_point_number]

            if current_path_action_point_json["isNeeded"]:
                path_action_point = PathActionPoint(self.point_click_function, path_action_point_number)
                path_action_points.append(path_action_point)
                self.set_point_position(path_action_point, current_path_action_point_json)

                path_action_point_command_name = current_path_action_point_json["Command"]
                self.set_path_action_point_command_to_reflect_json_file(path_action_point, current_path_action_point_json, current_path_action_point_number)
                number_of_additional_command_components = self.get_number_of_additional_path_action_point_command_components(path_action_point_command_name)

                path_action_point.set_t_value(current_path_action_point_json["t"])
                current_path_action_point_number += 1 + number_of_additional_command_components

            path_action_point_number += 1

    def set_required_points_to_reflect_json_file(self, required_points):
        """Updates the requried_points list to reflect what is in the JSON file"""

        required_point_number = 1

        for x in range(len(self.required_points_json)):
            current_required_points_json = self.required_points_json[x]

            # Determines if this point is specific to the GUI or the Auto Follower. If it belongs to the Auto Follower, then
            # That point should not be added
            if current_required_points_json["isNeeded"]:
                current_required_point = RequiredPoint(self.point_click_function, required_point_number + 1)
                required_points.append(current_required_point)

                current_required_point.set_t_value(current_required_points_json["t"])
                self.set_point_position(current_required_point, current_required_points_json)
                radian_angle = current_required_points_json["angle"]
                current_required_point.set_angle(math.degrees(radian_angle))

    def set_path_action_point_command_to_reflect_json_file(self, path_action_point, current_path_action_point_json, current_path_action_point_number):
        """Sets the command of the path modifying point to reflect what is in the json file (it will also combine the command components)"""

        path_action_point_command_name = current_path_action_point_json["Command"]
        path_action_point.set_command(path_action_point_command_name)

        current_command_parameters = current_path_action_point_json["args"]
        current_command_parameter_values = list(current_command_parameters.values())

        number_of_additional_command_components = self.get_number_of_additional_path_action_point_command_components(path_action_point_command_name)

        # Adding one to get to the next indexes past the original index
        for j in range(current_path_action_point_number + 1, current_path_action_point_number + number_of_additional_command_components + 1):
            path_action_point_component_data = self.path_action_points_json[j]
            component_parameters = path_action_point_component_data["args"]
            component_command_parameter_values = list(component_parameters.values())
            current_command_parameter_values += component_command_parameter_values

        path_action_point.set_command_parameter_values(current_command_parameter_values)

    def get_number_of_additional_path_action_point_command_components(self, path_action_point_command_name):
        """
            Returns:
                int: the number of components a command has"""

        # If it is not a combined command it has no more additional components, but if it is a combined command it will
        number_of_additional_command_components = 0
        if commands_retriever.combined_commands.__contains__(path_action_point_command_name):
            # One of a command's components is itself, so one must be subtracted
            number_of_additional_command_components = len(commands_retriever.combined_commands.get(path_action_point_command_name)) - 1

        return number_of_additional_command_components


json_file_loader = JSONFileLoader()

