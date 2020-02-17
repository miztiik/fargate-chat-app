#!/usr/bin/env python3

from aws_cdk import core

from fargate_chat_app.fargate_chat_app_stack import FargateChatAppStack


app = core.App()
FargateChatAppStack(app, "fargate-chat-app")

app.synth()
