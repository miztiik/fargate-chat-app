#!/usr/bin/env python3

from aws_cdk import core

from chat_app_stacks.vpc_stack import CustomVpcStack
from chat_app_stacks.fargate_cluster_stack import FargateClusterStack


app = core.App()

app_name = app.node.try_get_context('app_name')

env_US = core.Environment(account=app.node.try_get_context('envs')['dev']['account'],
                          region=app.node.try_get_context('envs')['dev']['region'])

vpc_stack = CustomVpcStack(
    app, f"{app_name}-vpc-stack", env=env_US, add_nat_to_vpc=True)

fargate_stack = FargateClusterStack(
    app, f"{app_name}-fargate-stack", env=env_US, custom_vpc=vpc_stack.custom_vpc)

# Tag the stack resources
core.Tag.add(app, key="Owner", value=app.node.try_get_context('owner'))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context('github_profile'))
core.Tag.add(app, key="ToKnowMore",
             value=app.node.try_get_context('youtube_profile'))


app.synth()
