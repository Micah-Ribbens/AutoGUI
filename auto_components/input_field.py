import tkinter
import inspect
from tkinter import messagebox

from miscellaneous.important_variables import *
from miscellaneous import important_variables


class InputField(Entry):
    """ Extends tkinter's class Entry. It adds the functionality of more easily setting the text, adding default text, and
        only allowing editing when the InputField is editable"""

    is_selected = False
    belongs_to = None
    is_editable = True
    command = None
    string_variable = None
    previous_text = ""
    error_message_function = None

    most_recent_key_press = None
    most_recent_key_press_was_valid = True

    def __init__(self, window_type, font, default_text, is_editable=True, text_color=black, background_color=white,
                 error_message_function=lambda text: None, name=""):

        """Initializes the object"""

        self.error_message_function = error_message_function

        self.string_variable = tkinter.StringVar()
        self.string_variable.trace("w", self.validate)

        super().__init__(window_type, font=font, fg=text_color, bg=background_color,
                         disabledbackground=background_color, disabledforeground=text_color, textvariable=self.string_variable)

        self.set_text(default_text) # Puts this text at the start of the Input Field (Default Text)

        self.is_editable = is_editable

        self.bind("<Key>", self.on_key_press)

    def set_text(self, text):
        """Sets the text of the InputField to the value provided if the InputField is editable"""

        self.delete(0, "end")
        self.insert(0, text)
        self.previous_text = str(text)

    def get_text(self):
        return self.get()

    def set_is_selected(self, is_selected):
        self.is_selected = is_selected

    def get_is_selected(self):
        """
            Returns:
                boolean: if the input field is selected"""

        return self.is_selected

    def set_command(self, command):
        """Sets the function that is called when the input field is clicked"""

        self.bind("<1>", lambda event: self.call_command())
        self.command = command

    def call_command(self):
        """Calls the command 'self.command'"""

        self.command(self)

    def set_belongs_to(self, belongs_to):
        """Sets the MovablePoint (like PathModifyingPoint) the InputField is belongs to"""

        self.belongs_to = belongs_to

    def get_belongs_to(self):
        """
            Returns:
                MovablePoint: the MovablePoint (like PathModifyingPoint) the InputField belongs to"""

        return self.belongs_to

    def focus_force(self) -> None:
        """Adds functionality to tkinter's build in focus_force() method; it not only moves the mouse to the InputField,
            but it also selects all the text in the InputField"""

        super().focus_force()
        super().select_range(0, len(self.get_text()))

    def stop_focusing(self):
        """Forces the robot to stop focusing"""

        super().select_range(0, 0)

    def validate(self, *args):
        #  If the text_is_valid we accept the incoming change otherwise we do not
        if self.most_recent_key_press_was_valid:
            self.previous_text = self.get_text()

        else:
            self.set_text(self.previous_text)

    def on_key_press(self, event):
        """Runs what should happen when a key is pressed"""

        self.want_error_validation = False
        self.most_recent_key_press = event.keysym

        # There are key bindings that should not trigger the InputField getting text in it. For instance, if one keyboard
        # shortcut was 'd' then typing 'd' should only do the shortcut, not put text in the InputField
        key_press_was_a_key_binding = important_variables.all_key_bindings.__contains__(self.most_recent_key_press)

        if self.most_recent_key_press == "BackSpace" or self.most_recent_key_press == "Delete":
            self.most_recent_key_press_was_valid = self.is_editable

        else:
            self.most_recent_key_press_was_valid = not key_press_was_a_key_binding and self.is_editable

    def get_error_message(self):
        """
            Returns:
                str: the error message if the data is invalid"""

        # For some unknown reason this just does not work
        return self.error_message_function(self.get_text())

