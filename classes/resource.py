import re, json, inspect
from .fields import Field, TagField
from .functions import AwsNoValue, Ref, GetAtt
from .utils import snake_to_camel


class Resource:

    GetAtt_attributes = []
    cloudformation_type = ""
    exclude_null=False

    def __init__(self, name:str, include_tags:bool=True, depends_on=[], **tags):
        # ensure that the name matches the name regex
        PATTERN_STRING = "^[a-zA-Z]{1}[a-zA-Z0-9]+$"
        NAME_PATTERN = re.compile(PATTERN_STRING)
        if not NAME_PATTERN.match(name):
            raise ValueError(f"The resource's name must match the expression `{PATTERN_STRING}`")
        self.name = name

        # set the tags
        if include_tags:
            self.tags = TagField(**tags)
    
    def __call__(self, attr:str=None):
        """
        Return a 'Ref' or 'GetAtt' object
        """
        if attr is None:
            # Looking for a Ref object
            return Ref(self)
        
        else:
            if attr not in self.GetAtt_attributes:
                raise ValueError(f"Parameter `attr` must be in {self.__class__.__name__}.GetAtt_attributes")
            return GetAtt(self, attr)

    def __setattr__(self, name, value):
        current_value = getattr(self, name, None)

        # If the current value of the changing variable is a Field object,
        # change the field's value instead of the attribute
        if isinstance(current_value, Field):
            try:
                self.__dict__[name].value = value
            except KeyError:
                self.__dict__[name] = self.__class__.__dict__[name]
                self.__dict__[name].value = value
        else:
            super().__setattr__(name, value)

    @property
    def fields(self):
        # Get all variables in the instance that are of type 'fields.Field'
        _func_name = inspect.stack()[0][3]
        fields = {snake_to_camel(attr): getattr(self, attr).value for attr in dir(self) if attr != _func_name and isinstance(getattr(self, attr), Field)}

        new_fields = {}
        # Convert the 'None' field values to {"Ref": "AWS::NoValue"}
        for key, value in fields.items():
            if value is None:
                fields[key] = AwsNoValue.value
            
            if not self.exclude_null:
                new_fields[key] = value
        
        return new_fields
    
    def to_cf_json(self):
        return {
            self.name: {
                "Type": self.cloudformation_type,
                "Properties": self.fields
            }
        }



class CompoundResource(Resource):

    nested_resources = []

    def __call__(self):
        return NotImplementedError()

    def to_cf_json(self):
        result = {}
        for res in self.nested_resources:
            result.update(res.to_cf_json())
        return result

class ConfigurationError(Exception):
    pass

