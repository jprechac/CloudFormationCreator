import json
from classes import fields
from classes.functions import Ref
from classes.resource import Resource, ConfigurationError

CIDR_BLOCK_REGEX = r"(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?"

class Vpc(Resource):

    cloudformation_type = "AWS::EC2::VPC"

    # Write out the fields that we could need
    cidr_block = fields.StringField(default="10.0.0.0/16",regex=CIDR_BLOCK_REGEX, required=True)
    enable_dns_hostnames = fields.BooleanField(default=False, required=False)
    enable_dns_support = fields.BooleanField(default=False, required=False)
    instance_tenancy = fields.StringField(default="default", required=False, choices=["dedicated", "default", "host"])

    # GetAtt attributes
    GetAtt_attributes = ["CidrBlock", "CidrBlockAssociations", "DefaultNetworkAcl", "DefaultSecurityGroup", "Ipv6CidrBlocks"]

    def __init__(self, name:str, cidr_block:str=None, enable_dns_hostnames:bool=None, enable_dns_support:bool=None, instance_tenancy:str=None, **kwargs):
        super().__init__(name, **kwargs)

        # instantiate the fields
        self.cidr_block = cidr_block
        self.enable_dns_hostnames = enable_dns_hostnames
        self.enable_dns_support = enable_dns_support
        self.instance_tenancy = instance_tenancy

class Subnet(Resource):

    cloudformation_type = "AWS::EC2::Subnet"
    exclude_null=True

    # Fields
    assign_ipv6_address_on_creation = fields.BooleanField(default=False, required=False)
    availability_zone = fields.StringField(required=True)    
    cidr_block = fields.StringField(regex=CIDR_BLOCK_REGEX, required=True)
    ipv6_cidr_block = fields.StringField(default=None, required=False)
    map_public_ip_on_launch = fields.BooleanField(default=False, required=False)
    outpost_arn = fields.StringField(default=None, required=False)
    vpc_id = fields.RefField(Vpc, required=True)

    GetAtt_attributes = []

    def __init__(
        self,
        name:str,
        assign_ipv6_address_on_creation:bool=assign_ipv6_address_on_creation.default,
        availability_zone:str=None,
        cidr_block:str=None,
        ipv6_cidr_block:str=ipv6_cidr_block.default,
        map_public_ip_on_launch:bool=map_public_ip_on_launch.default,
        outpost_arn:str=None,
        vpc_id:Ref=None,
        **tags
    ):
        super().__init__(name, **tags)

        # assign the fields
        self.assign_ipv6_address_on_creation = assign_ipv6_address_on_creation
        self.availability_zone = availability_zone
        self.cidr_block = cidr_block
        self.ipv6_cidr_block = ipv6_cidr_block
        self.map_public_ip_on_launch = map_public_ip_on_launch
        self.outpost_arn = outpost_arn
        self.vpc_id = vpc_id


class RouteTable(Resource):
    pass

class RouteTableAssociation(Resource):
    pass


class InternetGateway(Resource):

    cloudformation_type = "AWS::EC2::InternetGateway"

    def __init__(self, name:str, **tags):
        super().__init__(name, **tags)


class VpnGateway(Resource):
    pass


class VpcGatewayAttachment(Resource):

    cloudformation_type = "AWS::EC2::VPCGatewayAttachment"

    # Fields
    internet_gateway_id = fields.RefField(InternetGateway, required=False)
    vpc_id = fields.RefField(Vpc, required=True)
    vpn_gateway_id = fields.RefField(VpnGateway, required=False)

    def __init__(
        self,
        name:str,
        internet_gateway_id:Ref=None,
        vpc_id:Ref=None,
        vpn_gateway_id:Ref=None
    ):
        super().__init__(name, include_tags=False)

        # Cannot have both IG and Vpn
        if not (bool(internet_gateway_id) != bool(vpn_gateway_id)):
            raise ConfigurationError("Can only assign InternetGateway -or- VpnGateway")

        self.internet_gateway_id = internet_gateway_id
        self.vpc_id = vpc_id
        self.vpn_gateway_id = vpn_gateway_id


class NatGateway(Resource):
    pass



