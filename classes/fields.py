import json
import re

from .functions import Ref, GetAtt

class FieldValueError(ValueError):
    pass
class NullValueError(ValueError):
    pass

class Field:
    _set_value = False

    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)


    @property
    def value(self):
        return NotImplementedError()
    
    @value.setter
    def value(self, x):
        return NotImplementedError()
    
class StringField(Field):
    """

    Notes:
        - The '_set_value' is used to determine if the value.setter logic has been run.
          If that logic has not been run, then it must be in the value.getter before the value
          can be properly used.
    """
    DEFAULT = default = ""
    REGEX = regex = r".*"
    REQUIRED = required = False
    choices = []

    def __init__(self, default:str=DEFAULT, regex:str=REGEX, required:bool=REQUIRED, choices:list=[]):
        self.default = default
        self.regex = regex
        self.required = required
        self.choices = choices

        self.__value = self.default
    
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return f"{self.__class__.__name__}(value='{self.value}', required={self.required}, choices={self.choices})"
    
    @property
    def value(self):
        if not self._set_value:
            self.value = self.default
        return self.__value
    
    @value.setter
    def value(self, x):
        if x is None:
            # if the field is required, None is not a valid option
            if self.required:
                raise ValueError("Field cannot be None")
            # otherwise set x to the default
            x = self.default

        # If the value does not match the expression, raise an error
        if (self.regex != self.REGEX) and (not re.match(self.regex, x)):
            raise FieldValueError(f"Field value must match regex `{self.regex}`")
        # If there are choices, assert that the value is in the choices
        if (self.choices != []) and (x not in self.choices):
            raise ValueError(f"Value must be one of the following: `{self.choices}`. Value assigned: `{x}`")

        # Set the value
        self._set_value = True
        self.__value = x


class BooleanField(Field):
    DEFAULT = default = False
    REQUIRED = required = False

    def __init__(self, default:bool=DEFAULT, required:bool=REQUIRED):
        self.default = default
        self.required = required
        
        self.__value = None if self.required else self.default
        self._set_value = False if self.required else True
    
    @property
    def value(self):
        if not self._set_value:
            raise ValueError("Must set the field value before attempting to access it")
        return self.__value
    
    @value.setter
    def value(self, x):
        if not isinstance(x, bool):
            raise TypeError(f"Field value must be a boolean")
        elif (x is None) and (self.required):
            raise NullValueError("Field is required, value cannot be null")

        self._set_value = True
        self.__value = x


class TagField(Field):
    DEFAULT = default = {}
    REQUIRED = required = False

    def __init__(self, **tags):
        self.value = tags
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, x:dict):
        if not isinstance(x, dict):
            raise TypeError("Tags value must be of type `dict`")

        self.__value = self.format_tags(x)
    
    @staticmethod
    def format_tags(tags:dict):
        o = []
        for key, value in tags.items():
            o.append({"Key": key, "Value": value})
        return o

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(**{str(self.value)})"



class RefField(Field):
    REQUIRED=required=False

    def __init__(self, obj_type, required:bool=REQUIRED):
        self.obj_type = obj_type
        self.required = required

        self._set_value = False
        self.__value = None
    
    @property
    def value(self):
        if not self._set_value:
            raise ValueError("Field must be assigned before value can be accessed")
        return self.__value
    
    @value.setter
    def value(self, ref):
        # check if we are setting an object to None
        if ref is None:
            if self.required:
                raise ValueError("Field value cannot be 'None'")
            self._set_value = True
            self.__value = ref
            return

        referenced_object = ref.obj

        # Check that the 'ref' is a Ref object
        if not isinstance(ref, Ref):
            raise TypeError("Value must be a `Ref` object")

        # Check that x is an instance of the required object
        if not isinstance(referenced_object, self.obj_type):
            raise TypeError(f"Value must of type `{self.obj_type.__class__.__name__}`")

        self._set_value = True
        self.__value = ref.value


