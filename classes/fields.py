import json
import re

class FieldValueError(ValueError):
    pass
class NullValueError(ValueError):
    pass

class Field:
    @property
    def value(self):
        return NotImplementedError()
    
    @value.setter
    def value(self, x):
        return NotImplementedError()

class StringField(Field):
    DEFAULT = default = ""
    REGEX = regex = r"^*&"
    REQUIRED = required = False
    choices = []

    def __init__(self, default:str=DEFAULT, regex:str=REGEX, required:bool=REQUIRED, choices:list=[]):
        self.default = default
        self.regex = regex
        self.required = required
        self.choices = choices

        self.value = self.default
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, x):
        if x is None and self.required:
            raise ValueError("Field cannot be None")
        # If the value does not match the expression, raise an error
        if not re.match(self.regex, x):
            raise FieldValueError(f"Field value must match regex `{self.regex.pattern}`")
        # If there are choices, assert that the value is in the choices
        if (self.choices != []) and (x not in self.choices):
            raise ValueError(f"Value must be one of the following: `{self.choices}`")

        # Set the value
        self.__value = x


class BooleanField(Field):
    DEFAULT = default = False
    REQUIRED = required = False

    def __init__(self, default:bool=DEFAULT, required:bool=REQUIRED):
        self.__value = None
        self.required = required
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, x):
        if not isinstance(x, bool):
            raise TypeError(f"Field value must be a boolean")
        elif (x is None) and (self.required):
            raise NullValueError("Field is required, value cannot be null")
        else:
            self.__value = x



