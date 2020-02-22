#!/usr/bin/env python3

from aws_cdk import core

from chat_app_stacks.vpc_stack import CustomVpcStack
from chat_app_stacks.fargate_cluster_stack import FargateClusterStack


app = core.App()

env_US = core.Environment(account=app.node.try_get_context('envs')['dev']['account'],
                          region=app.node.try_get_context('envs')['dev']['region'])

vpc_stack = CustomVpcStack(app, "vpc-stack", env=env_US, add_nat_to_vpc=True)

fargate_stack = FargateClusterStack(
    app, "fargate-chat-app", env=env_US, custom_vpc=vpc_stack.custom_vpc)


app.synth()
