import os
import tkinter
from copy import deepcopy

from auto_components.drop_down_menu import DropDownMenu
from auto_components.required_points import RequiredPoint
from auto_features.data_validator import DataValidator
from miscellaneous import important_variables

from auto_components.grid_items import GridItems
from auto_components.input_field import InputField
from auto_components.movable_point import MovablePoint
from auto_components.titled_input_field import TitledInputField
from auto_features.json_file_loader import json_file_loader
from auto_components.point_alterable_fields_frame import PointAlterableFieldsFrame
from auto_components.path_modifying_point import PathModifyingPoint

from auto_components.path_action_point import PathActionPoint
from auto_features.json_file_writer import json_file_writer
from auto_features.path_creation import *

from tkinter import filedialog, messagebox

from tkinter import *
from auto_components.grid import Grid

from miscellaneous.utility_functions import *
from miscellaneous.important_variables import *
from miscellaneous.popup_variables import commands_frame_saver, commands_main_frame


class MainScreen:
    """The main screen of the application"""

    font_size = 22

    # Toolbar
    draw_button = Button(WINDOW, compound=tkinter.CENTER, text="Draw", bg=pleasing_green, fg=white, font=TINY_FONT)
    update_points_button = Button(WINDOW, compound=tkinter.CENTER, text="Update Points", bg=pleasing_green, fg=white, font=TINY_FONT)
    clear_field_button = Button(WINDOW, compound=tkinter.CENTER, text="Clear Field", bg=pleasing_green, fg=white, font=TINY_FONT)
    reset_input_fields_button = Button(WINDOW, compound=tkinter.CENTER, text="Reset Fields", bg=pleasing_green, fg=white, font=TINY_FONT)
    save_file_button = Button(WINDOW, compound=tkinter.CENTER, text="Save File", bg=pleasing_green, fg=white, font=TINY_FONT)
    toolbar_height = min(get_measurement(SCREEN_HEIGHT, 15), SCREEN_HEIGHT - FIELD_IMAGE_HEIGHT)
    toolbar_length = get_measurement(SCREEN_LENGTH, 40)
    toolbar_top_edge = SCREEN_HEIGHT - toolbar_height
    popup_windows = []

    # Switching Points Bar
    switching_points_bar_height = get_measurement(SCREEN_HEIGHT, 5)
    selected_point_field = InputField(WINDOW, SMALL_FONT, "1", True)
    switched_point_field = InputField(WINDOW, SMALL_FONT, "2", True)
    swap_points_button = Button(WINDOW, compound=tkinter.CENTER, text="Swap", bg=pleasing_green, fg=white, font=SMALL_FONT)
    switching_points_bar_top_edge = SCREEN_HEIGHT - toolbar_height - switching_points_bar_height

    # Point Action Bar
    delete_button = Button(WINDOW, compound=tkinter.CENTER, text="Delete", bg=pleasing_green, fg=white, font=SMALL_FONT)
    move_button = Button(WINDOW, compound=tkinter.CENTER, text="Move", bg=pleasing_green, fg=white, font=SMALL_FONT)
    add_button = Button(WINDOW, compound=tkinter.CENTER, text="Add", bg=pleasing_green, fg=white, font=SMALL_FONT)
    point_bar_length = SCREEN_LENGTH - FIELD_IMAGE_LENGTH
    point_action_bar_height = get_measurement(SCREEN_HEIGHT, 5)
    point_action_bar_top_edge = SCREEN_HEIGHT - toolbar_height - switching_points_bar_height - point_action_bar_height
    point_action_bar_buttons = [delete_button, move_button, add_button]

    # Miscellaneous
    file_name = ""
    selected_point = None
    selected_input_field = None

    # File Menu
    menu = Menu(WINDOW)
    file_menu = Menu(menu)
    menu.add_cascade(label='File', menu=file_menu)

    # Point Info:
    path_action_points = []
    path_modifying_points = []
    required_points = []
    current_points_altered_class = PathModifyingPoint
    next_points_altered = {PathModifyingPoint: PathActionPoint, PathActionPoint: RequiredPoint,
                           RequiredPoint: PathModifyingPoint}

    points_altered_to_point_list = {PathActionPoint: path_action_points, PathModifyingPoint: path_modifying_points, RequiredPoint: required_points}
    points_altered_to_frame_button_color = {PathActionPoint: path_action_point_color, PathModifyingPoint: path_modifying_point_color, RequiredPoint: required_point_color}
    points_altered_to_frame_name = {PathActionPoint: "Path Action Point", PathModifyingPoint: "Path Modifying Point",
                                    RequiredPoint: "Required Point"}

    # Point Alterable Field Frames:
    path_modifying_point_alterable_fields_frame = PointAlterableFieldsFrame(path_modifying_points, ["Vx", "Vy", "x power"])
    path_action_point_alterable_fields_frame = PointAlterableFieldsFrame(path_action_points, ["Speed", "tValue", "Command"])
    required_point_alterable_fields_frame = PointAlterableFieldsFrame(required_points, ["tValue", "Angle"])
    toggle_frame_button = Button(WINDOW, compound=tkinter.CENTER, text="Path Action Point", bg=path_action_point_color, fg=white, font=SMALL_FONT)
    path_action_points_input_fields = []
    path_modifying_points_input_fields = []
    required_points_input_fields = []
    points_altered_to_point_alterable_fields_frame = {PathActionPoint: path_action_point_alterable_fields_frame,
                                                      PathModifyingPoint: path_modifying_point_alterable_fields_frame,
                                                      RequiredPoint: required_point_alterable_fields_frame}
    points_altered_to_points_input_fields = {PathActionPoint: path_action_points_input_fields,
                                             PathModifyingPoint: path_modifying_points_input_fields,
                                             RequiredPoint: required_points_input_fields}
    toggle_frame_button_height = get_measurement(SCREEN_HEIGHT, 4)
    point_alterable_fields_frames_height = point_action_bar_top_edge - toggle_frame_button_height # The Point frames should go down to the top of the Point action bar

    # Commands Frame Dimensions
    commands_frame_length = get_measurement(SCREEN_LENGTH, 15)

    # Initial And End Conditions Frame
    initial_conditions_tab_length = SCREEN_LENGTH - toolbar_length - commands_frame_length
    initial_conditions_tab_left_edge = toolbar_length + commands_frame_length
    initial_angle_field = TitledInputField(WINDOW, SMALL_FONT, "45", "Initial Angle", title_field_background_color=blue, title_field_text_color=white)
    initial_speed_field = TitledInputField(WINDOW, SMALL_FONT, "1", "InitialSpeed", title_field_background_color=blue, title_field_text_color=white)
    path_is_closed_drop_down_menu = DropDownMenu(WINDOW, 0, ["Path Is Closed", "Path Is Open"])
    end_angle_field = TitledInputField(WINDOW, SMALL_FONT, "45", "End Angle", title_field_background_color=blue, title_field_text_color=white)
    placement_angle_field = TitledInputField(WINDOW, SMALL_FONT, "0", "Placement Angle", title_field_background_color=blue, title_field_text_color=white)

    initial_and_end_condition_fields = [initial_angle_field, initial_speed_field, end_angle_field, placement_angle_field]

    # Field Image
    right_field_image = tkinter.PhotoImage(file=right_field_image_path)
    left_field_image = tkinter.PhotoImage(file=left_field_image_path)
    current_field_image = left_field_image
    field_image_bounds = [0, 0, SCREEN_LENGTH - point_bar_length, SCREEN_HEIGHT - toolbar_height]
    image_left_edge = FIELD_IMAGE_LENGTH / 2
    image_top_edge = FIELD_IMAGE_HEIGHT / 2
    field_canvas = None

    # States
    class States:
        DELETION = "DELETION"
        MOVING = "MOVING"
        ADD = "ADD"
        INIT = "INIT"

    point_editing_state = States.ADD
    point_editing_state_to_point_button = {States.DELETION: delete_button, States.MOVING: move_button, States.ADD: add_button}

    right_field_canvas = None
    left_field_canvas = None

    # Path Drawing
    path_line_width = 8
    path_modifying_point_line_width = 5

    # Storing information for saving files
    previous_file_name = ""
    previous_file_path = ""
    key_binding_to_function = {}
    event_key_binding_to_function = {}

    # Input Field Quick Transition Shortcuts
    currently_selected_point_number = 1
    current_input_field_number = 1

    copied_point = None

    def __init__(self):
        """Used for setting up the entire GUI"""

        self.create_file_menu()

        WINDOW.bind("<Button-1>", lambda e: self.run_mouse_click(e))

        self.delete_button.configure(command=lambda: self.change_point_editing_state(self.States.DELETION, self.States.ADD))
        self.move_button.configure(command=lambda: self.change_point_editing_state(self.States.MOVING, self.States.INIT))
        self.add_button.configure(command=lambda: self.change_point_editing_state(self.States.ADD, self.States.DELETION))
        self.toggle_frame_button.configure(command=self.toggle_points_alterable_fields_frame)
        self.update_points_button.configure(command=self.update_points)
        self.draw_button.configure(command=self.draw_path)
        self.clear_field_button.configure(command=self.clear_field)
        self.reset_input_fields_button.configure(command=self.reset_all_point_input_fields)
        self.swap_points_button.configure(command=self.swap_points_function)
        self.save_file_button.configure(command=self.quick_save_file)

        commands_frame_saver.create_commands_frame(self.toolbar_length, self.toolbar_top_edge, self.commands_frame_length, self.toolbar_height)
        commands_main_frame.default_show_items()

        # Keyboard Shortcuts
        self.add_all_key_binding_shortcuts()
        self.set_button_colors()
        self.display_everything()

        self.initial_speed_field.error_message_function = DataValidator.get_float_error_message_function(-8, 8)
        self.initial_angle_field.error_message_function = DataValidator.get_float_error_message_function(0, 360)
        self.end_angle_field.error_message_function = DataValidator.get_float_error_message_function(0, 360)
        self.placement_angle_field.error_message_function = DataValidator.get_float_error_message_function(0, 360)

        points.set_points(self.path_modifying_points, self.path_action_points, self.required_points)

    def toggle_points_alterable_fields_frame(self, new_point_class=None):
        """Toggles the PointsAlterableFieldsFrame, so it switches to being able to edit PathActionPoints and PathModifyingPoints"""

        self.run_error_checking()

        if not self.all_input_field_text_is_valid():
            return

        # Resetting the input field the GUI thinks is selected
        self.currently_selected_point_number = 1
        self.current_input_field_number = 1

        self.unselect_input_fields()

        last_frame = self.points_altered_to_point_alterable_fields_frame.get(self.current_points_altered_class)
        last_frame.hide()

        self.current_points_altered_class = self.next_points_altered.get(self.current_points_altered_class)

        if new_point_class is not None:
            self.current_points_altered_class = new_point_class

        print(self.current_points_altered_class)
        new_frame = self.points_altered_to_point_alterable_fields_frame.get(self.current_points_altered_class)
        new_frame.show()

        frame_name = self.points_altered_to_frame_name.get(self.current_points_altered_class)
        frame_button_color = self.points_altered_to_frame_button_color.get(self.current_points_altered_class)

        self.toggle_frame_button.configure(bg=frame_button_color, text=frame_name)

    def change_point_editing_state(self, point_editing_state, state_after_double_click):
        """Changes the point editing state, so it can switch between adding, moving, deleting, and doing nothing with points"""

        # If the button is a toggle then it should toggle between INIT (doing nothing) and that point_editing_state
        if point_editing_state == self.point_editing_state:
            self.point_editing_state = state_after_double_click

        else:
            self.point_editing_state = point_editing_state

        self.set_button_colors()

    def create_file_menu(self):
        """Creates the file menu system that allows the user to navigate between loading and saving files"""

        self.file_menu.add_command(label="Load File", command=self.request_load_file)
        self.file_menu.add_command(label="Save File As", command=self.save_file_as)
        self.file_menu.add_command(label="Right Field Image", command=lambda: self.draw_field_image(self.right_field_image))
        self.file_menu.add_command(label="Left Field Image", command=lambda: self.draw_field_image(self.left_field_image))
        WINDOW.configure(menu=self.menu)

    def create_bottom_bar(self):
        """Creates the button bar at the bottom of the screen (updating points, draw button, etc.)"""

        grid = Grid([0, self.toolbar_top_edge, self.toolbar_length, self.toolbar_height], 1, None)
        grid.turn_into_grid([self.draw_button, self.update_points_button, self.save_file_button,
                             self.clear_field_button, self.reset_input_fields_button], None, None)

    def create_switch_points_bar(self):
        """Creates the bar that allows you to switch points around"""

        grid = Grid([SCREEN_LENGTH - self.point_bar_length, self.switching_points_bar_top_edge, self.point_bar_length, self.switching_points_bar_height], 1, None)
        grid.turn_into_grid([self.selected_point_field, self.switched_point_field, self.swap_points_button], None, None)

    def create_point_action_bar(self):
        """Creates the bar that allows you to be able to add, delete, and move points"""

        grid = Grid([SCREEN_LENGTH - self.point_bar_length, self.point_action_bar_top_edge, self.point_bar_length, self.point_action_bar_height], 1, None)
        grid.turn_into_grid([self.add_button, self.delete_button, self.move_button], None, None)

    def create_point_alterable_fields_frames(self):
        """Creates the bar that allows you to be able to modify the field's attributes like X, Y, Command, etc."""

        grid = Grid([SCREEN_LENGTH - self.point_bar_length, self.toggle_frame_button_height, self.point_bar_length, self.point_alterable_fields_frames_height], None, 1)

        # So they have the same dimensions
        grid.turn_into_grid([self.path_modifying_point_alterable_fields_frame], None, None)
        grid.turn_into_grid([self.path_action_point_alterable_fields_frame], None, None)
        grid.turn_into_grid([self.required_point_alterable_fields_frame], None, None)

        self.path_action_point_alterable_fields_frame.hide()
        self.required_point_alterable_fields_frame.hide()
        self.path_modifying_point_alterable_fields_frame.show()

        self.toggle_frame_button.place(x=grid.left_edge, y=0, width=self.point_bar_length, height=self.toggle_frame_button_height)

        frame_name = self.points_altered_to_frame_name.get(self.current_points_altered_class)
        frame_button_color = self.points_altered_to_frame_button_color.get(self.current_points_altered_class)

        self.toggle_frame_button.configure(bg=frame_button_color, text=frame_name)

    def save_file_as(self):
        """Saves a new file with the contents of the GUI"""

        self.run_error_checking()

        if len(self.path_modifying_points) < 2:
            messagebox.showerror("ERROR", "There must be at least 2 path modifying points")
            return

        if not self.all_input_field_text_is_valid():
            return

        file = filedialog.asksaveasfile(mode='w', defaultextension=".json")

        if file is not None:
            create_file("swerve_input.txt")
            create_file("swerve_output.txt")

            self.previous_file_name = get_file_name(file)
            self.previous_file_path = file.name

            self.save_file(get_file_name(file), file)


    def quick_save_file(self):
        """ Saves the file 'quickly.' The user only has to hit Ctrl + s or hit the save file button and the previous file
            will be replaced with the new contents"""

        if self.previous_file_path is not None and self.previous_file_name != "":
            file = open(self.previous_file_path, "w")
            self.save_file(self.previous_file_name, file)

        else:
            messagebox.showerror("ERROR", "No file has been previous selected. Either Load a File or Save a File as, so "
                                          "I know where to save the files")

    def save_file(self, file_name, file):
        """Saves the file with the contents of the GUI"""

        create_file("swerve_input.txt")
        create_file("swerve_output.txt")

        self.run_error_checking()
        if self.all_input_field_text_is_valid():
            self._save_file(file_name, file)

    def _save_file(self, file_name, file):
        """Saves the file with the contents of the GUI"""

        if len(self.path_modifying_points) < 2:
            messagebox.showerror("ERROR", "There must be at least 2 path modifying points")
            return

        start_all_json_contents = {
            "Name": file_name,
            "Closed": self.path_is_closed_drop_down_menu.get_selected_item() == "Path Is Closed",
            "ClosedValue": self.path_is_closed_drop_down_menu.get_selected_item(),
            "InitialAngle": self.initial_angle_field.get_text(),
            "EndAngle": self.end_angle_field.get_text(),
            "InitialSpeed": self.initial_speed_field.get_text(),
            "offsetAngle": self.placement_angle_field.get_text()
        }

        initial_path_action_point, first_required_point, last_required_point = self.get_path_action_points_to_reflect_conditions()
        path_action_points = copy_list(self.path_action_points)
        path_action_points.append(initial_path_action_point)

        json_file_writer.write_positions_to_file()

        if len(points.path_action_points) <= 1:
            first_path_action_point_coordinates = get_closest_path_point(path_action_points[0].get_field_left_edge(),
                                                                         path_action_points[0].get_field_top_edge())

            left_edge, top_edge = json_file_writer.get_next_path_action_point_coordinates(first_path_action_point_coordinates)
            additional_path_action_point = PathActionPoint(None, None, False)

            additional_path_action_point.set_field_left_edge(left_edge)
            additional_path_action_point.set_field_top_edge(top_edge)
            additional_path_action_point.set_speed(path_action_points[0].get_speed())
            additional_path_action_point.set_command("none")
            additional_path_action_point.is_needed = False

            path_action_points.append(additional_path_action_point)


        placement_angle = float(self.placement_angle_field.get_text())
        json_file_writer.write_file(file, self.path_modifying_points,
                                    path_action_points, start_all_json_contents, first_required_point,
                                    last_required_point, placement_angle)

        first_required_point.destroy()
        last_required_point.destroy()
        initial_path_action_point.destroy()

        file.close()

    def get_path_action_points_to_reflect_conditions(self):
        """
            Returns:
                list[MovablePoint]: {initial_path_action_point, first_required_point, last_required_point}; The updated control points
                that reflect what was entered in the conditions tab + the first and last required point"""

        last_path_modifying_point = self.path_modifying_points[len(self.path_modifying_points) - 1]
        # The first point on the path must have a path modifying point, so the robot has the information to start the path
        initial_required_point = self.get_required_point_at_path_modifying_point(self.path_modifying_points[0], float(self.initial_angle_field.get_text()), 0)
        last_required_point = self.get_required_point_at_path_modifying_point(last_path_modifying_point, float(self.end_angle_field.get_text()), len(points.path_modifying_points) - 1)

        initial_path_action_point: PathActionPoint = self.get_path_action_point_point_at_path_modifying_point(self.path_modifying_points[0], 0)

        additional_path_action_points = [initial_path_action_point, initial_required_point, last_required_point]

        for path_action_point in additional_path_action_points:
            path_action_point.is_needed = False

        return [initial_path_action_point, initial_required_point, last_required_point]

    def get_required_point_at_path_modifying_point(self, path_modifying_point, angle, path_modifying_point_path_index):
        """
            Returns:
                PathActionPoint: a PathActionPoint that is at the same position of the 'path_modifying_point' provided"""

        # None of these numbers matter because this PathActionPoint won't be on the screen
        required_point = RequiredPoint(None, 0, is_on_screen=False)

        required_point.set_field_left_edge(path_modifying_point.get_field_left_edge())
        required_point.set_field_top_edge(path_modifying_point.get_field_top_edge())
        required_point.set_angle(angle)
        required_point.set_t_value(path_modifying_point_path_index)

        return required_point

    def get_path_action_point_point_at_path_modifying_point(self, path_modifying_point, path_modifying_point_path_index):
        """
            Returns:
                PathActionPoint: a PathActionPoint that is at the same position of the 'path_modifying_point' provided"""

        # None of these numbers matter because this PathActionPoint won't be on the screen
        path_action_point = PathActionPoint(None, 0, is_on_screen=False)

        path_action_point.set_field_left_edge(path_modifying_point.get_field_left_edge())
        path_action_point.set_field_top_edge(path_modifying_point.get_field_top_edge())
        path_action_point.set_t_value(path_modifying_point_path_index)
        path_action_point.set_command("none")
        path_action_point.set_speed(float(self.initial_speed_field.get_text()))

        return path_action_point

    def display_everything(self):
        """Allows the user to be able to interact with the GUI"""

        # Creating all the grids on the screen (the 'bars')
        self.create_bottom_bar()
        self.create_point_action_bar()
        self.create_point_alterable_fields_frames()
        self.create_switch_points_bar()
        self.create_initial_conditions_bar()

        # Creating the canvas that holds all the points and the field image
        canvas_length = SCREEN_LENGTH - self.point_bar_length
        canvas_height = SCREEN_HEIGHT - self.toolbar_height

        self.field_canvas = Canvas(master=WINDOW, width=canvas_length,
                                        height=canvas_height, bg=blue)

        self.draw_field_image()
        self.field_canvas.place(x=0, y=0)

    def draw_field_image(self, field_image=None):
        """Displays the current field image"""

        if field_image is not None and field_image == self.right_field_image:
            important_variables.CENTER_OF_FIELD_HORIZONTAL_OFFSET = 0

        elif field_image is not None:
            important_variables.CENTER_OF_FIELD_HORIZONTAL_OFFSET = FIELD_IMAGE_LENGTH * PIXELS_TO_METERS_MULTIPLIER  # pixels -> meters

        if field_image is not None and self.current_field_image != field_image:
            self.current_field_image = field_image

            for point in self.required_points + self.path_action_points + self.path_modifying_points:

                # Mirroring all the points along the y axis
                left_edge = point.get_field_left_edge() * -1
                point.set_field_left_edge(left_edge)

            for points_list in [self.path_modifying_points, self.path_action_points, self.required_points]:
                self.update_points(points_list)

        self.field_canvas.create_image(self.image_left_edge, self.image_top_edge, image=self.current_field_image)

    def create_initial_conditions_bar(self):
        """Creates the bar for the conditions"""

        grid = Grid([self.initial_conditions_tab_left_edge, self.toolbar_top_edge, self.initial_conditions_tab_length, self.toolbar_height], 1, None)
        grid.turn_into_grid(self.initial_and_end_condition_fields + [self.path_is_closed_drop_down_menu], None, None)

    def create_point(self, mouse_left_edge, mouse_top_edge):
        """Puts a new point onto the screen"""

        min_left_edge, min_top_edge, length, height = self.field_image_bounds
        max_left_edge = min_left_edge + length
        max_top_edge = min_top_edge + height

        is_within_horizontal_bounds = mouse_left_edge >= min_left_edge and mouse_left_edge <= max_left_edge
        is_within_vertical_bounds = mouse_top_edge >= min_top_edge and mouse_top_edge <= max_top_edge

        if is_within_horizontal_bounds and is_within_vertical_bounds:
            # Initializing the point
            point = self.current_points_altered_class(self.point_click_function, len(self.points_list) + 1)

            point_left_edge = mouse_left_edge - point.base_length / 2
            point_top_edge = mouse_top_edge - point.base_height / 2

            point.place(want_to_update_input_fields=True, x=point_left_edge, y=point_top_edge, width=point.base_length, height=point.base_height)

            self.points_list.append(point)
            point.set_order_position(len(self.points_list))
            self.add_needed_point_creation_information(point)
            self.point_alterable_fields_frame.update()
    def unselect_input_fields(self, selected_input_field=None):
        """Makes all the points except the 'selected_input_field' become unselected"""

        for input_field in self.points_input_fields:
            if selected_input_field is None:
                input_field.set_is_selected(False)

            # Meaning we can now check if the input_field is the same as the selected_input_field because the input_field
            # is not None
            elif input_field != selected_input_field:
                input_field.set_is_selected(False)

        for point in self.points_list:
            if selected_input_field is None:
                point.unselect()

            # Meaning we can now check if the input_field is the same as the selected_input_field because the input_field
            # is not None
            elif selected_input_field.belongs_to != point:
                point.unselect()

        self.selected_input_field = None

    def update_input_fields(self):
        """So when a point is either added or deleted all the fields are recalculated to reflect the points"""

        # So there are no more input fields; then all the input fields can be populated
        # Creating a new variable, so the names don't conflict with the function name
        points_input_fields = self.points_input_fields
        points_input_fields[:] = []

        for point in self.points_list:
            points_input_fields += point.get_input_fields()

    def handle_input_field_click(self, selected_input_field, want_error_checking=True):
        """Makes the input field become selected and the point that input field belongs to selected (all others are unselected)"""

        if want_error_checking:
            self.run_error_checking()

        selected_point = selected_input_field.belongs_to
        self.currently_selected_point_number = self.points_list.index(selected_point) + 1
        self.current_input_field_number = selected_point.get_input_fields().index(selected_input_field) + 1

        self.unselect_input_fields(selected_input_field)

        # Once all the input field's are unselected then make the 'selected_input_field' selected
        selected_input_field.set_is_selected(True)
        selected_input_field.get_belongs_to().select()
        self.selected_input_field = selected_input_field

    # Click Functions
    def swap_points_function(self):
        """Swaps the points"""

        # Indexes and the point numbers are of a difference of 1
        point_index = int(self.selected_point_field.get_text()) - 1
        new_index = int(self.switched_point_field.get_text()) - 1

        point_index_is_valid = point_index >= 0 and point_index < len(self.points_list)
        new_index_is_valid = new_index >= 0 and new_index < len(self.points_list)

        if point_index == new_index or not point_index_is_valid or not new_index_is_valid:
            messagebox.showerror("ERROR", f"Can not swap points when invalid point order numbers are inputted. Values must be between 1 and {len(self.points_list)}")

        else:
            # Swaps the 'backend' position of the points
            swap_list_items(self.points_list, point_index, new_index)
            self.point_alterable_fields_frame.update()

    def get_points_list(self, point):
        """
            Returns:
                MovablePoint[]: the points list that the point belongs to (PathModifyingPoint, PathActionPoint, etc.)"""

        point_type = type(point)

        return self.points_altered_to_point_list.get(point_type)

    def get_index_of_point(self, point, points_list):
        """
            Returns:
                int: the index of the point within the points list gotten from get_points_list()"""

        return points_list.index(point)

    def point_click_function(self, point):
        """ Runs different things depending on what point_editing_state the GUI is in when the point was clicked:
            ADD: Adds a point
            MOVING: Selects a point
            DELETION: Deletes a point
        """

        points_list = self.get_points_list(point)
        index_of_point = self.get_index_of_point(point, points_list)

        if self.point_editing_state == self.States.DELETION:
            self.delete_point(index_of_point, points_list)

        if self.point_editing_state == self.States.MOVING:
            self.selected_point = point
            self.selected_point.select()

    def set_button_colors(self):
        """Sets the colors of the add, move, delete buttons; called upon point_editing_state change"""

        for button in self.point_action_bar_buttons:
            button.configure(bg=pleasing_green)

        point_button = self.point_editing_state_to_point_button.get(self.point_editing_state)

        # If the point_editing_state is in INIT then there will be no point button causing an error
        if point_button is not None:
            point_button.configure(bg=dark_green)

    def run_mouse_click(self, event):
        """Creates a point if the point_editing_state is ADD and moves a point if the point_editing_state is MOVE and a point is selected"""

        mouse_left_edge, mouse_top_edge = get_mouse_position()

        if self.point_editing_state == self.States.ADD:
            self.create_point(mouse_left_edge, mouse_top_edge)

        if self.point_editing_state == self.States.MOVING and self.selected_point is not None:
            self.selected_point.place(True, x=mouse_left_edge, y=mouse_top_edge)
            self.selected_point.unselect()
            self.selected_point = None

    def all_input_field_text_is_valid(self):
        """
            Returns:
                bool: whether the text in the InputField's are valid"""

        if not WANT_ERROR_CHECKING:
            return True

        return self.get_error_message() is None

    def run_error_checking(self):
        """Runs the error checking for all the input fields"""

        error_message = self.get_error_message()

        if error_message is not None and WANT_ERROR_CHECKING:
            messagebox.showerror("ERROR", error_message)

            # raise ValueError("There was bad input! Stopping the program")

    def get_error_message(self):
        """
            Returns:
                str: the error message of the input field's if the data was invalid (None if it is valid)"""

        return_value = None

        for point in self.points_list:
            for input_field in point.get_input_fields():
                error_message = input_field.get_error_message()

                if error_message is not None:
                    return_value = error_message
                    input_field.get_error_message()
                    break

            if return_value is not None:
                break

        for input_field in self.initial_and_end_condition_fields:
            error_message = input_field.get_error_message()

            if error_message is not None and return_value is None:
                return_value = error_message
                break

        return return_value

    def update_points(self, points_list=None):
        """Updates the points, so they reflect what the input field's have"""

        self.run_error_checking()

        if not self.all_input_field_text_is_valid():
            return

        if len(points.path_points) == 0:
            messagebox.showerror("ERROR", "Make sure you have drawn the path before trying to update the points")
            return

        path_modifying_point_path_indexes = get_path_modifying_point_path_indexes()
        update_path_action_and_required_point_location(points.path_action_points, points.required_points,
                                                       path_modifying_point_path_indexes, points.path_modifying_points)

        points_list = self.points_list if points_list is None else points_list

        for point in points_list:
            point.default_update_coordinates()

    def reset_point_input_fields(self, points):
        """Changes the input fields, so they reflect the points position on the screen"""

        for point in points:
            point.update_input_fields()

    def reset_all_point_input_fields(self):
        """Changes all the point input fields, so they reflect the points position on the screen"""

        self.reset_point_input_fields(self.path_action_points)
        self.reset_point_input_fields(self.path_modifying_points)
        self.reset_point_input_fields(self.required_points)

        self.reset_point_input_fields(self.path_action_points)
        self.reset_point_input_fields(self.path_modifying_points)
        self.reset_point_input_fields(self.required_points)

    def clear_field(self):
        """Clears the entire field of points and the path"""

        for point in self.path_action_points + self.path_modifying_points + self.required_points:
            point.destroy()

        # So they don't reassigned to a new spot in memory messing up the pointer the frames have to the lists
        self.path_action_points[:] = []
        self.path_modifying_points[:] = []
        self.required_points[:] = []

        self.field_canvas.delete("all")
        self.draw_field_image()

        # Updates the frames, so they contain the points data
        self.path_action_point_alterable_fields_frame.update()
        self.path_modifying_point_alterable_fields_frame.update()

    def change_point_order(self, is_up):
        """Moves the order of the currently selected point (1 -> 2)"""

        if self.selected_input_field is not None:
            point = self.selected_input_field.get_belongs_to()
            point_index, new_index = self.get_point_indexes(point, is_up)

            # Swaps the 'backend' position of the points
            swap_list_items(self.points_list, point_index, new_index)
            self.point_alterable_fields_frame.update()

    def get_point_indexes(self, selected_point, is_up):
        """
            Returns:
                 int: the new index of the point"""

        point_index = selected_point.get_order_position() - 1

        next_index = get_next_index(len(self.points_list) - 1, point_index)
        previous_index = get_previous_index(len(self.points_list) - 1, point_index)
        new_index = next_index if is_up else previous_index

        return [point_index, new_index]

    def draw_path(self):
        """Writes the data to the file, which calls AutoFollower.jar then it draws the points from AutoFollower.jar"""

        self.run_error_checking()

        if len(self.path_modifying_points) < 2:
            messagebox.showerror("ERROR", "There must be at least 2 path modifying points")
            return

        if self.all_input_field_text_is_valid():
            create_file("swerve_input.txt")
            create_file("swerve_output.txt")

            # So all the lines are deleted and the image is still on the canvas
            self.field_canvas.delete("all")
            self.draw_field_image()
            json_file_writer.write_positions_to_file()
            self.update_point_information()

            draw_path_lines(self.field_canvas, self.path_modifying_point_line_width, self.path_line_width)
            self.draw_robot_angle_lines()

            self.update_points()

    def update_point_information(self):
        """Updates all the point information, so drawing the path lines will work correctly"""

        unused, first_required_point, last_required_point = self.get_path_action_points_to_reflect_conditions()
        path_action_points = [first_required_point] + points.path_action_points + [last_required_point]
        required_points = [first_required_point] + self.required_points + [last_required_point]

        update_path_modifying_point_information(path_action_points=path_action_points, required_points=required_points)
        first_required_point.destroy()
        last_required_point.destroy()

    def draw_robot_angle_lines(self):
        """Draws the robot angle at each control point"""

        for path_modifying_point in self.path_modifying_points:
            angle = path_modifying_point.get_angle_at_point()
            point2_left_edge = path_modifying_point.get_left_edge() + math.cos(angle) * ROBOT_ANGLE_LINE_LENGTH

            y_distance = math.sin(angle) * ROBOT_ANGLE_LINE_LENGTH
            point2_top_edge = path_modifying_point.get_top_edge() - y_distance

            self.field_canvas.create_line([path_modifying_point.get_left_edge(), path_modifying_point.get_top_edge()], [point2_left_edge, point2_top_edge],
                                          fill=ROBOT_ANGLE_LINE_COLOR, width=ROBOT_ANGLE_LINE_WIDTH)

    # Loading in from files
    def request_load_file(self):
        """Loads a file onto the GUI"""

        file = filedialog.askopenfile(mode='r')

        if file is not None:
            self.load_file(file)

    def load_file(self, file):
        """Loads the file onto the GUI"""

        json_contents = json.load(file)
        self.previous_file_path = file.name
        self.previous_file_name = get_file_name(file)

        file.close()

        # Setting the text field information to reflect the file
        self.placement_angle_field.set_text(json_contents["offsetAngle"])
        self.initial_speed_field.set_text(json_contents["InitialSpeed"])
        self.end_angle_field.set_text(json_contents["EndAngle"])
        self.initial_angle_field.set_text(json_contents["InitialAngle"])
        self.path_is_closed_drop_down_menu.set_selected_item(json_contents["ClosedValue"])

        # Updating the points to reflect the file
        self.update_points_to_reflect_loaded_file(json_contents)
        self.add_needed_point_creation_information_for_all_points()

    def add_needed_point_creation_information_for_all_points(self):
        """ Adds all the information the other parts of the code need for a point to be created for all the points (
            for each point it calls add_needed_point_creation_information())"""

        for point in self.path_modifying_points + self.path_action_points:
            self.add_needed_point_creation_information(point)

        self.path_action_point_alterable_fields_frame.update()
        self.path_modifying_point_alterable_fields_frame.update()

    def add_needed_point_creation_information(self, point):
        """Adds all the information the other parts of the code need for a point to be created"""

        point.set_input_fields_command(self.handle_input_field_click)
        self.update_input_fields()

    def update_points_to_reflect_loaded_file(self, json_contents):
        """So the GUI reflects what is in the file (has to be delayed because it takes a while for the GUI to update and load the file)"""

        self.clear_field()

        json_file_loader.set_all_points_to_reflect_json_file(self.path_modifying_points, self.path_action_points,
                                                             self.required_points, json_contents, self.point_click_function)

        # So the points change location based on what is in the input fields
        self.update_points(self.path_action_points)
        self.update_points(self.path_modifying_points)
        self.update_points(self.required_points)

        # Otherwise the frame information does not update correctly
        self.toggle_points_alterable_fields_frame()
        self.toggle_points_alterable_fields_frame()
        self.toggle_points_alterable_fields_frame()

    def change_input_field_selection(self, event):
        """Changes the selected input field depending on what key was pressed

            Args:
                event (str): the event name. Here are all the possible values:
                'Up' -> Selects the next input field above the current one (belongs to the previous way point)
                'Down' -> Selects the next input field below the current one (belongs to the next way point)
                'Left' -> Selects the next input field to the right of the current one (belongs to the current way point)
                'Right' -> Selects the previous input field to the left the current one (belongs to the current way point)
            
            
            Returns:
                None
        """

        self.run_error_checking()

        if not self.all_input_field_text_is_valid():
            return

        if self.currently_selected_point_number > len(self.points_list) or self.currently_selected_point_number < 1:
            messagebox.showerror("ERROR", "Cannot Switch input fields because they do not exist!!!")
            return

        valid_event_types = ["Up", "Down", "Left", "Right", "Beginning", "End"]

        if not valid_event_types.__contains__(event):
            raise ValueError("Valid Data was not inputted!!!")

        user_modifiable_fields = self.get_user_modifiable_fields(self.currently_selected_point_number)
        # Modifying the numbers, so the selected input_field is not out of bounds of the input_fields on the screen
        max_input_field_number = len(user_modifiable_fields)

        if event == "Up":
            self.currently_selected_point_number -= 1

        if event == "Down":
            self.currently_selected_point_number += 1

        if event == "Left":
            self.current_input_field_number -= 1

        if event == "Right":
            self.current_input_field_number += 1

        if event == "Beginning":
            self.current_input_field_number = 1

        if event == "End":
            self.current_input_field_number = max_input_field_number

        if self.current_input_field_number > max_input_field_number:
            self.current_input_field_number = 1
            self.currently_selected_point_number += 1

        if self.current_input_field_number <= 0:
            self.current_input_field_number = max_input_field_number
            self.currently_selected_point_number -= 1

        self.make_input_field_selection_valid()
    def make_input_field_selection_valid(self):
        """Makes sure where the GUI thinks the next input field selection is valid"""

        # Making sure the currently selected points are cyclic 0 -> max_index -> 0 -> etc.
        max_selected_point_number = len(self.points_list)

        if self.currently_selected_point_number > max_selected_point_number:
            self.currently_selected_point_number = 1

        if self.currently_selected_point_number <= 0:
            self.currently_selected_point_number = max_selected_point_number

        self.focus_on_input_field(self.currently_selected_point_number, self.current_input_field_number)

    def add_all_key_binding_shortcuts(self):
        """Adds all the key binding shortcuts to the Auto GUI"""

        key_binding_to_function = {}

        key_binding_to_function["<Control-a>"] = lambda event: self.toggle_points_alterable_fields_frame(PathModifyingPoint)
        key_binding_to_function["<Control-c>"] = lambda event: self.copy_point()
        key_binding_to_function["<Control-d>"] = lambda event: self.toggle_points_alterable_fields_frame(RequiredPoint)
        key_binding_to_function["<KeyPress-d>"] = lambda event: self.draw_path()
        key_binding_to_function["<KeyPress-e>"] = lambda event: self.change_point_editing_state(self.States.MOVING,
                                                                                  self.States.MOVING)
        key_binding_to_function["<KeyPress-f>"] = lambda event: self.save_file_as()
        key_binding_to_function["<KeyPress-g>"] = lambda event: self.request_load_file()

        key_binding_to_function["<KeyPress-h>"] = lambda event: self.change_input_field_selection("Left")
        key_binding_to_function["<KeyPress-i>"] = lambda event: self.change_input_field_selection("Beginning")
        key_binding_to_function["<KeyPress-j>"] = lambda event: self.change_input_field_selection("Down")
        key_binding_to_function["<KeyPress-k>"] = lambda event: self.change_input_field_selection("Up")
        key_binding_to_function["<Control-l>"] = lambda event: self.request_load_file()
        key_binding_to_function["<KeyPress-l>"] = lambda event: self.change_input_field_selection("Right")
        key_binding_to_function["<KeyPress-o>"] = lambda event: self.change_input_field_selection("End")
        key_binding_to_function["<KeyPress-q>"] = lambda event: self.change_point_editing_state(self.States.ADD,
                                                                                   self.States.ADD)
        key_binding_to_function["<KeyPress-r>"] = lambda event: self.reset_all_point_input_fields()
        key_binding_to_function["<KeyPress-s>"] = lambda event: self.quick_save_file()
        key_binding_to_function["<Control-s>"] = lambda event: self.toggle_points_alterable_fields_frame(PathActionPoint)
        key_binding_to_function["<Control-v>"] = lambda event: self.paste_point()
        key_binding_to_function["<KeyPress-u>"] = lambda event: self.clear_field()
        key_binding_to_function["<KeyPress-w>"] = lambda event: self.change_point_editing_state(self.States.DELETION,
                                                                                               self.States.DELETION)
        key_binding_to_function["<KeyPress-z>"] = lambda event: self.swap_points_function()

        key_binding_to_function["<KeyPress-Return>"] = lambda event: self.update_points(self.points_list)
        key_binding_to_function["<Control-space>"] = lambda event: self.toggle_points_alterable_fields_frame()
        key_binding_to_function["<Control-BackSpace>"] = lambda event: self.delete_point()
        key_binding_to_function["<KeyPress-Up>"] = lambda event: self.change_point_order(False)
        key_binding_to_function["<KeyPress-Down>"] = lambda event: self.change_point_order(True)

        key_binding_to_function["<KeyPress-Tab>"] = lambda event: self.change_input_field_selection("Right")

        for key_binding in key_binding_to_function.keys():
            WINDOW.bind(key_binding, key_binding_to_function.get(key_binding))

            # Finding the event_key_binding because the event_key_binding has different information than the key_binding.
            # For instance, key_binding is '<KeyPress-u>' while event_key_binding is 'u'
            first_dash_index = key_binding.index("-")
            event_key_binding = key_binding[first_dash_index + 1:]
            event_key_binding = event_key_binding[:-1] # The last character of the string is '>' which is not needed

            important_variables.all_key_bindings.append(event_key_binding)

    def focus_on_input_field(self, point_number, input_field_number):
        """Moves the mouse to the input field and the desired location"""

        user_modifiable_field = self.get_user_modifiable_fields(point_number)[input_field_number - 1]

        user_modifiable_field.focus_force()
        self.handle_input_field_click(user_modifiable_field, want_error_checking=False)

    def get_user_modifiable_fields(self, point_number):
        """
            Returns:
                list[object] the fields the user can modify for that point number (in the PointAlterableFieldsFrame)"""

        point_index = point_number - 1
        point: MovablePoint = self.points_list[point_index]

        user_modifiable_fields = point.get_input_fields()

        return user_modifiable_fields

    def copy_point(self):
        """Copies the currently selected point into the 'clipboard'"""

        point_index = self.currently_selected_point_number - 1
        self.copied_point = self.points_list[point_index]

    def paste_point(self):
        """Pastes the copied_point into the GUI"""

        new_point = self.current_points_altered_class(self.point_click_function,
                                                      self.currently_selected_point_number + 1)

        if self.copied_point is not None:
            # Making the input fields alike
            copied_point_input_fields = self.copied_point.get_input_fields()
            new_point_input_fields = new_point.get_input_fields()

            for x in range(len(copied_point_input_fields)):
                copied_point_input_field = copied_point_input_fields[x]
                new_point_input_field = new_point_input_fields[x]

                new_point_input_field.set_text(copied_point_input_field.get_text())

        # Update the GUI
        self.points_list.insert(self.currently_selected_point_number, new_point)
        self.add_needed_point_creation_information(new_point)
        self.point_alterable_fields_frame.update()
        self.change_input_field_selection("Down")
        new_point.place(True, x=self.copied_point.get_left_edge(), y=self.copied_point.get_top_edge())

    def delete_point(self, index_of_point=None, points_list=None):
        """Deletes the currently selected point"""

        deletion_is_valid = True

        if index_of_point is None:
            index_of_point = self.currently_selected_point_number - 1

            # It is possible to hit the keyboard shortcut and not be able to delete validly
            index_is_valid = index_of_point >= 0 and index_of_point < len(self.points_list) and len(self.points_list) >= 0

            deletion_is_valid = index_is_valid and self.selected_input_field is not None

        if points_list is None:
            points_list = self.points_list

        if deletion_is_valid:
            point = points_list[index_of_point]
            del points_list[index_of_point]
            self.path_action_point_alterable_fields_frame.update()
            self.path_modifying_point_alterable_fields_frame.update()
            self.required_point_alterable_fields_frame.update()
            point.destroy()

            self.update_input_fields()

        # Makes sure we have a input field selected
        if deletion_is_valid and len(self.points_list) >= 1:
            self.make_input_field_selection_valid()

    @property
    def points_list(self):
        """The current points being modified that belong to the PointAlterableFieldsFrame"""
        
        return self.points_altered_to_point_list.get(self.current_points_altered_class)

    @property
    def point_alterable_fields_frame(self):
        """The current PointAlterableFieldsFrame that is on the screen"""
        
        return self.points_altered_to_point_alterable_fields_frame.get(self.current_points_altered_class)

    @property
    def points_input_fields(self):
        """The points input fields that are currently on the screen that belong to the PointAlterableFieldsFrame"""
        
        return self.points_altered_to_points_input_fields.get(self.current_points_altered_class)

    @property
    def current_point_list(self):
        """The points list that is currently in use"""
        
        # First number in Point states signifies if it is the path modifying points list being modified
        return self.points_altered_to_point_list.get(self.current_points_altered_class)
