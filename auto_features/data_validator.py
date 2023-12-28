import re


class DataValidator:
    """A class that gives validation functions"""

    validation_function = None

    @staticmethod
    def get_float_error_message_function(min_value, max_value, contains_acceptable_value_error_message_function=lambda text: None):
        """Sets the validation type wanted to a float"""

        return lambda text: DataValidator.get_number_error_message(float, text, min_value, max_value,
                                                         contains_acceptable_value_error_message_function)

    @staticmethod
    def get_number_error_message(type_wanted, text, min_value, max_value, contains_acceptable_value_error_message_function):
        """
            Returns:
                str: the error message if the float is not valid (None if it is valid)"""

        return_value = None

        # Going step by step to see if the data is valid (None means it is valid). If the data is valid after sequential
        # if statements, then it moves on to the next to make sure it passes the test
        if len(text) != 0 and not DataValidator.is_correct_type(type_wanted, text):
            DataValidator.is_correct_type(type_wanted, text)
            return_value = f"Expected type float, but did not get that type"

        if return_value is None:
            return_value = DataValidator.get_is_within_range_error_message(float(text), min_value, max_value)

        if return_value is None:
            return_value = contains_acceptable_value_error_message_function(text)

        return return_value

    @staticmethod
    def get_int_error_message_function(min_value, max_value, contains_acceptable_value_error_message_function=lambda: None):
        """
            Returns:
                str: the error message if the float is not valid (None if it is valid)"""

        return lambda text: DataValidator.get_number_error_message(int, text, min_value, max_value,
                                                                   contains_acceptable_value_error_message_function)

    @staticmethod
    def get_is_within_range_error_message(value, min_value, max_value):
        """
            Returns:
                str: the error message if the 'value' is not between 'min_value' and 'max_value'
                (None if the 'value' is between 'min_value' and 'max_value')"""

        return_value = None

        if value < min_value:
            return_value = f"The value {value} is smaller than the minimum value of {min_value}"

        if value > max_value:
            return_value = f"The value {value} is larger than the maximum value {max_value}"

        return return_value

    @staticmethod
    def is_correct_type(expected_type, value: str):
        """
            Returns:
                bool: if the value is the expected type"""

        return_value = True

        # If the value has a negative number, it will remove that because that messes with str.isnumeric()
        if len(value) != 0 and value[0] == "-":
            value = value[1:]

        values_list = value.split(".")

        all_values_are_numeric = True

        for current_value in values_list:
            if not current_value.isnumeric():
                all_values_are_numeric = False

        if expected_type == int:
            return_value = all_values_are_numeric and len(values_list) == 1

        if expected_type == float:
            values_list_length_is_valid = len(values_list) == 1 or len(values_list) == 2
            return_value = all_values_are_numeric and values_list_length_is_valid

        return return_value

