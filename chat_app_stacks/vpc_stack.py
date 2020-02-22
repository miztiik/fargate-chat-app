import aws_cdk.aws_ec2 as _ec2
from aws_cdk import core


class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, add_nat_to_vpc: True, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html

        app_configs = self.node.try_get_context('envs')

        if add_nat_to_vpc:
            nat_gw_provider = _ec2.NatProvider.instance(
                instance_type=_ec2.InstanceType('t2.micro')
            )

            env_configs = app_configs['dev']

            self.custom_vpc = _ec2.Vpc(self, "customVpcId",
                                       cidr=env_configs['vpc_config']['cidr'],
                                       max_azs=2,
                                       nat_gateway_provider=nat_gw_provider,
                                       nat_gateways=1,
                                       subnet_configuration=[
                                           _ec2.SubnetConfiguration(
                                               name="publicSubnet", cidr_mask=env_configs['vpc_config']['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC),
                                           _ec2.SubnetConfiguration(
                                               name="appSubnet", cidr_mask=env_configs['vpc_config']['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE),
                                           _ec2.SubnetConfiguration(
                                               name="dbSubnet", cidr_mask=env_configs['vpc_config']['cidr_mask'], subnet_type=_ec2.SubnetType.ISOLATED)
                                       ]
                                       )
        else:
            self.custom_vpc = _ec2.Vpc(self, "customVpcId",
                                       cidr=env_configs['vpc_config']['cidr'],
                                       max_azs=2,
                                       nat_gateways=0,
                                       subnet_configuration=[
                                           _ec2.SubnetConfiguration(
                                               name="frontEndSubnet", cidr_mask=env_configs['vpc_config']['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC),
                                           _ec2.SubnetConfiguration(
                                               name="backEndSubnet", cidr_mask=env_configs['vpc_config']['cidr_mask'], subnet_type=_ec2.SubnetType.ISOLATED)
                                       ]
                                       )
        output_1 = core.CfnOutput(
            self, "CustomVpcId",
            value=self.custom_vpc.vpc_id,
            description=f"This vpc has 2 public & 2 isolated subnets. No NATs"
        )
