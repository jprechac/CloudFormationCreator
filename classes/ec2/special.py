from .base import Vpc, InternetGateway, VpcGatewayAttachment # pylint: disable=relative-beyond-top-level
from classes.resource import CompoundResource

class VpcWithInternet(CompoundResource):
    
    def __init__(self, vpc_name:str, cidr_block:str=None, enable_dns_hostnames:bool=None, enable_dns_support:bool=None, instance_tenancy:str=None, **tags):
        # generate a VPC, internet gateway, and gateway attachment

        self.vpc = Vpc(vpc_name, cidr_block=cidr_block, enable_dns_hostnames=enable_dns_hostnames, enable_dns_support=enable_dns_support, instance_tenancy=instance_tenancy, **tags)
        self.nested_resources.append(self.vpc)

        self.internet_gateway = InternetGateway(f"{vpc_name}InternetGateway", **tags)
        self.nested_resources.append(self.internet_gateway)

        self.internet_gateway_attachment = VpcGatewayAttachment(f"{vpc_name}InternetGatewayAttachment", internet_gateway_id=self.internet_gateway(), vpc_id=self.vpc())
        self.nested_resources.append(self.internet_gateway_attachment)


