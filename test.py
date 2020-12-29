import json
from conf import *


# Test the compound stuff
from classes.ec2.base import Subnet
from classes.ec2.special import VpcWithInternet
internet_vpc = VpcWithInternet("MyVPC", cidr_block="172.16.0.0/16", enable_dns_hostnames=True, enable_dns_support=True, customer="me")

resources = {}
resources.update(internet_vpc.to_cf_json())

# Add a subnet
subnet = Subnet("PublicSubnet", availability_zone=REGION+"a", cidr_block="172.16.0.0/24", vpc_id=internet_vpc.vpc())
resources.update(subnet.to_cf_json())


template = {
    "AWSTemplateFormatVersion": CLOUDFORMATION_TEMPLATE_VERSION,
    "Resources": resources,
}
print("\nTemplate: ", template)

# test the stack with boto3
import boto3
from botocore.config import Config

my_config = Config(
    region_name=REGION
)

cf_client = boto3.client('cloudformation', config=my_config)

response = cf_client.create_stack(
    StackName='test',
    TemplateBody=json.dumps(template)
)
print(response)
