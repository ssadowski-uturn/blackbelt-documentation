from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.network import VPC
from diagrams.aws.network import VPCCustomerGateway, VpnGateway, SiteToSiteVpn
from diagrams.aws.network import ALB
from diagrams.aws.network import Route53

from diagrams.generic.network import Router
from diagrams.generic.network import Subnet
from diagrams.generic.network import Switch
from diagrams.generic.network import VPN

from diagrams.onprem.compute import Server


with Diagram("AWS", show=False):
    dns = Route53("dns")

    alb = ALB("API Load Balancer")

    with Cluster("AWS VPC"):
        cgw = VPCCustomerGateway("Customer VPN Gateway")
        vpngw = VpnGateway("AWS VPN Gateway")
        ecs = ECS("API ECS Service")

        vpc_services = [cgw, vpngw, ecs ]

    s2svpn = SiteToSiteVpn("AWS to Customer Premises")


    with Cluster("Data Center VLAN"):
        dcvpn = VPN("DC VPN Gateway")

        with Cluster("ECS-Anywhere Host Group"):
            ecsa = [Server("ECS-A Host"),
                    Server("ECS-A Host"),
                    Server("ECS-A Host")]

    dns >> alb >> ecs >> ecsa
    vpngw >> cgw >> s2svpn >> dcvpn
