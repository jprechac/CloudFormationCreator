import json
from . import fields, resource

class VPC(resource.Resource):

    # Write out the fields that we could need
    cidr_block = fields.StringField(regex=r"(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?", required=True)
    enable_dns_hostnames = fields.BooleanField(default=False, required=False)
    enable_dns_support = fields.BooleanField(default=False, required=False)
    instance_tenancy = fields.StringField(required=False, choices=["dedicated", "default", "host"])

    def __init__(self, name:str, cidr_block:str=None, enable_dns_hostnames:bool=None, enable_dns_support:bool=None, instance_tenancy:str=None, **kwargs):
        super().__init__(name, **kwargs)

        # instantiate the fields
        self.cidr_block.value = cidr_block
        self.enable_dns_hostnames.value = enable_dns_hostnames
        self.enable_dns_support = enable_dns_support
        self.instance_tenancy.value = instance_tenancy


    def to_dict(self):
        pass

    



