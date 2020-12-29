import re, json
from .fields import Field


class Resource:
    def __init__(self, name:str, **kwargs):
        # ensure that the name matches the name regex
        PATTERN_STRING = "^[a-zA-Z]{1}[a-zA-Z0-9]+$"
        NAME_PATTERN = re.compile(PATTERN_STRING)
        if not NAME_PATTERN.match(name):
            raise ValueError(f"The resource's name must match the expression `{PATTERN_STRING}`")
        self.name = name

        # set the tags
        self.tags = kwargs

    @property
    def fields(self):
        # Get all variables in the instance that are of type 'fields.Field'
        pass
