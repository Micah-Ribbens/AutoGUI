from auto_components.command_parameter_saver import CommandParameterSaver
from auto_components.movable_point import MovablePoint
from auto_components.drop_down_menu import DropDownMenu
from auto_components.input_field import InputField
from auto_features.data_validator import DataValidator
from miscellaneous.popup_variables import *
from miscellaneous.important_variables import *
from auto_features.commands_retriever import commands_retriever
from miscellaneous.important_variables import points
from auto_features.path_creation import *


class PathActionPoint(MovablePoint):
    """The points along the robot path that dictate the actions along the path"""
    
    command_parameter_saver = None
    adjusted_angle = None  # For the required points- they are different from the GUI angles (and they are in radians)
    t_value = -1

    def __init__(self, click_function, button_number, is_on_screen=True):
        """Initializes the object"""

        super().__init__(path_action_point_color, selected_path_action_point_color, click_function, button_number)

        self.speed_field = InputField(WINDOW, SMALL_FONT, 1.0, error_message_function=DataValidator.get_float_error_message_function(-10_000, 10_000))
        self.t_value_field = InputField(WINDOW, SMALL_FONT, "0", error_message_function=self.get_t_value_error_message)
        self.command_drop_down_menu = DropDownMenu(WINDOW, 0, commands_retriever.get_command_names())

        self.left_edge_field.is_editable = False
        self.top_edge_field.is_editable = False

        self.user_modifiable_fields += [self.speed_field, self.t_value_field, self.command_drop_down_menu]
        self.set_command(commands_retriever.get_command_names()[0])  # So there is a value for current_command

        self.command_parameter_saver = CommandParameterSaver()
        self.command_drop_down_menu.set_command(self.update_popup_window, [])
        self.update_input_fields_belongs_to()

        # If the point is not on the screen, then it should be visible to the user (this point will be later destroyed),
        # But it still renders onto the screen if it is visible, which should not happen
        if not is_on_screen:
            self.place(x=0, y=0, width=0, height=0)

    def get_t_value_error_message(self, string_t_value):
        return_value = None
        t_value = float(string_t_value)

        if t_value < 0 or t_value > len(points.path_modifying_points) - 1:
            return_value = f"The t value must be between 0 and {len(points.path_modifying_points) - 1}"

        return return_value

    def path_modifying_point_number_is_valid(self, number):
        """
            Returns:
                bool: whether the PathModifyingPoint value is valid"""

        return int(number) >= 1 and int(number) <= len(points.path_modifying_points)

    def update_popup_window(self):
        """Updates the pop up window and updates the input field's values with the command_parameter_saver's values"""

        command_popup_window = commands_frame_saver.get_command_popup_window(self.get_command_name())
        command_popup_window.show()

        command_popup_window.set_input_fields_text(self.get_command_parameter_values())
        command_popup_window.set_save_button_command(self.save_command_parameter_values)

    def save_command_parameter_values(self):
        """Saves the values of the command parameters that were in the CommandPopupWindow"""

        command_popup_window = commands_frame_saver.get_command_popup_window(self.get_command_name())
        command_values = command_popup_window.get_input_field_values()
        self.command_parameter_saver.set_command_parameter_values(self.get_command_name(), command_values)

    def set_speed(self, speed):
        self.speed_field.set_text(speed)

    # Get commands
    def get_command_name(self):
        return self.command_drop_down_menu.get_selected_item()

    def set_command(self, value):
        self.command_drop_down_menu.set_selected_item(value)

    def get_speed(self):
        return float(self.speed_field.get_text())

    def get_combined_command_parameter_names(self):
        """Calls the method of the same name in 'self.command_parameter_saver' and gives it self.get_command_name() as the parameter"""

        return commands_retriever.get_combined_command_parameter_names(self.get_command_name())

    def get_command_parameter_values(self):
        """Calls the method of the same name in 'self.command_parameter_saver' and gives it self.get_command_name() as the parameter"""

        return self.command_parameter_saver.get_command_parameter_values(self.get_command_name())

    def get_command_parameter_value(self, parameter_name):
        """Calls the method of the same name in 'self.command_parameter_saver' and gives it self.get_command_name() and 'parameter_name' as the parameters"""

        return self.command_parameter_saver.get_command_parameter_value(self.get_command_name(), parameter_name)

    def set_command_parameter_values(self, values):
        """Calls the method of the same name in 'self.command_parameter_saver' and gives it self.get_command_name() and 'values' as the parameters"""

        self.command_parameter_saver.set_command_parameter_values(self.get_command_name(), values)

    def set_t_value(self, t_value):
        """Sets the t_value"""

        self.t_value_field.set_text(t_value)

    def get_t_value(self):
        """
            Returns:
                float: the t_value"""

        return float(self.t_value_field.get_text())

    def place(self, want_to_update_input_fields=False, **kwargs):
        """Places the point on the screen and updates the t"""

        super().place(want_to_update_input_fields, **kwargs)

        if len(points.path_points) != 0 and want_to_update_input_fields:
            path_point = get_closest_path_point(self.get_field_left_edge(), self.get_field_top_edge())

            t_value = get_path_index_t_value(*path_point)
            self.set_t_value(t_value)

            self.set_field_left_edge(path_point[0], want_rounding=True)
            self.set_field_top_edge(path_point[1], want_rounding=True)

            self.default_update_coordinates()

    def default_update_coordinates(self):
        """Updates the coordinates of the path action point based on the t value of the point"""

        path_point_index = get_t_value_path_index(self, points.path_modifying_point_path_indexes)
        path_point = points.path_points[path_point_index]

        self.set_field_left_edge(path_point[0], want_rounding=True)
        self.set_field_top_edge(path_point[1], want_rounding=True)

        MovablePoint.default_update_coordinates(self)