from auto_components.drop_down_menu import DropDownMenu
from auto_components.grid_items import GridItems
from auto_components.movable_point import MovablePoint
from auto_components.input_field import InputField
from auto_components.path_action_point import PathActionPoint
from auto_features.data_validator import DataValidator
from miscellaneous.important_variables import *


class RequiredPoint(PathActionPoint):
    """The points that dictate the path of the robot"""

    angle_at_point = 0
    path_index = 0

    def __init__(self, click_function, button_number, is_on_screen=True):
        """Initializes the object"""

        super().__init__(click_function, button_number, is_on_screen=is_on_screen)
        self.configure(bg=required_point_color)

        self.color, self.base_color = required_point_color, required_point_color
        self.selected_color = selected_required_point_color

        self.angle_field = InputField(WINDOW, SMALL_FONT, "30", True,
                                 error_message_function=DataValidator.get_float_error_message_function(0, 360))

        self.user_modifiable_fields = []
        for field in self.base_modifiable_fields:
            self.user_modifiable_fields.append(field)

        self.user_modifiable_fields += [self.t_value_field, self.angle_field]

        self.user_modifiable_fields_grid = GridItems(self.user_modifiable_fields, GridItems.horizontal_grid)

        self.update_input_fields_belongs_to()

    def set_angle(self, angle):
        """Sets the angle of the RequiredPoint"""

        self.angle_field.set_text(angle)

    def get_angle(self):
        """
            Returns:
                float: the angle of the robot at the RequiredPoint"""

        return float(self.angle_field.get_text())

