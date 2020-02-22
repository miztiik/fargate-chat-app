from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecr as _ecr
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as _elbv2

from aws_cdk import core


class FargateClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, custom_vpc, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        fargate_cluster = _ecs.Cluster(self,
                                       "fargateClusterId",
                                       vpc=custom_vpc)

        core.CfnOutput(self, "ClusterNameOutput",
                       value=f"{fargate_cluster.cluster_name}", export_name="ClusterName")

        """
        Service running chat service
        """

        chat_app_task_def = _ecs.FargateTaskDefinition(
            self, "chatAppTaskDef")

        chat_app_container = chat_app_task_def.add_container("chatAppContainer",
                                                             environment={
                                                                 'github': 'https://github.com/miztiik'
                                                             },
                                                             image=_ecs.ContainerImage.from_registry(
                                                                 "mystique/fargate-chat-app:latest"),
                                                             logging=_ecs.LogDrivers.aws_logs(
                                                                 stream_prefix="Mystique")
                                                             )

        chat_app_container.add_port_mappings(
            _ecs.PortMapping(container_port=3000, protocol=_ecs.Protocol.TCP)
        )

        chat_app_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "chatAppServiceId",
            cluster=fargate_cluster,
            task_definition=chat_app_task_def,
            assign_public_ip=False,
            public_load_balancer=True,
            listener_port=80,
            desired_count=1,
            # cpu=1024,
            # memory_limit_mib=2048,
            # service_name="chatAppService",
        )
        core.CfnOutput(
            self, "chatAppServiceUrl", value=f"http://{chat_app_service.load_balancer.load_balancer_dns_name}")
