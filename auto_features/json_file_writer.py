import math
import uuid
from tkinter import messagebox

from auto_components.path_action_point import PathActionPoint
from miscellaneous.important_variables import *
from auto_features.path_creation import *
from auto_features.commands_retriever import commands_retriever
from miscellaneous.utility_functions import truncate

class JSONFileWriter:
    """The class that writes all the files"""

    path_action_point_json_items = []
    path_action_point_left_edge = 0
    path_action_point_top_edge = 0
    last_angle = 0
    path_modifying_point_to_current_angle = {}
    path_modifying_point_path_indexes_length = []
    path_modifying_point_to_angle = {}
    required_point_index_to_angle = {}
    path_modifying_point_path_indexes = None

    def write_file(self, file, all_path_modifying_points, all_path_action_points,
                   start_all_json_contents, first_required_point, last_required_point, placement_angle):
        """"Writes the JSON file that the Auto Path code uses"""

        self.last_angle = math.radians(placement_angle)  # So it is converted to radians
        self.path_modifying_point_path_indexes = get_path_modifying_point_path_indexes()
        all_json_contents = start_all_json_contents

        required_points = points.required_points
        required_points = [first_required_point] + required_points + [last_required_point]

        update_path_modifying_point_information(all_path_action_points, all_path_modifying_points, required_points)

        # All the lists need an empty line after them and the last list does not need a comma
        # ALso have to call the make_*_accurate because the input fields don't always reflect what the GUI shows
        self.update_path_modifying_point_json(all_json_contents, all_path_modifying_points)

        self.update_required_points_json(all_json_contents, required_points)

        self.update_path_action_points_json(all_json_contents, all_path_action_points)

        json.dump(all_json_contents, file, indent=JSON_MAX_INDENT)

    def update_path_modifying_point_json(self, all_json_contents, path_modifying_points):
        """ Updates 'all_json_contents' so it contains the 'path_modifying_points' in it, so the file that is eventually written
            can contain all the information necessary for the Auto Path Follower"""

        # The contents of the control points list
        path_modifying_point_json_items = []

        # So all_json_contents can now contain all the control points (and modifications to 'path_modifying_point_json_items' will be tracked
        # How the GUI and Auto Follower name points is different, which is why these names are different
        all_json_contents["ControlPoints"] = path_modifying_point_json_items

        for path_modifying_point in path_modifying_points:
            left_edge = path_modifying_point.get_field_left_edge()
            top_edge = path_modifying_point.get_field_top_edge()

            spline_order = path_modifying_point.get_spline_order()

            new_path_modifying_point_list_item = {
                "X": left_edge,
                "Y": top_edge,
                "Vx": path_modifying_point.get_horizontal_velocity(),
                "Vy": path_modifying_point.get_vertical_velocity(),
                "order": spline_order
            }

            path_modifying_point_json_items.append(new_path_modifying_point_list_item)

    def update_required_points_json(self, all_json_contents, required_points):
        """ Updates 'all_json_contents' so it contains the 'required_points' in it, so the file that is eventually written
            can contain all the information necessary for the Auto Path Follower"""

        # The contents of the control points list
        required_points_json = []

        # So all_json_contents can now contain all the required points (and modifications to 'required_points_json' will be tracked
        all_json_contents["RequiredPoints"] = required_points_json

        for required_point in required_points:

            left_edge = required_point.get_field_left_edge()
            top_edge = required_point.get_field_top_edge()

            new_required_point_json = {
                "X": left_edge,
                "Y": top_edge,
                "angle-GUI": required_point.get_angle(),
                "angle": math.radians(required_point.get_angle()),
                "t": required_point.get_t_value()
            }

            new_required_point_json_args = {}
            new_required_point_json["args"] = new_required_point_json_args

            new_required_point_json["isNeeded"] = required_point.is_needed

            required_points_json.append(new_required_point_json)

    def update_path_action_points_json(self, all_json_contents, all_path_action_points):
        """
            Returns:
                str: the path_action_points JSON"""

        path_action_points = points.path_action_points

        self.path_action_point_json_items = []

        # How the GUI and Auto Follower define points is different, which is why the names are different here
        all_json_contents["WayPoints"] = self.path_action_point_json_items

        for path_action_point in path_action_points:
            self.update_path_action_point_command_components_json(path_action_point)

    def update_path_action_point_command_components_json(self, path_action_point: PathActionPoint):
        """Updates the command components; some commands are a conglomerate of 2+ commands, so this provides that architecture"""

        base_command_name = path_action_point.get_command_name()
        command_component_names = []

        # If there are no components for that command, then the components should be 0
        if commands_retriever.combined_commands.get(base_command_name) is not None:
            # The first one should be ignored because that is the base command, which is already accounted for
            command_component_names = commands_retriever.combined_commands.get(base_command_name)[1:]

        self.path_action_point_left_edge, self.path_action_point_top_edge = path_action_point.get_field_left_edge(), path_action_point.get_field_top_edge()

        base_command_unique_identifier = str(uuid.uuid4())[:4]  # Only first 4 digits are needed for a unique value
        self.update_path_action_point_command_json(path_action_point, base_command_name, base_command_unique_identifier, True, 0, path_action_point.is_needed)

        # Have to set these, so the next point will be the closest to the point of the base command
        index = get_t_value_path_index(path_action_point, points.path_modifying_point_path_indexes)
        self.path_action_point_left_edge, self.path_action_point_top_edge = points.path_points[index]

        for x in range(len(command_component_names)):
            self.path_action_point_left_edge, self.path_action_point_top_edge = self.get_next_path_action_point_coordinates([self.path_action_point_left_edge, self.path_action_point_top_edge])
            t_value = self.get_path_index_t_value([self.path_action_point_left_edge, self.path_action_point_top_edge])
            path_action_point.set_t_value(t_value)

            self.update_path_action_point_command_json(path_action_point, command_component_names[x],
                                                         base_command_unique_identifier, False, x + 1, path_action_point.is_needed)


    def get_surrounding_path_modifying_point_indexes(self, path_index):
        """ 
            Returns:
                list[int]: {previous_path_modifying_point_index, next_path_modifying_point_index}; the indexes of the
                path modifying points that are before and after the 'path_index'"""

        previous_path_modifying_point_path_index = self.path_modifying_point_path_indexes[0]
        next_path_modifying_point_path_index = self.path_modifying_point_path_indexes[1]

        for path_modifying_point_path_index in self.path_modifying_point_path_indexes:
            if (path_modifying_point_path_index > previous_path_modifying_point_path_index and
                    path_modifying_point_path_index <= path_index):

                previous_path_modifying_point_path_index = path_modifying_point_path_index

            if (path_modifying_point_path_index < next_path_modifying_point_path_index and
                    path_modifying_point_path_index >= path_index):

                next_path_modifying_point_path_index = path_modifying_point_path_index

    def update_path_action_point_command_json(self, path_action_point, base_command_name, base_command_unique_identifier, is_base_command, command_component_number, is_needed):
        """ Updates the json for the base path modifying point command or command component- The data for all of these will be in
            commands.json"""

        new_path_action_point_json_item = {}
        current_command_parameter_names = commands_retriever.get_command_parameter_base_names(base_command_name)

        self.add_path_action_point_tracking_values(new_path_action_point_json_item, is_base_command, base_command_unique_identifier, command_component_number)

        self.add_keys_and_values_to_dictionary(["X", "Y", "Speed", "Command", "t"],
                                               [self.path_action_point_left_edge, self.path_action_point_top_edge, path_action_point.get_speed(),
                                                base_command_name, path_action_point.get_t_value()],
                                               new_path_action_point_json_item)

        current_command_parameter_values = self.get_command_parameters_values(current_command_parameter_names,
                                                                              path_action_point)
        new_path_action_point_json_item_args = {}
        new_path_action_point_json_item["args"] = new_path_action_point_json_item_args
        self.add_keys_and_values_to_dictionary(current_command_parameter_names, current_command_parameter_values,
                                               new_path_action_point_json_item_args)

        self.path_action_point_json_items.append(new_path_action_point_json_item)
        new_path_action_point_json_item["isNeeded"] = is_needed


    def add_path_action_point_tracking_values(self, new_path_action_point_json_item, is_base_command, base_command_unique_identifier, subcomponent_number):
        """ Adds the values that are used for tracking where components of a command belong to in 'new_path_action_point_json_item'
            the tracking values are 'name' and 'belongsTo'"""
        
        if is_base_command:
            new_path_action_point_json_item["name"] = base_command_unique_identifier
            new_path_action_point_json_item["belongsTo"] = "self"
        
        else:
            new_path_action_point_json_item["name"] = f"{base_command_unique_identifier} [{subcomponent_number}]"
            new_path_action_point_json_item["belongsTo"] = base_command_unique_identifier

    def get_command_parameters_values(self, current_parameter_names, path_action_point):
        """
            Returns:
                list[str]: the values of the command parameters for the 'path_action_point'"""

        command_parameters_values = []

        for current_parameter_name in current_parameter_names:
            parameter_value = path_action_point.get_command_parameter_value(current_parameter_name)
            command_parameters_values.append(parameter_value)

        return command_parameters_values

    def get_next_path_action_point_coordinates(self, previous_coordinates):
        """
            Returns:
                list[float]: [left_edge, top_edge]; the coordinates of the next path modifying point. This is important because if one GUI path modifying point command
                is the combination of 2+ Auto path modifying point commands then those 2+ points need to be spaced apart otherwise the Auto code
                raises an error"""

        return_value = []
        previous_coordinates_index = points.path_points.index(previous_coordinates)
        distance = 0

        for x in range(previous_coordinates_index, len(points.path_points)):
            new_coordinates = points.path_points[x]
            distance += math.dist(previous_coordinates, new_coordinates)

            if distance >= MINIMUM_DISTANCE_BETWEEN_PATH_MODIYFING_POINTS:
                return_value = new_coordinates
                break

        # If it could not find coordinates that are not far enough from the previous path modifying point then a path modifying point can't be there
        # Because the Auto code will raise an Error if path modifying points are too close to each other
        if len(return_value) == 0:
            raise ValueError("It is not possible to have a path modifying point there because it will be too close" +
                             "to other path modifying points")

        return return_value

    def add_keys_and_values_to_dictionary(self, keys, values, dictionary):
        """Adds the key value pairs to the dictionary"""

        for x in range(len(keys)):
            dictionary_key = keys[x]
            dictionary_value = values[x]

            dictionary[dictionary_key] = dictionary_value

    def update_angle_key_and_value_pairs(self, keys, values):
        """Updates all the key value pairs that are angles: the key has 'angle' in its name"""

        for x in range(len(keys)):
            dictionary_key = keys[x]
            dictionary_value = values[x]

            if dictionary_key.__contains__("angle") or dictionary_key.__contains__("Angle"):
                current_radian_angle = float(dictionary_value) * math.pi / 180
                delta_angle = current_radian_angle - self.last_angle

                values[x] = delta_angle
                keys.append(f"{dictionary_key}-GUI")
                values.append(dictionary_value)

                # So the GUI angle (field centric) can be stored also.
                self.last_angle = current_radian_angle

    def write_positions_to_file(self):
        """Writes the control points [x, y] to a file, so the JAR file can give all the points for the path"""

        all_json_contents = {}

        self.update_path_modifying_point_json(all_json_contents, points.path_modifying_points)
        json.dump(all_json_contents, open("swerve_input.txt", "w+"), indent=JSON_MAX_INDENT)

        os.system("java -jar AutoFollower.jar swerve_input.txt swerve_output.txt")
        swerve_output_reading = open("swerve_output.txt", "r")
        file_current_contents = get_string(swerve_output_reading.read()[:-1])  # The last enter must be deleted

        file_current_contents_list = file_current_contents.split("\n")
        last_path_point = file_current_contents_list[-1]
        # remaining_file_current_contents = get_string(file_current_contents_list[:-1])

        remaining_file_current_contents = ""
        for item in file_current_contents_list[:-1]:
            remaining_file_current_contents += f"{item}\n"

        if len(file_current_contents.split("\n")) <= 2:
            messagebox.showerror("ERROR", "Java does not seem to be installed on your system !!!")
            raise ValueError("Java does not seem to be installed on your system !!!")

        swerve_output = open("swerve_output.txt", "w+")

        # The file does not have the last Path Action Point number
        swerve_output.write(f"{remaining_file_current_contents}Control Point: {len(points.path_modifying_points) - 1}\n{last_path_point}")
        swerve_output.close()

        update_meter_path_points()


json_file_writer = JSONFileWriter()