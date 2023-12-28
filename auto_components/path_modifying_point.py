from auto_components.drop_down_menu import DropDownMenu
from auto_components.movable_point import MovablePoint
from auto_components.input_field import InputField
from auto_features.data_validator import DataValidator
from miscellaneous.important_variables import *


class PathModifyingPoint(MovablePoint):
    """The points that dictate the path of the robot"""

    angle_at_point = 0
    path_index = 0

    def __init__(self, click_function, button_number):
        """Initializes the object"""

        super().__init__(path_modifying_point_color, selected_path_modifying_point_color, click_function, button_number)

        self.vertical_velocity_field = InputField(WINDOW, SMALL_FONT, "1", error_message_function=DataValidator.get_float_error_message_function(-10_000, 10_000))
        self.horizontal_velocity_field = InputField(WINDOW, SMALL_FONT, "1", error_message_function=DataValidator.get_float_error_message_function(-10_000, 10_000))
        self.spline_order_input_field = InputField(WINDOW, SMALL_FONT, "1", error_message_function=self.get_spline_order_error_message)
        self.user_modifiable_fields += [self.horizontal_velocity_field, self.vertical_velocity_field, self.spline_order_input_field]

        self.update_input_fields_belongs_to()

    def get_spline_order_error_message(self, value):
        """
            Returns:
                str: the error message if the value is invalid, None otherwise"""

        return_value = None
        valid_values = ["1", "5"]

        if not valid_values.__contains__(value):
            return_value = f"Value {value} is not within the valid values: {valid_values}"

        return return_value

    def set_horizontal_velocity(self, value):
        self.horizontal_velocity_field.set_text(value)

    def set_vertical_velocity(self, value):
        self.vertical_velocity_field.set_text(value)

    def set_spline_order(self, value):
        self.spline_order_input_field.set_text(value)

    def get_horizontal_velocity(self):
        return float(self.horizontal_velocity_field.get_text())

    def get_vertical_velocity(self):
        return float(self.vertical_velocity_field.get_text())

    def get_spline_order(self):
        return int(self.spline_order_input_field.get_text())

    def get_angle_at_point(self):
        """
            Returns:
                float: the angle of the robot at this point"""

        return self.angle_at_point

    def set_angle_at_point(self, angle):
        """Sets the angle of the robot at this point"""

        self.angle_at_point = angle